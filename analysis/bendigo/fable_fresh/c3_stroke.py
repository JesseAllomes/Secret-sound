"""Within each winding stroke of 27149: pair-start intervals vs click level (does loudness track speed?), double-click spacing."""
import numpy as np, scipy.signal as ss, librosa
sr=44100; y,_=librosa.load('/home/user/secret-sound/listening/full/27149_Grandfather-Clock-Winding.mp3',sr=sr,mono=True)
b,a=ss.butter(4,1500/(sr/2),'high'); yh=ss.filtfilt(b,a,y); e=np.abs(ss.hilbert(yh)); e=np.convolve(e,np.ones(18)/18,'same'); db=20*np.log10(e+1e-6)
pk,_=ss.find_peaks(db,height=-20,distance=int(0.004*sr)); t=pk/sr; lv=db[pk]
groups=np.split(np.arange(len(t)),np.where(np.diff(t)>0.15)[0]+1)
for g in groups:
    if len(g)<6: continue
    starts=[g[0]]; 
    for i in g[1:]:
        if t[i]-t[starts[-1]]>0.012: starts.append(i)
    print(f'stroke at {t[g[0]]:.2f}s: {len(starts)} pawl drops')
    iv=np.diff(t[starts])*1000
    print('  intervals ms:',' '.join(f'{v:.0f}' for v in iv))
    print('  levels dB  :',' '.join(f'{lv[i]:.0f}' for i in starts))
    dbl=[ (t[i+1]-t[i])*1000 for i in starts if i+1<len(t) and t[i+1]-t[i]<0.012]
    print('  double-click spacing ms:',' '.join(f'{v:.1f}' for v in dbl))
    # correlation level vs interval
    if len(iv)>4: print('  corr(level, following interval) =',np.corrcoef(lv[starts][:-1],iv)[0,1].round(2))
