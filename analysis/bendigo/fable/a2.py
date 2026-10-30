import numpy as np, soundfile as sf, scipy.signal as sg, librosa, librosa.display
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x, sr = sf.read('ss.wav'); m = x.mean(1)
t = np.arange(len(m))/sr*1000
fig, ax = plt.subplots(4,1, figsize=(14,16))
ax[0].plot(t, m, lw=0.5); ax[0].set_xlim(0,273); ax[0].set_title('waveform'); ax[0].grid(alpha=.3)
ax[0].set_xticks(np.arange(0,275,10))
for n,(nfft,hop) in enumerate([(256,16),(1024,32)]):
    S = librosa.stft(m, n_fft=nfft, hop_length=hop, window='hann')
    D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, hop_length=hop, x_axis='ms', y_axis='linear', ax=ax[1+n], cmap='magma', vmin=-70, vmax=0)
    ax[1+n].set_title(f'STFT nfft={nfft} linear'); ax[1+n].set_ylim(0, 22050 if n==0 else 8000)
S = librosa.stft(m, n_fft=1024, hop_length=32)
D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
librosa.display.specshow(D, sr=sr, hop_length=32, x_axis='ms', y_axis='log', ax=ax[3], cmap='magma', vmin=-70, vmax=0)
ax[3].set_ylim(60, 22050); ax[3].set_title('log freq')
plt.tight_layout(); plt.savefig('spec1.png', dpi=80)
# Long-term spectrum (Welch) and peaks
f, P = sg.welch(m, sr, nperseg=2048, noverlap=1536)
Pdb = 10*np.log10(P/P.max())
pk, pr = sg.find_peaks(Pdb, prominence=4, distance=3)
print('LTAS peaks (Hz, dB rel max):')
for i in pk: print(f'  {f[i]:7.0f} Hz  {Pdb[i]:6.1f} dB')
# band energies
def band(lo,hi):
    sel=(f>=lo)&(f<hi); return 10*np.log10(np.trapezoid(P[sel],f[sel])/np.trapezoid(P,f))
for lo,hi in [(0,100),(100,200),(200,500),(500,1000),(1000,2000),(2000,4000),(4000,8000),(8000,12000),(12000,16000),(16000,22050)]:
    print(f'band {lo:5d}-{hi:5d}: {band(lo,hi):6.1f} dB of total')
cen = librosa.feature.spectral_centroid(y=m, sr=sr, n_fft=512, hop_length=64)[0]
print('centroid per 1.45ms frame (kHz):', ' '.join(f'{c/1000:.1f}' for c in cen))
print('overall centroid', librosa.feature.spectral_centroid(y=m, sr=sr)[0].mean())
