"""Mid North Coast only: harvest.py's work for given episodes, so many machines can each take one.

    python harvest_one.py <n> [<n> ...] --out <dir>

For each episode index n in eps.json: find the plays, transcribe 75 s before to 45 s after each group (as harvest.py),
then keep the audio (stack_plays.py: plays/*.flac, segments/*.mp3). Writes <out>/rec_<n>.json, <out>/transcripts/,
<out>/plays/, <out>/segments/. Merge the records into harvest.jsonl afterwards (sorted by n).
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import stack_plays as sp  # noqa: E402
from find_plays import find, load  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("n", type=int, nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    from faster_whisper import WhisperModel
    out = Path(args.out)
    for d in ("transcripts", "plays", "segments"):
        (out / d).mkdir(parents=True, exist_ok=True)
    sp.HERE = out                                    # stack_plays writes plays/ and segments/ under its HERE
    eps = json.loads((HERE / "eps.json").read_text())
    clue8 = load(str(HERE / "clue_orig.wav"))
    clue, _ = sf.read(HERE / "clue_orig.wav")
    clue = clue.mean(axis=1) if clue.ndim > 1 else clue
    ev_a = int(0.04 * sp.SR)
    ev = clue[ev_a:int(0.40 * sp.SR)] - clue[ev_a:int(0.40 * sp.SR)].mean()
    ev /= np.linalg.norm(ev)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    for n in args.n:
        e = eps[n]
        with tempfile.TemporaryDirectory() as td:
            mp3 = Path(td) / "ep.mp3"
            subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-o", str(mp3), e["url"]], check=True)
            ep = load(str(mp3))
            plays = find(clue8, ep, 0.6)
            rec = {"n": n, "date": e["date"], "title": e["title"], "url": e["url"], "plays": plays, "windows": []}
            groups = []
            for p in plays:
                if groups and p["t"] - groups[-1][-1]["t"] < 120:
                    groups[-1].append(p)
                else:
                    groups.append([p])
            a16 = load(str(mp3), 16000) if plays else None
            for g in groups:
                t0, t1 = max(0, g[0]["t"] - 75), min(len(ep) / 8000, g[-1]["t"] + 45)
                segs, _ = model.transcribe(a16[int(t0 * 16000):int(t1 * 16000)], beam_size=1, vad_filter=True)
                text = "\n".join(f"[{t0 + s.start:7.1f}] {s.text.strip()}" for s in segs)
                rec["windows"].append({"t0": t0, "t1": t1, "text": text})
                name = f"{n:03d}_{e['date'][5:16].replace(' ', '-')}_{int(t0)}.txt"
                (out / "transcripts" / name).write_text(f"{e['title']}\n{e['date']}\nplays: {g}\n\n{text}\n")
        cut = sp.episode_plays(rec, clue, ev, ev_a)[1] if plays else []
        (out / f"rec_{n:03d}.json").write_text(json.dumps(rec))
        print(f"{n:3d} {e['date'][5:16]} plays={len(plays):2d} cut={len(cut)} {e['title'][:60]}", flush=True)


if __name__ == "__main__":
    main()
