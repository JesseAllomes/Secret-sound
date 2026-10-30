"""Resonant modes: frequency, decay time (T60 / damping), and timing of the low 62 Hz and 791 Hz
components, plus a few others. Uses narrow-band filtering + envelope slope, and a complex-exponential
(matrix pencil / Prony-like) fit on short tail windows. Orig time throughout."""
import numpy as np, soundfile as sf, scipy.signal as ss, scipy.optimize as so, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
orig, _ = sf.read(f'{ROOT}/clues/mnc/clue.wav')
t = np.arange(len(stk))/sr - OFF
to = np.arange(len(orig))/sr

def bp(x, f0, bw, order=4):
    sos = ss.butter(order, [f0-bw/2, f0+bw/2], btype='band', fs=sr, output='sos')
    return ss.sosfiltfilt(sos, x)

def env(x, win_ms):
    n = int(sr*win_ms/1000); return 20*np.log10(np.sqrt(np.convolve(x**2, np.ones(n)/n, 'same'))+1e-9)

def decay_fit(e, tt, t0, t1):
    m = (tt>=t0)&(tt<=t1); p = np.polyfit(tt[m], e[m], 1)
    return p[0], -60/p[0]  # dB/s, T60

def inst_freq(x, tt, t0, t1):
    """mean instantaneous frequency of analytic signal in window"""
    m = (tt>=t0)&(tt<=t1); a = ss.hilbert(x); ph = np.unwrap(np.angle(a[m]))
    f = np.diff(ph)*sr/(2*np.pi); return np.median(f), np.percentile(f,[25,75])

print("=== Narrow-band envelope decay (stacked), orig time ===")
rows = [
  # f0, bw, windows (fit start, fit end) for after-B and after-C
  (62, 40, [(0.155,0.215),(0.29,0.35)]),
  (164, 30, [(0.14,0.20),(0.27,0.33)]),
  (220, 40, [(0.14,0.20),(0.27,0.33)]),
  (330, 30, [(0.13,0.19),(0.26,0.32)]),
  (472, 30, [(0.13,0.19),(0.27,0.35)]),
  (791, 30, [(0.13,0.20),(0.265,0.37)]),
  (1125, 40, [(0.13,0.19),(0.265,0.34)]),
  (1300, 40, [(0.13,0.19),(0.265,0.34)]),
  (1700, 40, [(0.13,0.19),(0.265,0.33)]),
  (1850, 40, [(0.13,0.19),(0.265,0.33)]),
  (2033, 40, [(0.13,0.19),(0.265,0.33)]),
  (2570, 40, [(0.13,0.19),(0.265,0.33)]),
  (3190, 40, [(0.13,0.19),(0.265,0.33)]),
]
fig, ax = plt.subplots(len(rows), 1, figsize=(13, 2.0*len(rows)), sharex=True)
for a,(f0,bw,wins) in zip(ax, rows):
    y = bp(stk, f0, bw); e = env(y, 2.0)
    a.plot(t, e, lw=0.7); a.set_ylabel(f'{f0} Hz'); a.set_xlim(-0.02,0.42); a.set_ylim(e.max()-70, e.max()+2)
    s = []
    for (t0,t1) in wins:
        sl, T60 = decay_fit(e, t, t0, t1)
        fm, (q1,q3) = inst_freq(y, t, t0, t1)
        pk = t[(t>=t0-0.03)&(t<=t1)][np.argmax(e[(t>=t0-0.03)&(t<=t1)])]
        lvl = e[(t>=t0-0.03)&(t<=t1)].max()
        s.append(f"win {t0:.3f}-{t1:.3f}: peak {lvl:5.1f}dB at {pk:.3f}s, slope {sl:7.0f} dB/s, T60 {T60*1000:5.0f} ms, f_inst {fm:7.1f} Hz (IQR {q1:.0f}-{q3:.0f})")
        a.axvspan(t0,t1,color='g',alpha=0.1)
    print(f"{f0:5d} Hz (bw {bw}): " + ' | '.join(s))
ax[-1].set_xlabel('orig time (s)'); plt.tight_layout(); plt.savefig(f'{OUT}/mode_envelopes.png', dpi=100)

