import numpy as np, soundfile as sf, scipy.signal as sg
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
x, sr = sf.read('ss.wav'); m = x.mean(1); N=len(m); t=np.arange(N)/sr*1000
def bp(lo,hi,order=4):
    sos=sg.butter(order,[lo,hi],btype='band',fs=sr,output='sos'); return sg.sosfiltfilt(sos,m)
def envdb(y, w_ms=0.25):
    w=max(1,int(w_ms/1000*sr)); e=np.sqrt(np.convolve(y**2,np.ones(w)/w,'same')); return 20*np.log10(e+1e-7)
# 1. onsets from high-passed signal
hp = sg.sosfiltfilt(sg.butter(4,800,btype='high',fs=sr,output='sos'), m)
e = envdb(hp, 0.5)
# smooth and detect rises >8 dB within 2ms relative to preceding 5 ms min
ons=[]
for i in range(int(0.005*sr), N):
    prev=e[i-int(0.005*sr):i-int(0.001*sr)].min()
    if e[i]-prev>9 and (not ons or i-ons[-1]>int(0.012*sr)):
        ons.append(i)
print('HP onsets (ms):', [round(o/sr*1000,1) for o in ons])
print('intervals (ms):', [round((b-a)/sr*1000,1) for a,b in zip(ons,ons[1:])])
# per-onset: peak level in following 15 ms, rise time 10-90%, local 'decay' to -10 dB
for o in ons:
    seg=np.abs(hp[o:o+int(0.03*sr)]); pk=seg.max(); ip=np.argmax(seg)
    ee=e[o-int(0.002*sr):o+int(0.04*sr)]; emax=ee.max(); imax=np.argmax(ee)
    # time from peak to -10dB and -20dB
    def tdown(db):
        j=np.where(ee[imax:]<emax-db)[0]; return round(j[0]/sr*1000,1) if len(j) else None
    print(f'onset {o/sr*1000:6.1f} ms: HP peak {20*np.log10(pk):6.1f} dBFS at +{ip/sr*1000:4.1f} ms, t-10dB {tdown(10)} ms, t-20dB {tdown(20)} ms')
# 2. full-band 0.25ms envelope around onsets to view attack
fig,axs=plt.subplots(len(ons),1,figsize=(12,2.2*len(ons)))
for a,o in zip(axs,ons):
    s0=max(0,o-int(0.004*sr)); s1=min(N,o+int(0.025*sr))
    a.plot(t[s0:s1],m[s0:s1],lw=0.6); a.axvline(o/sr*1000,color='r',lw=0.5); a.set_title(f'onset {o/sr*1000:.1f} ms full-band'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig('onsets.png',dpi=80)
# 3. band envelopes
fig,axs=plt.subplots(7,1,figsize=(14,16),sharex=True)
bands=[(40,160),(160,400),(400,560),(560,1200),(1200,2100),(2100,2800),(2800,5000)]
for a,(lo,hi) in zip(axs,bands):
    y=bp(lo,hi); a.plot(t,envdb(y,1.0),lw=0.8); a.set_ylabel(f'{lo}-{hi}'); a.grid(alpha=.3); a.set_ylim(-75,-20)
    for o in ons: a.axvline(o/sr*1000,color='r',lw=0.4)
axs[-1].set_xticks(np.arange(0,275,10)); plt.tight_layout(); plt.savefig('bands.png',dpi=80)
# 4. decay fit of 2.1-2.8k and 3.5-4.5k and 400-560 after each onset: fit slope over 3..20ms after peak
for lo,hi in [(400,560),(2100,2800),(3500,4500),(5500,7500)]:
    y=bp(lo,hi); ed=envdb(y,1.0)
    out=[]
    for o in ons:
        seg=ed[o:o+int(0.045*sr)]; ip=np.argmax(seg[:int(0.01*sr)])
        a0=ip+int(0.002*sr); a1=min(len(seg), ip+int(0.03*sr))
        # stop fit at next onset
        nxt=[p for p in ons if p>o]
        if nxt: a1=min(a1, nxt[0]-o-int(0.002*sr))
        if a1-a0<int(0.006*sr): out.append('n/a'); continue
        tt=np.arange(a0,a1)/sr*1000; p=np.polyfit(tt,seg[a0:a1],1)
        slope=p[0]  # dB/ms
        t60=60/(-slope) if slope<0 else float('inf')
        fc=np.sqrt(lo*hi); Q=np.pi*fc*(t60/1000)/6.91 if slope<0 else float('inf')
        out.append(f'{slope:5.2f} dB/ms (T60 {t60:5.0f} ms, Q~{Q:4.0f})')
    print(f'band {lo}-{hi}:', ' | '.join(out))
# 5. low-frequency
y=bp(40,200); f,Pl=sg.welch(y,sr,nperseg=4096); sel=(f<400)
print('LF spectrum peaks:', [(round(f[i]),round(10*np.log10(Pl[i]/Pl[sel].max()),1)) for i in sg.find_peaks(10*np.log10(Pl[sel]+1e-20),prominence=6)[0]])
an=sg.hilbert(y); inst=np.diff(np.unwrap(np.angle(an)))/(2*np.pi)*sr
print('LF inst freq per 10ms (Hz):', ' '.join(f'{np.median(inst[i:i+441]):.0f}' for i in range(0,N-441,441)))
print('LF env dB per 10ms:', ' '.join(f'{envdb(y,10)[i]:.0f}' for i in range(0,N,441)))
# 6. inter-burst noise spectra vs burst spectra
def spec(s0,s1):
    f,P=sg.welch(m[int(s0/1000*sr):int(s1/1000*sr)],sr,nperseg=512); return f,10*np.log10(P+1e-20)
f,Pb=spec(92,112); f,Pg=spec(60,88); f,Pg2=spec(175,210); f,Pb2=spec(145,165)
for lo,hi in [(0,300),(300,700),(700,1500),(1500,3000),(3000,5000),(5000,8000),(8000,12000),(12000,16000)]:
    sel=(f>=lo)&(f<hi)
    print(f'{lo:5d}-{hi:5d} Hz: burst@92 {Pb[sel].mean():6.1f}  gap60-88 {Pg[sel].mean():6.1f}  burst@145 {Pb2[sel].mean():6.1f}  gap175-210 {Pg2[sel].mean():6.1f} dB')
# 7. envelope autocorrelation
ef=10**(envdb(hp,1.0)/20); ef=ef-ef.mean(); ac=sg.correlate(ef,ef,'full')[N-1:]; ac/=ac[0]
lag=np.arange(N)/sr*1000
pk,_=sg.find_peaks(ac[int(0.01*sr):int(0.15*sr)],prominence=0.05)
print('env autocorr peaks (ms, r):', [(round(lag[p+int(0.01*sr)],1), round(ac[p+int(0.01*sr)],2)) for p in pk])
# 8. first 2 ms: is it a decaying tail or an attack?
print('first 3 ms envelope (0.25ms steps):', ' '.join(f'{v:.0f}' for v in envdb(m,0.25)[:int(0.003*sr):11]))
print('spectral flatness overall', np.exp(np.mean(np.log(np.abs(np.fft.rfft(m))**2+1e-12)))/np.mean(np.abs(np.fft.rfft(m))**2))
