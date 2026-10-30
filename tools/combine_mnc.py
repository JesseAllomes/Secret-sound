"""Mid North Coast only: one ranking across runs from both scorers, so a clip has to sound right to CLAP *and* carry
the clue's structure (steel_score: two strokes ~138 ms apart, thump, ring, isolation) to rank high.

    python tools/combine_mnc.py <results dir> [<results dir> ...] [--out combined.csv] [--top 40]

Each results dir holds clap_scores.csv (clap_index) and scores.csv (steel_score). Scores are turned into percentiles
within each scorer over all clips seen, and combined as their geometric mean. Clips matching a wrong on-air guess
(tools/wrong_filter.py) are marked and listed last.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wrong_filter  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--out", default="combined.csv")
    ap.add_argument("--top", type=int, default=40)
    args = ap.parse_args()
    clap, steel, info = {}, {}, {}
    for d in map(Path, args.dirs):
        for r in csv.DictReader(open(d / "clap_scores.csv", encoding="utf-8")):
            clap[r["id"]] = max(clap.get(r["id"], 0.0), float(r["score"]))
            info.setdefault(r["id"], {"name": r.get("name", ""), "query": r.get("query", ""), "run": d.name})
        if (d / "scores.csv").exists():
            for r in csv.DictReader(open(d / "scores.csv", encoding="utf-8")):
                i = Path(r["file"]).stem
                steel[i] = max(steel.get(i, 0.0), float(r["score"]))
                info.setdefault(i, {"name": r.get("name", ""), "query": r.get("query", ""), "run": d.name})
    both = [i for i in clap if i in steel]

    def pct(d):
        v = np.array(sorted(d.values()))
        return {k: float(np.searchsorted(v, x, side="right")) / len(v) for k, x in d.items()}

    pc, ps = pct(clap), pct(steel)
    rows = [{"id": i, "combined": round(float(np.sqrt(pc[i] * ps[i])), 4), "clap": round(clap[i], 4),
             "steel": round(steel[i], 4), "clap_pct": round(pc[i], 3), "steel_pct": round(ps[i], 3), **info[i]}
            for i in both]
    wrong_filter.mark(rows, wrong_filter.load_guesses(ROOT / "analysis/mnc/onair_guesses.json"))
    rows.sort(key=lambda r: (r["onair_verdict"] == "wrong", -r["combined"]))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(both)} clips scored by both (CLAP {len(clap)}, steel {len(steel)})")
    for r in rows[:args.top]:
        tag = f"  [on air {r['onair_verdict']}]" if r["onair"] else ""
        print(f"{r['combined']:.3f}  clap {r['clap']:.3f} ({r['clap_pct']:.2f})  steel {r['steel']:.3f} "
              f"({r['steel_pct']:.2f})  {r['id']}  [{r['query']}] {r['name'][:55]}{tag}")


if __name__ == "__main__":
    main()
