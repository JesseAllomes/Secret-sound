"""Suggest what a Secret Sound might be. Two models, both run on the CPU:

- AST (AudioSet): tags the sound against 527 general categories.
- CLAP: ranks a list of specific candidates ("stapler being pressed", ...) by how well each
  description matches the sound. Edit candidates.txt to add ideas, wrong guesses are marked.

    .venv-sound\\Scripts\\python sound_id.py clue.wav [--wrong wrong.txt] [--candidates candidates.txt]

clue.crop.json next to the clue (from crop.py) is used if present. First run downloads the
models (about 1 GB) into the Hugging Face cache.
"""
import argparse
import json
from pathlib import Path

import librosa
import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification, ClapModel, ClapProcessor

HERE = Path(__file__).resolve().parent


def load(path):
    path = Path(path)
    crop = path.with_suffix(".crop.json")
    x, _ = librosa.load(path, sr=48000, mono=True)
    if crop.exists():
        c = json.loads(crop.read_text())
        x = x[int(max(0, c["CLIP_START"]) * 48000):int(c["CLIP_END"] * 48000)]
    return x


def ast_tags(x, top):
    name = "MIT/ast-finetuned-audioset-10-10-0.4593"
    fe, model = ASTFeatureExtractor.from_pretrained(name), ASTForAudioClassification.from_pretrained(name)
    y = librosa.resample(x, orig_sr=48000, target_sr=16000)
    with torch.no_grad():
        p = torch.sigmoid(model(**fe(y, sampling_rate=16000, return_tensors="pt")).logits)[0]
    idx = p.argsort(descending=True)[:top]
    return [(model.config.id2label[int(i)], float(p[i])) for i in idx]


def clap_rank(x, labels):
    name = "laion/clap-htsat-unfused"
    proc, model = ClapProcessor.from_pretrained(name), ClapModel.from_pretrained(name)
    # A sub-second sound is padded to CLAP's 10 s window; repeating it keeps it from being mostly silence.
    gap = np.zeros(int(0.3 * 48000), np.float32)
    rep = np.tile(np.concatenate([x, gap]), max(1, int(10 * 48000 / (len(x) + len(gap)))))
    with torch.no_grad():
        a = model.get_audio_features(**proc(audio=[rep], sampling_rate=48000, return_tensors="pt"))
        t = model.get_text_features(**proc(text=[f"the sound of {l}" for l in labels],
                                          return_tensors="pt", padding=True))
    # transformers 5 wraps the projected embeddings in an output object
    a, t = (getattr(v, "pooler_output", v) for v in (a, t))
    a, t = torch.nn.functional.normalize(a, dim=-1), torch.nn.functional.normalize(t, dim=-1)
    s = (t @ a.T).squeeze(1)
    return sorted(zip(labels, s.tolist()), key=lambda z: -z[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clue")
    ap.add_argument("--candidates", default=str(HERE / "candidates.txt"))
    ap.add_argument("--wrong", help="file of guesses already ruled out (one per line)")
    ap.add_argument("--top", type=int, default=40)
    args = ap.parse_args()
    x = load(args.clue)
    print(f"{len(x) / 48000:.3f} s of audio\n\nAudioSet tags:")
    for name, p in ast_tags(x, 15):
        print(f"  {p:.3f}  {name}")
    labels = [ln.strip() for ln in open(args.candidates, encoding="utf-8")
              if ln.strip() and not ln.startswith("#")]
    wrong = set()
    if args.wrong:
        wrong = {ln.strip().lower() for ln in open(args.wrong, encoding="utf-8") if ln.strip()}
    print(f"\nCLAP ranking of {len(labels)} candidates (x = already guessed wrong):")
    for i, (label, s) in enumerate(clap_rank(x, labels)[:args.top], 1):
        print(f"  {i:3d}  {s:.3f}  {'x ' if label.lower() in wrong else '  '}{label}")


if __name__ == "__main__":
    main()
