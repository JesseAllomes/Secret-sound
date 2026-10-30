"""Score sound-effect files against the measured fingerprint of the Mid North Coast Secret Sound.

A library take is never sample-identical to the clue, so this scores the physical pattern Fable
measured (analysis/analysis.md) instead of the waveform:

  pre     a faint dry click 25-90 ms before the first stroke
  gap     two strokes about 137 ms apart (B then C), with a timing tolerance
  crunch  B is a multi-impact crunch, C a single clean snap
  thump   a low-frequency (40-120 Hz) thump lagging each stroke by 15-45 ms
  ring    a narrow, long-T60 ring at 500-1200 Hz after C, weaker after B
  dry     no reverb: the sound falls 40 dB within about 150 ms of C

Every candidate stroke pair in every file is scored; the best pair is reported with its gap.

    python steel_score.py <folder> [--meta meta.json] [--csv out.csv] [--top 30] [--jobs 4]
    python steel_score.py <folder> --null <general folder>    # z against a null set
    python steel_score.py <folder> --sfx-json sfx.json         # fuse with sfx_match.py --out (CLAP/mel score)
    python steel_score.py <folder> --ab 5 --clue clue.wav --out <dir>   # clue-then-candidate mp3s
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

SR = 48000
AUDIO_EXT = {".wav", ".mp3", ".flac", ".ogg", ".aif", ".aiff", ".m4a"}
WEIGHTS = {"gap": 0.20, "pre": 0.10, "crunch": 0.20, "thump": 0.15, "ring": 0.25, "dry": 0.10}
TARGET_GAP = 0.137
GAP_TOL = 0.040


def band_env(y, lo, hi, smooth_ms):
    sos = signal.butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    e = np.abs(signal.sosfiltfilt(sos, y))
    n = max(1, int(smooth_ms * SR / 1000))
    return np.convolve(e, np.ones(n) / n, mode="same")


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-9))


def strokes(y):
    """Clusters of high-frequency impacts. Returns [(start_s, level, impacts)], level in linear HF envelope."""
    hf = band_env(y, 2000, 10000, 0.5)
    peak = hf.max()
    if peak <= 0:
        return []
    idx, _ = signal.find_peaks(hf, height=peak * 10 ** (-36 / 20), distance=int(0.004 * SR),
                               prominence=peak * 10 ** (-40 / 20))
    out = []
    for i in idx:
        t = i / SR
        if out and t - out[-1]["last"] <= 0.020 and t - out[-1]["start"] <= 0.060:
            s = out[-1]
            s["last"] = t
            s["peaks"].append(hf[i])
        else:
            out.append({"start": t, "last": t, "peaks": [hf[i]]})
    res = []
    for s in out:
        lv = max(s["peaks"])
        res.append((s["start"], lv, sum(p >= lv * 10 ** (-20 / 20) for p in s["peaks"])))
    return res


def ring_stats(y, t0, t1):
    """Strongest narrow mode in 500-1200 Hz between t0 and t1: (freq, Q, prominence dB, T60 s, level dB)."""
    a, b = int(t0 * SR), int(t1 * SR)
    seg = y[a:b]
    if len(seg) < int(0.02 * SR):
        return 0.0, 0.0, 0.0, 0.0, -180.0
    n = max(SR, 1 << int(np.ceil(np.log2(len(seg)))))
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    f = np.fft.rfftfreq(n, 1 / SR)
    band = (f >= 500) & (f <= 1200)
    k = np.flatnonzero(band)[np.argmax(spec[band])]
    f0, pk = f[k], spec[k]
    half = pk / np.sqrt(2)
    lo = k
    while lo > 0 and spec[lo] > half:
        lo -= 1
    hi = k
    while hi < len(spec) - 1 and spec[hi] > half:
        hi += 1
    q = f0 / max(f[hi] - f[lo], f[1] - f[0])
    ctx = (f >= 300) & (f <= 2000)
    prom = db(pk) - db(np.median(spec[ctx]))
    # T60 from the decay slope of the mode's envelope after its peak
    sos = signal.butter(2, [f0 * 0.95, f0 * 1.05], btype="band", fs=SR, output="sos")
    env = db(np.abs(signal.hilbert(signal.sosfiltfilt(sos, seg))))
    env = np.convolve(env, np.ones(int(0.005 * SR)) / int(0.005 * SR), mode="same")
    j = int(np.argmax(env))
    tail = env[j:]
    t60 = 0.0
    if len(tail) > int(0.03 * SR):
        tt = np.arange(len(tail)) / SR
        keep = tail > tail[0] - 40
        if keep.sum() > int(0.02 * SR):
            slope = np.polyfit(tt[keep], tail[keep], 1)[0]
            t60 = float(min(5.0, 60 / -slope)) if slope < 0 else 5.0
    return float(f0), float(q), float(prom), t60, float(db(pk / len(seg)))


def thump_score(lf, t):
    """1 when an LF peak lands 15-45 ms after the stroke and stands >= 6 dB over the LF just before it."""
    a, b = int((t + 0.005) * SR), int((t + 0.080) * SR)
    pre = lf[max(0, int((t - 0.020) * SR)):max(1, int(t * SR))]
    if b > len(lf) or not len(pre):
        return 0.0, 0.0
    j = int(np.argmax(lf[a:b]))
    lag = (a + j) / SR - t
    rise = db(lf[a + j]) - db(np.mean(pre) + 1e-9)
    lag_ok = 1.0 if 0.015 <= lag <= 0.045 else max(0.0, 1 - min(abs(lag - 0.015), abs(lag - 0.045)) / 0.03)
    return lag_ok * float(np.clip(rise / 6, 0, 1)), lag


def decay_time(y, t, floor_db):
    """Seconds after t for the broadband envelope to fall 40 dB (or to the noise floor + 3 dB)."""
    env = db(np.convolve(np.abs(y), np.ones(int(0.005 * SR)) / int(0.005 * SR), mode="same"))
    a = int(t * SR)
    seg = env[a:a + int(0.6 * SR)]
    if not len(seg):
        return 0.6
    j = int(np.argmax(seg[:int(0.03 * SR)] if len(seg) > int(0.03 * SR) else seg))
    target = max(seg[j] - 40, floor_db + 3)
    below = np.flatnonzero(seg[j:] < target)
    return below[0] / SR if len(below) else 0.6


def score_pair(y, st, i, k, lf, floor_db):
    tb, lb, nb = st[i]
    tc, lc, nc = st[k]
    gap = tc - tb
    f = {"gap_ms": round(gap * 1000, 1)}
    f["gap"] = float(np.exp(-0.5 * ((gap - TARGET_GAP) / GAP_TOL) ** 2))
    pre = [s for s in st if tb - 0.090 <= s[0] <= tb - 0.025]
    if pre:
        rel = db(max(s[1] for s in pre)) - db(lb)
        f["pre"] = 1.0 if -24 <= rel <= -3 else 0.4
    else:
        f["pre"] = 0.0
    crunch_b = float(np.clip((nb - 1) / 3, 0, 1))
    snap_c = 1.0 if nc <= 2 else (0.5 if nc == 3 else 0.0)
    f["crunch"] = (crunch_b + snap_c) / 2
    th_b, lag_b = thump_score(lf, tb)
    th_c, lag_c = thump_score(lf, tc)
    f["thump"] = (th_b + th_c) / 2
    f["thump_lag_ms"] = round((lag_b + lag_c) / 2 * 1000, 1)
    f0, q, prom, t60, lev_c = ring_stats(y, tc + 0.030, tc + 0.330)
    *_, lev_b = ring_stats(y, tb + 0.030, min(tc, tb + 0.130))
    ratio = lev_c - lev_b
    f.update(ring_hz=round(f0), ring_q=round(q), ring_t60=round(t60, 3), ring_c_vs_b_db=round(ratio, 1))
    f["ring"] = float(np.mean([min(1, t60 / 0.25), min(1, q / 60), np.clip(prom / 20, 0, 1),
                               np.clip(ratio / 10, 0, 1)]))
    d = decay_time(y, tc, floor_db)
    f["decay_ms"] = round(d * 1000)
    f["dry"] = float(np.clip((0.5 - d) / 0.35, 0, 1))
    f["score"] = sum(WEIGHTS[n] * f[n] for n in WEIGHTS)
    f["t_b"] = round(tb, 3)
    return f


def score_signal(y):
    """Best-scoring stroke pair in a signal, or None when it has no plausible pair."""
    st = strokes(y)
    if len(st) < 2:
        return None
    lf = band_env(y, 40, 120, 5)
    env = np.convolve(np.abs(y), np.ones(int(0.005 * SR)) / int(0.005 * SR), mode="same")
    floor_db = float(np.percentile(db(env), 10))
    top = max(s[1] for s in st)
    loud = [j for j, s in enumerate(st) if s[1] >= top * 10 ** (-20 / 20)]
    best = None
    for i in loud:
        for k in loud:
            if 0.060 <= st[k][0] - st[i][0] <= 0.260:
                f = score_pair(y, st, i, k, lf, floor_db)
                if best is None or f["score"] > best["score"]:
                    best = f
    return best


def score_file(path):
    try:
        y, _ = librosa.load(path, sr=SR, mono=True)
    except Exception as exc:
        return {"file": str(path), "error": str(exc)}
    if len(y) < int(0.2 * SR) or not np.any(y):
        return {"file": str(path), "error": "too short or silent"}
    best = score_signal(y)
    return {"file": str(path), **best} if best else {"file": str(path), "error": "no stroke pair"}


def score_folder(folder, jobs):
    files = sorted(p for p in Path(folder).rglob("*") if p.suffix.lower() in AUDIO_EXT)
    if jobs > 1:
        with ProcessPoolExecutor(jobs) as ex:
            return list(ex.map(score_file, files, chunksize=16))
    return [score_file(p) for p in files]


def mechanism_report(rows):
    """Evidence per search query (mechanism): count, best, median of top 5, mean features of top 5."""
    by = {}
    for r in rows:
        by.setdefault(r.get("query") or "(none)", []).append(r)
    out = []
    for q, rs in by.items():
        rs = sorted(rs, key=lambda r: -r["score"])
        top5 = rs[:5]
        feats = {n: round(float(np.mean([r[n] for r in top5])), 2) for n in WEIGHTS}
        out.append({"query": q, "n": len(rs), "best": round(rs[0]["score"], 3),
                    "median_top5": round(float(np.median([r["score"] for r in top5])), 3),
                    "matches": [n for n, v in feats.items() if v >= 0.6],
                    "never": [n for n, v in feats.items() if v < 0.2], **feats})
    return sorted(out, key=lambda r: -r["median_top5"])


def write_ab(rows, n, clue_path, out_dir):
    """Clue (its crop, untouched), 0.4 s gap, candidate excerpt of the same length aligned on stroke B; x4."""
    clue_path = Path(clue_path)
    y, _ = librosa.load(clue_path, sr=SR, mono=True)
    crop = clue_path.with_suffix(".crop.json")
    if crop.exists():
        c = json.loads(crop.read_text())
        y = y[int(max(0, c["CLIP_START"]) * SR):int(c["CLIP_END"] * SR)]
    clue_best = score_signal(y)
    clue_tb = clue_best["t_b"] if clue_best else 0.0
    ffmpeg = shutil.which("ffmpeg")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for k, r in enumerate(rows[:n], 1):
        x, _ = librosa.load(r["file"], sr=SR, mono=True)
        a = max(0, int((r["t_b"] - clue_tb) * SR))
        cand = x[a:a + len(y)]
        cand = np.pad(cand, (0, len(y) - len(cand)))
        cand = cand * (np.max(np.abs(y)) / max(np.max(np.abs(cand)), 1e-9))
        gap = np.zeros(int(0.4 * SR), np.float32)
        pair = np.concatenate([y, gap, cand, gap * 2])
        audio = np.tile(pair, 4)
        mech = re.sub(r"[^a-z0-9]+", "-", (r.get("query") or "candidate").lower()).strip("-")[:30]
        name = f"AB_steel{k}_{mech}_{Path(r['file']).stem}"
        if ffmpeg:
            with tempfile.TemporaryDirectory() as td:
                wav = Path(td) / "ab.wav"
                sf.write(wav, audio, SR)
                dest = out_dir / f"{name}.mp3"
                subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "192k", str(dest)],
                               check=True)
        else:
            dest = out_dir / f"{name}.wav"
            sf.write(dest, audio, SR)
        made.append(dest)
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--meta", help="meta.json from freesound_pull.py (names, urls, search queries)")
    ap.add_argument("--null", help="folder of general effects to use as the null distribution")
    ap.add_argument("--sfx-json", help="sfx_match.py --out ranking to fuse with (CLAP/mel similarity)")
    ap.add_argument("--sfx-weight", type=float, default=0.4)
    ap.add_argument("--csv", help="write every file's best pair here")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--ab", type=int, default=0, help="make A/B files for the top N")
    ap.add_argument("--clue", help="clue.wav for --ab (clue.crop.json next to it is used)")
    ap.add_argument("--out", help="folder for --ab files")
    args = ap.parse_args()

    meta = json.loads(Path(args.meta).read_text(encoding="utf-8")) if args.meta else {}
    rows = [r for r in score_folder(args.folder, args.jobs) if "error" not in r]
    for r in rows:
        info = meta.get(Path(r["file"]).stem, {})
        r["name"], r["query"], r["url"] = info.get("name", Path(r["file"]).name), info.get("query", ""), info.get("url", "")

    if args.null:
        null = np.array([r["score"] for r in score_folder(args.null, args.jobs) if "error" not in r])
        med, mad = np.median(null), np.median(np.abs(null - np.median(null))) * 1.4826 or 1e-6
        for r in rows:
            r["z"] = round((r["score"] - med) / mad, 2)
            r["null_pct"] = round(100 * float(np.mean(null < r["score"])), 1)
        print(f"null: {len(null)} files, median {med:.3f}, robust sd {mad:.3f}, p99 {np.percentile(null, 99):.3f}")

    key = "score"
    if args.sfx_json:
        sfx = {str(r["id"]): float(r["score"]) for r in json.loads(Path(args.sfx_json).read_text(encoding="utf-8"))}
        vals = np.array(list(sfx.values())) if sfx else np.zeros(1)
        lo, hi = np.percentile(vals, 1), np.percentile(vals, 99)
        for r in rows:
            s = sfx.get(Path(r["file"]).stem)
            r["sfx"] = round(float(np.clip((s - lo) / (hi - lo + 1e-9), 0, 1)), 3) if s is not None else 0.0
            r["fused"] = (1 - args.sfx_weight) * r["score"] + args.sfx_weight * r["sfx"]
        key = "fused"

    rows.sort(key=lambda r: -r[key])
    if args.csv and rows:
        fields = list(dict.fromkeys(k for r in rows for k in r))
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    print(f"\n{len(rows)} files with a stroke pair. Top {args.top} by {key}:")
    for k, r in enumerate(rows[:args.top], 1):
        feats = " ".join(f"{n} {r[n]:.2f}" for n in WEIGHTS)
        print(f"{k:3d}  {r[key]:.3f}  gap {r['gap_ms']:5.1f} ms  ring {r['ring_hz']:4d} Hz T60 {r['ring_t60']:.2f}  "
              f"[{feats}]  {r['name']}")

    if any(r["query"] for r in rows):
        print("\nEvidence per mechanism (search query):")
        for m in mechanism_report(rows):
            print(f"  {m['query'][:32]:32s} n={m['n']:4d} best {m['best']:.3f} median-top5 {m['median_top5']:.3f}  "
                  f"matches {','.join(m['matches']) or '-'}  never {','.join(m['never']) or '-'}")

    if args.ab:
        if not (args.clue and args.out):
            ap.error("--ab needs --clue and --out")
        for p in write_ab(rows, args.ab, args.clue, args.out):
            print(f"A/B: {p}")


if __name__ == "__main__":
    main()
