"""Zoomed waveforms of each attack (0.1 ms resolution), rise times, sub-impacts, and high-band click structure."""
import numpy as np, soundfile as sf, scipy.signal as ss
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
orig, _ = sf.read(f'{ROOT}/clues/mnc/clue.wav')
t = np.arange(len(stk))/sr - OFF; to = np.arange(len(orig))/sr
hp = ss.sosfiltfilt(ss.butter(4, 2000, 'high', fs=sr, output='sos'), stk)
hpo = ss.sosfiltfilt(ss.butter(4, 2000, 'high', fs=sr, output='sos'), orig)
def env(x, win_ms):
    n = max(1,int(sr*win_ms/1000)); return np.sqrt(np.convolve(x**2, np.ones(n)/n, 'same'))

events = [('A', 0.055, 0.110), ('B', 0.105, 0.180), ('C', 0.240, 0.320), ('between', 0.175, 0.250), ('late', 0.320, 0.400)]
fig, ax = plt.subplots(len(events), 2, figsize=(16, 3.2*len(events)))
for k,(name, t0, t1) in enumerate(events):
    m = (t>=t0)&(t<=t1); mo = (to>=t0)&(to<=t1)
    ax[k,0].plot(t[m], stk[m], lw=0.5, label='stacked'); ax[k,0].plot(to[mo], orig[mo]-0.9, lw=0.5, label='orig (-0.9)')
    ax[k,0].set_title(f'{name} full band'); ax[k,0].legend(loc='upper right', fontsize=7)
    ax[k,1].plot(t[m], hp[m], lw=0.5); ax[k,1].plot(to[mo], hpo[mo]-0.5, lw=0.5)
    ax[k,1].plot(t[m], 20*np.log10(env(hp,0.5)[m]+1e-9)/100+0.6, lw=0.8, color='k')
    ax[k,1].set_title(f'{name} >2 kHz (black: 0.5 ms env dB/100+0.6)')
    for a in ax[k]: a.grid(alpha=.3); a.set_xlim(t0,t1)
plt.tight_layout(); plt.savefig(f'{OUT}/attacks.png', dpi=100)

# Click (>2 kHz) sub-impact list using a 0.3 ms envelope
e = 20*np.log10(env(hp, 0.3)+1e-9); bg = np.median(e[t<-0.02])
pk, pr = ss.find_peaks(e, height=bg+12, distance=int(sr*0.0015), prominence=4)
print(f"high-band (>2 kHz) click sub-impacts, stacked; bg {bg:.1f} dB")
for p,h,pm in zip(pk, pr['peak_heights'], pr['prominences']):
    print(f"  {t[p]:+.4f}s  {h:6.1f} dB  prom {pm:4.1f}")

# Rise time: 10-90% of the full-band 0.25 ms envelope around each main attack
ef = env(stk, 0.25)
for name, t0, t1 in [('A',0.058,0.070),('B',0.108,0.125),('C',0.244,0.260)]:
    m = (t>=t0)&(t<=t1); seg = ef[m]; tt = t[m]; pkv = seg.max(); ip = np.argmax(seg)
    i10 = np.where(seg[:ip] >= 0.1*pkv)[0]; i90 = np.where(seg[:ip] >= 0.9*pkv)[0]
    i10 = i10[0] if len(i10) else 0; i90 = i90[0] if len(i90) else ip
    # first sample where env exceeds bg+10 dB
    onset = tt[np.where(20*np.log10(seg+1e-9) > bg+10)[0][0]]
    print(f"{name}: onset(>bg+10dB) {onset:.4f}s, peak {tt[ip]:.4f}s ({20*np.log10(pkv):.1f} dB), 10-90% rise {1000*(tt[i90]-tt[i10]):.2f} ms")

# Spectral centroid in 2 ms steps across the attacks
print("\nspectral centroid (Hz) / 2 ms frames, stacked:")
for name, t0, t1 in [('A',0.058,0.080),('B',0.108,0.140),('C',0.244,0.280)]:
    s=[]
    for tt0 in np.arange(t0, t1, 0.002):
        seg = stk[int((tt0+OFF)*sr):int((tt0+OFF)*sr)+int(0.002*sr)]*np.hanning(int(0.002*sr))
        F = np.abs(np.fft.rfft(seg, 4096))**2; fr = np.fft.rfftfreq(4096,1/sr)
        s.append(f"{tt0:.3f}:{(F*fr).sum()/F.sum():5.0f}")
    print(f"  {name}: " + ' '.join(s))
