"""Analyse Freesound 641862 'Key_Old_Recorder' the same way as the clue, and compare.
Outputs printed tables and figures recorder_overview.png, recorder_events.png, recorder_vs_clue.png."""
import numpy as np, soundfile as sf, scipy.signal as ss, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
SR = 48000
r, sr0 = sf.read(f'{ROOT}/listening/full/641862_Key-Old-Recorder.mp3')
if r.ndim > 1: r = r.mean(1)
r = ss.resample_poly(r, SR, sr0); sr = SR
r = r / np.abs(r).max() * 0.9
stk, _ = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
t = np.arange(len(r))/sr

def env(x, ms):
    n = max(1, int(sr*ms/1000)); return 20*np.log10(np.sqrt(np.convolve(x**2, np.ones(n)/n, 'same'))+1e-9)
def bp(x, lo, hi, order=4): return ss.sosfiltfilt(ss.butter(order, [lo, hi], 'band', fs=sr, output='sos'), x)
def hpf(x, f): return ss.sosfiltfilt(ss.butter(4, f, 'high', fs=sr, output='sos'), x)
def lpf(x, f): return ss.sosfiltfilt(ss.butter(4, f, 'low', fs=sr, output='sos'), x)

# ---- 1. overview: event list over the whole file
E = env(r, 1.0); bg = np.percentile(E, 20)
print(f"recorder: {len(r)/sr:.2f} s, noise floor (20th pct of 1 ms env) {bg:.1f} dB")
pk, pr = ss.find_peaks(E, height=bg+20, distance=int(sr*0.04), prominence=10)
print("events (1 ms env peaks > floor+20 dB, >=40 ms apart):")
for p, h in zip(pk, pr['peak_heights']):
    print(f"  {t[p]:7.3f}s  {h:6.1f} dB")
fig, ax = plt.subplots(3, 1, figsize=(16, 9), sharex=True)
ax[0].plot(t, r, lw=0.3); ax[0].set_ylabel('waveform')
ax[1].plot(t, E, lw=0.5); ax[1].set_ylabel('1 ms env dB'); ax[1].set_ylim(-80, 0)
ax[2].plot(t, env(lpf(r, 250), 2), lw=0.5, label='<250 Hz'); ax[2].plot(t, env(hpf(r, 2000), 2), lw=0.5, label='>2 kHz')
ax[2].plot(t, env(bp(r, 740, 840), 2), lw=0.5, label='740-840 Hz'); ax[2].legend(); ax[2].set_ylim(-90, -5); ax[2].set_ylabel('band env dB')
for a in ax:
    for w in [7.04, 13.02, 3.92, 1.72, 8.32]: a.axvline(w, color='r', lw=0.5, alpha=0.6)
ax[-1].set_xlabel('s'); plt.tight_layout(); plt.savefig(f'{OUT}/recorder_overview.png', dpi=90)

