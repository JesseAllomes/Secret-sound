"""Pull only the steel/spring queries with freesound_pull's own search/fetch, retrying 403s."""
import json
import sys
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "/home/user/secret-sound")
import freesound_pull as fp  # noqa: E402

folder = Path(sys.argv[1])
folder.mkdir(parents=True, exist_ok=True)
queries = [q.strip() for q in open(sys.argv[2], encoding="utf-8") if q.strip()]
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
                items = fp.search(token, q, 150, 30)
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
