"""Detail checks: (a) sub-impact periodicity inside B and C, (b) whine lines: part of the clip or station?,
(c) LF force-pulse analysis: deconvolve 62 Hz resonator to estimate the driving force envelope,
(d) spectral similarity of the A/B/C attacks, (e) early broadband decay (room/dryness)."""
import numpy as np, soundfile as sf, scipy.signal as ss, glob
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
orig, _ = sf.read(f'{ROOT}/clues/mnc/clue.wav')
t = np.arange(len(stk))/sr - OFF
def seg(x, t0, t1, off=OFF): return x[int((t0+off)*sr):int((t1+off)*sr)]
def env(x, win_ms):
    n = max(1,int(sr*win_ms/1000)); return np.sqrt(np.convolve(x**2, np.ones(n)/n, 'same'))

# (a) sub-impact periodicity: autocorrelation of >2 kHz envelope inside B and C
hp = ss.sosfiltfilt(ss.butter(4, 2000, 'high', fs=sr, output='sos'), stk)
print("(a) autocorrelation of >2 kHz 0.2 ms envelope within attacks (lag of first 3 peaks):")
for name, t0, t1 in [('A', 0.057, 0.075), ('B', 0.108, 0.130), ('C', 0.245, 0.268)]:
    e = env(seg(hp,t0,t1), 0.2); e = e - e.mean()
    ac = np.correlate(e, e, 'full')[len(e)-1:]; ac /= ac[0]
    pk, _ = ss.find_peaks(ac, distance=int(sr*0.0008))
    print(f"   {name}: " + ', '.join(f"{1000*p/sr:.2f} ms (r={ac[p]:.2f})" for p in pk[:4]))
    # also the raw sub-burst list from the 0.2 ms env
    pk2, pr = ss.find_peaks(20*np.log10(env(seg(hp,t0,t1),0.2)+1e-9), prominence=6, distance=int(sr*0.0008))
    print(f"      sub-bursts: " + ', '.join(f"{t0+p/sr:.4f}" for p in pk2))

# Also: within B, the full-band waveform shows two bursts. Energy time-profile at 1 ms, >1 kHz
bp1 = ss.sosfiltfilt(ss.butter(4, 1000, 'high', fs=sr, output='sos'), stk)
print("\n   >1 kHz energy per 1 ms (dB), B 0.106-0.132 and C 0.243-0.270:")
for name,t0,t1 in [('B',0.106,0.132),('C',0.243,0.270)]:
    s = seg(bp1,t0,t1); n = int(0.001*sr)
    vals = [20*np.log10(np.sqrt((s[i:i+n]**2).mean())+1e-9) for i in range(0, len(s)-n+1, n)]
    print(f"   {name}: " + ' '.join(f"{t0+i*0.001:.3f}:{v:.0f}" for i,v in enumerate(vals)))

