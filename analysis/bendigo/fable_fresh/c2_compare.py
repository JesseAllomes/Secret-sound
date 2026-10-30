"""Clue vs clock windows: 1/3-octave long-term spectra, centroids, strongest sustained ring, click-pair statistics."""
import numpy as np, scipy.signal as ss, librosa, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D='/home/user/secret-sound/listening/full/'
srcs={'clue':('/home/user/secret-sound/clues/bendigo/clue_b.wav',0,0.273),
      '27149@4.19':(D+'27149_Grandfather-Clock-Winding.mp3',4.19,0.273),
      '27149@4.0-5.2':(D+'27149_Grandfather-Clock-Winding.mp3',4.0,1.2),
      '805328@2.0':(D+'805328_CLOCKMech-Samsung-Galaxy-Smartphone-CU-Grandfather.mp3',2.0,0.273),
      '805328@0-3.5':(D+'805328_CLOCKMech-Samsung-Galaxy-Smartphone-CU-Grandfather.mp3',0.0,3.5)}
sr=44100; edges=1000*2**(np.arange(-14,14)/3)  # 1/3 oct from 39 Hz
edges=edges[edges<16000]
fig,ax=plt.subplots(figsize=(14,6))
for name,(f,s,d) in srcs.items():
    x,_=librosa.load(f,sr=sr,mono=True,offset=s,duration=d)
    N=1<<18; X=np.abs(np.fft.rfft(x*np.hanning(len(x)),N))**2; fr=np.fft.rfftfreq(N,1/sr)
    tot=X[(fr>40)&(fr<8000)].sum()
    bands=[10*np.log10(X[(fr>=lo)&(fr<hi)].sum()/tot+1e-12) for lo,hi in zip(edges[:-1],edges[1:])]
    cen=lambda lo,hi: (lambda m: np.sum(fr[m]*X[m])/np.sum(X[m]))((fr>=lo)&(fr<hi))
    A=10*np.log10(X+1e-20); m=(fr>400)&(fr<8000); pk,_=ss.find_peaks(np.where(m,A,-300),prominence=8,distance=int(30/(sr/N))); o=np.argsort(-A[pk])[:6]
    print(f'{name:14s} centroid 40-8k: {cen(40,8000):5.0f} Hz | 1-8k: {cen(1000,8000):5.0f} | strongest lines 0.4-8k: '+' '.join(f'{fr[pk[i]]:.0f}({A[pk[i]]-A[pk].max():.0f})' for i in o))
    print('   1/3-oct (dB rel 40-8k total) from 39 Hz:',' '.join(f'{b:.0f}' for b in bands))
    ax.plot(np.sqrt(edges[:-1]*edges[1:]),bands,marker='o',label=name)
ax.set_xscale('log'); ax.set_xlabel('Hz'); ax.set_ylabel('dB rel total 40-8k'); ax.legend(); ax.grid(True,which='both',alpha=.3); ax.set_ylim(-45,0)
plt.tight_layout(); plt.savefig('fig_clock_thirdoct.png',dpi=100)
# click pair statistics on 27149 whole file: loud clicks (>-12 dBFS in >1.5k env), their intervals
y,_=librosa.load(D+'27149_Grandfather-Clock-Winding.mp3',sr=sr,mono=True)
b,a=ss.butter(4,1500/(sr/2),'high'); yh=ss.filtfilt(b,a,y); e=np.abs(ss.hilbert(yh)); e=np.convolve(e,np.ones(18)/18,'same'); db=20*np.log10(e+1e-6)
pk,_=ss.find_peaks(db,height=-14,distance=int(0.004*sr)); t=pk/sr
iv=np.diff(t)*1000
print('27149 loud clicks (>-14 dB in >1.5k env):',len(pk))
h,edg=np.histogram(iv,bins=[0,4,6,8,10,12,15,20,30,40,50,60,80,100,150,300,1000]); print('interval histogram ms:',list(zip(edg[:-1].astype(int),h)))
# stroke structure: group clicks into strokes separated by >150 ms
groups=np.split(t,np.where(np.diff(t)>0.15)[0]+1)
print('strokes (start s, n loud clicks, duration ms, mean interval between pair-starts):')
for g in groups:
    if len(g)<3: continue
    # pair-merge: clicks within 12 ms of previous are same pair
    starts=[g[0]]+[g[i] for i in range(1,len(g)) if g[i]-g[i-1]>0.012]
    print(f'  {g[0]:5.2f}s n={len(g):3d} dur={1000*(g[-1]-g[0]):4.0f} pairs={len(starts)} pair-interval={1000*np.mean(np.diff(starts)) if len(starts)>1 else 0:5.1f} ms  ({len(starts)/(g[-1]-g[0]+0.05):4.1f}/s)')
