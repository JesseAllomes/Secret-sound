import numpy as np, soundfile as sf, scipy.signal as sg
x, sr = sf.read('ss.wav'); m = x.mean(1); N=len(m); t=np.arange(N)/sr*1000
# precise strike times from 2.8-6k band: first crossing of 25% of local peak amplitude
y=sg.sosfiltfilt(sg.butter(4,[2800,6000],btype='band',fs=sr,output='sos'),m)
e=np.abs(sg.hilbert(y))
groups=[(5,60),(85,140),(140,205),(205,250),(250,273)]
st=[]
for a,b in groups:
    ia,ib=int(a/1000*sr),int(b/1000*sr); seg=e[ia:ib]; ip=np.argmax(seg); pk=seg[ip]
    j=ip
    while j>0 and seg[j]>0.2*pk: j-=1
    st.append((ia+j)/sr*1000); 
    # rise 10-90
    k10=j
    while k10<ip and seg[k10]<0.1*pk: k10+=1
    k90=k10
    while k90<ip and seg[k90]<0.9*pk: k90+=1
    print(f'strike start {(ia+j)/sr*1000:6.1f} ms, peak {20*np.log10(pk):6.1f} dB at {(ia+ip)/sr*1000:6.1f}, rise10-90 {(k90-k10)/sr*1000:.2f} ms')
print('strike times', [round(s,1) for s in st], 'intervals', [round(b-a,1) for a,b in zip(st,st[1:])])
# high-res modal analysis in windows after strikes: fit via FFT zero-pad, report freqs, and decay via narrow band
def modes(a,b,lo,hi,n=8,prom=6):
    ia,ib=int(a/1000*sr),int(b/1000*sr); seg=m[ia:ib]*np.hanning(ib-ia)
    F=np.abs(np.fft.rfft(seg,1<<16)); fr=np.fft.rfftfreq(1<<16,1/sr); Fd=20*np.log10(F+1e-9)
    sel=(fr>lo)&(fr<hi); Fd=Fd[sel]-Fd[sel].max(); fr=fr[sel]
    pk,_=sg.find_peaks(Fd,prominence=prom); pk=sorted(pk,key=lambda p:-Fd[p])[:n]
    return [(round(fr[p]),round(Fd[p])) for p in pk]
print('modes 97-135ms 1.5-6k:', modes(97,135,1500,6000))
print('modes 150-200ms 1.5-6k:', modes(150,200,1500,6000))
print('modes 15-80ms 1.5-6k:', modes(15,80,1500,6000))
print('modes 215-250 1.5-6k:', modes(215,250,1500,6000))
print('modes 10-80ms 100-1000:', modes(10,80,100,1000))
print('modes 95-140ms 100-1000:', modes(95,140,100,1000))
print('modes 150-210ms 100-1000:', modes(150,210,100,1000))
# instantaneous frequency of 474 line & 2.4k lines
for fc,bw,a,b in [(474,30,10,85),(2562,60,95,140),(2330,60,95,140),(2562,60,15,80),(4350,150,146,200)]:
    sos=sg.butter(3,[fc-bw/2,fc+bw/2],btype='band',fs=sr,output='sos'); z=sg.sosfiltfilt(sos,m)
    an=sg.hilbert(z); inst=np.diff(np.unwrap(np.angle(an)))/(2*np.pi)*sr; amp=20*np.log10(np.abs(an)+1e-7)
    ia,ib=int(a/1000*sr),int(b/1000*sr)
    print(f'{fc} Hz line {a}-{b}ms: inst f per 5ms:', ' '.join(f'{np.median(inst[i:i+221]):.0f}' for i in range(ia,ib-221,221)), '| amp:', ' '.join(f'{np.mean(amp[i:i+221]):.0f}' for i in range(ia,ib,221)))
    # exponential decay fit on amp after its peak within window
    seg=amp[ia:ib]; ip=np.argmax(seg); tt=np.arange(ip+44,len(seg))/sr*1000
    if len(tt)>100:
        p=np.polyfit(tt,seg[ip+44:],1); print(f'   decay {p[0]:.2f} dB/ms -> T60 {60/-p[0] if p[0]<0 else float("inf"):.0f} ms, Q~{np.pi*fc*(60/-p[0]/1000)/6.91 if p[0]<0 else 0:.0f}')
