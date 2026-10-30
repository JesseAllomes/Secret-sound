"""Measure the MNC Secret Sound clue: events, timing, spectra, resonances, decay, LF content.

Outputs text to stdout and PNG figures next to this script. No model tokens, no downloads.
"""
import sys, os
import numpy as np
import soundfile as sf
import librosa
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CLUE = os.path.join(ROOT, 'clues/mnc/clue.wav')
STACK = os.path.join(ROOT, 'clues/mnc/clue_stacked.wav')


def load(path):
    y, sr = sf.read(path, dtype='float64')
    if y.ndim > 1:
        y = y.mean(axis=1)
    return y, sr


def db(x):
    return 20 * np.log10(np.maximum(np.abs(x), 1e-12))


def envelope_ms(y, sr, win_ms=1.0):
    n = max(1, int(sr * win_ms / 1000))
    e = np.sqrt(signal.convolve(y ** 2, np.ones(n) / n, mode='same'))
    return e


def onsets(y, sr, thresh_db=-35, min_gap_ms=4):
    e = envelope_ms(y, sr, 0.5)
    ed = db(e / (np.max(e) + 1e-12))
    # onset = where envelope rises by >12 dB within 2 ms
    n2 = int(sr * 0.002)
    rise = ed[n2:] - ed[:-n2]
    cand = np.where((rise > 12) & (ed[n2:] > thresh_db))[0] + n2
    ev = []
    last = -1e9
    for c in cand:
        if c - last > sr * min_gap_ms / 1000:
            ev.append(c)
        last = c
    return ev, ed


def band_energy(y, sr, lo, hi):
    sos = signal.butter(4, [lo, hi], btype='band', fs=sr, output='sos')
    return signal.sosfiltfilt(sos, y)


def peaks_spectrum(seg, sr, nfft=8192, nmax=12, fmin=60):
    w = np.hanning(len(seg))
    S = np.abs(np.fft.rfft(seg * w, nfft))
    f = np.fft.rfftfreq(nfft, 1 / sr)
    Sd = db(S / S.max())
    pk, props = signal.find_peaks(Sd, prominence=6, distance=int(40 / (f[1] - f[0])))
    pk = [p for p in pk if f[p] >= fmin]
    pk = sorted(pk, key=lambda p: -Sd[p])[:nmax]
    return [(round(float(f[p]), 1), round(float(Sd[p]), 1)) for p in sorted(pk)]


def decay_time(y, sr, f0, bw=60, t0=0.0):
    """T60-style decay of a narrow band around f0 after t0 (fit on 25 dB range)."""
    lo, hi = max(20, f0 - bw / 2), f0 + bw / 2
    b = band_energy(y, sr, lo, hi)
    e = envelope_ms(b, sr, 2.0)
    ed = db(e + 1e-12)
    i0 = int(t0 * sr)
    seg = ed[i0:]
    pk = int(np.argmax(seg)) + i0
    top = ed[pk]
    # find where it falls 25 dB
    below = np.where(ed[pk:] < top - 25)[0]
    if len(below) == 0:
        return None, pk / sr
    i1 = pk + below[0]
    t = np.arange(pk, i1) / sr
    p = np.polyfit(t, ed[pk:i1], 1)
    slope = p[0]  # dB/s
    if slope >= 0:
        return None, pk / sr
    return -60 / slope, pk / sr


