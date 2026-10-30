"""Low-frequency content, spectral flatness/noise, mp3 pre-echo check."""
import numpy as np, scipy.signal as ss, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x=np.load('mono.npy'); sr=44100; t=np.arange(len(x))/sr*1000
fig,ax=plt.subplots(5,1,figsize=(14,12),sharex=True)
for i,(lo,hi) in enumerate([(40,120),(120,300),(300,700),(700,1500),(1500,3000)]):
    sos=ss.butter(4,[lo,hi],'bandpass',fs=sr,output='sos'); y=ss.sosfiltfilt(sos,x)
    ax[i].plot(t,y,lw=.6); ax[i].set_ylabel(f'{lo}-{hi} Hz')
    e=np.abs(ss.hilbert(y)); pk,_=ss.find_peaks(e,prominence=e.max()*0.25,distance=int(0.008*sr))
    print(f'{lo}-{hi} Hz: peak env {e.max():.4f} at {t[np.argmax(e)]:.1f} ms; prominent bursts at',[round(t[p],1) for p in pk])
ax[-1].set_xlabel('ms'); plt.tight_layout(); plt.savefig('fig_bands.png',dpi=110)
# 40-120 Hz: zero-crossing period in the first 40 ms
sos=ss.butter(4,[40,120],'bandpass',fs=sr,output='sos'); y=ss.sosfiltfilt(sos,x)
zc=np.where(np.diff(np.sign(y[:int(0.05*sr)]))>0)[0]/sr*1000
print('LF positive zero crossings ms:',zc.round(1),'periods',np.diff(zc).round(1))
# spectral flatness per 5.8 ms frame (256) and per-frame centroid
f,tt,S=ss.stft(x,sr,nperseg=256,noverlap=192); P=np.abs(S)**2+1e-14
flat=np.exp(np.mean(np.log(P),0))/np.mean(P,0); cen=np.sum(f[:,None]*P,0)/np.sum(P,0)
print('frame ms, flatness, centroid Hz (every 3rd frame):')
for i in range(0,len(tt),3): print(f'{tt[i]*1000:6.1f} {flat[i]:.3f} {cen[i]:6.0f}')
# high band (8-16 kHz) envelope: impulsive clicks vs sustained hiss
sos=ss.butter(4,[8000,15500],'bandpass',fs=sr,output='sos'); y=ss.sosfiltfilt(sos,x); e=np.abs(ss.hilbert(y))
e=np.convolve(e,np.ones(22)/22,'same'); db=20*np.log10(e+1e-7)
pk,_=ss.find_peaks(db,prominence=8,distance=int(0.004*sr))
print('8-15.5k band peaks ms/dB:',[(round(t[p],1),round(db[p],1)) for p in pk])
print('8-15.5k band median dB',np.median(db).round(1),'min',db.min().round(1))
