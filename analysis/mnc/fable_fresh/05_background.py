"""Station background vs. the recording: spectrum of pre-clip region (orig and stacked), the fixed
spectral lines near 11/13 kHz, bandwidth, and per-play consistency of the stacked clip."""
import numpy as np, soundfile as sf, scipy.signal as ss, glob
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
orig, _ = sf.read(f'{ROOT}/clues/mnc/clue.wav')
t = np.arange(len(stk))/sr - OFF; to = np.arange(len(orig))/sr

def psd(x, nfft=4096):
    f, P = ss.welch(x, sr, nperseg=nfft, noverlap=nfft//2); return f, 10*np.log10(P+1e-15)

print("=== Welch PSD, dB/Hz, selected bands: orig pre-clip (0-0.05), orig post (0.40-0.63), stacked body (0.10-0.37), stacked post (0.40-0.65) ===")
segs = {'orig pre 0-0.05': orig[:int(0.05*sr)], 'orig post 0.40-0.63': orig[int(0.40*sr):],
        'stacked body 0.10-0.37': stk[int(0.15*sr):int(0.42*sr)], 'stacked post 0.42-0.65': stk[int(0.47*sr):]}
edges = [20,50,100,200,400,800,1600,3200,6400,9000,10500,11500,12500,13500,16000,20000,24000]
for k,v in segs.items():
    f,P = psd(v, 2048)
    print(f"{k:26s} " + ' '.join(f"{lo}-{hi}:{P[(f>=lo)&(f<hi)].mean():5.0f}" for lo,hi in zip(edges[:-1],edges[1:])))

# Fixed lines: fine spectrum of stacked body vs orig body, 8-16 kHz
f, Ps = psd(stk[int(0.15*sr):int(0.42*sr)], 8192); _, Po = psd(orig[int(0.10*sr):int(0.37*sr)], 8192)
print("\nnarrow spectral lines 5-20 kHz in stacked body (prominence>10 dB):")
pk, pr = ss.find_peaks(Ps, prominence=10)
for p in pk:
    if 5000 < f[p] < 20000: print(f"  {f[p]:8.1f} Hz  {Ps[p]:6.1f} dB  prom {pr['prominences'][list(pk).index(p)]:.1f}   orig there: {Po[p]:6.1f}")
print("narrow spectral lines 5-20 kHz in orig pre-clip:")
f2, Pp = psd(orig[:int(0.05*sr)], 2048); pk, pr = ss.find_peaks(Pp, prominence=8)
for i,p in enumerate(pk):
    if 5000 < f2[p] < 20000: print(f"  {f2[p]:8.1f} Hz  {Pp[p]:6.1f} dB  prom {pr['prominences'][i]:.1f}")

# Mains hum check: 50 Hz and harmonics in orig pre/post and in stacked body
print("\nlow-frequency lines (<400 Hz):")
for k,v in segs.items():
    f,P = psd(v, min(8192, len(v))); pk, pr = ss.find_peaks(P, prominence=6)
    s = [f"{f[p]:.0f}({P[p]:.0f})" for i,p in enumerate(pk) if f[p] < 400]
    print(f"  {k:26s}: " + ' '.join(s))

# Per-play consistency: load plays, align to clip window, measure the median absolute deviation
files = sorted(glob.glob(f'{ROOT}/harvest/mnc/plays/*.flac'))
X = []
for fp in files:
    x,_ = sf.read(fp); X.append(x[:120000] if len(x)>=120000 else np.pad(x,(0,120000-len(x))))
X = np.array(X)  # plays: 1.0 s before clip start -> t = i/sr - 1.0
tp = np.arange(120000)/sr - 1.0
# normalise each play by its RMS in the clip body
body = (tp>0.10)&(tp<0.37)
g = np.sqrt((X[:,body]**2).mean(1)); X = X/g[:,None]
med = np.median(X, 0); mean = X.mean(0)
# correlation of each play with median over body
c = np.array([np.corrcoef(x[body], med[body])[0,1] for x in X])
print(f"\nplays: {len(X)}; corr with median over body: median {np.median(c):.3f}, 10th pct {np.percentile(c,10):.3f}, min {c.min():.3f}")
# per-block common ratio recomputed at 5 ms, and time at which it falls off at the end
print("5 ms common ratio (energy of mean / mean energy), 0.33-0.42 s and 0.03-0.07:")
for t0 in list(np.arange(0.03,0.075,0.005)) + list(np.arange(0.33,0.42,0.005)):
    m = (tp>=t0)&(tp<t0+0.005)
    r = (mean[m]**2).mean()/((X[:,m]**2).mean())
    print(f"  {t0:.3f}: {r:.3f}")

# Does the median of plays show anything AFTER 0.38 that the stacked file gated out? band energy of median 0.35-0.60 vs noise
em = 20*np.log10(np.sqrt(np.convolve(med**2, np.ones(480)/480,'same'))+1e-9)
print("\nmedian-of-plays 10 ms envelope dB, 0.30-0.60 s:")
print(' '.join(f"{tt:.2f}:{em[int((tt+1.0)*sr)]:.0f}" for tt in np.arange(0.30,0.60,0.01)))
print("median-of-plays 10 ms envelope dB, -0.10-0.12 s:")
print(' '.join(f"{tt:.2f}:{em[int((tt+1.0)*sr)]:.0f}" for tt in np.arange(-0.10,0.12,0.01)))

# high-band (>3 kHz) in median of plays around 0.34-0.40 (the late small click) and beyond
hpm = ss.sosfiltfilt(ss.butter(4, 3000, 'high', fs=sr, output='sos'), med)
eh = 20*np.log10(np.sqrt(np.convolve(hpm**2, np.ones(96)/96,'same'))+1e-9)
print("median-of-plays >3 kHz 2 ms envelope dB, 0.30-0.50 s:")
print(' '.join(f"{tt:.3f}:{eh[int((tt+1.0)*sr)]:.0f}" for tt in np.arange(0.30,0.50,0.005)))
sf.write(f'{OUT}/plays_median_norm.wav', med/np.abs(med).max()*0.9, sr)