# ---- 2. per-window detail (window = 0.7 s starting at the matcher offset, like the stacked clue)
def seg(x, t0, dur): i = int(t0*sr); return x[i:i+int(dur*sr)]
def analyse_window(t0, label):
    w = seg(r, t0, 0.70); tw = np.arange(len(w))/sr
    hp = hpf(w, 2000); lp = lpf(w, 250); b791 = bp(w, 760, 820)
    e05 = env(hp, 0.5); bgw = np.percentile(e05, 20)
    pkh, prh = ss.find_peaks(e05, height=bgw+15, distance=int(sr*0.008), prominence=8)
    print(f"\n=== window {label} at {t0:.2f}s ===")
    print(f"  >2 kHz click peaks (0.5 ms env):")
    for p, h in zip(pkh, prh['peak_heights']):
        # duration above peak-15 dB around p
        a = p
        while a > 0 and e05[a] > h-15: a -= 1
        b = p
        while b < len(e05)-1 and e05[b] > h-15: b += 1
        # rise shape: crescendo or abrupt (level 3 ms before peak vs peak)
        pre = e05[max(0,p-int(0.003*sr))]
        print(f"    t={tw[p]:.4f}s ({t0+tw[p]:.3f}s abs) {h:6.1f} dB, width(-15dB) {1000*(b-a)/sr:5.1f} ms, 3 ms before peak {pre-h:+5.1f} dB -> {'crescendo' if pre-h > -12 else 'abrupt'}")
    # LF thud
    elp = env(lp, 2.0); pkl, prl = ss.find_peaks(elp, height=np.percentile(elp,20)+15, distance=int(sr*0.03), prominence=6)
    print("  <250 Hz thud peaks (2 ms env):")
    for p, h in zip(pkl, prl['peak_heights']):
        # inst freq around peak
        a = ss.hilbert(bp(w, 30, 150)); f = np.diff(np.unwrap(np.angle(a)))*sr/(2*np.pi)
        m = slice(max(0,p-int(0.01*sr)), min(len(f), p+int(0.03*sr)))
        print(f"    t={tw[p]:.4f}s {h:6.1f} dB  inst f (30-150 band, +-) {np.median(f[m]):5.1f} Hz")
    # full-band spectral peaks in the tail after the loudest click
    if len(pkh):
        p0 = pkh[np.argmax(prh['peak_heights'])]
        tail = w[p0+int(0.015*sr): p0+int(0.135*sr)]
        if len(tail) > 1000:
            F = np.abs(np.fft.rfft(tail*np.hanning(len(tail)), 1<<16)); fr = np.fft.rfftfreq(1<<16, 1/sr); L = 20*np.log10(F+1e-9)
            pkf, prf = ss.find_peaks(L, prominence=12, distance=int(8/(fr[1]-fr[0])))
            top = sorted(np.argsort(L[pkf])[::-1][:14], key=lambda i: fr[pkf[i]])
            print("  tail spectral peaks (15-135 ms after loudest click): " + ', '.join(f"{fr[pkf[i]]:.0f}Hz/{L[pkf[i]]:.0f}dB" for i in top))
            # decay of top 3 narrow bands
            for i in sorted(np.argsort(L[pkf])[::-1][:5], key=lambda i: fr[pkf[i]]):
                f0 = fr[pkf[i]]
                if f0 < 40 or f0 > 12000: continue
                y = env(bp(w, max(20,f0-20), f0+20), 2.0); tt = tw
                m = (tt >= tw[p0]+0.02) & (tt <= tw[p0]+0.12)
                sl = np.polyfit(tt[m], y[m], 1)[0]
                print(f"     {f0:7.1f} Hz: slope {sl:7.0f} dB/s, T60 {-60/sl*1000 if sl<0 else float('inf'):6.0f} ms")
    # brightness: spectral centroid of 8 ms at the loudest click
    if len(pkh):
        p0 = pkh[np.argmax(prh['peak_heights'])]
        s = w[max(0,p0-int(0.002*sr)):p0+int(0.006*sr)]*np.hanning(int(0.008*sr))[:len(w[max(0,p0-int(0.002*sr)):p0+int(0.006*sr)])]
        F = np.abs(np.fft.rfft(s, 8192))**2; fr = np.fft.rfftfreq(8192, 1/sr)
        print(f"  centroid of loudest click (8 ms): {(F*fr).sum()/F.sum():.0f} Hz; 4-8 kHz 1 ms env peak {env(bp(w,4000,8000),1).max():.1f} dB, 16-20 kHz {env(bp(w,16000,20000),1).max():.1f} dB")
    # dryness
    e48 = env(bp(w, 4000, 8000), 0.5)
    if len(pkh):
        p0 = pkh[np.argmax(prh['peak_heights'])]; ip = p0-24+np.argmax(e48[p0-24:p0+24]); pkv = e48[ip]
        j20 = ip + np.argmax(e48[ip:] < pkv-20); j30 = ip + np.argmax(e48[ip:] < pkv-30)
        print(f"  4-8 kHz: -20 dB after {1000*(j20-ip)/sr:.1f} ms, -30 dB after {1000*(j30-ip)/sr:.1f} ms")
    return w

wins = [(7.04, 'best'), (13.02, '2nd'), (3.92, '3rd'), (1.72, '4th'), (8.32, '5th')]
W = {}
for t0, lab in wins: W[lab] = analyse_window(t0, lab)

# ---- 3. figure: the five windows, full band + >2 kHz + <250 Hz
fig, ax = plt.subplots(len(wins), 3, figsize=(18, 2.6*len(wins)))
for k, (t0, lab) in enumerate(wins):
    w = W[lab]; tw = np.arange(len(w))/sr
    ax[k,0].plot(tw, w, lw=0.4); ax[k,0].set_title(f'{lab} @ {t0:.2f}s full band')
    ax[k,1].plot(tw, env(hpf(w,2000),0.5), lw=0.5); ax[k,1].set_ylim(-80,-5); ax[k,1].set_title('>2 kHz env dB')
    ax[k,2].plot(tw, lpf(w,250), lw=0.6); ax[k,2].set_title('<250 Hz waveform')
    for a in ax[k]: a.grid(alpha=.3); a.set_xlim(0, 0.7)
