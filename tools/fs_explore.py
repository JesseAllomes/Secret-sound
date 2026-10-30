"""Explore around one Freesound sound: its details, its pack, the uploader's other sounds, and Freesound's own
"similar sounds" (content-based). Downloads previews into a folder in the same shape pull_queries.py writes.

    python tools/fs_explore.py <sound id> <out folder> [--similar 150] [--user 150]

Writes <out>/<id>.mp3, <out>/meta.json (query = "seed" / "pack" / "user" / "similar") and <out>/seed.json (the seed
sound's full description, tags, pack, uploader, geotag). About 5-10 API requests.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import freesound_pull as fp  # noqa: E402

BASE = "https://freesound.org/apiv2"
FIELDS = "id,name,tags,duration,username,url,previews,pack,description"


def get(path, token, **params):
    fp.api_slot()
    q = urllib.parse.urlencode({**params, "token": token})
    with urllib.request.urlopen(f"{BASE}{path}?{q}", timeout=60) as r:
        return json.load(r)


def pages(path, token, limit, **params):
    out, page = [], 1
    while len(out) < limit:
        try:
            d = get(path, token, page=page, page_size=150, fields=FIELDS, **params)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break
            raise
        out += d.get("results", [])
        if not d.get("next"):
            break
        page += 1
    return out[:limit]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sid")
    ap.add_argument("folder")
    ap.add_argument("--similar", type=int, default=150)
    ap.add_argument("--user", type=int, default=150)
    args = ap.parse_args()
    token = fp.key()
    out = Path(args.folder)
    out.mkdir(parents=True, exist_ok=True)
    seed = get(f"/sounds/{args.sid}/", token, fields=FIELDS + ",geotag,created,license,num_downloads,avg_rating,ac_analysis")
    (out / "seed.json").write_text(json.dumps(seed, indent=1))
    print("seed:", seed["name"], "|", seed.get("username"), "| pack:", seed.get("pack"), "| tags:", seed.get("tags"))
    print("description:", (seed.get("description") or "")[:600])
    found = [("seed", seed)]
    if seed.get("pack"):
        pid = str(seed["pack"]).rstrip("/").split("/")[-1]
        found += [("pack", s) for s in pages(f"/packs/{pid}/sounds/", token, 300)]
    found += [("user", s) for s in pages(f"/users/{urllib.parse.quote(seed['username'])}/sounds/", token, args.user)]
    try:
        found += [("similar", s) for s in pages(f"/sounds/{args.sid}/similar/", token, args.similar)]
    except urllib.error.HTTPError as e:
        print("similar sounds unavailable:", e.code)
    meta = {}
    for q, s in found:
        meta.setdefault(str(s["id"]), {"id": s["id"], "name": s["name"], "tags": s.get("tags", []), "duration": s.get("duration"),
                                       "username": s.get("username"), "url": s.get("url"), "query": q,
                                       "description": (s.get("description") or "")[:300], "previews": s.get("previews")})
    with ThreadPoolExecutor(16) as ex:
        ok = sum(ex.map(lambda m: fp.fetch(m, out), [m for m in meta.values() if m.get("previews")]))
    for m in meta.values():
        m.pop("previews", None)
    (out / "meta.json").write_text(json.dumps(meta))
    counts = {q: sum(m["query"] == q for m in meta.values()) for q in ("seed", "pack", "user", "similar")}
    print(f"{len(meta)} sounds ({counts}), {ok} downloaded")


if __name__ == "__main__":
    main()
