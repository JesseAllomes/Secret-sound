import sys; sys.path.insert(0,'/home/user/secret-sound')
import numpy as np, librosa, steel_score as ss
SR=ss.SR
def seg(f,a,b):
    y,_=librosa.load(f,sr=SR,mono=True); return y[int(a*SR):int(b*SR)]
def show(name,y):
    st=ss.strokes(y); top=max(s[1] for s in st)
    print(name,'strokes:',[(round(float(t),3),round(float(ss.db(l/top)),1),int(n)) for t,l,n in st])
    r=ss.score_signal(y); print('  ',{k:(round(float(v),3) if isinstance(v,(float,np.floating)) else v) for k,v in r.items()} if r else None)
for k in range(4): show(f'clue#{k+1}', seg('clue_x4.mp3',k*1.231,k*1.231+0.631))
show('AB-clue', seg('ab_light.mp3',0,0.66))
show('light-switch', seg('ab_light.mp3',1.12,1.78))
