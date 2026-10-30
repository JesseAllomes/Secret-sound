"""Mark clips whose file name matches an exact on-air guess (analysis/mnc/onair_guesses.json), so A/B packs skip
actions already guessed wrong. Mid North Coast only.

    python tools/wrong_filter.py <scores.csv> [--guesses analysis/mnc/onair_guesses.json] [--out marked.csv]

Adds two columns: "onair" (the matching guess and date, or empty) and "onair_verdict" (wrong / warm / unclear).
A clip is dropped from A/B only when it matches a guess with verdict "wrong"; warm and unclear matches are kept and
marked. Matching is by action, not object: each guess carries clip_patterns (groups of regexes that must all match
the clip's name), so "closing the microwave door" does not catch a clip of pushing the microwave's button.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_guesses(path):
    out = []
    for g in json.loads(Path(path).read_text(encoding="utf-8")):
        for pat in g.get("clip_patterns") or []:
            try:
                out.append((g, [re.compile(p, re.I) for p in pat]))
            except re.error:
                continue
    return out


def match(name, guesses):
    """Best on-air match for a clip name: a 'wrong' match wins only if no warm/unclear guess also matches."""
    hits = [g for g, pats in guesses if pats and all(p.search(name) for p in pats)]
    if not hits:
        return None
    keep = [g for g in hits if g.get("verdict") != "wrong"]
    return (keep or hits)[0]


def mark(rows, guesses, name_key="name"):
    for r in rows:
        g = match(r.get(name_key) or "", guesses)
        r["onair"] = f"{g['date']}: {g['guess']}" if g else ""
        r["onair_verdict"] = g.get("verdict", "") if g else ""
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--guesses", default=str(ROOT / "analysis/mnc/onair_guesses.json"))
    ap.add_argument("--out")
    args = ap.parse_args()
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    mark(rows, load_guesses(args.guesses))
    out = args.out or args.csv.replace(".csv", "_marked.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["onair"])
        w.writeheader()
        w.writerows(rows)
    n = sum(r["onair_verdict"] == "wrong" for r in rows)
    print(f"{len(rows)} clips, {n} match a wrong on-air guess, "
          f"{sum(r['onair_verdict'] == 'warm' for r in rows)} match a warm one; wrote {out}")


if __name__ == "__main__":
    main()
