"""Basic facts: channels, levels, start/end amplitude, mp3 vs wav decode, DC, clipping."""
import numpy as np, soundfile as sf, librosa, sys
W='/home/user/secret-sound/clues/bendigo/clue_b.wav'
M='/home/user/secret-sound/clues/bendigo/bendigo_secret_sound_210926.mp3'
d,sr=sf.read(W); print('wav',d.shape,sr)
L,R=d[:,0],d[:,1]
print('L-R max abs diff',np.max(np.abs(L-R)),'corr',np.corrcoef(L,R)[0,1])
print('peak L',np.max(np.abs(L)),'peak R',np.max(np.abs(R)),'rms',np.sqrt(np.mean(L**2)))
print('DC',L.mean())
print('first 10 samples',L[:10])
print('last 10 samples',L[-10:])
# rms of first/last 5 ms
n=int(0.005*sr)
print('rms first 5ms',np.sqrt(np.mean(L[:n]**2)),'rms last 5ms',np.sqrt(np.mean(L[-n:]**2)))
# mp3 decode via librosa
m,msr=librosa.load(M,sr=None,mono=False); print('mp3',m.shape,msr)
mm=m[0] if m.ndim>1 else m
print('mp3 len',len(mm),len(mm)/msr)
# align
c=np.correlate(mm[:len(L)+2000],L,mode='valid'); lag=np.argmax(c); print('lag',lag,'peak corr',c[lag]/np.sqrt(np.sum(L**2)*np.sum(mm[lag:lag+len(L)]**2)))
# samples near clipping
print('n samples >0.95',np.sum(np.abs(L)>0.95),'>0.99',np.sum(np.abs(L)>0.99))
np.save('/home/user/secret-sound/analysis/bendigo/fable_fresh/mono.npy',(L+R)/2)
