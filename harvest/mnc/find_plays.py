"""Find plays of the Secret Sound clue in a podcast episode by normalised cross-correlation.

    find_plays.py clue.wav episode.mp3 [--thresh 0.6]  -> prints JSON list of {t, ncc}
"""
import json
import subprocess
import sys

import numpy as np
from scipy import signal

SR = 8000


def load(path, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def band(x):
    sos = signal.butter(4, [300, 3800], btype="band", fs=SR, output="sos")
    return signal.sosfiltfilt(sos, x)


def find(clue, ep, thresh):
    c = band(clue[int(0.04 * SR):int(0.40 * SR)])          # the event itself, without the crop's lead-in/tail
    c = (c - c.mean()) / (np.linalg.norm(c) + 1e-12)
    x = band(ep)
    num = signal.fftconvolve(x, c[::-1], mode="valid")
    e = np.convolve(x ** 2, np.ones(len(c)), mode="valid")
    s = np.convolve(x, np.ones(len(c)), mode="valid")
    den = np.sqrt(np.maximum(e - s ** 2 / len(c), 1e-12))
    ncc = num / den
    peaks, _ = signal.find_peaks(ncc, height=thresh, distance=int(0.5 * SR))
    return [{"t": round(p / SR - 0.04, 2), "ncc": round(float(ncc[p]), 3)} for p in peaks]


if __name__ == "__main__":
    thresh = float(sys.argv[sys.argv.index("--thresh") + 1]) if "--thresh" in sys.argv else 0.6
    print(json.dumps(find(load(sys.argv[1]), load(sys.argv[2]), thresh)))
