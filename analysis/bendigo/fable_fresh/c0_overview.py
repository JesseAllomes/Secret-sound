"""Overview of a long recording: click train over the whole file (rate, intervals, levels), spectrogram figure."""
import sys, numpy as np, scipy.signal as ss, librosa, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
f=sys.argv[1]; tag=sys.argv[2]
y,sr=librosa.load(f,sr=44100,mono=True); t=np.arange(len(y))/sr
print(tag,'len s',len(y)/sr,'peak dBFS',20*np.log10(np.abs(y).max()),'rms',20*np.log10(np.sqrt(np.mean(y**2))))
b,a=ss.butter(4,1500/(sr/2),'high'); yh=ss.filtfilt(b,a,y)
e=np.abs(ss.hilbert(yh)); k=int(0.0004*sr); e=np.convolve(e,np.ones(k)/k,'same'); db=20*np.log10(e+1e-6)
n1=int(0.0015*sr); n3=int(0.003*sr)
# jump detector as for the clue
jump=np.zeros_like(db); mx=ss.order_filter if False else None
from scipy.ndimage import maximum_filter1d, minimum_filter1d
fut=maximum_filter1d(db,n1,origin=-(n1//2)); past=minimum_filter1d(db,n3,origin=n3//2-1)
jump=fut-past
pk,_=ss.find_peaks(jump,height=12,distance=int(0.006*sr))
lv=np.array([db[p:p+n1].max() for p in pk])
# keep main clicks: >= -40 dBFS... report distribution
print('clicks found',len(pk),'; level percentiles dB',np.percentile(lv,[10,50,90]).round(1))
main=pk[lv>np.percentile(lv,50)]
iv=np.diff(main)/sr*1000
print('main clicks',len(main),'median interval ms',np.median(iv).round(1),'IQR',np.percentile(iv,[25,75]).round(1))
# rate over time in 0.5 s bins
for s in np.arange(0,len(y)/sr,0.5):
    m=(main/sr>=s)&(main/sr<s+0.5); c=m.sum()
    rms=20*np.log10(np.sqrt(np.mean(y[int(s*sr):int((s+.5)*sr)]**2))+1e-9)
    print(f'  {s:4.1f}-{s+.5:4.1f}s: {c:3d} main clicks ({2*c:3d}/s), rms {rms:6.1f} dBFS')
np.save(f'{tag}_clicks.npy',main/sr*1000)
fig,ax=plt.subplots(2,1,figsize=(16,8),sharex=True)
ax[0].plot(t,y,lw=.3); ax[0].vlines(main/sr,-np.abs(y).max(),np.abs(y).max(),color='r',alpha=.2)
fr,tt,S=ss.stft(y,sr,nperseg=1024,noverlap=768); P=20*np.log10(np.abs(S)+1e-7)
ax[1].pcolormesh(tt,fr/1000,P,vmin=P.max()-80,vmax=P.max(),shading='auto',cmap='magma'); ax[1].set_ylim(0,10); ax[1].set_xlabel('s')
plt.tight_layout(); plt.savefig(f'fig_{tag}_overview.png',dpi=90)
