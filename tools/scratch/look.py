import sys; sys.path.insert(0,'/home/user/secret-sound')
import numpy as np, librosa, steel_score as ss
SR=ss.SR
for f in sys.argv[1:]:
    y,_=librosa.load(f,sr=SR,mono=True)
    env=np.convolve(np.abs(y),np.ones(480)/480,'same'); d=ss.db(env)
    # find active regions
    act=d>d.max()-35
    edges=np.flatnonzero(np.diff(act.astype(int)))
    print(f, len(y)/SR,'s')
    st=ss.strokes(y)
    print(' strokes (t, dB, impacts):',[(round(t,3),round(float(ss.db(l)-ss.db(max(s[1] for s in st))),1),n) for t,l,n in st])
