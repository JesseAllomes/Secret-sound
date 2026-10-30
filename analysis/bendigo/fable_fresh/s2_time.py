"""Envelope, onsets, inter-onset intervals, envelope autocorrelation."""
import numpy as np, scipy.signal as ss, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x=np.load('mono.npy'); sr=44100; t=np.arange(len(x))/sr
# Hilbert envelope, smoothed 1 ms
env=np.abs(ss.hilbert(x)); k=int(0.001*sr); env_s=np.convolve(env,np.ones(k)/k,'same')
# fine-resolution RMS 0.5 ms hop
w=int(0.002*sr); h=int(0.0005*sr)
rms=np.array([np.sqrt(np.mean(x[i:i+w]**2)) for i in range(0,len(x)-w,h)]); trms=np.arange(len(rms))*h/sr+w/sr/2
# onset: high-passed signal energy jump (>1.5 kHz) with 0.25 ms hop
b,a=ss.butter(4,1500/(sr/2),'high'); xh=ss.filtfilt(b,a,x)
eh=np.abs(ss.hilbert(xh)); eh=np.convolve(eh,np.ones(int(0.0005*sr))/int(0.0005*sr),'same')
db=20*np.log10(eh+1e-6)
# derivative of dB envelope
dd=np.gradient(db)*sr/1000  # dB per ms
# peaks in dd with prominence
pk,pr=ss.find_peaks(dd,height=3,distance=int(0.004*sr))
print('candidate onsets (ms), dB/ms slope, level dB after:')
for p in pk:
    print(f'{p/sr*1000:7.2f}  slope {dd[p]:5.1f}  lvl {db[min(p+int(0.001*sr),len(db)-1)]:6.1f}  pre {db[max(p-int(0.001*sr),0)]:6.1f}')
# broadband onsets using plain envelope
pk2,_=ss.find_peaks(env_s,prominence=0.004,distance=int(0.005*sr))
print('envelope peaks (ms), amp:',[(round(p/sr*1000,1),round(env_s[p],4)) for p in pk2])
# autocorrelation of envelope
e=env_s-env_s.mean(); ac=np.correlate(e,e,'full')[len(e)-1:]; ac/=ac[0]
lagpk,_=ss.find_peaks(ac,distance=int(0.01*sr))
print('env autocorr peaks (ms, r):',[(round(l/sr*1000,1),round(ac[l],2)) for l in lagpk[:8]])
fig,ax=plt.subplots(4,1,figsize=(14,12),sharex=True)
ax[0].plot(t*1000,x,lw=.4); ax[0].set_ylabel('wave')
ax[1].plot(t*1000,20*np.log10(env_s+1e-6)); ax[1].plot(t*1000,db,alpha=.7); ax[1].set_ylabel('env dB (full, >1.5k)'); ax[1].set_ylim(-70,-15)
ax[2].plot(t*1000,dd); ax[2].set_ylabel('dB/ms (>1.5k)')
for p in pk: ax[2].axvline(p/sr*1000,c='r',alpha=.4)
b,a=ss.butter(4,300/(sr/2),'low'); xl=ss.filtfilt(b,a,x)
ax[3].plot(t*1000,xl); ax[3].set_ylabel('<300 Hz'); ax[3].set_xlabel('ms')
plt.tight_layout(); plt.savefig('fig_time.png',dpi=110)
np.save('onsets_ms.npy',pk/sr*1000)
