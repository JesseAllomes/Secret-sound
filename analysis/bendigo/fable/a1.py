import numpy as np, soundfile as sf, scipy.signal as sg
x, sr = sf.read('ss.wav')
print('shape', x.shape, 'sr', sr, 'dur', x.shape[0]/sr)
L, R = x[:,0], x[:,1]
m = x.mean(1)
print('peak L R', np.abs(L).max(), np.abs(R).max(), 'rms L R', np.sqrt((L**2).mean()), np.sqrt((R**2).mean()))
print('LR corr', np.corrcoef(L,R)[0,1], 'side rms', np.sqrt(((L-R)**2).mean()))
# leading/trailing digital silence?
nz = np.nonzero(np.abs(m) > 1e-5)[0]
print('first nonzero sample', nz[0], 'last', nz[-1], 'of', len(m))
# envelope in 1 ms frames
w = int(0.001*sr)
env = np.array([np.sqrt((m[i:i+w]**2).mean()) for i in range(0, len(m)-w, w)])
pk = env.max()
print('env dB per ms:')
print(' '.join(f'{20*np.log10(e/pk+1e-9):.0f}' for e in env))
# peak sample
ip = np.argmax(np.abs(m)); print('peak sample at', ip/sr*1000, 'ms')
# onset detection: half-wave rectified diff of 0.5ms env
w2 = int(0.0005*sr)
env2 = np.array([np.sqrt((m[i:i+w2]**2).mean()) for i in range(0, len(m)-w2, w2//2)])
d = np.diff(20*np.log10(env2+1e-6))
idx = np.where(d>6)[0]
print('onset candidates (ms):', [round(i*w2/2/sr*1000,1) for i in idx])
