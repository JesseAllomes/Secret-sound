"""Pull short everyday-object sound effects from Freesound for Secret Sound matching (local only).

    python freesound_pull.py <out folder> [--per-query 300] [--max-seconds 20] [--queries more.txt]

Reads the API key from ~/.secret-song/freesound.key. Saves <id>.mp3 (the HQ preview) and
meta.json (id, name, tags, duration, user, url). Already-downloaded ids are skipped, so it can be
re-run with more queries. Then build a scoring database with --make-db and score with run.py.
"""
import argparse
import json
import sqlite3
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

API = "https://freesound.org/apiv2/search/text/"
QUERIES = """click plastic|snap plastic|clip plastic|latch|button press|button click|switch click|toggle switch|
light switch|power point plug|plug socket|charger plug|phone charger|usb plug|cable plug in|
kettle switch|kettle lid|toaster|microwave door|microwave button|fridge door|oven door|dishwasher door|
cupboard door|drawer close|cabinet latch|magnetic catch|lid close|lid snap|container lid|tupperware|
jar lid|bottle cap|bottle opening|cap click|pump bottle|soap dispenser|spray bottle|trigger spray|
aerosol|toothbrush|electric toothbrush|razor|hair clip|hair dryer switch|shower head|shower nozzle|
tap turn|faucet handle|toilet flush|toilet seat|tissue box|pen click|pen cap|marker cap|stapler|
hole punch|scissors|tape dispenser|tape measure|ruler|binder clip|paper clip|clipboard|
keyboard key|mouse click|remote control|remote battery cover|battery cover|game controller|
nintendo switch|console click|phone case|phone lock button|camera shutter|lighter|zippo|
gas lighter|igniter|stove knob|bbq igniter|measuring cup|measuring spoon|whisk|tongs|peeler|
can opener|ring pull|bottle opener|cork|lunch box|zip lock bag|velcro|zipper|buckle|seatbelt|
belt buckle|car door|car key|key fob|keys|padlock|lock click|door handle|door latch|screen door|
gate latch|letterbox|mailbox|umbrella|folding chair|pram|clothes peg|hanger|iron click|
vacuum button|fan switch|lamp switch|pull cord|blind cord|curtain rod|velux|window latch|
sliding window|watch clasp|bracelet clasp|necklace clasp|cufflink|ring box|jewellery box|
glasses case|sunglasses case|compact mirror|makeup compact|lipstick|nail clippers|tweezers|
dog clicker|clicker|tally counter|timer wind|kitchen timer|egg timer|thermostat|dial turn|
knob click|ratchet|tool click|spring|spring boing|lever|lever pull|handle pull|crank|
cupboard knock|tap on plastic|tap on glass|cup on table|mug down|plate down|cutlery|spoon""".replace("\n", "")


def key():
    return (Path.home() / ".secret-song" / "freesound.key").read_text().strip()


_api_lock = threading.Lock()
_api_last = [0.0]


def api_slot(gap=1.05):
    """Freesound allows 60 API requests a minute; space every search request (across threads)
    at least `gap` seconds apart. Preview downloads are file-server requests and don't count."""
    with _api_lock:
        wait = _api_last[0] + gap - time.time()
        if wait > 0:
            time.sleep(wait)
        _api_last[0] = time.time()


def search(token, query, per_query, max_s):
    out, page = [], 1
    while len(out) < per_query:
        q = urllib.parse.urlencode({"query": query, "filter": f"duration:[0.15 TO {max_s}]", "page": page,
                                    "page_size": 150, "fields": "id,name,tags,duration,username,url,previews",
                                    "token": token})
        for k in range(4):
            api_slot()
            try:
                with urllib.request.urlopen(f"{API}?{q}", timeout=60) as r:
                    d = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(30 * (k + 1))
                    continue
                if e.code == 404:          # past the last page
                    return out
                raise
        else:
            return out
        out += d.get("results", [])
        if not d.get("next"):
            break
        page += 1
    return out[:per_query]


def fetch(item, folder):
    p = folder / f"{item['id']}.mp3"
    if p.exists():
        return True
    try:
        url = item["previews"]["preview-hq-mp3"]
        req = urllib.request.Request(url, headers={"User-Agent": "secret-sound-matcher"})
        p.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        return True
    except Exception:  # noqa: BLE001 - one bad preview is skipped
        return False


def make_db(folder, db_path):
    """A toolkit database whose 'songs' are the effects, ready for run.py go --score-only."""
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(Path(__file__).parent))
    from common import SCHEMA
    c = sqlite3.connect(db_path)
    c.executescript(SCHEMA)
    for m in meta.values():
        p = folder / f"{m['id']}.mp3"
        if p.exists():
            c.execute("INSERT OR IGNORE INTO songs(key, artist, title, list, status, path, url, updated) "
                      "VALUES (?,?,?,?,?,?,?,?)", (f"fs{m['id']}", m.get("username", ""), m["name"],
                                                   m.get("query", ""), "ok", str(p), m.get("url", ""), time.time()))
    c.commit()
    print(f"{db_path}: {c.execute('SELECT COUNT(*) FROM songs').fetchone()[0]} effects")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--per-query", type=int, default=300)
    ap.add_argument("--max-seconds", type=float, default=20)
    ap.add_argument("--queries", help="file with extra queries, one per line")
    ap.add_argument("--make-db", help="write a scoring database here from what is downloaded")
    ap.add_argument("--parallel", type=int, default=3, help="searches at once (they share the 60/min limit)")
    ap.add_argument("--downloads", type=int, default=16, help="preview downloads at once")
    args = ap.parse_args()
    folder = Path(args.out)
    folder.mkdir(parents=True, exist_ok=True)
    if args.make_db:
        make_db(folder, args.make_db)
        return
    meta_path = folder / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    queries = [q.strip() for q in QUERIES.split("|") if q.strip()]
    if args.queries:
        queries += [q.strip() for q in open(args.queries, encoding="utf-8") if q.strip()]
    token = key()
    done_queries = {m.get("query") for m in meta.values()}
    todo = [q for q in queries if q not in done_queries]
    print(f"{len(queries) - len(todo)} queries already pulled, {len(todo)} to go", flush=True)
    lock = threading.Lock()
    downloads = ThreadPoolExecutor(args.downloads)

    def one(q):
        items = search(token, q, args.per_query, args.max_seconds)
        with lock:
            items = [i for i in items if str(i["id"]) not in meta]
            for i in items:              # claim them so a parallel query doesn't fetch them twice
                meta[str(i["id"])] = {"id": i["id"], "name": i["name"], "tags": i.get("tags", []),
                                      "duration": i.get("duration"), "username": i.get("username"),
                                      "url": i.get("url"), "query": q}
        ok = sum(downloads.map(lambda i: fetch(i, folder), items))
        with lock:
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            print(f"{q}: {len(items)} new, {ok} downloaded, {len(meta)} total", flush=True)

    with ThreadPoolExecutor(args.parallel) as ex:
        list(ex.map(one, todo))
    downloads.shutdown()
    print(f"done: {len(meta)} effects", flush=True)


if __name__ == "__main__":
    main()
