"""Measure the key presses in Freesound 641862 (old tape recorder piano key) and compare to the clue.

Finds every press event in the 16.5 s file, measures each one the same way as the clue
(sub-event timing, band energy, spectral peaks, decay), then compares the owner's best window
(7.04 s) with the clue using envelope correlation and spectral distance.
"""
import os
import numpy as np
import soundfile as sf
import librosa
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
REC = os.path.join(ROOT, 'listening/full/641862_Key-Old-Recorder.mp3')
CLUE = os.path.join(ROOT, 'clues/mnc/clue_stacked.wav')
CLUE_OFF = 0.05


def db(x):
    return 20 * np.log10(np.maximum(np.abs(x), 1e-12))


def env(y, sr, ms):
    n = max(1, int(sr * ms / 1000))
    return np.sqrt(signal.convolve(y ** 2, np.ones(n) / n, mode='same'))


def bandpass(y, sr, lo, hi):
    hi = min(hi, sr / 2 - 1)
    sos = signal.butter(4, [lo, hi], btype='band', fs=sr, output='sos')
    return signal.sosfiltfilt(sos, y)


def peaks_spectrum(seg, sr, nfft=16384, nmax=12, fmin=40):
    w = np.hanning(len(seg))
    S = np.abs(np.fft.rfft(seg * w, nfft))
    f = np.fft.rfftfreq(nfft, 1 / sr)
    Sd = db(S / S.max())
    pk, _ = signal.find_peaks(Sd, prominence=6, distance=int(40 / (f[1] - f[0])))
    pk = [p for p in pk if f[p] >= fmin]
    pk = sorted(pk, key=lambda p: -Sd[p])[:nmax]
    return [(round(float(f[p]), 0), round(float(Sd[p]), 1)) for p in sorted(pk)]


BANDS = [(20, 100), (100, 250), (250, 600), (600, 1500), (1500, 3000), (3000, 6000), (6000, 12000), (12000, 20000)]


def band_profile(y, sr, t0, t1):
    seg = y[int(t0 * sr):int(t1 * sr)]
    out = []
    for lo, hi in BANDS:
        b = bandpass(seg, sr, lo, hi)
        out.append(db(np.sqrt(np.mean(b ** 2))))
    out = np.array(out)
    return out - out.max()


def describe_event(y, sr, t0, label, dur=0.45):
    """Print envelope and sub-onsets for an event starting at t0."""
    seg = y[int(t0 * sr):int((t0 + dur) * sr)]
    e = env(seg, sr, 5.0)
    ed = db(e / e.max())
    print(f"\n--- {label}: t0={t0:.3f}s, peak {db(np.max(np.abs(seg))):.1f} dBFS")
    step = int(0.01 * sr)
    print("  5ms-RMS envelope every 10 ms (dB rel peak):")
    vals = [f"{i/sr:.2f}:{ed[i]:5.1f}" for i in range(0, len(seg), step)]
    for k in range(0, len(vals), 9):
        print("   " + "  ".join(vals[k:k + 9]))
    # sub-onsets: 0.5 ms envelope rising > 12 dB within 2 ms
    e2 = env(seg, sr, 0.5)
    e2d = db(e2 / e2.max())
    n2 = int(0.002 * sr)
    rise = e2d[n2:] - e2d[:-n2]
    cand = np.where((rise > 12) & (e2d[n2:] > -32))[0] + n2
    ev, last = [], -1e9
    for c in cand:
        if c - last > sr * 0.006:
            ev.append(c)
        last = c
    print("  sub-onsets (s rel t0, level dB):", [(round(c / sr, 3), round(float(e2d[min(c + n2, len(e2d) - 1)]), 1)) for c in ev])
    # band profile for loudest 60 ms and the following 150 ms
    pk = int(np.argmax(e))
    a = max(0, pk - int(0.01 * sr)) / sr
    print(f"  band profile (dB rel max) loud part [{a:.3f},{a+0.06:.3f}]:", np.round(band_profile(seg, sr, a, a + 0.06), 1).tolist())
    print(f"  band profile tail [{a+0.06:.3f},{a+0.2:.3f}]:", np.round(band_profile(seg, sr, a + 0.06, a + 0.2), 1).tolist())
    print("  spectral peaks loud part:", peaks_spectrum(seg[int(a * sr):int((a + 0.08) * sr)], sr))
    print("  spectral peaks tail:", peaks_spectrum(seg[int((a + 0.08) * sr):int((a + 0.25) * sr)], sr))
    # decay: time for 5ms envelope to fall 20 dB after peak, and 30 dB
    after = ed[pk:]
    t20 = np.argmax(after < -20) / sr if np.any(after < -20) else None
    t30 = np.argmax(after < -30) / sr if np.any(after < -30) else None
    print(f"  broadband decay after peak: -20 dB at {t20}, -30 dB at {t30}")
    return seg


