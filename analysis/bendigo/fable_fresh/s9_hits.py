"""Per-hit: rise time, impact spectrum tilt (first 2.5 ms), 2.32k vs 2.55k excitation ratio, HF/ring ratio; floor between hits."""
import numpy as np, scipy.signal as ss
x=np.load('mono.npy'); sr=44100; t=np.arange(len(x))/sr*1000
hits=[('pre0',0.0),('E1',14.6),('E2',92.4),('E3',145.7),('E4',212.7),('E5',258.6)]
env=np.abs(ss.hilbert(x)); env=np.convolve(env,np.ones(9)/9,'same')
def bandlevel(seg,lo,hi):
    N=1<<14; A=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),N))**2; f=np.fft.rfftfreq(N,1/sr); m=(f>=lo)&(f<hi); return 10*np.log10(A[m].sum()+1e-14)
print('hit  onset  peak(dBFS)  10-90% rise(ms)  tilt: L(6-15k)-L(2-5k) first 2.5ms | tail 5-20ms  | 2.2-2.4k vs 2.5-2.65k (tail 4-20 ms) | 300-700 | 40-120')
for name,o in hits:
    i0=int(o/1000*sr); seg=env[i0:i0+int(0.004*sr)]; pk=seg.max(); ipk=np.argmax(seg)
    try:
        i10=np.where(seg[:ipk+1]>=0.1*pk)[0][0]; i90=np.where(seg[:ipk+1]>=0.9*pk)[0][0]; rise=(i90-i10)/sr*1000
    except: rise=float('nan')
    a=x[i0:i0+int(0.0025*sr)]; b=x[i0+int(0.005*sr):i0+int(0.02*sr)]; c=x[i0+int(0.004*sr):i0+int(0.02*sr)]
    tilt_a=bandlevel(a,6000,15000)-bandlevel(a,2000,5000); tilt_b=bandlevel(b,6000,15000)-bandlevel(b,2000,5000)
    r=bandlevel(c,2200,2420)-bandlevel(c,2480,2660)
    lf=bandlevel(c,300,700)-bandlevel(c,2000,5000); lf2=bandlevel(x[i0:i0+int(0.03*sr)],40,120)-bandlevel(x[i0:i0+int(0.03*sr)],2000,5000)
    print(f'{name:4s} {o:6.1f} {20*np.log10(pk):8.1f} {rise:8.2f}   {tilt_a:6.1f} | {tilt_b:6.1f}   | {r:6.1f}  | {lf:6.1f} | {lf2:6.1f}')
# floor between hits
N=1<<14; f=np.fft.rfftfreq(N,1/sr)
for s,e in [(182,200),(236,252),(76,90)]:
    seg=x[int(s/1000*sr):int(e/1000*sr)]; A=20*np.log10(np.abs(np.fft.rfft(seg*np.hanning(len(seg)),N))+1e-9)
    print(f'floor {s}-{e} ms: rms dBFS {20*np.log10(np.sqrt(np.mean(seg**2))):.1f}; band levels (rel 2-5k): ',
          ' '.join(f'{lo}-{hi}:{bandlevel(seg,lo,hi)-bandlevel(seg,2000,5000):.0f}' for lo,hi in [(40,120),(120,300),(300,700),(700,1500),(1500,2000),(5000,8000),(8000,15000)]))
# amplitude ratio sequence of main hits & intervals
print('main-hit peaks dBFS:',[round(20*np.log10(env[int(o/1000*sr):int(o/1000*sr)+150].max()),1) for _,o in hits])
