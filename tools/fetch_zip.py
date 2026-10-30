"""Download a shared zip of sounds (OneDrive, Google Drive or Dropbox link), unzip it into its own folder, write a manifest.

    python tools/fetch_zip.py <share link> <dest folder> [--manifest data_manifests/work_zip.tsv]

The zip is too big for git, so the repo keeps the manifest (path, bytes, sha256 of every file) and the link
(<manifest>.url); running this again with the same link rebuilds the same folder. Already-downloaded zips are reused.
"""
import argparse
import base64
import hashlib
import json
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path


def direct_url(link):
    m = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?id=)([\w-]+)", link)
    if m:
        return f"https://drive.usercontent.google.com/download?id={m.group(1)}&export=download&confirm=t"
    if "dropbox.com" in link:
        return re.sub(r"([?&])dl=0", r"\1dl=1", link) if "dl=0" in link else link + ("&" if "?" in link else "?") + "dl=1"
    return link


def onedrive_request(link):
    """Personal OneDrive (1drv.ms) links: onedrive.live.com blocks cloud IPs, but the anonymous share API works
    with a public 'Badger' token (the one OneDrive's own web viewer uses)."""
    req = urllib.request.Request("https://api-badgerp.svc.ms/v1.0/token", method="POST",
                                 data=b'{"appId":"5cbed6ac-a083-4e14-b191-b4ba07653de2"}',
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        token = json.load(r)["token"]
    enc = base64.urlsafe_b64encode(link.strip().encode()).decode().rstrip("=")
    return urllib.request.Request(f"https://my.microsoftpersonalcontent.com/_api/v2.0/shares/u!{enc}/driveitem/content",
                                  headers={"Authorization": f"Badger {token}", "Prefer": "autoredeem"})


def download(url, dest):
    tmp = dest.with_suffix(".part")
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        total, got = int(r.headers.get("Content-Length") or 0), 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            got += len(chunk)
            if got % (100 << 20) < (1 << 20):
                print(f"{got >> 20} MB" + (f" of {total >> 20} MB" if total else ""), flush=True)
    tmp.rename(dest)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("link")
    ap.add_argument("dest")
    ap.add_argument("--manifest", default="data_manifests/work_zip.tsv")
    args = ap.parse_args()
    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    zpath = dest.parent / f"{dest.name}.zip"
    if not zpath.exists():
        is_od = re.search(r"1drv\.ms|onedrive\.live\.com", args.link)
        download(onedrive_request(args.link) if is_od else direct_url(args.link), zpath)
    if not zipfile.is_zipfile(zpath):
        head = zpath.read_bytes()[:300]
        zpath.unlink()
        raise SystemExit(f"not a zip (is the link shared with 'Anyone with the link'?): {head[:200]!r}")
    with zipfile.ZipFile(zpath) as z:
        z.extractall(dest)  # zipfile drops absolute paths and '..' parts
    for junk in dest.rglob("__MACOSX"):
        shutil.rmtree(junk, ignore_errors=True)
    files = sorted(p for p in dest.rglob("*") if p.is_file())
    man = Path(args.manifest)
    man.parent.mkdir(parents=True, exist_ok=True)
    with open(man, "w", encoding="utf-8") as f:
        f.write(f"# zip sha256 {sha256(zpath)} bytes {zpath.stat().st_size}\npath\tbytes\tsha256\n")
        for p in files:
            f.write(f"{p.relative_to(dest)}\t{p.stat().st_size}\t{sha256(p)}\n")
    man.with_suffix(".url").write_text(args.link.strip() + "\n", encoding="utf-8")
    by_ext = {}
    for p in files:
        by_ext[p.suffix.lower()] = by_ext.get(p.suffix.lower(), 0) + 1
    print(f"{len(files)} files in {dest}; by type: {dict(sorted(by_ext.items(), key=lambda kv: -kv[1]))}; manifest {man}")


if __name__ == "__main__":
    main()
