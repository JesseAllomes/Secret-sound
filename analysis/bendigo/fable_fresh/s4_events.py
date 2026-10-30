"""Refined onset list (level jump criterion) and per-event short spectra."""
import numpy as np, scipy.signal as ss
x=np.load('mono.npy'); sr=44100
b,a=ss.butter(4,1500/(sr/2),'high'); xh=ss.filtfilt(b,a,x)
eh=np.abs(ss.hilbert(xh)); k=int(0.0004*sr); eh=np.convolve(eh,np.ones(k)/k,'same'); db=20*np.log10(eh+1e-6)
# jump: max over next 1.5 ms minus min over previous 3 ms
n1=int(0.0015*sr); n3=int(0.003*sr); jump=np.zeros_like(db)
for i in range(n3,len(db)-n1): jump[i]=db[i:i+n1].max()-db[i-n3:i].min()
pk,_=ss.find_peaks(jump,height=9,distance=int(0.006*sr))
print('onsets by >9 dB jump (ms): jump dB, peak level after, floor before')
ev=[]
for p in pk:
    lvl=db[p:p+n1].max(); pre=db[p-n3:p].min(); print(f'{p/sr*1000:7.2f}  +{jump[p]:4.1f}  peak {lvl:6.1f}  pre {pre:6.1f}'); ev.append(p/sr*1000)
ev=np.array(ev); print('intervals',np.diff(ev).round(1))
# full-band version for the first event
eb=np.abs(ss.hilbert(x)); eb=np.convolve(eb,np.ones(k)/k,'same'); dbb=20*np.log10(eb+1e-6)
print('full-band env dB at 0,2,5,8,10,12,14,16,20 ms:',[round(dbb[int(m/1000*sr)],1) for m in [0,2,5,8,10,12,14,16,20]])
# per-event spectra: 12 ms hann window starting at onset, zero padded; list peaks
N=1<<15; fr=np.fft.rfftfreq(N,1/sr)
wins=[(0,12,'pre-0 tail (0-12ms)'),(12,40,'E1 12-40ms'),(40,90,'E1 tail 40-90'),(92,130,'E2 92-130'),(130,145,'E2 tail'),(146,185,'E3 146-185'),(185,214,'E3 tail'),(216,250,'E4 216-250'),(263,273,'E5 263-end')]
for s,e,name in wins:
    seg=x[int(s/1000*sr):int(e/1000*sr)]; seg=seg*np.hanning(len(seg))
    A=20*np.log10(np.abs(np.fft.rfft(seg,N))+1e-9); A-=A.max()
    pk2,pr=ss.find_peaks(A,height=-30,prominence=5,distance=int(60/(sr/N)))
    o=np.argsort(-A[pk2])[:14]
    print(name,':',' '.join(f'{fr[pk2[i]]:.0f}({A[pk2[i]]:.0f})' for i in o))
