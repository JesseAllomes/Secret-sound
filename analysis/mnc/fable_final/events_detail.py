"""Fine structure of the two clue events: sub-onsets at 0.25 ms resolution, per-event spectra,
spectral similarity between event A (0.11 s) and event B (0.25 s), LF thump timing and hum check.
Works on the stacked clue (median of 415 broadcasts); times printed on the ORIGINAL clip timeline.
"""
import os
import numpy as np
import soundfile as sf
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STACK = os.path.join(ROOT, 'clues/mnc/clue_stacked.wav')
OFF = 0.05


def db(x):
    return 20 * np.log10(np.maximum(np.abs(x), 1e-12))


def env(y, sr, ms):
    n = max(1, int(sr * ms / 1000))
    return np.sqrt(signal.convolve(y ** 2, np.ones(n) / n, mode='same'))


def bp(y, sr, lo, hi):
    hi = min(hi, sr / 2 - 1)
    sos = signal.butter(4, [lo, hi], btype='band', fs=sr, output='sos')
    return signal.sosfiltfilt(sos, y)


y, sr = sf.read(STACK, dtype='float64')
t = np.arange(len(y)) / sr - OFF

# 1. Fine envelope (0.25 ms) around each event, print 1 ms steps
e = env(y, sr, 0.25)
ed = db(e / e.max())
for name, a, b in [('A', 0.055, 0.135), ('B', 0.240, 0.320)]:
    print(f"\nEvent {name}: 0.25 ms RMS envelope, 1 ms steps, dB rel global peak")
    rows = []
    for tt in np.arange(a, b, 0.001):
        i = int((tt + OFF) * sr)
        rows.append(f"{tt:.3f}:{ed[i]:5.1f}")
    for k in range(0, len(rows), 10):
        print("   " + "  ".join(rows[k:k + 10]))

# 2. Attack time (10%-90% of peak amplitude in the 2 ms envelope) for the main bursts
e2 = env(y, sr, 2.0)
for name, a, b in [('A-click 0.06', 0.055, 0.075), ('A-main 0.11', 0.100, 0.140), ('B 0.25', 0.240, 0.275)]:
    seg = e2[int((a + OFF) * sr):int((b + OFF) * sr)]
    pk = np.max(seg)
    i10 = np.argmax(seg > 0.1 * pk)
    i90 = np.argmax(seg > 0.9 * pk)
    ipk = np.argmax(seg)
    print(f"{name}: peak {db(pk/e2.max()):5.1f} dB at {a + ipk/sr:.4f} s, 10-90% rise {(i90-i10)/sr*1000:.2f} ms")

# 3. Spectral similarity A vs B (first 25 ms of each main burst)
def spec(a, dur=0.025, nfft=8192):
    seg = y[int((a + OFF) * sr):int((a + dur + OFF) * sr)]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), nfft))
    f = np.fft.rfftfreq(nfft, 1 / sr)
    return f, S


f, SA = spec(0.108)
f, SB = spec(0.248)
m = (f > 100) & (f < 12000)
la, lb = np.log(SA[m] + 1e-9), np.log(SB[m] + 1e-9)
print(f"\nLog-spectrum correlation A(0.108-0.133) vs B(0.248-0.273): {np.corrcoef(la, lb)[0,1]:.3f}")
# octave-band comparison
print("Octave band levels (dB rel each event's max):  band   A      B")
for lo in [62, 125, 250, 500, 1000, 2000, 4000, 8000]:
    mm = (f >= lo) & (f < 2 * lo)
    pa = 10 * np.log10((SA[mm] ** 2).sum())
    pb = 10 * np.log10((SB[mm] ** 2).sum())
    print(f"  {lo:5d}-{2*lo:5d} Hz  {pa - 10*np.log10((SA[m]**2).max()*len(SA[m])):6.1f}  {pb - 10*np.log10((SB[m]**2).max()*len(SB[m])):6.1f}")