def main():
    y, sr = sf.read(REC, dtype='float64')
    if y.ndim > 1:
        y = y.mean(axis=1)
    print(f"Recorder file: sr={sr} dur={len(y)/sr:.2f}s peak={db(np.max(np.abs(y))):.1f} dBFS")
    # noise floor
    e = env(y, sr, 20.0)
    floor = np.percentile(e, 20)
    print(f"noise floor (20th pct 20ms RMS): {db(floor):.1f} dBFS")
    # events: 20 ms envelope exceeding floor + 20 dB, min gap 300 ms
    thr = floor * 10 ** (20 / 20)
    above = e > thr
    starts = np.where(np.diff(above.astype(int)) == 1)[0]
    events, last = [], -1e9
    for s in starts:
        if s - last > 0.3 * sr:
            events.append(s / sr)
        last = s
    print("Events (s):", [round(t, 2) for t in events])
    for t in events:
        seg = y[int(t * sr):int((t + 0.5) * sr)]
        print(f"  {t:6.2f}s peak {db(np.max(np.abs(seg))):6.1f} dBFS, 20ms env max {db(np.max(env(seg, sr, 20))):6.1f}")

    # Owner's best window
    describe_event(y, sr, 7.04, 'RECORDER owner-best window 7.04', dur=0.63)
    # Also the first couple of events to see variability
    for t in events[:6]:
        describe_event(y, sr, max(0, t - 0.01), f'RECORDER event {t:.2f}', dur=0.5)

    # Clue for identical treatment
    c, csr = sf.read(CLUE, dtype='float64')
    describe_event(c, csr, CLUE_OFF + 0.04, 'CLUE (stacked, from 0.04 s original)', dur=0.42)

    # Envelope correlation between clue and recorder window at various shifts
    cr = librosa.resample(c, orig_sr=csr, target_sr=sr)
    ce = env(cr, sr, 2.0)
    ce = ce[int((CLUE_OFF + 0.03) * sr):int((CLUE_OFF + 0.40) * sr)]
    ce = ce / ce.max()
    best = []
    for t in np.arange(6.5, 8.0, 0.005):
        seg = y[int(t * sr):int(t * sr) + len(ce)]
        if len(seg) < len(ce):
            break
        se = env(seg, sr, 2.0)
        se = se / (se.max() + 1e-12)
        r = np.corrcoef(db(ce + 1e-6), db(se + 1e-6))[0, 1]
        best.append((r, t))
    best.sort(reverse=True)
    print("\nBest log-envelope correlation of clue (0.03-0.40) vs recorder windows:", [(round(r, 3), round(t, 3)) for r, t in best[:5]])

    # Long-term spectra comparison (1/3-octave-ish) for clue event vs recorder best event
    def third_oct(seg, sr):
        S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 32768)) ** 2
        f = np.fft.rfftfreq(32768, 1 / sr)
        centres = 50 * 2 ** (np.arange(0, 27) / 3)
        out = []
        for fc in centres:
            m = (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))
            out.append(10 * np.log10(S[m].sum() + 1e-18))
        out = np.array(out)
        return centres, out - out.max()
    cc, cs = third_oct(cr[int((CLUE_OFF + 0.04) * sr):int((CLUE_OFF + 0.40) * sr)], sr)
    rt = best[0][1]
    rc, rs = third_oct(y[int(rt * sr):int((rt + 0.36) * sr)], sr)
    print("\n1/3-octave spectrum (dB rel max): centre  clue  recorder  diff")
    for fc, a, b in zip(cc, cs, rs):
        if fc < 16000:
            print(f"  {fc:7.0f}  {a:6.1f}  {b:6.1f}  {a-b:6.1f}")


if __name__ == '__main__':
    main()
