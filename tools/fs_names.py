"""Look up Freesound names and tags for clips that came without meta.json (e.g. the work zip), cheaply.

    python tools/fs_names.py <scores.csv> <meta.json> [--top 300]

Takes the ids of the top rows of a clap_index/steel_score CSV, asks Freesound for 100 ids per request
(filter id:(a OR b ...)), and adds name/tags/username/url to meta.json. 300 ids = 3 API requests.
"""
import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import freesound_pull as fp  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("meta")
    ap.add_argument("--top", type=int, default=300)
    args = ap.parse_args()
    meta_path = Path(args.meta)
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    ids = []
    for row in csv.DictReader(open(args.csv, encoding="utf-8")):
        if row["id"].isdigit() and row["id"] not in meta and row["id"] not in ids:
            ids.append(row["id"])
        if len(ids) >= args.top:
            break
    token = fp.key()
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        q = urllib.parse.urlencode({"query": "", "filter": f"id:({' OR '.join(batch)})", "page_size": 150,
                                    "fields": "id,name,tags,duration,username,url", "token": token})
        fp.api_slot()
        with urllib.request.urlopen(f"{fp.API}?{q}", timeout=60) as r:
            for it in json.load(r).get("results", []):
                meta[str(it["id"])] = {**it, "query": "work zip"}
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    print(f"{len(ids)} ids looked up, meta has {len(meta)}")


if __name__ == "__main__":
    main()
