import numpy as np, soundfile as sf, scipy.signal as sg
x4, sr4 = sf.read('../x4.wav'); 
if x4.ndim>1: x4=x4.mean(1)
print('x4', len(x4)/sr4, 's, sr', sr4, 'peak', np.abs(x4).max())
w=int(0.01*sr4)
env=np.array([np.sqrt((x4[i:i+w]**2).mean()) for i in range(0,len(x4)-w,w)])
pk=env.max()
print('x4 env dB per 10ms:'); print(' '.join(f'{20*np.log10(e/pk+1e-9):.0f}' for e in env))
# resample clip to 48k and cross-correlate
ss, sr = sf.read('ss.wav'); ss=ss.mean(1)
ssr = sg.resample_poly(ss, 160, 147)
c = sg.correlate(x4, ssr, mode='valid')
c /= (np.sqrt(np.convolve(x4**2, np.ones(len(ssr)), 'valid'))*np.sqrt((ssr**2).sum())+1e-12)
pks,_ = sg.find_peaks(c, height=0.3, distance=int(0.2*sr4))
print('normalized xcorr peaks (s, r):', [(round(p/sr4,3), round(c[p],3)) for p in pks])
print('max r', c.max(), 'at', np.argmax(c)/sr4)
for f in ['../clue_b.wav','../ff.wav']:
    y,s=sf.read(f); y=y.mean(1); n=min(len(y),len(ss))
    print(f, 'corr with ss', np.corrcoef(y[:n], ss[:n])[0,1], 'peak', np.abs(y).max())
