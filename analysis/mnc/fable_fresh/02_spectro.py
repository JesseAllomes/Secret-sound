"""Spectrograms and per-event spectra of the stacked clip (orig time)."""
import numpy as np, soundfile as sf, scipy.signal as ss, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
orig, _ = sf.read(f'{ROOT}/clues/mnc/clue.wav')
t = np.arange(len(stk))/sr - OFF

fig, ax = plt.subplots(3, 1, figsize=(14, 14))
for a, (nfft, hop, fmax, title) in zip(ax, [(256, 16, 24000, 'stacked 256-pt (5 ms) linear to 24 kHz'),
                                             (1024, 32, 6000, 'stacked 1024-pt (21 ms) 0-6 kHz'),
                                             (4096, 64, 1200, 'stacked 4096-pt (85 ms) 0-1200 Hz')]):
    f, tt, S = ss.spectrogram(stk, sr, nperseg=nfft, noverlap=nfft-hop, window='hann', mode='magnitude')
    S = 20*np.log10(S+1e-9)
    m = f <= fmax
    a.pcolormesh(tt-OFF, f[m], S[m], vmin=S.max()-80, vmax=S.max(), cmap='magma', shading='auto')
    a.set_xlim(-0.02, 0.42); a.set_title(title); a.set_ylabel('Hz')
ax[-1].set_xlabel('orig time (s)')
plt.tight_layout(); plt.savefig(f'{OUT}/spectrogram.png', dpi=100)

# Per-event spectra: attack (first 6 ms) and tail (next 40 ms), 1/6-octave smoothed summary
def spec(x, t0, dur, nfft=8192):
    i0 = int((t0+OFF)*sr); seg = stk[i0:i0+int(dur*sr)]*np.hanning(int(dur*sr))
    F = np.abs(np.fft.rfft(seg, nfft)); fr = np.fft.rfftfreq(nfft, 1/sr)
    return fr, 20*np.log10(F+1e-9)

def summarise(fr, L, label):
    edges = [20,60,120,250,500,1000,2000,3000,4000,6000,8000,12000,16000,24000]
    s = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (fr>=lo)&(fr<hi); s.append(f"{lo}-{hi}:{L[m].max():5.0f}")
    print(f"{label:38s} " + ' '.join(s))

print("peak dB per band (max bin, relative units) for windows of stacked clip")
windows = [('A attack 0.060-0.068', 0.060, 0.008), ('A tail 0.068-0.100', 0.068, 0.032),
           ('B pre 0.100-0.112', 0.100, 0.012), ('B attack 0.112-0.120', 0.112, 0.008), ('B 0.120-0.135', 0.120, 0.015),
           ('B thump 0.135-0.175', 0.135, 0.040), ('B tail 0.175-0.245', 0.175, 0.070),
           ('C attack 0.247-0.255', 0.247, 0.008), ('C 0.255-0.270', 0.255, 0.015), ('C thump 0.270-0.320', 0.270, 0.050),
           ('C tail 0.320-0.380', 0.320, 0.060)]
for label, t0, d in windows:
    fr, L = spec(stk, t0, d); summarise(fr, L, label)

# Fine spectral peaks in the tails (long windows for resolution)
print("\n=== top spectral peaks, long windows (stacked) ===")
for label, t0, d in [('B tail 0.130-0.245', 0.130, 0.115), ('C tail 0.265-0.380', 0.265, 0.115),
                     ('A tail 0.066-0.108', 0.066, 0.042)]:
    fr, L = spec(stk, t0, d, nfft=1<<16)
    pk, pr = ss.find_peaks(L, prominence=8, distance=int(5/(fr[1]-fr[0])))
    order = np.argsort(L[pk])[::-1][:25]
    print(label)
    for i in sorted(order, key=lambda i: fr[pk[i]]):
        print(f"   {fr[pk[i]]:8.1f} Hz  {L[pk[i]]:6.1f} dB  prom {pr['prominences'][i]:4.1f}")
