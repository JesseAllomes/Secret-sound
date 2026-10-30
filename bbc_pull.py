"""Pull BBC Sound Effects (sound-effects.bbcrewind.co.uk) for a list of searches.

    python bbc_pull.py <out folder> --queries queries.txt [--per-query 30]

Writes <id>.mp3 and meta.json in the same shape freesound_pull.py does (id, name, duration, url, query), so
steel_score.py --meta works on either. Already-downloaded ids are skipped. No API key needed.
"""
import argparse
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = "https://sound-effects-api.bbcrewind.co.uk/api/sfx/search"
MEDIA = "https://sound-effects-media.bbcrewind.co.uk/mp3/{}.mp3"
UA = {"User-Agent": "secret-sound/1.0", "Content-Type": "application/json"}


def search(query, size):
    body = json.dumps({"criteria": {"from": 0, "size": size, "query": query}}).encode()
    with urllib.request.urlopen(urllib.request.Request(API, data=body, headers=UA), timeout=60) as r:
        return json.load(r).get("results", [])


def fetch(sid, folder):
    p = folder / f"{sid}.mp3"
    if p.exists():
        return True
    try:
        p.write_bytes(urllib.request.urlopen(urllib.request.Request(MEDIA.format(sid), headers=UA), timeout=120).read())
        return True
    except Exception as exc:
        print(f"  {sid}: {exc}", flush=True)
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--queries", required=True)
    ap.add_argument("--per-query", type=int, default=30)
    args = ap.parse_args()
    folder = Path(args.folder)
    folder.mkdir(parents=True, exist_ok=True)
    meta_path = folder / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    queries = [q.strip() for q in open(args.queries, encoding="utf-8") if q.strip() and not q.startswith("#")]
    with ThreadPoolExecutor(6) as pool:
        for q in queries:
            try:
                res = search(q, args.per_query)
            except Exception as exc:
                print(f"{q}: search failed: {exc}", flush=True)
                continue
            new = [r for r in res if str(r["id"]) not in meta]
            ok = sum(pool.map(lambda r: fetch(r["id"], folder), new))
            for r in new:
                meta[str(r["id"])] = {"id": r["id"], "name": r.get("description", ""), "duration": r.get("duration"),
                                      "url": f"https://sound-effects.bbcrewind.co.uk/search?q={r['id']}", "query": q}
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            print(f"{q}: {len(res)} found, {len(new)} new, {ok} downloaded, {len(meta)} total", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    main()
