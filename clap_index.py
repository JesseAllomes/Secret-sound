"""Sound-matching index: embed every clip in a folder once with CLAP, then rank any clue against it.

sfx_match.py re-embeds the whole folder for every clue. This keeps the embeddings in the folder
(.clap_<window ms>.npz), adds only new files on later runs, and queries one or more folders in seconds.
The index is clue-free, so the same folder serves Mid North Coast and Bendigo; the clue and the --tag name
keep their rankings and A/B files apart.

    python clap_index.py build <folder> [<folder> ...] [--win 0.64] [--max-events 24]
    python clap_index.py query <clue> <folder> [<folder> ...] --tag mnc [--top 40] [--csv out.csv] [--ab 10 --out dir]

The window should be about the clue's length (MNC 0.631 s -> 0.64; Bendigo 0.273 s -> 0.28). query uses the
index whose window is nearest the clue's length. Ranking: best CLAP cosine per file, then the top --rerank files
are re-scored 0.7 CLAP + 0.3 log-mel envelope (as sfx_match.py) at their best event.
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from sfx_match import SR, events, load_clue, mel_env

AUDIO = (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aif", ".aiff")


def index_path(folder, win):
    return Path(folder) / f".clap_{int(round(win * 1000))}.npz"


def load_index(folder, win):
    p = index_path(folder, win)
    if not p.exists():
        return {"file": np.array([], str), "at": np.zeros(0), "emb": np.zeros((0, 0), np.float32)}
    z = np.load(p, allow_pickle=False)
    return {"file": z["path"], "at": z["at"], "emb": z["emb"]}


def audio_files(folder):
    return sorted(p for p in Path(folder).rglob("*") if p.suffix.lower() in AUDIO and not p.name.startswith("."))


def strongest(ev, k):
    """Keep the k loudest event windows (onset order kept)."""
    if len(ev) <= k:
        return ev
    keep = sorted(np.argsort([-np.sqrt(np.mean(w ** 2)) for _, w in ev])[:k])
    return [ev[i] for i in keep]


def build(folder, embedder, win=0.64, max_events=24, batch=16, save_every=200, log=print):
    """Embed every audio file in folder not yet in its index. Returns the number of files added."""
    folder = Path(folder)
    idx = load_index(folder, win)
    done = set(idx["file"].tolist())
    todo = [f for f in audio_files(folder) if str(f.relative_to(folder)) not in done]
    n = int(round(win * SR))
    files, ats, embs = list(idx["file"]), list(idx["at"]), [idx["emb"]] if len(idx["emb"]) else []
    pend_f, pend_a, pend_w = [], [], []

    def flush():
        if pend_w:
            embs.append(np.concatenate([embedder.embed(pend_w[i:i + batch]) for i in range(0, len(pend_w), batch)]))
            files.extend(pend_f)
            ats.extend(pend_a)
            pend_f.clear(), pend_a.clear(), pend_w.clear()
        if embs:
            np.savez(index_path(folder, win), path=np.array(files, str), at=np.array(ats, float),
                     emb=np.concatenate(embs).astype(np.float32))

    for i, f in enumerate(todo, 1):
        try:
            y, _ = librosa.load(f, sr=SR, mono=True, duration=90)
        except Exception as e:  # noqa: BLE001 - skip unreadable files
            log(f"skip {f.name}: {e}")
            continue
        for at, w in strongest(events(y, n), max_events):
            pend_f.append(str(f.relative_to(folder)))
            pend_a.append(at)
            pend_w.append(w.astype(np.float32))
        if i % save_every == 0:
            flush()
            log(f"{folder.name}: {i}/{len(todo)} new files embedded")
    flush()
    log(f"{folder.name}: {len(todo)} new, {len(set(files))} files, {len(files)} events in {index_path(folder, win).name}")
    return len(todo)


def nearest_win(folder, length):
    wins = [int(m.group(1)) / 1000 for p in Path(folder).glob(".clap_*.npz") if (m := re.match(r"\.clap_(\d+)\.npz$", p.name))]
    return min(wins, key=lambda w: abs(w - length)) if wins else None


def folder_meta(folder):
    m = Path(folder) / "meta.json"
    if not m.exists():
        return {}
    data = json.loads(m.read_text(encoding="utf-8"))
    return {str(v["id"]): v for v in data} if isinstance(data, list) else data


def query(clue, folders, embedder, rerank=200, log=print):
    """Rank every indexed file in folders against the clue. Returns rows sorted best first."""
    n = len(clue)
    ce = embedder.embed([clue])[0]
    cm = mel_env(clue)
    best = []
    for folder in map(Path, folders):
        win = nearest_win(folder, n / SR)
        if win is None:
            log(f"{folder}: no index, run build first")
            continue
        idx, meta = load_index(folder, win), folder_meta(folder)
        sims = idx["emb"] @ ce
        top = {}
        for k, name in enumerate(idx["file"]):
            if name not in top or sims[k] > sims[top[name]]:
                top[name] = k
        for name, k in top.items():
            m = meta.get(Path(name).stem, {})
            best.append({"folder": str(folder), "file": str(folder / name), "id": Path(name).stem,
                         "at": round(float(idx["at"][k]), 3), "clap": round(float(sims[k]), 4),
                         "query": m.get("query", ""), "name": m.get("name") or m.get("desc", "")})
    best.sort(key=lambda r: -r["clap"])
    for r in best:
        r["mel"], r["score"] = None, r["clap"]
    for r in best[:rerank]:
        y, _ = librosa.load(r["file"], sr=SR, mono=True, offset=r["at"], duration=n / SR + 0.05)
        w = np.pad(y[:n], (0, max(0, n - len(y))))
        r["mel"] = round(float(1 - np.mean(np.abs(mel_env(w) - cm))), 4)
        r["score"] = round(0.7 * r["clap"] + 0.3 * r["mel"], 4)
    best[:rerank] = sorted(best[:rerank], key=lambda r: -r["score"])
    return best


def clue_onset(clue):
    """Where events() would start a window on the clue, so A/B pairs line up the same way."""
    on = librosa.onset.onset_detect(y=clue, sr=SR, units="samples", backtrack=True, delta=0.2)
    return max(0, int(on[0]) - int(0.02 * SR)) if len(on) else 0


def write_ab(rows, n, clue, tag, out_dir):
    """Clue, 0.4 s gap, candidate excerpt of the same length starting at its best event minus the clue's lead-in; x4."""
    ffmpeg = shutil.which("ffmpeg")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lead = clue_onset(clue) / SR
    made = []
    for k, r in enumerate(rows[:n], 1):
        x, _ = librosa.load(r["file"], sr=SR, mono=True, offset=max(0.0, r["at"] - lead), duration=len(clue) / SR)
        cand = np.pad(x, (0, max(0, len(clue) - len(x))))[:len(clue)]
        cand = cand * (np.max(np.abs(clue)) / max(np.max(np.abs(cand)), 1e-9))
        gap = np.zeros(int(0.4 * SR), np.float32)
        audio = np.tile(np.concatenate([clue, gap, cand, gap * 2]), 4)
        label = re.sub(r"[^a-z0-9]+", "-", (r.get("query") or r.get("name") or "candidate").lower()).strip("-")[:30]
        stem = f"AB_{tag}_clap{k}_{label}_{r['id']}"
        with tempfile.TemporaryDirectory() as td:
            wav = Path(td) / "ab.wav"
            sf.write(wav, audio, SR)
            dest = out_dir / f"{stem}.mp3"
            if ffmpeg:
                subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "192k", str(dest)], check=True)
            else:
                dest = out_dir / f"{stem}.wav"
                shutil.copy(wav, dest)
        made.append(dest)
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("folders", nargs="+")
    b.add_argument("--win", type=float, default=0.64)
    b.add_argument("--max-events", type=int, default=24)
    q = sub.add_parser("query")
    q.add_argument("clue")
    q.add_argument("folders", nargs="+")
    q.add_argument("--tag", required=True, choices=["mnc", "bendigo"], help="which competition this clue belongs to")
    q.add_argument("--top", type=int, default=40)
    q.add_argument("--rerank", type=int, default=200)
    q.add_argument("--csv")
    q.add_argument("--ab", type=int, default=0)
    q.add_argument("--out", default="ab_clap")
    args = ap.parse_args()
    from sfx_match import Clap
    clap = Clap()
    if args.cmd == "build":
        for f in args.folders:
            build(f, clap, args.win, args.max_events)
        return
    clue = load_clue(args.clue)
    rows = query(clue, args.folders, clap, args.rerank)
    for r in rows[:args.top]:
        mel = f"{r['mel']:.3f}" if r["mel"] is not None else "  -  "
        print(f"{r['score']:.3f} clap {r['clap']:.3f} mel {mel}  {r['id']} @{r['at']:.2f}s  [{r['query']}] {r['name'][:60]}")
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["score", "clap", "mel", "id", "at", "query", "name", "file", "folder"])
            w.writeheader()
            w.writerows(rows)
    if args.ab:
        for p in write_ab(rows, args.ab, clue, args.tag, args.out):
            print(p)


if __name__ == "__main__":
    main()