def analyse(path, label, offset=0.0):
    y, sr = load(path)
    print(f"\n===== {label}: {path}  sr={sr} dur={len(y)/sr:.3f}s peak={np.max(np.abs(y)):.3f} ({db(np.max(np.abs(y))):.1f} dBFS)")
    ev, ed = onsets(y, sr)
    print("Onset candidates (s, in-file / original-timeline):")
    for e in ev:
        print(f"  {e/sr:7.4f}  /  {e/sr-offset:7.4f}   level {ed[e+int(0.002*sr)]:.1f} dB")

    # Fine envelope print in 5 ms steps across active region
    print("Envelope (5 ms RMS, dB rel peak):")
    e5 = envelope_ms(y, sr, 5.0)
    e5d = db(e5 / e5.max())
    step = int(0.005 * sr)
    line = []
    for i in range(0, len(y), step):
        t = i / sr - offset
        if -0.02 < t < 0.45:
            line.append(f"{t:.3f}:{e5d[i]:5.1f}")
    for k in range(0, len(line), 8):
        print("   " + "  ".join(line[k:k + 8]))

    # Band energies over time (10 ms)
    bands = [(20, 100), (100, 250), (250, 600), (600, 1500), (1500, 3000), (3000, 6000), (6000, 12000), (12000, 20000)]
    print("Band RMS (dB rel overall peak band) per 10 ms, columns:", bands)
    bes = []
    for lo, hi in bands:
        hi = min(hi, sr / 2 - 1)
        bes.append(envelope_ms(band_energy(y, sr, lo, hi), sr, 10.0))
    bes = np.array(bes)
    ref = bes.max()
    step = int(0.010 * sr)
    for i in range(0, len(y), step):
        t = i / sr - offset
        if -0.02 < t < 0.42:
            print(f"  t={t:6.3f} " + " ".join(f"{db(bes[b, i]/ref):6.1f}" for b in range(len(bands))))

    # Spectra of each event window
    print("Spectral peaks (Hz, dB rel max) for windows:")
    windows = [(-0.0, 0.05), (0.05, 0.10), (0.10, 0.15), (0.15, 0.20), (0.20, 0.25), (0.25, 0.30), (0.30, 0.36), (0.36, 0.45)]
    for a, b in windows:
        i0, i1 = int((a + offset) * sr), int((b + offset) * sr)
        if i1 > len(y):
            continue
        seg = y[i0:i1]
        pk = peaks_spectrum(seg, sr)
        print(f"  [{a:.2f},{b:.2f}) rms={db(np.sqrt(np.mean(seg**2))):6.1f} dBFS  peaks: {pk}")

    # Whole-event spectrum with long FFT
    i0, i1 = int((0.04 + offset) * sr), int((0.40 + offset) * sr)
    seg = y[i0:i1]
    print("Whole-event spectral peaks (0.04-0.40 s):", peaks_spectrum(seg, sr, nfft=32768, nmax=20))

    # Spectral centroid per 10 ms
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=int(0.005 * sr)))
    cent = librosa.feature.spectral_centroid(S=S, sr=sr)[0]
    roll = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.85)[0]
    times = librosa.frames_to_time(np.arange(len(cent)), sr=sr, hop_length=int(0.005 * sr)) - offset
    print("Spectral centroid / 85% rolloff per 10 ms (Hz):")
    for t, c, r in zip(times[::2], cent[::2], roll[::2]):
        if -0.01 < t < 0.42:
            print(f"  t={t:6.3f} centroid={c:7.0f} rolloff={r:7.0f}")

    # Decay of main spectral peaks after major event
    print("Narrow-band decay (T60 extrapolated from first 25 dB) for candidate resonances:")
    for f0 in [120, 180, 260, 330, 440, 560, 700, 900, 1200, 1600, 2100, 2700, 3400, 4500, 6000]:
        for t0 in [0.09, 0.24]:
            T60, tpk = decay_time(y, sr, f0, bw=max(40, f0 * 0.12), t0=t0 + offset)
            if T60:
                print(f"  f0={f0:5d} Hz after t0={t0:.2f}: T60~{T60*1000:6.0f} ms (peak at {tpk-offset:.3f})")
    return y, sr


if __name__ == '__main__':
    y1, sr1 = analyse(CLUE, 'ORIGINAL', offset=0.0)
    y2, sr2 = analyse(STACK, 'STACKED(median of 415)', offset=0.05)

    # cross-check alignment of stacked vs original
    n = min(len(y1), len(y2) - int(0.05 * sr2))
    c = np.corrcoef(y1[:n], y2[int(0.05 * sr2):int(0.05 * sr2) + n])[0, 1]
    print(f"\nCorrelation original vs stacked (shift 0.05 s): {c:.3f}")

    # figures
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    t = np.arange(len(y2)) / sr2 - 0.05
    axes[0].plot(t, y2, lw=0.5)
    axes[0].set_xlim(-0.02, 0.45)
    axes[0].set_title('Stacked clue waveform (original timeline)')
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y2, n_fft=1024, hop_length=48)), ref=np.max)
    librosa.display.specshow(D, sr=sr2, hop_length=48, x_axis='time', y_axis='log', ax=axes[1], cmap='magma')
    axes[1].set_ylim(50, 20000)
    axes[1].set_xlim(0.03, 0.50)
    axes[1].set_title('Spectrogram (log f)')
    D2 = librosa.amplitude_to_db(np.abs(librosa.stft(y2, n_fft=256, hop_length=16)), ref=np.max)
    librosa.display.specshow(D2, sr=sr2, hop_length=16, x_axis='time', y_axis='linear', ax=axes[2], cmap='magma')
    axes[2].set_xlim(0.03, 0.50)
    axes[2].set_title('Spectrogram (high time resolution, linear f)')
    plt.tight_layout()
    plt.savefig(os.path.join(HERE, 'clue_stacked_analysis.png'), dpi=110)
    print("saved", os.path.join(HERE, 'clue_stacked_analysis.png'))