# (b) whine lines: PSD of stacked pre-clip (0.0-0.055) vs mean PSD of individual plays pre-clip (-0.5..-0.05) and in-clip
files = sorted(glob.glob(f'{ROOT}/harvest/mnc/plays/*.flac'))
X = np.array([sf.read(f)[0][:120000] for f in files])
tp = np.arange(120000)/sr - 1.0
def welch(x, n=2048): f,P = ss.welch(x, sr, nperseg=n, noverlap=n//2); return f, P
f, Ps_pre = welch(seg(stk, 0.0, 0.055))
f, Ps_body = welch(seg(stk, 0.13, 0.245))
Pp_pre = np.mean([welch(x[(tp>-0.6)&(tp<-0.05)])[1] for x in X[:120]], 0)
Pp_body = np.mean([welch(x[(tp>0.13)&(tp<0.245)])[1] for x in X[:120]], 0)
print("\n(b) spectral lines 8-16 kHz: stacked pre-clip (0-0.055) and stacked body (0.13-0.245) vs mean single-play PSDs (dB)")
for lo,hi in [(8300,8400),(9100,9200),(11150,11250),(11500,11650),(12000,12100),(12650,12720),(13300,13400),(13800,13900),(15700,15800)]:
    m=(f>=lo)&(f<hi)
    print(f"   {lo}-{hi}: stk_pre {10*np.log10(Ps_pre[m].max()):6.1f}  stk_body {10*np.log10(Ps_body[m].max()):6.1f}  play_pre {10*np.log10(Pp_pre[m].max()):6.1f}  play_body {10*np.log10(Pp_body[m].max()):6.1f}")
# whole-band comparison for context
for lo,hi in [(100,300),(1000,2000),(5000,8000),(8000,11000),(11000,14000),(14000,16000)]:
    m=(f>=lo)&(f<hi)
    print(f"   band {lo}-{hi}: stk_pre {10*np.log10(Ps_pre[m].mean()):6.1f}  stk_body {10*np.log10(Ps_body[m].mean()):6.1f}  play_pre {10*np.log10(Pp_pre[m].mean()):6.1f}  play_body {10*np.log10(Pp_body[m].mean()):6.1f}")

# time-frequency of the 8-16 kHz region at 10 ms steps to see whether the lines are continuous
fsp, tsp, S = ss.spectrogram(stk, sr, nperseg=2048, noverlap=1536, mode='magnitude'); S=20*np.log10(S+1e-9)
print("\n   line tracks (dB) at 10 ms steps, orig time -0.03..0.40:")
for fl in [8355, 11197, 11531, 12018, 12680, 13846, 15146]:
    i = np.argmin(np.abs(fsp-fl)); row = S[i]
    print(f"   {fl:6d} Hz: " + ' '.join(f"{tsp[j]-OFF:.2f}:{row[j]:.0f}" for j in range(0,len(tsp),1) if -0.03 < tsp[j]-OFF < 0.42))

# (c) LF force pulse: inverse-filter the 62 Hz resonator (f=62, damping fitted) from LP200 signal to get driving force
lp = ss.sosfiltfilt(ss.butter(4, 250, 'low', fs=sr, output='sos'), stk)
for f0, zeta_T60 in [(62.0, 0.16)]:
    d = 6.91/zeta_T60  # damping 1/s
    w0 = 2*np.pi*f0
    # continuous resonator H(s) = w0^2/(s^2+2 d s + w0^2); inverse = apply (s^2 + 2d s + w0^2)/w0^2 via finite differences
    x = lp; dt = 1/sr
    acc = np.gradient(np.gradient(x, dt), dt); vel = np.gradient(x, dt)
    force = (acc + 2*d*vel + w0**2*x)/w0**2
    force = ss.sosfiltfilt(ss.butter(4, 300, 'low', fs=sr, output='sos'), force)
    fig, ax = plt.subplots(2,1, figsize=(13,6), sharex=True)
    ax[0].plot(t, lp); ax[0].set_ylabel('LP250'); ax[0].set_xlim(0.09,0.36); ax[0].grid(alpha=.3)
    ax[1].plot(t, force); ax[1].set_ylabel(f'est. drive (62 Hz, T60 {zeta_T60*1000:.0f} ms removed)'); ax[1].grid(alpha=.3)
    for a in ax:
        for tt in [0.064,0.117,0.250]: a.axvline(tt, color='r', lw=0.6, alpha=0.6)
    plt.tight_layout(); plt.savefig(f'{OUT}/lf_force.png', dpi=100)
    e = env(force, 3.0)
    pk, pr = ss.find_peaks(e, distance=int(sr*0.008), height=e.max()*0.15)
    print("\n(c) LF driving-force envelope peaks (orig time, rel amplitude):")
    for p in pk:
        if 0.09 < t[p] < 0.36: print(f"   {t[p]:.4f}s  {e[p]/e.max():.2f}")

# (d) attack spectral similarity (first 8 ms, 1/3-oct smoothed, 300-12000 Hz)
def third_oct(x):
    F = np.abs(np.fft.rfft(x*np.hanning(len(x)), 8192)); fr = np.fft.rfftfreq(8192,1/sr)
    cs = 300*2**(np.arange(0,16)/3); out=[]
    for c in cs:
        m=(fr>=c/2**(1/6))&(fr<c*2**(1/6)); out.append(20*np.log10(np.sqrt((F[m]**2).mean())+1e-9))
    return cs, np.array(out)
spec = {}
for name,t0 in [('A',0.0585),('B',0.1105),('C',0.2465),('B2',0.1205)]:
    cs, L = third_oct(seg(stk,t0,t0+0.008)); spec[name]=L-L.max()
print("\n(d) 1/3-octave attack spectra (dB re max), 8 ms windows:")
print("   centre Hz: " + ' '.join(f"{c:6.0f}" for c in cs))
for k,v in spec.items(): print(f"   {k:2s}       : " + ' '.join(f"{x:6.1f}" for x in v))
for a,b in [('A','B'),('B','C'),('A','C'),('B','B2')]:
    print(f"   corr {a}-{b}: {np.corrcoef(spec[a],spec[b])[0,1]:.2f}")

# (e) early broadband decay after A (dryness): 4-8 kHz 0.5 ms envelope, time to fall 20 dB
b48 = ss.sosfiltfilt(ss.butter(4,[4000,8000],'band',fs=sr,output='sos'), stk)
e = 20*np.log10(env(b48,0.5)+1e-9)
for name,t0 in [('A',0.0635),('B',0.118),('C',0.2507)]:
    i0 = int((t0+OFF)*sr); pk = e[i0-24:i0+24].max(); ip = i0-24+np.argmax(e[i0-24:i0+24])
    j20 = ip + np.argmax(e[ip:] < pk-20); j30 = ip + np.argmax(e[ip:] < pk-30)
    print(f"(e) {name}: 4-8 kHz peak {pk:.1f} dB at {t[ip]:.4f}; -20 dB after {1000*(j20-ip)/sr:.1f} ms; -30 dB after {1000*(j30-ip)/sr:.1f} ms")
