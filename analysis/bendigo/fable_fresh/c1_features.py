"""Same feature set as the clue analysis, on any file window: onsets/intervals, chatter, ring lines+T60, LF, tilt, floor."""
import sys, numpy as np, scipy.signal as ss, librosa
from scipy.ndimage import maximum_filter1d, minimum_filter1d
f=sys.argv[1]; start=float(sys.argv[2]); dur=float(sys.argv[3]) if len(sys.argv)>3 else 0.273; tag=sys.argv[4] if len(sys.argv)>4 else 'win'
y,sr=librosa.load(f,sr=44100,mono=True,offset=start,duration=dur); x=y; t=np.arange(len(x))/sr*1000
print(f'== {tag}: {f.split("/")[-1]} @ {start:.3f}s, {len(x)/sr*1000:.0f} ms, peak {20*np.log10(np.abs(x).max()):.1f} dBFS')
# onsets
b,a=ss.butter(4,1500/(sr/2),'high'); xh=ss.filtfilt(b,a,x)
eh=np.abs(ss.hilbert(xh)); k=int(0.0004*sr); eh=np.convolve(eh,np.ones(k)/k,'same'); db=20*np.log10(eh+1e-6)
n1=int(0.0015*sr); n3=int(0.003*sr)
jump=maximum_filter1d(db,n1,origin=-(n1//2))-minimum_filter1d(db,n3,origin=n3//2-1)
pk,_=ss.find_peaks(jump,height=9,distance=int(0.006*sr))
env=np.abs(ss.hilbert(x)); env=np.convolve(env,np.ones(9)/9,'same')
rows=[]
for p in pk: rows.append((t[p],jump[p],db[p:p+n1].max(),db[max(p-n3,0):p].min()))
print('onsets (ms): jump, peak>1.5k dB, floor before')
for r in rows: print(f'  {r[0]:6.1f} +{r[1]:4.1f} {r[2]:6.1f} {r[3]:6.1f}')
# main hits = jumps >= 15 dB or peak within 12 dB of max
mx=max(r[2] for r in rows) if rows else 0
main=[r for r in rows if r[1]>=15 or r[2]>=mx-10]
on=np.array([r[0] for r in main]); print('MAIN onsets ms',on.round(1),' intervals',np.diff(on).round(1))
# chatter: HF impulses
sos=ss.butter(4,[6000,15500],'bandpass',fs=sr,output='sos'); yh=ss.sosfiltfilt(sos,x); e=np.abs(ss.hilbert(yh)); e=np.convolve(e,np.ones(5)/5,'same'); dbh=20*np.log10(e+1e-7)
fl=ss.medfilt(dbh,int(0.01*sr)|1); p2,_=ss.find_peaks(dbh-fl,height=8,distance=int(0.002*sr))
print('HF impulses ms:',' '.join(f'{t[p]:.1f}({dbh[p]:.0f})' for p in p2))
# spectrum peaks whole window
N=1<<16; fr=np.fft.rfftfreq(N,1/sr); X=np.fft.rfft(x*np.hanning(len(x)),N); A=20*np.log10(np.abs(X)+1e-9); A-=A.max()
pk3,pr=ss.find_peaks(A,height=-30,prominence=6,distance=int(40/(sr/N))); o=np.argsort(-A[pk3])[:25]
print('whole-window peaks Hz(dB):',' '.join(f'{fr[pk3[i]]:.0f}({A[pk3[i]]:.0f})' for i in o))
def bl(lo,hi): m=(fr>=lo)&(fr<hi); return 10*np.log10(np.sum(np.abs(X[m])**2)+1e-12)
tot=10*np.log10(np.sum(np.abs(X)**2))
print('band energy rel total:',' '.join(f'{lo}-{hi}:{bl(lo,hi)-tot:.1f}' for lo,hi in [(0,100),(100,200),(200,400),(400,800),(800,1500),(1500,2000),(2000,3000),(3000,5000),(5000,8000),(8000,12000),(12000,16000)]))
# tails after each main hit: lines 1.5-8k and decay of top 4 lines
for i,o_ in enumerate(on):
    nxt=on[i+1] if i+1<len(on) else t[-1]
    s=o_+4; e_=min(o_+60,nxt-2)
    if e_-s<15: continue
    seg=x[int(s/1000*sr):int(e_/1000*sr)]; seg=seg*np.hanning(len(seg)); A2=20*np.log10(np.abs(np.fft.rfft(seg,N))+1e-9)
    m=(fr>=1000)&(fr<=9000); A2=A2-A2[m].max(); pk4,_=ss.find_peaks(np.where(m,A2,-200),height=-15,prominence=5,distance=int(60/(sr/N)))
    o2=np.argsort(-A2[pk4])[:10]
    line=f'tail {s:.0f}-{e_:.0f}: '+' '.join(f'{fr[pk4[j]]:.0f}({A2[pk4[j]]:.0f})' for j in o2)
    # decay of the top 3 lines
    dec=[]
    for j in o2[:3]:
        f0=fr[pk4[j]]; bw=max(40,f0*0.03); sos=ss.butter(4,[f0-bw/2,f0+bw/2],'bandpass',fs=sr,output='sos'); yb=ss.sosfiltfilt(sos,x)
        dbb=20*np.log10(np.abs(ss.hilbert(yb))+1e-7); mm=(t>=s)&(t<e_); sl=np.polyfit(t[mm],dbb[mm],1)[0]
        dec.append(f'{f0:.0f}:T60={-60/sl:.0f}ms' if sl<0 else f'{f0:.0f}:rise')
    print(line,' | ',' '.join(dec))
# low band lines and LF/ring ratio per hit, tilt per hit
def bl2(seg,lo,hi):
    Nn=1<<14; AA=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),Nn))**2; ff=np.fft.rfftfreq(Nn,1/sr); m=(ff>=lo)&(ff<hi); return 10*np.log10(AA[m].sum()+1e-14)
print('per main hit: peak dBFS | tilt first2.5ms (6-15k minus 2-5k) | 40-120 rel 2-5k (30ms) | 300-700 rel 2-5k')
for o_ in on:
    i0=int(o_/1000*sr); a=x[i0:i0+int(0.0025*sr)]; c=x[i0:i0+int(0.03*sr)]
    if len(c)<int(0.02*sr): continue
    print(f'  {o_:6.1f} {20*np.log10(env[i0:i0+150].max()):6.1f} | {bl2(a,6000,15000)-bl2(a,2000,5000):6.1f} | {bl2(c,40,120)-bl2(c,2000,5000):6.1f} | {bl2(c,300,700)-bl2(c,2000,5000):6.1f}')
seg=x[:int(0.06*sr)]; pk5,_=ss.find_peaks(A,height=-30,prominence=6); lowp=[(round(fr[p]),round(A[p])) for p in pk5 if fr[p]<1500][:12]
print('low lines <1.5k whole window:',lowp)
# floor: quietest 15 ms
w=int(0.015*sr); r=np.array([np.sqrt(np.mean(x[i:i+w]**2)) for i in range(0,len(x)-w,w//3)]); print(f'quietest 15 ms rms {20*np.log10(r.min()+1e-9):.1f} dBFS, loudest {20*np.log10(r.max()):.1f}')
