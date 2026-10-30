import numpy as np, soundfile as sf, scipy.signal as sg
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x, sr = sf.read('ss.wav'); m = x.mean(1); N=len(m); t=np.arange(N)/sr*1000
strikes=[0,12,92,146,213,255]
print('=== per-strike spectra (first 22 ms after strike, zero-padded), peaks >-18dB rel seg max')
for s in strikes:
    a=int(s/1000*sr); b=min(N,a+int(0.022*sr)); seg=m[a:b]*np.hanning(b-a)
    F=np.abs(np.fft.rfft(seg,1<<15)); fr=np.fft.rfftfreq(1<<15,1/sr); Fd=20*np.log10(F/F.max()+1e-9)
    sel=fr<9000; pk,_=sg.find_peaks(Fd[sel],prominence=5,distance=20)
    pk=[p for p in pk if Fd[p]>-18]
    print(f'strike {s:3d} ms:', ', '.join(f'{fr[p]:.0f}({Fd[p]:.0f})' for p in sorted(pk,key=lambda p:-Fd[p])[:14]))
print('=== narrowband tone tracking (dB, per 5 ms)')
for fc,bw in [(86,30),(345,40),(474,40),(603,40),(1141,80),(2326,120),(2562,120),(3359,150),(3962,200),(6481,300)]:
    sos=sg.butter(3,[fc-bw/2,fc+bw/2],btype='band',fs=sr,output='sos'); y=sg.sosfiltfilt(sos,m)
    e=np.sqrt(np.convolve(y**2,np.ones(221)/221,'same')); ed=20*np.log10(e+1e-7)
    print(f'{fc:5d} Hz:', ' '.join(f'{ed[i]:.0f}' for i in range(110,N,221)))
# first 3 ms spectrum
seg=m[:int(0.003*sr)]*np.hanning(int(0.003*sr)); F=np.abs(np.fft.rfft(seg,1<<14)); fr=np.fft.rfftfreq(1<<14,1/sr); Fd=20*np.log10(F/F.max()+1e-9)
pk,_=sg.find_peaks(Fd[fr<8000],prominence=4); print('first 3ms peaks:',[(round(fr[p]),round(Fd[p])) for p in sorted(pk,key=lambda p:-Fd[p])[:8]])
# high-res spectrogram 0-6k
fig,ax=plt.subplots(2,1,figsize=(14,10))
for a,(nfft,hop,fmax) in zip(ax,[(2048,16,6000),(512,8,10000)]):
    f,tt,S=sg.stft(m,sr,nperseg=nfft,noverlap=nfft-hop,padded=False)
    D=20*np.log10(np.abs(S)+1e-9); D-=D.max()
    a.pcolormesh(tt*1000,f,D,vmin=-60,vmax=0,cmap='magma',shading='auto'); a.set_ylim(0,fmax); a.set_xticks(np.arange(0,275,10)); a.set_title(f'nfft {nfft}')
    a.set_yticks(np.arange(0,fmax+1,500 if fmax<=6000 else 1000)); a.grid(alpha=.2,color='w')
plt.tight_layout(); plt.savefig('spec2.png',dpi=80)
