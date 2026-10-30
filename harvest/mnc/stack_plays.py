"""Mid North Coast only: line up every broadcast play of the clue and stack them into a cleaner copy.

Each play in harvest.jsonl is the same recording with different background and talk-over. This re-downloads each
episode, cuts 1.0 s before to 1.5 s after every play at 48 kHz, aligns each cut to the clue to the sample, sets its
level and polarity, and writes:
  stack/clue_stacked_median.wav, stack/clue_stacked_mean.wav  (2.5 s; the clue sits at 1.000-1.631 s)
  stack/report.txt   per-play fit, and per 25 ms block how much of the sound is common to every play.
It also keeps the audio while each episode is downloaded:
  plays/<n>_<date>_<t>.flac      every play, 1.0 s before to 1.5 s after, aligned, as broadcast (no level change)
  segments/<n>_<date>_<t0>.mp3   every transcribed segment (same window and name as transcripts/), 64 kb/s mono
The "common" ratio (energy of the mean / mean energy) is ~1 where all plays carry the same sound and ~1/N where they
differ (speech, music, noise), so it shows whether the station's recording runs past the edges of our 0.631 s clip.

    python stack_plays.py [--min-fit 0.7] [--jobs 4]
"""
import argparse
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).parent
SR = 48000
PRE, POST = 1.0, 1.5            # seconds kept before the clue's start and after it
SEARCH = 0.08                   # +/- seconds searched around the harvest's play time


