import sys; sys.path.insert(0,'/home/user/secret-sound')
import numpy as np, librosa, steel_score as ss
SR=ss.SR
f,t0,t1=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
y,_=librosa.load(f,sr=SR,mono=True); y=y[int(t0*SR):int(t1*SR)]
hf=ss.band_env(y,2000,10000,1); lf=ss.band_env(y,40,120,3); mid=ss.band_env(y,600,1100,3); bb=np.convolve(np.abs(y),np.ones(48)/48,'same')
ref=[x.max() for x in (bb,hf,mid,lf)]
print(' ms   broad   HF   600-1100  LF40-120')
for i in range(0,len(y)-240,240):
    s=slice(i,i+240)
    print(f'{(i)/SR*1000:5.0f} '+' '.join(f'{ss.db(x[s].max()/r):6.1f}' for x,r in zip((bb,hf,mid,lf),ref)) + '  '+'#'*int(max(0,40+ss.db(bb[s].max()/ref[0]))/2))
