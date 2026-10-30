"""Match a Secret Sound against a folder of sound-effect files.

A library recording won't be the same take as the clue, so this compares sound character,
not waveforms. Each library file is cut into its individual events (onsets), each event is
embedded with CLAP's audio encoder, and the clue is compared with every event. A second,
model-free score compares the short-time spectra (log-mel envelope over time). Results are
ranked by the combined score with the best-matching event's time, for A/B listening.

    .venv-sound\\Scripts\\python sfx_match.py clue.wav sfx_folder [--meta meta.json] [--top 30]

clue.crop.json next to the clue is used if present. Embeddings are cached in the folder.
"""
import argparse
import json
from pathlib import Path

import librosa
import numpy as np
import torch
from transformers import ClapModel, ClapProcessor

SR = 48000


def load_clue(path):
    path = Path(path)
    x, _ = librosa.load(path, sr=SR, mono=True)
    crop = path.with_suffix(".crop.json")
    if crop.exists():
        c = json.loads(crop.read_text())
        x = x[int(max(0, c["CLIP_START"]) * SR):int(c["CLIP_END"] * SR)]
    return x


def events(y, length):
    """Windows of `length` samples starting just before each strong onset."""
    if len(y) <= length:
        return [(0.0, np.pad(y, (0, length - len(y))))]
    on = librosa.onset.onset_detect(y=y, sr=SR, units="samples", backtrack=True, delta=0.2)
    out, last = [], -length
    for s in on:
        s = max(0, s - int(0.02 * SR))
        if s - last < length // 2:
            continue
        w = y[s:s + length]
        if len(w) < length or np.sqrt(np.mean(w ** 2)) < 0.005:
            continue
        out.append((s / SR, w))
        last = s
        if len(out) >= 60:
            break
    return out or [(0.0, y[:length])]


def mel_env(w):
    m = librosa.power_to_db(librosa.feature.melspectrogram(y=w, sr=SR, n_fft=2048, hop_length=480, n_mels=48))
    m -= m.max()
    return np.clip(m, -60, 0) / 60.0


class Clap:
    def __init__(self):
        name = "laion/clap-htsat-unfused"
        self.proc, self.model = ClapProcessor.from_pretrained(name), ClapModel.from_pretrained(name)

    def embed(self, clips):
        gap = np.zeros(int(0.3 * SR), np.float32)
        reps = [np.tile(np.concatenate([c, gap]), max(1, int(10 * SR / (len(c) + len(gap))))) for c in clips]
        with torch.no_grad():
            a = self.model.get_audio_features(**self.proc(audio=reps, sampling_rate=SR, return_tensors="pt"))
        a = getattr(a, "pooler_output", a)
        return torch.nn.functional.normalize(a, dim=-1).numpy()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clue")
    ap.add_argument("folder")
    ap.add_argument("--meta", help="json list of {id, desc, ...}; file stem = id")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--out", help="write the ranking as json here")
    args = ap.parse_args()
    clue = load_clue(args.clue)
    n = len(clue)
    clap = Clap()
    ce = clap.embed([clue])[0]
    cm = mel_env(clue)
    meta = {}
    if args.meta:
        meta = {str(m["id"]): m for m in json.load(open(args.meta, encoding="utf-8"))}
    files = sorted(p for p in Path(args.folder).iterdir() if p.suffix.lower() in (".mp3", ".wav", ".ogg", ".flac", ".m4a"))
    rows = []
    for i, f in enumerate(files, 1):
        try:
            y, _ = librosa.load(f, sr=SR, mono=True, duration=90)
        except Exception as e:  # noqa: BLE001 - skip unreadable files
            print(f"skip {f.name}: {e}")
            continue
        ev = events(y, n)
        emb = clap.embed([w for _, w in ev])
        sims = emb @ ce
        mels = [1 - np.mean(np.abs(mel_env(w) - cm)) for _, w in ev]
        combo = 0.7 * sims + 0.3 * np.array(mels)
        k = int(np.argmax(combo))
        rows.append({"id": f.stem, "file": str(f), "at": round(ev[k][0], 3), "score": round(float(combo[k]), 4),
                     "clap": round(float(sims[k]), 4), "mel": round(float(mels[k]), 4),
                     "desc": meta.get(f.stem, {}).get("desc", "")})
        if i % 50 == 0:
            print(f"{i}/{len(files)}", flush=True)
    rows.sort(key=lambda r: -r["score"])
    for r in rows[:args.top]:
        print(f"{r['score']:.3f} clap {r['clap']:.3f} mel {r['mel']:.3f}  {r['id']} @{r['at']:.2f}s  {r['desc'][:80]}")
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
