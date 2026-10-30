"""Mid North Coast only: build the evidence package for an analysis pass (no model needed to run this).

Writes package/mnc_evidence.md with, for every segment where the clue was played (oldest first):
date, jackpot amounts said, and the transcript from 45 s before the first play to 30 s after the last (caller guess,
Sarge's reaction, any clues). Also a jackpot timeline. Copies the clue audio alongside.
"""
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "package"
OUT.mkdir(exist_ok=True)
LINE = re.compile(r"^\[\s*([\d.]+)\]\s*(.*)$")
MONEY = re.compile(r"\$ ?\d[\d,]*|\b\d,\d{3}\b")

recs = [json.loads(l) for l in open(HERE / "harvest.jsonl")]
recs = [r for r in recs if r["plays"]]
recs.sort(key=lambda r: r["n"], reverse=True)          # oldest episode first
parts, timeline = [], []
for r in recs:
    date = r["date"][5:16]
    for w in r["windows"]:
        plays = [p["t"] for p in r["plays"] if w["t0"] <= p["t"] <= w["t1"]]
        if not plays:
            continue
        lo, hi = min(plays) - 45, max(plays) + 30
        lines = []
        for ln in w["text"].splitlines():
            m = LINE.match(ln)
            if m and lo <= float(m.group(1)) <= hi:
                lines.append(f"[{float(m.group(1)) - min(plays):+6.1f}s] {m.group(2)}")
        money = sorted({x.replace(" ", "") for x in MONEY.findall(w["text"])})
        timeline.append((date, money))
        parts.append(f"### {date} (segment at {int(min(plays))} s, {len(plays)} play(s))\n"
                     f"Amounts said: {', '.join(money) or 'none'}\n\n```\n" + "\n".join(lines) + "\n```\n")
head = ("# Mid North Coast Secret Sound: evidence from the Sarge for Breakfast podcast\n\n"
        "Every segment where the clue was played, oldest first. Times are relative to the first play in the segment "
        "(negative = before the sound). Transcribed automatically (faster-whisper small.en): names and some words may be "
        "misheard. 'Absolutely not!' is the show's catchphrase for a wrong answer (a promo voice, 'Promo Sally').\n\n"
        f"Episodes with plays: {len(recs)}, segments: {len(parts)}. First episode with the sound: {recs[0]['date'][5:16]}; "
        f"latest: {recs[-1]['date'][5:16]}.\n\n## Jackpot amounts said per segment\n"
        + "\n".join(f"- {d}: {', '.join(m) or '-'}" for d, m in timeline) + "\n\n## Segments\n\n")
(OUT / "mnc_evidence.md").write_text(head + "\n".join(parts))
for f in ("clue_orig.wav",):
    shutil.copy(HERE / f, OUT / "clue_original.wav")
shutil.copy(HERE.parents[1] / "clues" / "mnc" / "clue_stacked.wav", OUT / "clue_stacked.wav")
print(OUT / "mnc_evidence.md", len(parts), "segments,", (OUT / "mnc_evidence.md").stat().st_size // 1024, "KB")