# Low-frequency waveform: lowpass 200 Hz, plot and zero crossings -> period
lp = ss.sosfiltfilt(ss.butter(4, 200, 'low', fs=sr, output='sos'), stk)
lpo = ss.sosfiltfilt(ss.butter(4, 200, 'low', fs=sr, output='sos'), orig)
fig, ax = plt.subplots(2,1, figsize=(13,6), sharex=True)
ax[0].plot(t, lp, lw=0.8); ax[0].set_ylabel('stacked LP200'); ax[0].set_xlim(0.05,0.40); ax[0].grid(alpha=.3)
ax[1].plot(to, lpo, lw=0.8); ax[1].set_ylabel('orig LP200'); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.savefig(f'{OUT}/lowpass200.png', dpi=100)
zc = np.where(np.diff(np.sign(lp))>0)[0]; zt = t[zc]
zt = zt[(zt>0.10)&(zt<0.40)]
print("\nLP200 positive-going zero crossings (orig time) and implied period/frequency:")
for a_, b_ in zip(zt[:-1], zt[1:]):
    print(f"  {a_:.4f} -> {b_:.4f}  period {1000*(b_-a_):5.1f} ms  f={1/(b_-a_):6.1f} Hz")

# Peak-amplitude of LP200 half-cycles -> decay of the LF oscillation after each hit
print("\nLP200 extrema (orig time, amplitude):")
ex, _ = ss.find_peaks(np.abs(lp), distance=int(sr*0.004), height=0.01)
for i in ex:
    if 0.10 < t[i] < 0.40: print(f"  {t[i]:.4f}s  {lp[i]:+.3f}")

# Matrix-pencil (ESPRIT-like) modal fit on tails to get damped sinusoid params
def matrix_pencil(x, fs, M=24, decim=1):
    x = x[::decim]; fs = fs/decim
    N = len(x); L = N//2
    H = np.array([x[i:i+L] for i in range(N-L)])
    U,s,Vh = np.linalg.svd(H, full_matrices=False)
    V = Vh.conj().T[:, :M]
    V1, V2 = V[:-1], V[1:]
    z = np.linalg.eigvals(np.linalg.pinv(V1) @ V2)
    f = np.angle(z)*fs/(2*np.pi); d = -np.log(np.abs(z))*fs  # damping (1/s)
    # amplitudes by LS
    n = np.arange(N); Z = z[None,:]**n[:,None]; a = np.linalg.lstsq(Z, x, rcond=None)[0]
    return f, d, np.abs(a)

print("\n=== matrix-pencil modal fits (stacked, decimated to 6 kHz, 0-3 kHz) ===")
dec = 8
lp3 = ss.sosfiltfilt(ss.butter(6, 2900, 'low', fs=sr, output='sos'), stk)
for label, t0, t1 in [('after B 0.135-0.245', 0.135, 0.245), ('after C 0.270-0.380', 0.270, 0.380), ('after A 0.068-0.108', 0.068, 0.108)]:
    seg = lp3[int((t0+OFF)*sr):int((t1+OFF)*sr)]
    f, d, a = matrix_pencil(seg, sr, M=30, decim=dec)
    keep = (f>15)&(d>0)&(d<400)
    idx = np.argsort(-a[keep]); f, d, a = f[keep][idx], d[keep][idx], a[keep][idx]
    print(label)
    for fi, di, ai in list(zip(f,d,a))[:12]:
        print(f"   {fi:7.1f} Hz  damping {di:6.1f} 1/s  T60 {6.91/di*1000:6.0f} ms  Q {np.pi*fi/di:6.1f}  amp {20*np.log10(ai+1e-9):6.1f} dB")

print("\n=== matrix-pencil fits, 0-12 kHz band (decim 2) ===")
lp12 = ss.sosfiltfilt(ss.butter(6, 11500, 'low', fs=sr, output='sos'), stk)
for label, t0, t1 in [('after B 0.126-0.180', 0.126, 0.180), ('after C 0.258-0.320', 0.258, 0.320), ('after A 0.066-0.100', 0.066, 0.100)]:
    seg = lp12[int((t0+OFF)*sr):int((t1+OFF)*sr)]
    f, d, a = matrix_pencil(seg, sr, M=40, decim=2)
    keep = (f>300)&(d>0)&(d<800)
    idx = np.argsort(-a[keep]); f, d, a = f[keep][idx], d[keep][idx], a[keep][idx]
    print(label)
    for fi, di, ai in list(zip(f,d,a))[:14]:
        print(f"   {fi:7.1f} Hz  damping {di:6.1f} 1/s  T60 {6.91/di*1000:6.0f} ms  Q {np.pi*fi/di:6.1f}  amp {20*np.log10(ai+1e-9):6.1f} dB")