# normalise properly
ma = (f >= 62) & (f < 16000)
tot_a = 10 * np.log10((SA[ma] ** 2).sum())
tot_b = 10 * np.log10((SB[ma] ** 2).sum())
print("Octave band share of energy (dB rel event total):  band   A      B")
for lo in [62, 125, 250, 500, 1000, 2000, 4000, 8000]:
    mm = (f >= lo) & (f < 2 * lo)
    pa = 10 * np.log10((SA[mm] ** 2).sum()) - tot_a
    pb = 10 * np.log10((SB[mm] ** 2).sum()) - tot_b
    print(f"  {lo:5d}-{2*lo:5d} Hz  {pa:6.1f}  {pb:6.1f}")

# 4. LF thump timing: 40-110 Hz band envelope peaks, and 100-250 band
for lo, hi in [(40, 110), (110, 250), (350, 500), (700, 870), (1000, 1300), (1500, 2200)]:
    b = bp(y, sr, lo, hi)
    eb = env(b, sr, 3.0)
    ebd = db(eb / e2.max())
    pk, _ = signal.find_peaks(ebd, prominence=6, distance=int(0.01 * sr))
    pk = [p for p in pk if 0.04 < t[p] < 0.42 and ebd[p] > -45]
    print(f"band {lo}-{hi} Hz peaks (t, dB rel global 2ms peak):", [(round(t[p], 3), round(float(ebd[p]), 1)) for p in pk][:8])

# 5. Hum / tonal components in the quiet head (original -0.05..0.05) and tail (0.42..0.60)
for name, a, b in [('head', -0.05, 0.05), ('tail', 0.42, 0.62)]:
    seg = y[int((a + OFF) * sr):int((b + OFF) * sr)]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 65536))
    ff = np.fft.rfftfreq(65536, 1 / sr)
    Sd = db(S / S.max())
    pk, _ = signal.find_peaks(Sd, prominence=10)
    pk = sorted(pk, key=lambda p: -Sd[p])[:10]
    print(f"{name} quiet region tonal peaks:", [(round(float(ff[p]), 1), round(float(Sd[p]), 1)) for p in sorted(pk)], f"rms {db(np.sqrt(np.mean(seg**2))):.1f} dBFS")

# 6. Ring at ~790 Hz after B: fit exponential decay, estimate Q
b = bp(y, sr, 740, 840)
eb = env(b, sr, 1.5)
i0 = int((0.26 + OFF) * sr); i1 = int((0.34 + OFF) * sr)
seg = db(eb[i0:i1])
tt = np.arange(len(seg)) / sr
p = np.polyfit(tt, seg, 1)
T60 = -60 / p[0]
print(f"\n790 Hz ring after B: slope {p[0]:.0f} dB/s, T60 {T60*1000:.0f} ms, Q ~ {np.pi*790*T60/6.91:.0f}")
# does 790 Hz exist before B?
eb_d = db(eb / eb.max())
print("790 Hz band level at t=0.12,0.15,0.20,0.24,0.26,0.28,0.30,0.33:", [round(float(eb_d[int((x+OFF)*sr)]),1) for x in [0.12,0.15,0.20,0.24,0.26,0.28,0.30,0.33]])
b4 = bp(y, sr, 400, 470)
eb4 = db(env(b4, sr, 1.5) / e2.max())
print("435 Hz band level at same times:", [round(float(eb4[int((x+OFF)*sr)]),1) for x in [0.12,0.15,0.20,0.24,0.26,0.28,0.30,0.33]])

# 7. Zero-crossing / instantaneous frequency of the LF thump after B (0.27-0.33)
b = bp(y, sr, 40, 150)
seg = b[int((0.27 + OFF) * sr):int((0.34 + OFF) * sr)]
zc = np.where(np.diff(np.sign(seg)) != 0)[0]
if len(zc) > 2:
    per = np.diff(zc) / sr * 2
    print("LF thump after B: mean period-based freq", round(float(1 / np.mean(per)), 1), "Hz; cycle freqs:", [round(float(1/pp),0) for pp in per[:10]])
b = bp(y, sr, 80, 300)
seg = b[int((0.135 + OFF) * sr):int((0.19 + OFF) * sr)]
zc = np.where(np.diff(np.sign(seg)) != 0)[0]
if len(zc) > 2:
    per = np.diff(zc) / sr * 2
    print("LF after A (0.135-0.19): mean freq", round(float(1 / np.mean(per)), 1), "Hz; cycle freqs:", [round(float(1/pp),0) for pp in per[:10]])
