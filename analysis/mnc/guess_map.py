"""Mid North Coast only: turn every on-air play into (guess, Sarge's reaction) and map what the guesses have in common.

No model tokens. For every play segment in harvest/mnc/harvest.jsonl:
  guess    = what was said from the last play of the clue up to Sarge's verdict (or 35 s, whichever is first)
  reaction = the verdict and the 20 s after it, graded by keywords:
             3 hot/close/almost/"words in"/"first half"   2 right track/warmer/good guess   0 "absolutely not"/wrong
             1 anything else (no clear verdict heard)
Then:
  - word warmth: every content word across guesses, its count and mean reaction grade
  - CLAP text-audio score: how much the CLAP model thinks each guess's words describe the clue audio (--clap)
Writes guess_map.csv and guess_map.md next to this script.

    python analysis/mnc/guess_map.py [--clap] [--clue clues/mnc/clue_v6b.wav]
"""
import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
LINE = re.compile(r"^\[\s*([\d.]+)\]\s*(.*)$")
VERDICT = re.compile(r"(?i)absolutely not|not the secret sound|that'?s not it|you'?re (?:hot|close|warm)|so close|"
                     r"very close|remarkably close|getting (?:warmer|closer)|right track|almost|first half|"
                     r"words that would be|good guess|wonderful guess|great guess|not quite|move away")
GRADES = [(3, re.compile(r"(?i)\bhot\b|so close|very close|remarkably close|\balmost\b|first half|words that would be|"
                         r"you'?re close")),
          (2, re.compile(r"(?i)right track|getting (?:warmer|closer)|\bwarm\b|good guess|wonderful guess|great guess|"
                         r"not quite")),
          (0, re.compile(r"(?i)absolutely not|not the secret sound|that'?s not it|move away|nowhere near"))]
STOP = set("""a an the and or but if then so to of in on at by for with from up down out over into onto off is it its
it's i i'm im you your you're we our they them he she his her this that these those there here what when where who
how why be been being am are was were do does did doing have has had having can could would should will just like
think reckon guess maybe probably yeah yes no oh um uh ah okay ok well mate sarge sound secret really very going
gonna get got getting go one some something thing things kind sort bit little say said know mean right good""".split())


def words(text):
    out = []
    for w in re.findall(r"[a-z']+", text.lower()):
        w = w.strip("'")
        if len(w) < 3 or w in STOP:
            continue
        for suf in ("ing", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                w = w[: -len(suf)]
                break
        out.append(w)
    return out


def grade(text):
    for g, rx in GRADES:
        if rx.search(text):
            return g
    return 1


def segments(harvest):
    rows = []
    for rec in map(json.loads, open(harvest)):
        for w in rec["windows"]:
            plays = [p["t"] for p in rec["plays"] if w["t0"] <= p["t"] <= w["t1"]]
            if not plays:
                continue
            last = max(plays)
            lines = [(float(m.group(1)), m.group(2)) for ln in w["text"].splitlines() if (m := LINE.match(ln))]
            after = [(t, s) for t, s in lines if t >= last - 1]
            vt = next((t for t, s in after if t > last + 2 and VERDICT.search(s)), None)
            end = min(vt if vt is not None else last + 35, last + 35)
            guess = " ".join(s for t, s in after if t < end)
            react = " ".join(s for t, s in after if vt is not None and vt <= t <= vt + 20)
            rows.append({"date": rec["date"][5:16], "n": rec["n"], "t": round(last, 1), "guess": guess.strip(),
                         "reaction": react.strip(), "grade": grade(react) if react else 1})
    rows.sort(key=lambda r: -r["n"])            # oldest first
    return rows


def clap_scores(rows, clue_path):
    import librosa
    import torch
    from sfx_match import SR, Clap, load_clue
    clap = Clap()
    ce = clap.embed([load_clue(clue_path)])[0]
    texts = [r["guess"][:300] or "silence" for r in rows]
    out = []
    with torch.no_grad():
        for i in range(0, len(texts), 32):
            t = clap.proc(text=texts[i:i + 32], return_tensors="pt", padding=True, truncation=True)
            e = clap.model.get_text_features(**t)
            e = getattr(e, "pooler_output", e)
            out.append(torch.nn.functional.normalize(e, dim=-1).numpy())
    del librosa, SR
    return np.concatenate(out) @ ce


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--harvest", default=str(ROOT / "harvest/mnc/harvest.jsonl"))
    ap.add_argument("--clap", action="store_true")
    ap.add_argument("--clue", default=str(ROOT / "clues/mnc/clue_v6b.wav"))
    args = ap.parse_args()
    rows = segments(args.harvest)
    if args.clap:
        import sys
        sys.path.insert(0, str(ROOT))
        for r, s in zip(rows, clap_scores(rows, args.clue)):
            r["clap"] = round(float(s), 4)
    with open(HERE / "guess_map.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "n", "t", "grade", "clap", "guess", "reaction"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    stats = defaultdict(list)
    for r in rows:
        for wd in set(words(r["guess"])):
            stats[wd].append(r["grade"])
    common = sorted(((w, len(g), np.mean(g)) for w, g in stats.items() if len(g) >= 3), key=lambda x: (-x[2], -x[1]))
    graded = [r for r in rows if r["grade"] != 1]
    md = ["# Mid North Coast: guesses and Sarge's reactions (generated by guess_map.py, no model)", "",
          f"Segments: {len(rows)}; with a clear verdict: {len(graded)} "
          f"(hot/close {sum(r['grade'] == 3 for r in rows)}, warm {sum(r['grade'] == 2 for r in rows)}, "
          f"wrong {sum(r['grade'] == 0 for r in rows)}). Grades come from keywords in the reaction, so check the text.", "",
          "## Warm and hot reactions (oldest first)", ""]
    for r in rows:
        if r["grade"] >= 2:
            md += [f"- **{r['date']}** (grade {r['grade']}{', clap %.3f' % r['clap'] if 'clap' in r else ''})  ",
                   f"  guess: {r['guess'][:300]}  ", f"  reaction: {r['reaction'][:300]}"]
    md += ["", "## Word warmth (words in at least 3 guesses; mean grade, 0 wrong .. 3 hot)", "",
           "| word | guesses | mean grade |", "|---|---|---|"]
    md += [f"| {w} | {n} | {m:.2f} |" for w, n, m in common[:60]]
    if args.clap:
        top = sorted(rows, key=lambda r: -r["clap"])[:25]
        g = np.array([r["grade"] for r in graded])
        c = np.array([r["clap"] for r in graded])
        corr = float(np.corrcoef(g, c)[0, 1]) if len(graded) > 2 else float("nan")
        md += ["", f"## Guesses CLAP thinks describe the clue best (clue: {Path(args.clue).name})", "",
               f"Correlation between CLAP score and Sarge's grade over graded guesses: {corr:+.2f} "
               "(near 0 = CLAP's text sense does not track Sarge; treat the ranking as weak).", ""]
        md += [f"- {r['clap']:.3f} [grade {r['grade']}] {r['date']}: {r['guess'][:200]}" for r in top]
    (HERE / "guess_map.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(rows)} segments, {len(graded)} graded; wrote {HERE / 'guess_map.md'}")


if __name__ == "__main__":
    main()
