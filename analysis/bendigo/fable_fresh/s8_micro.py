"""Micro-structure: is the 7-14 ms sub-onset pattern real impacts or beating? HF impulse timeline, AM of ring band, phase continuity."""
import numpy as np, scipy.signal as ss, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x=np.load('mono.npy'); sr=44100; t=np.arange(len(x))/sr*1000
# (a) HF 6-15.5k impulses at 0.1 ms smoothing, list >8 dB above local floor
sos=ss.butter(4,[6000,15500],'bandpass',fs=sr,output='sos'); yh=ss.sosfiltfilt(sos,x)
eh=np.abs(ss.hilbert(yh)); eh=np.convolve(eh,np.ones(5)/5,'same'); dbh=20*np.log10(eh+1e-7)
floor=ss.medfilt(dbh,int(0.01*sr)|1)
pk,_=ss.find_peaks(dbh-floor,height=8,distance=int(0.002*sr))
print('HF (6-15.5k) impulses ms (level dB, above floor):')
print(' '.join(f'{t[p]:.1f}({dbh[p]:.0f},+{dbh[p]-floor[p]:.0f})' for p in pk))
# (b) AM of the 2.2-2.7k band: envelope spectrum (modulation frequency)
sos=ss.butter(4,[2200,2700],'bandpass',fs=sr,output='sos'); yr=ss.sosfiltfilt(sos,x); er=np.abs(ss.hilbert(yr))
for s,e in [(14,90),(94,144),(148,212)]:
    seg=er[int(s/1000*sr):int(e/1000*sr)]; seg=seg-seg.mean(); seg*=np.hanning(len(seg))
    M=np.abs(np.fft.rfft(seg,1<<15)); fm=np.fft.rfftfreq(1<<15,1/sr); m=(fm>20)&(fm<400)
    pkm,_=ss.find_peaks(M[m],prominence=M[m].max()*.2); print(f'ring-band AM {s}-{e} ms: modulation peaks Hz',[round(fm[m][p],0) for p in pkm][:6])
# (c) phase continuity of the 2575 line: demodulate, look at phase jumps
f0=2575; z=x*np.exp(-2j*np.pi*f0*t/1000); sos=ss.butter(4,25,'low',fs=sr,output='sos'); z=ss.sosfiltfilt(sos,z)
ph=np.unwrap(np.angle(z)); inst=np.gradient(ph)/(2*np.pi)*sr+f0
print('2575-line instantaneous freq (Hz) & amp dB at 5 ms steps:')
for ms in range(2,272,5):
    i=int(ms/1000*sr); print(f'{ms:4d} {inst[i]:7.0f} {20*np.log10(abs(z[i])+1e-7):6.1f}',end=' |')
print()
# (d) zoom figures
fig,ax=plt.subplots(3,1,figsize=(14,10))
m=(t<60); ax[0].plot(t[m],x[m],lw=.5); ax[0].plot(t[m],yh[m]*3,lw=.5,alpha=.6); ax[0].set_title('0-60 ms: wave (blue), 6-15.5k x3 (orange)')
m=(t>88)&(t<145); ax[1].plot(t[m],x[m],lw=.5); ax[1].plot(t[m],yh[m]*3,lw=.5,alpha=.6); ax[1].set_title('88-145 ms')
m=(t>143)&(t<215); ax[2].plot(t[m],x[m],lw=.5); ax[2].plot(t[m],yh[m]*3,lw=.5,alpha=.6); ax[2].set_title('143-215 ms'); ax[2].set_xlabel('ms')
plt.tight_layout(); plt.savefig('fig_zoom.png',dpi=110)
