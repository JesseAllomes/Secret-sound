import numpy as np
from numpy.polynomial import legendre as Lg
Nd=11
rg,rw=Lg.leggauss(60); rg=(rg+1)/2; rw=rw/2
th=np.linspace(0,2*np.pi,160,endpoint=False); tw=2*np.pi/160
R,T=np.meshgrid(rg,th,indexing='ij'); W=((rw*rg)[:,None]*tw*np.ones_like(R)).ravel()
X=(R*np.cos(T)).ravel(); Y=(R*np.sin(T)).ravel()
def lp(x,i,d):
    c=np.zeros(Nd+1); c[i]=1
    for _ in range(d): c=Lg.legder(c)
    return Lg.legval(x,c)
idx=[(i,j) for i in range(Nd+1) for j in range(Nd+1-i)]
def fn(dx,dy): return np.array([lp(X,i,dx)*lp(Y,j,dy) for i,j in idx])
Wf=fn(0,0); Wxx=fn(2,0); Wyy=fn(0,2); Wxy=fn(1,1)
M=(Wf*W)@Wf.T
s,U=np.linalg.eigh(M); keep=s>1e-9*s.max(); Tm=U[:,keep]/np.sqrt(s[keep])
for nu in [0.28,0.3,0.33,0.35,0.4]:
    K=((Wxx+Wyy)*W)@(Wxx+Wyy).T - 2*(1-nu)*((Wxx*W)@Wyy.T-(Wxy*W)@Wxy.T)
    w=np.sort(np.linalg.eigvalsh(Tm.T@K@Tm)); w=w[w>1.0]; f=np.sqrt(w); u=[f[0]]
    for x in f[1:14]:
        if abs(x-u[-1])/u[-1]>2e-3: u.append(x)
    print("nu=%.2f lambda^2:"%nu,np.round(u[:5],3)," ratios:",np.round(np.array(u[:5])/u[0],3))
