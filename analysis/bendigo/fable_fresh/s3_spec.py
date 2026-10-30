"""Spectrogram and whole-clip spectral peaks."""
import numpy as np, scipy.signal as ss, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x=np.load('mono.npy'); sr=44100
for n,name in [(512,'fine'),(2048,'tonal')]:
    f,t,S=ss.stft(x,sr,nperseg=n,noverlap=n-32,window='hann')
    P=20*np.log10(np.abs(S)+1e-7)
    fig,ax=plt.subplots(figsize=(14,8))
    ax.pcolormesh(t*1000,f/1000,P,vmin=P.max()-70,vmax=P.max(),shading='auto',cmap='magma')
    ax.set_ylim(0,16 if name=='fine' else 8); ax.set_xlabel('ms'); ax.set_ylabel('kHz'); ax.set_title(f'STFT n={n}')
    plt.tight_layout(); plt.savefig(f'fig_spec_{name}.png',dpi=110)
# Whole clip spectrum, zero-padded
N=1<<16; X=np.fft.rfft(x*np.hanning(len(x)),N); fr=np.fft.rfftfreq(N,1/sr); A=20*np.log10(np.abs(X)+1e-9); A-=A.max()
pk,pr=ss.find_peaks(A,height=-45,prominence=6,distance=int(40/(sr/N)))
order=np.argsort(-A[pk])
print('whole-clip peaks (Hz, dB rel max, prominence):')
for i in order[:40]: print(f'{fr[pk[i]]:8.1f}  {A[pk[i]]:6.1f}  {pr["prominences"][i]:5.1f}')
# band energy summary
def band(lo,hi): m=(fr>=lo)&(fr<hi); return 10*np.log10(np.sum(np.abs(X[m])**2)+1e-12)
tot=10*np.log10(np.sum(np.abs(X)**2))
print('band energy rel total dB:')
for lo,hi in [(0,100),(100,200),(200,400),(400,800),(800,1500),(1500,2000),(2000,3000),(3000,5000),(5000,8000),(8000,12000),(12000,16000),(16000,22050)]:
    print(f'{lo:6d}-{hi:6d}: {band(lo,hi)-tot:6.1f}')
fig,ax=plt.subplots(2,1,figsize=(14,8)); ax[0].plot(fr,A); ax[0].set_xlim(0,12000); ax[0].set_ylim(-70,2); ax[0].grid()
ax[1].plot(fr,A); ax[1].set_xlim(0,1500); ax[1].set_ylim(-70,2); ax[1].grid(); ax[1].set_xlabel('Hz')
plt.tight_layout(); plt.savefig('fig_spectrum.png',dpi=110)
# mp3 lowpass? check energy above 16k
print('max dB in 15.5-16.5k',A[(fr>15500)&(fr<16500)].max(),' 16.5-20k',A[(fr>16500)&(fr<20000)].max())
