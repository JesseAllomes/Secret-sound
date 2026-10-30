"""Mid North Coast only: pull caller guesses, clues and jackpot mentions out of the harvested transcripts.

For each segment, keeps the lines from 40 s before the first play to 25 s after the last that look like a guess or a
clue, plus every dollar amount. Writes guesses.tsv (date, segment, time, kind, text) and prints a compact list.
"""
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
GUESS = re.compile(r"(?i)\b(i think it'?s|i think (?:that )?(?:is|it is)|is it (?:a|an|the|someone|somebody|when)|my guess|"
                   r"i reckon|i'?m going (?:to say|with)|i'?ll (?:say|go with)|i(?:'d| would) say|it'?s (?:a|an|the|someone|"
                   r"somebody) \w+ing|sounds? like|could it be|maybe it'?s|has to be|is that)\b")
CLUE = re.compile(r"(?i)\b(clue|hint|cryptic|it'?s not|close|warm|cold|you'?re on the right|right track|nowhere near)\b")
MONEY = re.compile(r"\$ ?\d[\d,]*")
LINE = re.compile(r"^\[\s*([\d.]+)\]\s*(.*)$")

rows = []
for rec in map(json.loads, open(HERE / "harvest.jsonl")):
    if not rec["plays"]:
        continue
    date = rec["date"][5:16]
    for w in rec["windows"]:
        plays = [p["t"] for p in rec["plays"] if w["t0"] <= p["t"] <= w["t1"]]
        if not plays:
            continue
        lo, hi = min(plays) - 40, max(plays) + 25
        for ln in w["text"].splitlines():
            m = LINE.match(ln)
            if not m:
                continue
            t, text = float(m.group(1)), m.group(2)
            money = MONEY.findall(text)
            if money:
                rows.append((date, int(w["t0"]), t, "jackpot", " ".join(money) + "  | " + text))
            if lo <= t <= hi:
                if GUESS.search(text):
                    rows.append((date, int(w["t0"]), t, "guess", text))
                elif CLUE.search(text):
                    rows.append((date, int(w["t0"]), t, "clue?", text))
with open(HERE / "guesses.tsv", "w", newline="") as f:
    csv.writer(f, delimiter="\t").writerows([("date", "segment", "t", "kind", "text"), *rows])
for r in rows:
    print(f"{r[0]}  {r[3]:7s} {r[4][:170]}")