plt.tight_layout(); plt.savefig(f'{OUT}/recorder_events.png', dpi=90)

# ---- 4. side-by-side with the clue, aligned on the loudest click
def align_on_loudest(x):
    e = env(hpf(x,2000), 0.5); return np.argmax(e)
w = W['best']; ic = align_on_loudest(w); ik = align_on_loudest(stk)
fig, ax = plt.subplots(4, 2, figsize=(18, 11))
for col, (x, name, i0) in enumerate([(stk, 'clue (stacked)', ik), (w, 'recorder best window', ic)]):
    tt = (np.arange(len(x)) - i0)/sr
    ax[0,col].plot(tt, x, lw=0.4); ax[0,col].set_title(name + ' (t=0 at loudest >2 kHz click)')
    ax[1,col].plot(tt, env(hpf(x,2000),0.5), lw=0.5); ax[1,col].set_ylim(-80,-5); ax[1,col].set_ylabel('>2 kHz')
    ax[2,col].plot(tt, lpf(x,250), lw=0.6); ax[2,col].set_ylabel('<250 Hz')
    ax[3,col].plot(tt, env(bp(x,760,820),2), lw=0.6, label='760-820'); ax[3,col].plot(tt, env(bp(x,1100,1150),2), lw=0.6, label='1100-1150')
    ax[3,col].plot(tt, env(bp(x,1830,1870),2), lw=0.6, label='1830-1870'); ax[3,col].set_ylim(-90,-15); ax[3,col].legend(fontsize=7)
    for a in ax[:,col]: a.set_xlim(-0.25, 0.4); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(f'{OUT}/recorder_vs_clue.png', dpi=90)

# ---- 5. spectrogram of the best window and of the clue for visual comparison
fig, ax = plt.subplots(2, 1, figsize=(14, 9))
for a, (x, name) in zip(ax, [(stk, 'clue stacked'), (w, 'recorder best window')]):
    f, tt, S = ss.spectrogram(x, sr, nperseg=1024, noverlap=1024-32, mode='magnitude'); S = 20*np.log10(S+1e-9)
    m = f <= 8000; a.pcolormesh(tt, f[m], S[m], vmin=S.max()-80, vmax=S.max(), cmap='magma', shading='auto'); a.set_title(name)
plt.tight_layout(); plt.savefig(f'{OUT}/recorder_spectro.png', dpi=90)

# ---- 6. matrix pencil modes after loudest click in best window and in clue, 0-6 kHz
def matrix_pencil(x, fs, M=30, decim=4):
    x = x[::decim]; fs = fs/decim; N = len(x); L = N//2
    H = np.array([x[i:i+L] for i in range(N-L)]); U, s, Vh = np.linalg.svd(H, full_matrices=False)
    V = Vh.conj().T[:, :M]; z = np.linalg.eigvals(np.linalg.pinv(V[:-1]) @ V[1:])
    f = np.angle(z)*fs/(2*np.pi); d = -np.log(np.abs(z))*fs
    n = np.arange(N); Z = z[None,:]**n[:,None]; a = np.linalg.lstsq(Z, x, rcond=None)[0]
    return f, d, np.abs(a)
print("\n=== matrix-pencil modes 20-5800 Hz, 20-130 ms after loudest click ===")
for x, name, i0 in [(stk, 'clue', ik), (w, 'recorder best', ic)]:
    s = lpf(x, 5800)[i0+int(0.02*sr): i0+int(0.13*sr)]
    f, d, a = matrix_pencil(s, sr, M=36, decim=4)
    keep = (f > 20) & (d > 0) & (d < 600); idx = np.argsort(-a[keep]); f, d, a = f[keep][idx], d[keep][idx], a[keep][idx]
    print(name + ': ' + ', '.join(f"{fi:.0f}Hz(T60 {6.91/di*1000:.0f}ms,{20*np.log10(ai+1e-9):.0f}dB)" for fi, di, ai in list(zip(f, d, a))[:12]))
sf.write(f'{OUT}/recorder_best_window_48k.wav', w, sr)
