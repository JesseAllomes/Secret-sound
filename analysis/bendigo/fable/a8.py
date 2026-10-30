import numpy as np, soundfile as sf, scipy.signal as sg
x, sr = sf.read('ss.wav'); m = x.mean(1); N=len(m)
strikes=[13.4,97.6,148.9,216.3,264.9]
print('=== impact click hardness: spectrum of first 1.5 ms after strike start')
for s in strikes:
    a=int(s/1000*sr); b=a+int(0.0015*sr); seg=m[a:b]*np.hanning(b-a); F=np.abs(np.fft.rfft(seg,4096))**2; fr=np.fft.rfftfreq(4096,1/sr)
    def E(lo,hi): return 10*np.log10(F[(fr>=lo)&(fr<hi)].sum()+1e-20)
    print(f'strike {s}: 1-4k {E(1000,4000):.1f}  4-8k {E(4000,8000):.1f}  8-16k {E(8000,16000):.1f}  -> (8-16k)-(1-4k) = {E(8000,16000)-E(1000,4000):.1f} dB')
print('=== compare: ring window 5-20ms after strike')
for s in strikes:
    a=int(s/1000*sr)+int(0.005*sr); b=min(N,a+int(0.015*sr)); seg=m[a:b]*np.hanning(b-a); F=np.abs(np.fft.rfft(seg,4096))**2; fr=np.fft.rfftfreq(4096,1/sr)
    def E(lo,hi): return 10*np.log10(F[(fr>=lo)&(fr<hi)].sum()+1e-20)
    print(f'strike {s}: (8-16k)-(1-4k) = {E(8000,16000)-E(1000,4000):.1f} dB')
print('=== narrowband tracks of candidate higher shell modes (dB per 5ms)')
for fc,bw in [(6050,250),(6500,250),(11630,300),(5020,200),(1583,100),(478,30),(597,30)]:
    sos=sg.butter(3,[fc-bw/2,fc+bw/2],btype='band',fs=sr,output='sos'); z=sg.sosfiltfilt(sos,m)
    e=np.sqrt(np.convolve(z**2,np.ones(221)/221,'same')); ed=20*np.log10(e+1e-7)
    print(f'{fc:5d}:', ' '.join(f'{ed[i]:.0f}' for i in range(110,N,221)))
# last 40 ms vs previous: check for fade-out
for a,b in [(200,235),(235,255),(255,273)]:
    seg=m[int(a/1000*sr):int(b/1000*sr)]; print(f'rms {a}-{b} ms: {20*np.log10(np.sqrt((seg**2).mean())):.1f} dBFS')
print('last 3 ms env (0.25ms):', ' '.join(f'{20*np.log10(np.sqrt((m[i:i+11]**2).mean())+1e-7):.0f}' for i in range(N-int(0.003*sr),N-11,11)))
# noise floor estimate: quietest 5 ms window
w=int(0.005*sr); r=np.array([np.sqrt((m[i:i+w]**2).mean()) for i in range(0,N-w,22)]); i=np.argmin(r); print(f'quietest 5ms window at {i*22/sr*1000:.0f} ms: {20*np.log10(r[i]):.1f} dBFS; loudest: {20*np.log10(r.max()):.1f}')