def cut(mp3, t, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(mp3), "-t", f"{dur:.3f}",
                          "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def align(x, ev, lo):
    """Best lag of the clue's event part inside x (normalised correlation), searched from lo over 2*SEARCH."""
    n, m = len(ev), int(2 * SEARCH * SR)
    seg = x[lo:lo + m + n - 1]
    num = np.correlate(seg, ev, mode="valid")              # ev is zero-mean, so the window mean drops out
    c1, c2 = np.concatenate([[0], np.cumsum(seg)]), np.concatenate([[0], np.cumsum(seg ** 2)])
    s1, s2 = c1[n:] - c1[:-n], c2[n:] - c2[:-n]
    r = num / np.sqrt(np.maximum(s2 - s1 ** 2 / n, 1e-20))
    k = int(np.argmax(np.abs(r)))
    return float(r[k]), lo + k


def saved_plays(rec, clue, ev, ev_a):
    """The episode's plays from plays/*.flac (already aligned), or None if any is missing (then re-download)."""
    tag = f"{rec['n']:03d}_{rec['date'][5:16].replace(' ', '-')}"
    files = [HERE / "plays" / f"{tag}_{p['t']:.2f}.flac" for p in rec["plays"]]
    segs = [HERE / "segments" / f"{tag}_{int(w['t0'])}.mp3" for w in rec["windows"]]
    if not all(f.exists() for f in files + segs):
        return None
    out = []
    for p, f in zip(rec["plays"], files):
        seg, _ = sf.read(f)
        r, _ = align(seg, ev, int((PRE - SEARCH) * SR) + ev_a)
        body = seg[int(PRE * SR):int(PRE * SR) + len(clue)]
        g = float(body @ clue) / float(clue @ clue)
        out.append({"date": rec["date"][5:16], "t": p["t"], "fit": round(abs(r), 3), "gain": round(g, 3),
                    "seg": seg / g if abs(g) > 1e-6 else seg})
    return out


def episode_plays(rec, clue, ev, ev_a):
    saved = saved_plays(rec, clue, ev, ev_a)
    if saved is not None:
        return rec, saved
    out = []
    with tempfile.TemporaryDirectory() as td:
        mp3 = Path(td) / "ep.mp3"
        if subprocess.run(["curl", "-sS", "-L", "-o", str(mp3), rec["url"]]).returncode:
            return rec, []
        tag = f"{rec['n']:03d}_{rec['date'][5:16].replace(' ', '-')}"
        for w in rec["windows"]:
            dest = HERE / "segments" / f"{tag}_{int(w['t0'])}.mp3"
            if not dest.exists():
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w['t0']:.2f}", "-i", str(mp3), "-t",
                                f"{w['t1'] - w['t0']:.2f}", "-ac", "1", "-b:a", "64k", str(dest)], check=True)
        for p in rec["plays"]:
            start = p["t"] - PRE - SEARCH
            x = cut(mp3, start, PRE + POST + 2 * SEARCH + 0.1)
            if start < 0:
                x = np.concatenate([np.zeros(int(round(-start * SR))), x])
            r, lag = align(x, ev, int(PRE * SR) + ev_a)   # x starts PRE+SEARCH before the expected clue start
            c0 = lag - ev_a                       # sample where the clue's first sample sits
            a = c0 - int(PRE * SR)
            seg = x[a:a + int((PRE + POST) * SR)] if a >= 0 else None
            if seg is None or len(seg) < int((PRE + POST) * SR):
                continue
            body = seg[int(PRE * SR):int(PRE * SR) + len(clue)]
            g = float(body @ clue) / float(clue @ clue)          # level and polarity relative to our clue
            dest = HERE / "plays" / f"{tag}_{p['t']:.2f}.flac"
            if not dest.exists():
                sf.write(dest, (seg / max(np.max(np.abs(seg)), 1.0)).astype(np.float32), SR, subtype="PCM_24")
            out.append({"date": rec["date"][5:16], "t": p["t"], "fit": round(abs(r), 3), "gain": round(g, 3),
                        "seg": seg / g if abs(g) > 1e-6 else seg})
    return rec, out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-fit", type=float, default=0.7)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    clue, sr = sf.read(HERE / "clue_orig.wav")
    assert sr == SR, sr
    clue = clue.mean(axis=1) if clue.ndim > 1 else clue
    ev_a, ev_b = int(0.04 * SR), int(0.40 * SR)              # the event itself, as find_plays.py uses
    ev = clue[ev_a:ev_b] - clue[ev_a:ev_b].mean()
    ev /= np.linalg.norm(ev)
    (HERE / "plays").mkdir(exist_ok=True)
    (HERE / "segments").mkdir(exist_ok=True)
    recs = [json.loads(line) for line in open(HERE / "harvest.jsonl")]
    recs = [r for r in recs if r["plays"]]
    plays = []
    with ThreadPoolExecutor(args.jobs) as ex:
        for k, (rec, got) in enumerate(ex.map(lambda r: episode_plays(r, clue, ev, ev_a), recs), 1):
            plays += got
            print(f"{k}/{len(recs)} {rec['date'][5:16]}: {len(got)}/{len(rec['plays'])} plays cut", flush=True)
    keep = [p for p in plays if p["fit"] >= args.min_fit]
    out = HERE / "stack"
    out.mkdir(exist_ok=True)
    m = np.array([p["seg"] for p in keep])
    med, mean = np.median(m, axis=0), m.mean(axis=0)
    peak = max(np.max(np.abs(med)), np.max(np.abs(mean)), 1e-9)
    sf.write(out / "clue_stacked_median.wav", (med / peak * 0.9).astype(np.float32), SR)
    sf.write(out / "clue_stacked_mean.wav", (mean / peak * 0.9).astype(np.float32), SR)
    np.savez_compressed(out / "aligned_plays.npz", seg=m.astype(np.float32),
                        date=np.array([p["date"] for p in keep]), t=np.array([p["t"] for p in keep]))
    blk = int(0.025 * SR)
    lines = [f"plays cut {len(plays)}, kept {len(keep)} with fit >= {args.min_fit}; clue sits at "
             f"{PRE:.3f}-{PRE + len(clue) / SR:.3f} s", "",
             "block (s from clue start)  common ratio  mean dB  median dB   (common: ~1 same sound in every play, "
             f"~{1 / max(len(keep), 1):.3f} unrelated)"]
    for b in range(0, m.shape[1] - blk + 1, blk):
        sl = slice(b, b + blk)
        common = float(np.sum(mean[sl] ** 2) / (np.mean(np.sum(m[:, sl] ** 2, axis=1)) + 1e-20))
        db = lambda y: 10 * np.log10(np.mean(y ** 2) + 1e-20)  # noqa: E731
        lines.append(f"{b / SR - PRE:+7.3f}  {common:6.3f}  {db(mean[sl]):7.1f}  {db(med[sl]):7.1f}")
    lines += ["", "per play: date, time in episode, fit, gain"]
    lines += [f"{p['date']}  {p['t']:8.2f}  {p['fit']:.3f}  {p['gain']:+.3f}" for p in sorted(plays, key=lambda p: -p["fit"])]
    (out / "report.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:3 + (m.shape[1] // blk) + 1]))


if __name__ == "__main__":
    main()
