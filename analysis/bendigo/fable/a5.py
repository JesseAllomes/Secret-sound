import numpy as np, soundfile as sf, scipy.signal as sg
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x, sr = sf.read('ss.wav'); m = x.mean(1); N=len(m); t=np.arange(N)/sr*1000
hp = sg.sosfiltfilt(sg.butter(4,1000,btype='high',fs=sr,output='sos'), m)
env = np.abs(sg.hilbert(hp)); env = sg.sosfiltfilt(sg.butter(2,400,fs=sr,output='sos'), env)
# modulation spectrum of envelope (whole clip, and per segment)
def modspec(e, label):
    e=e-e.mean(); e*=np.hanning(len(e)); F=np.abs(np.fft.rfft(e, 1<<16)); fr=np.fft.rfftfreq(1<<16,1/sr)
    sel=(fr>5)&(fr<400); Fd=20*np.log10(F[sel]/F[sel].max()+1e-9)
    pk,_=sg.find_peaks(Fd,prominence=3); top=sorted(pk,key=lambda i:-Fd[i])[:8]
    print(label,'modulation peaks (Hz,dB):',[(round(fr[sel][i],1),round(Fd[i],1)) for i in top])
modspec(env.copy(),'whole')
modspec(env[:int(0.09*sr)].copy(),'0-90ms')
modspec(env[int(0.09*sr):int(0.18*sr)].copy(),'90-180ms')
modspec(env[int(0.18*sr):].copy(),'180-273ms')
# fine autocorr of envelope
e=env-env.mean(); ac=sg.correlate(e,e,'full')[N-1:]; ac/=ac[0]; lag=np.arange(N)/sr*1000
pk,_=sg.find_peaks(ac[:int(0.06*sr)],prominence=0.03)
print('fine env autocorr peaks <60ms:',[(round(lag[p],2),round(ac[p],2)) for p in pk])
# also raw-signal autocorrelation low band for pitch
y=sg.sosfiltfilt(sg.butter(4,[40,300],btype='band',fs=sr,output='sos'),m)
ac2=sg.correlate(y,y,'full')[N-1:]; ac2/=ac2[0]
pk2,_=sg.find_peaks(ac2[int(0.003*sr):int(0.03*sr)],prominence=0.05)
print('LF signal autocorr peaks:',[(round(lag[p+int(0.003*sr)],2),round(ac2[p+int(0.003*sr)],2)) for p in pk2])
fig,ax=plt.subplots(3,1,figsize=(14,9))
ax[0].plot(t,hp,lw=0.5); ax[0].plot(t,env,'r',lw=1); ax[0].set_xticks(np.arange(0,275,10)); ax[0].grid(alpha=.3); ax[0].set_title('>1kHz signal + envelope')
ax[1].plot(lag[:int(0.1*sr)],ac[:int(0.1*sr)]); ax[1].set_title('envelope autocorr'); ax[1].grid(alpha=.3); ax[1].set_xticks(np.arange(0,100,5))
ax[2].plot(t,y,lw=0.7); ax[2].set_title('40-300 Hz band'); ax[2].set_xticks(np.arange(0,275,10)); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig('env.png',dpi=80)
