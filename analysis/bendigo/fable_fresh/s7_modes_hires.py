"""High-resolution mode lines from clean ring tails; stability across events."""
import numpy as np, scipy.signal as ss
x=np.load('mono.npy'); sr=44100
N=1<<17; fr=np.fft.rfftfreq(N,1/sr)
def peaks(s,e,lo=1500,hi=8000,thr=-28):
    seg=x[int(s/1000*sr):int(e/1000*sr)]; seg=seg*np.hanning(len(seg))
    A=20*np.log10(np.abs(np.fft.rfft(seg,N))+1e-9); m=(fr>=lo)&(fr<=hi); A=A-A[m].max()
    pk,pr=ss.find_peaks(np.where(m,A,-200),height=thr,prominence=4)
    return [(round(fr[p],0),round(A[p],1)) for p in pk]
for s,e in [(18,88),(40,90),(96,142),(150,210),(218,256),(96,210)]:
    print(f'tail {s}-{e} ms (res {1000/(e-s):.0f} Hz) 1.5-8k:',peaks(s,e))
print('low band 50-1500 Hz, tail 18-88:',peaks(18,88,50,1500,-30))
print('low band 50-1500 Hz, tail 96-210:',peaks(96,210,50,1500,-30))
print('low band 0-60 ms (incl thump):',peaks(0,60,40,1500,-30))
