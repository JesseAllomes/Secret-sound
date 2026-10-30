"""Pull Freesound previews for exactly the searches in a file (none of freesound_pull.py's built-in list).

    python pull_queries.py <out folder> <queries file> [--per-query 150] [--max-seconds 30]

Uses freesound_pull.py's search and fetch (API key from ~/.secret-song/freesound.key, 60 requests a minute).
Writes <id>.mp3 and meta.json with each clip's query. Searches already in meta.json are skipped; 403/429 responses
are retried after a pause.
"""
import argparse
import json
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import freesound_pull as fp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("queries")
    ap.add_argument("--per-query", type=int, default=150)
    ap.add_argument("--max-seconds", type=float, default=30)
    args = ap.parse_args()
    folder = Path(args.folder)
    folder.mkdir(parents=True, exist_ok=True)
    queries = [q.strip() for q in open(args.queries, encoding="utf-8") if q.strip() and not q.startswith("#")]
    meta_path = folder / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    done = {m.get("query") for m in meta.values()}
    token = fp.key()
    with ThreadPoolExecutor(16) as dl:
        for q in queries:
            if q in done:
                continue
            items = None
            for wait in (20, 60, 120):
                try:
                    items = fp.search(token, q, args.per_query, args.max_seconds)
                    break
                except urllib.error.HTTPError as e:
                    print(f"{q}: HTTP {e.code}, waiting {wait} s", flush=True)
                    time.sleep(wait)
            if items is None:
                print(f"{q}: gave up", flush=True)
                continue
            new = [i for i in items if str(i["id"]) not in meta]
            ok = sum(dl.map(lambda i: fp.fetch(i, folder), new))
            for i in new:
                meta[str(i["id"])] = {"id": i["id"], "name": i["name"], "tags": i.get("tags", []),
                                      "duration": i.get("duration"), "username": i.get("username"),
                                      "url": i.get("url"), "query": q}
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            print(f"{q}: {len(items)} found, {len(new)} new, {ok} downloaded, {len(meta)} total", flush=True)


if __name__ == "__main__":
    main()
