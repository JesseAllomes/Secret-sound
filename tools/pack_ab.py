"""Package the A/B files of a clap_index ranking into a numbered folder + zip with an INDEX.txt.

    python tools/pack_ab.py <scores.csv> <ab folder> <out folder> --title "..." [--n 20]

Skips rows whose onair_verdict is "wrong" (tools/wrong_filter.py) and marks warm/unclear on-air matches in the index.
"""
import argparse
import csv
import re
import shutil
import zipfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("ab")
    ap.add_argument("out")
    ap.add_argument("--title", default="")
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    ab = {re.search(r"_([^_]+)\.mp3$", p.name).group(1): p for p in Path(args.ab).glob("*.mp3")}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    lines, k = [args.title, ""], 0
    for r in csv.DictReader(open(args.csv, encoding="utf-8")):
        if r.get("onair_verdict") == "wrong" or r["id"] not in ab:
            continue
        k += 1
        name = re.sub(r"[^A-Za-z0-9]+", "-", (r.get("name") or r["id"]).rsplit(".", 1)[0]).strip("-")[:40]
        shutil.copy(ab[r["id"]], out / f"{k:02d}_{name}_{r['id']}.mp3")
        note = f"   [on air {r['onair_verdict']}: {r['onair']}]" if r.get("onair") else ""
        src = f"freesound.org/s/{r['id']}" if r["id"].isdigit() and len(r["id"]) < 8 else f"BBC {r['id']}"
        lines.append(f"{k:2d}. {float(r['score']):.3f}  {r.get('name', '')}  [{r.get('query', '')}]  ({src}){note}")
        if k >= args.n:
            break
    (out / "INDEX.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    z = out.with_suffix(".zip")
    with zipfile.ZipFile(z, "w") as zf:
        for p in sorted(out.iterdir()):
            zf.write(p, p.name)
    print("\n".join(lines))
    print(z)


if __name__ == "__main__":
    main()
