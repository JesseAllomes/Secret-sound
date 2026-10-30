"""Bendigo only: list the Cogho & Jules podcast feed, and transcribe episodes looking for the Secret Sound segment.

    python transcribe_eps.py feed --out eps.json                 (all pages of the feed)
    python transcribe_eps.py run eps.json <first> <last> --out <dir>

`run` downloads each episode, transcribes it in full (faster-whisper small.en) and writes <dir>/transcripts/<n>_<date>.txt
plus <dir>/hits_<n>.json with every line that mentions the competition (secret sound, jackpot, sponsor, clue words).
"""
import argparse
import json
import re
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED = ("https://www.omnycontent.com/d/playlist/566281f8-200e-4c9f-8378-a4870055423b/48bd6f7b-42bf-4d0f-88b9-a5fb00d4e352/"
        "266b4537-88c7-496b-9177-a5fb00d53e0c/podcast.rss")
ATOM = "{http://www.w3.org/2005/Atom}"
HIT = re.compile(r"(?i)secret sound|jackpot|firewood|bendigo firewood|incorrect guess|wrong guess|i'?m a classic|"
                 r"need a hand|old school|the sound|what is that sound|clue")


def feed(out):
    url, eps = FEED, []
    while url:
        with urllib.request.urlopen(url, timeout=60) as r:
            root = ET.fromstring(r.read())
        ch = root.find("channel")
        for it in ch.findall("item"):
            enc = it.find("enclosure")
            if enc is not None:
                eps.append({"title": it.findtext("title"), "date": it.findtext("pubDate"), "url": enc.get("url")})
        nxt = [l.get("href") for l in ch.findall(f"{ATOM}link") if l.get("rel") == "next"]
        url = nxt[0] if nxt else None
    Path(out).write_text(json.dumps(eps, indent=0))
    print(len(eps), "episodes", eps[-1]["date"] if eps else "")


def load16(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    import numpy as np
    return np.frombuffer(raw, np.int16).astype("float32") / 32768


def run(eps_path, first, last, out):
    from faster_whisper import WhisperModel
    eps = json.loads(Path(eps_path).read_text())
    out = Path(out)
    (out / "transcripts").mkdir(parents=True, exist_ok=True)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    for n in range(first, min(last, len(eps) - 1) + 1):
        e = eps[n]
        with tempfile.TemporaryDirectory() as td:
            mp3 = Path(td) / "ep.mp3"
            subprocess.run(["curl", "-sS", "-L", "--retry", "4", "-o", str(mp3), e["url"]], check=True)
            segs, _ = model.transcribe(load16(mp3), beam_size=1, vad_filter=True)
            lines = [f"[{s.start:7.1f}] {s.text.strip()}" for s in segs]
        tag = f"{n:03d}_{(e['date'] or '')[5:16].replace(' ', '-')}"
        (out / "transcripts" / f"{tag}.txt").write_text(f"{e['title']}\n{e['date']}\n\n" + "\n".join(lines) + "\n")
        hits = [ln for ln in lines if HIT.search(ln)]
        (out / f"hits_{n:03d}.json").write_text(json.dumps({"n": n, "title": e["title"], "date": e["date"], "hits": hits}))
        print(f"{tag} {len(lines)} lines, {len(hits)} hits  {e['title'][:60]}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("feed")
    f.add_argument("--out", default="eps.json")
    r = sub.add_parser("run")
    r.add_argument("eps")
    r.add_argument("first", type=int)
    r.add_argument("last", type=int)
    r.add_argument("--out", required=True)
    a = ap.parse_args()
    feed(a.out) if a.cmd == "feed" else run(a.eps, a.first, a.last, a.out)


if __name__ == "__main__":
    main()
