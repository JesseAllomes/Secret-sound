"""Resonance measures after each stroke: how much ringing follows a click relative to the click."""
import sys
sys.path.insert(0, '/home/user/secret-sound')
import numpy as np, librosa, steel_score as ss
from scipy import signal
SR = ss.SR
BANDS = {"low": (150, 400), "mid": (400, 2500), "hi": (2500, 8000)}


def bp(y, lo, hi):
    sos = signal.butter(4, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfiltfilt(sos, y)


def rms_db(x):
    return float(ss.db(np.sqrt(np.mean(x ** 2)) if len(x) else 1e-9))


def stroke_measures(y, t, t_end):
    """t = stroke time, t_end = where the next stroke begins (or end of file)."""
    out = {}
    a = int(t * SR)
    for name, (lo, hi) in BANDS.items():
        x = bp(y, lo, hi)
        att = rms_db(x[a:a + int(0.015 * SR)])                        # the click itself, 0-15 ms
        s1 = rms_db(x[a + int(0.040 * SR):a + int(0.090 * SR)])       # 40-90 ms after
        s2 = rms_db(x[a + int(0.090 * SR):min(a + int(0.140 * SR), int(t_end * SR))])  # 90-140 ms after
        out[f"att_{name}"] = round(att, 1)
        out[f"sus1_{name}"] = round(s1 - att, 1)
        out[f"sus2_{name}"] = round(s2 - att, 1)
    # sharpness: energy share above 3 kHz and centroid in the first 20 ms
    seg = y[a:a + int(0.020 * SR)]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 4096)) ** 2
    f = np.fft.rfftfreq(4096, 1 / SR)
    out["hf_share"] = round(float(spec[f > 3000].sum() / spec[(f > 100)].sum()), 2)
    out["centroid"] = round(float(np.sum(f * spec) / spec.sum()))
    # tail tonality 30-130 ms after (cut at t_end): peak-to-median in 300-3000 Hz, autocorr peak
    b0, b1 = a + int(0.030 * SR), min(a + int(0.130 * SR), int(t_end * SR))
    tail = y[b0:b1]
    if len(tail) > int(0.04 * SR):
        tail = bp(tail, 200, 4000)
        sp = np.abs(np.fft.rfft(tail * np.hanning(len(tail)), 1 << 16))
        ff = np.fft.rfftfreq(1 << 16, 1 / SR)
        band = (ff >= 300) & (ff <= 3000)
        out["tail_peak_db"] = round(float(ss.db(sp[band].max()) - ss.db(np.median(sp[band]))), 1)
        out["tail_peak_hz"] = round(float(ff[band][np.argmax(sp[band])]))
        ac = signal.correlate(tail, tail, mode="full")[len(tail) - 1:]
        ac /= ac[0] + 1e-12
        lo, hi = int(SR / 3000), int(SR / 300)
        out["tail_ac"] = round(float(ac[lo:hi].max()), 2)
        # tail level relative to attack (broadband)
        out["tail_rel"] = round(rms_db(y[b0:b1]) - rms_db(y[a:a + int(0.015 * SR)]), 1)
    else:
        out.update(tail_peak_db=0.0, tail_peak_hz=0, tail_ac=0.0, tail_rel=-60.0)
    return out


def measure(y, tb, tc, t_end=None):
    t_end = t_end if t_end is not None else len(y) / SR
    return {"B": stroke_measures(y, tb, tc), "C": stroke_measures(y, tc, t_end)}


if __name__ == "__main__":
    for f in sys.argv[1:]:
        y, _ = librosa.load(f, sr=SR, mono=True)
        r = ss.score_signal(y)
        if not r:
            print(f, "no pair"); continue
        tb = r["t_b"]; tc = tb + r["gap_ms"] / 1000
        m = measure(y, tb, tc)
        print(f, f"tb={tb:.3f} gap={r['gap_ms']}")
        for k in ("B", "C"):
            print("  ", k, m[k])
