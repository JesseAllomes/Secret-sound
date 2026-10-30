import numpy as np
from numpy.polynomial import polynomial as P
Nd=14
funcs=[]
for i in range(Nd+1):
    for j in range(Nd+1-i):
        c=np.zeros((Nd+1,Nd+1)); c[i,j]=1; funcs.append(c)
rg,rw=np.polynomial.legendre.leggauss(60); rg=(rg+1)/2; rw=rw/2
th=np.linspace(0,2*np.pi,128,endpoint=False); tw=2*np.pi/128
R,T=np.meshgrid(rg,th,indexing='ij'); W=((rw*rg)[:,None]*tw*np.ones_like(R)).ravel()
X=(R*np.cos(T)).ravel(); Y=(R*np.sin(T)).ravel()
def ev(c,dx=0,dy=0):
    for _ in range(dx): c=P.polyder(c,axis=0)
    for _ in range(dy): c=P.polyder(c,axis=1)
    return P.polyval2d(X,Y,c) if c.size else np.zeros_like(X)
Wf=np.array([ev(c) for c in funcs]); Wxx=np.array([ev(c,2,0) for c in funcs]); Wyy=np.array([ev(c,0,2) for c in funcs]); Wxy=np.array([ev(c,1,1) for c in funcs])
M=(Wf*W)@Wf.T
s,U=np.linalg.eigh(M); keep=s>1e-13*s.max(); Tm=U[:,keep]/np.sqrt(s[keep])
for nu in [0.28,0.3,0.33,0.35,0.4]:
    K=((Wxx+Wyy)*W)@(Wxx+Wyy).T - 2*(1-nu)*((Wxx*W)@Wyy.T-(Wxy*W)@Wxy.T)
    w=np.sort(np.linalg.eigvalsh(Tm.T@K@Tm)); f=np.sqrt(np.abs(w))
    f=f[f>1.0]; u=[f[0]]
    for x in f[1:14]:
        if abs(x-u[-1])/u[-1]>2e-3: u.append(x)
    print("nu=%.2f abs:"%nu,np.round(u[:5],3)," ratios:",np.round(np.array(u[:5])/u[0],3))
