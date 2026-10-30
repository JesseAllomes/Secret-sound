"""Decay (T60, Q) of candidate modes via narrow band-pass + log-envelope fit, per event."""
import numpy as np, scipy.signal as ss
x=np.load('mono.npy'); sr=44100; t=np.arange(len(x))/sr*1000
modes=[78.7,133,197,254,342,491,606,844,1141,1589,1791,2098,2226,2338,2461,2535,2575,2637,2744,3085,3366,3680,3758,3941,4065,4177,4233,4382,4442,4975,5054,6492,7526]
onsets=[12.2,92.8,146.3,216.2,263.9]
def bp(f,bw):
    sos=ss.butter(4,[max(f-bw/2,20),f+bw/2],'bandpass',fs=sr,output='sos'); return ss.sosfiltfilt(sos,x)
print('mode  BW | per-event: peak dB (rel clip max) ; decay dB/10ms ; T60 ms ; Q  (fit over 5-35ms after onset, before next onset)')
for f in modes:
    bw=max(40,f*0.03)
    y=bp(f,bw); e=np.abs(ss.hilbert(y)); db=20*np.log10(e+1e-7)
    line=f'{f:7.0f} {bw:4.0f} |'
    for i,o in enumerate(onsets):
        nxt=onsets[i+1] if i+1<len(onsets) else 273
        s=o+4; e_=min(o+40,nxt-3)
        if e_-s<10: line+='   (short)   |'; continue
        m=(t>=s)&(t<e_); 
        slope,icpt=np.polyfit(t[m],db[m],1)
        pk=db[(t>=o)&(t<o+6)].max()
        if slope<0:
            T60=-60/slope; Q=np.pi*f*T60/1000/np.log(1000)*np.log(1000)/np.log(1000)  # Q = pi f T60 / ln(1000)
            Q=np.pi*f*(T60/1000)/np.log(1000)
            line+=f' {pk:6.1f} {slope*10:6.1f} {T60:5.0f} {Q:5.0f}|'
        else: line+=f' {pk:6.1f}  (rise) |'
    print(line)
