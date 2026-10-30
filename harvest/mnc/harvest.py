"""Walk the podcast back in time, find every play of the clue, transcribe the talk around each one.

Writes harvest.jsonl (one line per episode) and transcripts/<date>_<n>.txt. Stops after 6 consecutive
BEST BITS episodes with no plays, once at least one play has been found (or after 12 at the start).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

sys.path.insert(0, str(Path(__file__).parent))
from find_plays import find, load  # noqa: E402

HERE = Path(__file__).parent
eps = json.loads((HERE / "eps.json").read_text())
clue = load(str(HERE / "clue_orig.wav"))
model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
(HERE / "transcripts").mkdir(exist_ok=True)
out = open(HERE / "harvest.jsonl", "a")
done = {json.loads(l)["url"] for l in open(HERE / "harvest.jsonl")} if (HERE / "harvest.jsonl").stat().st_size else set()
found_any, misses = False, 0
for n, e in enumerate(eps):
    if e["url"] in done:
        continue
    mp3 = HERE / "ep.mp3"
    r = subprocess.run(["curl", "-sS", "-L", "-o", str(mp3), e["url"]])
    if r.returncode:
        print("download failed", e["title"], flush=True)
        continue
    ep = load(str(mp3))
    plays = find(clue, ep, 0.6)
    rec = {"n": n, "date": e["date"], "title": e["title"], "url": e["url"], "plays": plays, "windows": []}
    # group plays within 120 s into one segment; transcribe 75 s before to 45 s after
    groups = []
    for p in plays:
        if groups and p["t"] - groups[-1][-1]["t"] < 120:
            groups[-1].append(p)
        else:
            groups.append([p])
    if plays:
        a16 = load(str(mp3), 16000)
    for g in groups:
        t0, t1 = max(0, g[0]["t"] - 75), min(len(ep) / 8000, g[-1]["t"] + 45)
        segs, _ = model.transcribe(a16[int(t0 * 16000):int(t1 * 16000)], beam_size=1, vad_filter=True)
        text = "\n".join(f"[{t0 + s.start:7.1f}] {s.text.strip()}" for s in segs)
        rec["windows"].append({"t0": t0, "t1": t1, "text": text})
        name = f"{n:03d}_{e['date'][5:16].replace(' ', '-')}_{int(t0)}.txt"
        (HERE / "transcripts" / name).write_text(f"{e['title']}\n{e['date']}\nplays: {g}\n\n{text}\n")
    out.write(json.dumps(rec) + "\n")
    out.flush()
    print(f"{n:3d} {e['date'][5:16]} plays={len(plays):2d} {e['title'][:60]}", flush=True)
    if plays:
        found_any, misses = True, 0
    elif e["title"].startswith("BEST BITS"):
        misses += 1
    if (found_any and misses >= 6) or (not found_any and misses >= 12):
        print("stopping: sound not found in recent regular episodes", flush=True)
        break
mp3 = HERE / "ep.mp3"
if mp3.exists():
    os.remove(mp3)
