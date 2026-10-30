"""Resonance-aware scorer for the Mid North Coast Secret Sound (builds on steel_score.py).

steel_score.py rewards the clue's timing pattern (pre-click, two strokes 137 ms apart, crunch then
snap, lagging thumps, a mode near 790 Hz) but let through sharp, non-resonant clicks that the
listener rejected (staplers, door handles, latches, a 3-hole punch). Measured on those rejects and
on the clue, what separates them is not how LOUD the ringing is (the clue's ring sits ~19 dB under
its click, like the rejects) but how PURE it is, and how soft the second stroke is:

  tone   30-130 ms after C the clue is one narrow mode: spectral peak 36-39 dB over the median of
         300-3000 Hz, autocorrelation 0.68-0.73. Rejects: 10-25 dB, 0.12-0.49 (BBC switch 19/0.49).
  soft   C carries 3 % of its energy above 3 kHz (centroid ~1.2 kHz); rejects 11-59 %. B is 16 %.
  pitch  the mode near 790 Hz, with a wide tolerance (another unit of the same object differs)

Both are per stroke, cut at the next loud stroke, so busy recordings cannot borrow a tail.

    python res_score.py <folder> --meta meta.json [--null <folder>] [--csv out.csv] [--jobs 4]
    python res_score.py <folder> --meta meta.json --ab 10 --clue clue_clean.wav --out <dir> --per-family 2
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
from scipy import signal

import steel_score as ss

SR = ss.SR
WEIGHTS = {"tone": 0.25, "pitch": 0.12, "soft": 0.12, "gap": 0.10, "crunch": 0.08, "thump": 0.10,
           "pre": 0.03, "ring": 0.05, "dry": 0.05, "mode2": 0.05, "iso": 0.05}
# the weighted sum is then multiplied by (0.6 + 0.4 * iso): a busy recording (music loop, a dozen
# actions) can at most reach 0.6 of its feature score

FAMILIES = {
    "typewriter": ["typewriter"], "nail gun": ["nail gun", "brad nailer", "nailer"],
    "staple gun": ["staple gun", "electric stapler"], "tin lid": ["tin lid", "metal lid", "biscuit tin", "mint tin", "tin close", "cookie tin", "pencil case tin"],
    "letterbox": ["letterbox", "mail slot"], "cash drawer": ["cash drawer", "cash register drawer"],
    "clicker toy": ["clicker toy", "tin clicker", "frog clicker", "tally counter"],
    "camera shutter": ["camera shutter", "slr shutter"], "tape measure": ["tape measure"],
    "case latch": ["briefcase latch", "suitcase latch", "toolbox latch", "guitar case latch", "lunch box latch"],
    "padlock": ["padlock"], "gate/window latch": ["gate latch", "window latch"],
    "lighter": ["zippo", "lighter"], "staple gun": ["staple gun", "electric stapler", "stapler spring"], "umbrella": ["umbrella"], "buckle/clasp": ["seatbelt", "watch clasp"],
    "car": ["glovebox", "handbrake"], "kitchen gadget": ["nutcracker", "bottle opener", "tongs"],
    "pull/rocker switch": ["pull cord", "pull switch", "rocker switch"],
    "keyboard": ["keyboard"], "pen": ["pen click"], "ratchet tool": ["ratchet", "caulking", "locking pliers"],
    "spring": ["spring"], "case/box": ["glasses case", "purse clasp", "jewellery box", "kiss lock", "lunchbox", "cigarette case", "compact mirror"],
    "toilet roll holder": ["toilet roll", "toilet paper"], "hose fitting": ["hose"], "stud/snap": ["snap fastener", "press stud"],
    "bolt": ["barrel bolt", "slide bolt"], "punch/trimmer": ["ticket punch", "paper trimmer"],
    "toy gun/igniter": ["cap gun", "piezo"], "register/adding machine": ["adding machine", "cash register key"],
    "cassette/tape deck": ["cassette", "tape deck", "tape recorder", "walkman", "vcr", "video cassette", "boombox",
                           "dictaphone"],
    "radio/lamp/fan switch": ["radio", "desk lamp", "fan switch"],
    "camera": ["camera", "polaroid"], "projector/viewer": ["slide projector", "view master"],
    "counter": ["mechanical counter", "click counter"], "coin/meter": ["parking meter", "coin"],
    "telephone": ["telephone", "rotary dial"], "pencil": ["mechanical pencil"],
    "generic click/lever": ["lever press", "lever click", "button mechanical", "push button", "latch click metal",
                            "spring clack", "metal clack", "click clack", "clicky button"],
    "stapler": ["stapler", "stapling"], "door handle": ["door handle", "door lever"], "door latch": ["door latch"],
    "stamp": ["stamp", "embosser"], "binder/clip": ["binder", "clipboard", "bulldog", "fold back", "money clip"],
    "light switch": ["light switch", "toggle switch", "torch switch"], "hole punch": ["paper punch", "hole punch"],
    "toaster": ["toaster"], "bin": ["pedal bin"], "label/price gun": ["label maker", "price gun"],
    "clippers/cutters": ["nail clippers", "secateurs", "tin snips", "garlic press"], "mousetrap": ["mousetrap"],
    "clamp": ["spring clamp"],
}


def family(query):
    q = (query or "").lower()
    for fam, keys in FAMILIES.items():
        if any(k in q for k in keys):
            return fam
    return q or "(none)"


def bp(y, lo, hi, order=4):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfiltfilt(sos, y)


def rms_db(x):
    return float(ss.db(np.sqrt(np.mean(x ** 2)))) if len(x) else -180.0


def narrow_db(y, a, b, hz):
    """RMS level (dB) of y[a:b] in a +-3 % band around hz."""
    seg = y[a:b]
    if hz <= 0 or len(seg) < int(0.02 * SR):
        return -180.0
    sos = signal.butter(2, [hz * 0.97, hz * 1.03], btype="band", fs=SR, output="sos")
    return rms_db(signal.sosfilt(sos, seg))


def stroke_tone(y, t, t_end):
    """Per-stroke: HF share of the first 20 ms, tail purity 30-130 ms after (cut at t_end), the tail
    tone's level in a window 500-180 ms before the stroke (before the pair's first stroke, for any
    gap up to 180 ms) so a steady hum or a music note is not counted as a ring, and a second tonal
    peak in 350-600 Hz."""
    a = int(t * SR)
    seg = y[a:a + int(0.020 * SR)]
    none = {"hf_share": 1.0, "tail_peak_db": 0.0, "tail_hz": 0, "tail_ac": 0.0, "novel_db": 0.0, "mode2_db": 0.0, "mode2_hz": 0}
    if len(seg) < int(0.010 * SR):
        return none
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 4096)) ** 2
    f = np.fft.rfftfreq(4096, 1 / SR)
    tot = spec[f > 100].sum() + 1e-12
    hf = float(spec[f > 3000].sum() / tot)
    b0, b1 = a + int(0.030 * SR), min(a + int(0.130 * SR), int(t_end * SR), len(y))
    tail = y[b0:b1]
    if len(tail) < int(0.040 * SR):
        return {**none, "hf_share": hf}
    tail = bp(tail, 200, 4000)
    n = 1 << 16
    sp = np.abs(np.fft.rfft(tail * np.hanning(len(tail)), n))
    ff = np.fft.rfftfreq(n, 1 / SR)
    band = (ff >= 300) & (ff <= 3000)
    pk = float(ss.db(sp[band].max()) - ss.db(np.median(sp[band])))
    hz = float(ff[band][np.argmax(sp[band])])
    ac = signal.correlate(tail, tail, mode="full")[len(tail) - 1:]
    ac = ac / (ac[0] + 1e-12)
    lo, hi = int(SR / 3000), int(SR / 300)
    # novelty: the tail tone's narrowband level now vs before the pair's first stroke
    p1 = max(0, int((t - 0.180) * SR))
    p0 = max(0, int((t - 0.500) * SR))
    if p1 - p0 < int(0.060 * SR):               # the event starts the file: use its first 60 ms, however short
        p0, p1 = 0, max(int(0.060 * SR), p1)
    novel = narrow_db(y, b0, b1, hz) - narrow_db(y, p0, p1, hz)
    # a second tonal peak 350-600 Hz, contrast over the band median, excluding +-6 % of the main tone
    band2 = (ff >= 350) & (ff <= 600) & ((ff < hz * 0.94) | (ff > hz * 1.06))
    if band2.any():
        m2 = float(ss.db(sp[band2].max()) - ss.db(np.median(sp[band])))
        m2hz = float(ff[band2][np.argmax(sp[band2])])
        m2 = m2 if narrow_db(y, b0, b1, m2hz) - narrow_db(y, p0, p1, m2hz) >= 8 else 0.0
    else:
        m2, m2hz = 0.0, 0.0
    return {"hf_share": hf, "tail_peak_db": pk, "tail_hz": hz, "tail_ac": float(ac[lo:hi].max()),
            "novel_db": novel, "mode2_db": m2, "mode2_hz": m2hz}


def score_signal(y):
    """Best-scoring stroke pair in a signal with the resonance features, or None."""
    st = ss.strokes(y)
    if len(st) < 2:
        return None
    lf = ss.band_env(y, 40, 120, 5)
    env_db = ss.db(ss.smooth(np.abs(y), 0.005 * SR))
    floor_db = float(np.percentile(env_db, 10))
    top = max(s[1] for s in st)
    loud = [j for j, s in enumerate(st) if s[1] >= top * 10 ** (-20 / 20)]
    tone = {}
    for n, j in enumerate(loud):
        t_end = st[loud[n + 1]][0] if n + 1 < len(loud) else len(y) / SR
        tone[j] = stroke_tone(y, st[j][0], t_end)
    best = None
    for i in loud:
        for k in loud:
            if not 0.060 <= st[k][0] - st[i][0] <= 0.260:
                continue
            f = ss.score_pair(y, st, i, k, lf, env_db, floor_db)
            f["steel"] = f.pop("score")
            tb, tc = tone[i], tone[k]
            f["tail_peak_db"] = round(tc["tail_peak_db"], 1)
            f["tail_hz"] = round(tc["tail_hz"])
            f["tail_ac"] = round(tc["tail_ac"], 2)
            f["hf_b"] = round(tb["hf_share"], 2)
            f["hf_c"] = round(tc["hf_share"], 2)
            f["novel_db"] = round(tc["novel_db"], 1)
            f["mode2_hz"] = round(tc["mode2_hz"])
            f["mode2_db"] = round(tc["mode2_db"], 1)
            novel = float(np.clip((tc["novel_db"] - 6) / 12, 0, 1))
            f["tone"] = novel * float(np.mean([np.clip((tc["tail_peak_db"] - 10) / 25, 0, 1),
                                               np.clip((tc["tail_ac"] - 0.2) / 0.5, 0, 1)]))
            f["mode2"] = float(np.clip((tc["mode2_db"] - 6) / 10, 0, 1))
            f["soft"] = float(np.mean([1 - np.clip((tc["hf_share"] - 0.10) / 0.30, 0, 1),
                                       1 - np.clip((tb["hf_share"] - 0.30) / 0.40, 0, 1)]))
            hz = max(tc["tail_hz"], 1.0)
            f["pitch"] = float(max(np.exp(-0.5 * (np.log2(hz / ss.RING_HZ) / 0.4) ** 2),
                                   0.7 * np.exp(-0.5 * (np.log2(hz / 440.0) / 0.3) ** 2)))
            f["score"] = sum(WEIGHTS[n] * f[n] for n in WEIGHTS) * (0.6 + 0.4 * f["iso"])
            if best is None or f["score"] > best["score"]:
                best = f
    return best


def score_file(path):
    try:
        y, _ = librosa.load(path, sr=SR, mono=True)
    except Exception as exc:  # noqa: BLE001
        return {"file": str(path), "error": str(exc)}
    if len(y) < int(0.2 * SR) or not np.any(y):
        return {"file": str(path), "error": "too short or silent"}
    best = score_signal(y)
    return {"file": str(path), **best} if best else {"file": str(path), "error": "no stroke pair"}


def score_folder(folder, jobs):
    files = sorted(p for p in Path(folder).rglob("*") if p.suffix.lower() in ss.AUDIO_EXT)
    if jobs > 1:
        with ProcessPoolExecutor(jobs) as ex:
            return list(ex.map(score_file, files, chunksize=8))
    return [score_file(p) for p in files]


def family_report(rows):
    by = {}
    for r in rows:
        by.setdefault(r["family"], []).append(r)
    out = []
    for fam, rs in by.items():
        rs = sorted(rs, key=lambda r: -r["score"])
        top5 = rs[:5]
        feats = {n: round(float(np.mean([r[n] for r in top5])), 2) for n in WEIGHTS}
        out.append({"family": fam, "n": len(rs), "best": round(rs[0]["score"], 3),
                    "median_top5": round(float(np.median([r["score"] for r in top5])), 3),
                    "fit": [n for n, v in feats.items() if v >= 0.6], "fail": [n for n, v in feats.items() if v < 0.3],
                    **feats})
    return sorted(out, key=lambda r: -r["median_top5"])


def write_ab(rows, clue_path, out_dir, prefix="AB_res"):
    """Clue (whole file), 0.4 s gap, candidate excerpt of the same length aligned on stroke B, 0.8 s gap; x4."""
    y, _ = librosa.load(clue_path, sr=SR, mono=True)
    clue_best = score_signal(y)
    clue_tb = clue_best["t_b"] if clue_best else 0.112
    ffmpeg = shutil.which("ffmpeg")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for k, r in enumerate(rows, 1):
        x, _ = librosa.load(r["file"], sr=SR, mono=True)
        a = max(0, int((r["t_b"] - clue_tb) * SR))
        cand = x[a:a + len(y)]
        cand = np.pad(cand, (0, len(y) - len(cand)))
        cand = cand * (np.max(np.abs(y)) / max(np.max(np.abs(cand)), 1e-9))
        gap = np.zeros(int(0.4 * SR), np.float32)
        pair = np.concatenate([y, gap, cand, gap, gap])
        audio = np.tile(pair, 4)
        fam = re.sub(r"[^a-z0-9]+", "-", r["family"].lower()).strip("-")[:24]
        name = f"{prefix}{k}_{fam}_{Path(r['file']).stem}"
        # sanity check: the excerpt's own strokes, relative to the clue's B
        cst = ss.strokes(cand)
        ctop = max((s[1] for s in cst), default=1e-9)
        r["excerpt_strokes"] = [(round(t, 3), round(float(ss.db(l / ctop)), 1)) for t, l, _ in cst if l >= ctop * 10 ** (-20 / 20)]
        if ffmpeg:
            with tempfile.TemporaryDirectory() as td:
                wav = Path(td) / "ab.wav"
                sf.write(wav, audio, SR)
                dest = out_dir / f"{name}.mp3"
                subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "192k", str(dest)], check=True)
        else:
            dest = out_dir / f"{name}.wav"
            sf.write(dest, audio, SR)
        r["ab"] = str(dest)
        made.append(dest)
    return made


def pick_diverse(rows, n, per_family):
    out, seen = [], {}
    for r in rows:
        if seen.get(r["family"], 0) >= per_family:
            continue
        seen[r["family"]] = seen.get(r["family"], 0) + 1
        out.append(r)
        if len(out) >= n:
            break
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--meta")
    ap.add_argument("--null")
    ap.add_argument("--csv")
    ap.add_argument("--json")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--ab", type=int, default=0)
    ap.add_argument("--per-family", type=int, default=2)
    ap.add_argument("--clue")
    ap.add_argument("--out")
    ap.add_argument("--exclude", help="file of freesound ids (one per line) to leave out")
    ap.add_argument("--cache", help="json of per-file results; files already in it are not rescored")
    args = ap.parse_args()

    meta = json.loads(Path(args.meta).read_text(encoding="utf-8")) if args.meta else {}
    excl = set(Path(args.exclude).read_text().split()) if args.exclude else set()
    cache = json.loads(Path(args.cache).read_text(encoding="utf-8")) if args.cache and Path(args.cache).exists() else {}
    files = sorted(p for p in Path(args.folder).rglob("*") if p.suffix.lower() in ss.AUDIO_EXT and str(p) not in cache)
    if files:
        with ProcessPoolExecutor(args.jobs) as ex:
            for r in ex.map(score_file, files, chunksize=8):
                cache[r["file"]] = r
        if args.cache:
            Path(args.cache).write_text(json.dumps(cache, default=float), encoding="utf-8")
    rows = [dict(r) for r in cache.values() if "error" not in r and Path(r["file"]).stem not in excl
            and Path(r["file"]).parent == Path(args.folder)]
    for r in rows:
        info = meta.get(Path(r["file"]).stem, {})
        r["name"], r["query"], r["url"] = info.get("name", Path(r["file"]).name), info.get("query", ""), info.get("url", "")
        r["duration"] = info.get("duration")
        r["family"] = family(r["query"])
    if args.null:
        null = np.array([r["score"] for r in score_folder(args.null, args.jobs) if "error" not in r])
        med, mad = np.median(null), np.median(np.abs(null - np.median(null))) * 1.4826 or 1e-6
        for r in rows:
            r["z"] = round((r["score"] - med) / mad, 2)
            r["null_pct"] = round(100 * float(np.mean(null < r["score"])), 1)
        print(f"null: {len(null)} files, median {med:.3f}, robust sd {mad:.3f}, p95 {np.percentile(null, 95):.3f}, "
              f"p99 {np.percentile(null, 99):.3f}, max {null.max():.3f}")
    rows.sort(key=lambda r: -r["score"])
    if args.csv and rows:
        fields = list(dict.fromkeys(k for r in rows for k in r))
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    print(f"\n{len(rows)} files with a stroke pair. Top {args.top}:")
    for k, r in enumerate(rows[:args.top], 1):
        feats = " ".join(f"{n} {r[n]:.2f}" for n in WEIGHTS)
        print(f"{k:3d}  {r['score']:.3f} (steel {r['steel']:.2f})  gap {r['gap_ms']:5.1f}  tail {r['tail_hz']:4d} Hz "
              f"pk {r['tail_peak_db']:4.1f} ac {r['tail_ac']:.2f} new {r['novel_db']:4.0f} m2 {r['mode2_hz']:3d}/{r['mode2_db']:3.0f} hfC {r['hf_c']:.2f}  [{feats}]  {r['family']} | {r['name'][:40]}")
    if rows and any(r["query"] for r in rows):
        print("\nEvidence per family:")
        for m in family_report(rows):
            print(f"  {m['family'][:24]:24s} n={m['n']:4d} best {m['best']:.3f} median-top5 {m['median_top5']:.3f}  "
                  f"fit {','.join(m['fit']) or '-'}  fail {','.join(m['fail']) or '-'}")
    if args.ab:
        if not (args.clue and args.out):
            ap.error("--ab needs --clue and --out")
        chosen = pick_diverse(rows, args.ab, args.per_family)
        for p in write_ab(chosen, args.clue, args.out):
            print(f"A/B: {p}")
        for r in chosen:
            print(f"   {Path(r['file']).stem}: excerpt strokes (t, dB) {r['excerpt_strokes']}")
    if args.json:
        Path(args.json).write_text(json.dumps(rows[:200], default=float, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
