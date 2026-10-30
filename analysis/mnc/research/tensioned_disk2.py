import numpy as np
from numpy.polynomial import polynomial as P
# clamped circular plate with tension (stiff membrane), unit radius.  energy: D/2 (lap w)^2 + T/2 |grad w|^2 ; kinetic: rho h w^2 /2
# basis (1-r^2) x^i y^j ; separate symmetry classes by angular parity not needed.
Nd=12
def mul(a,b): return P.polymul(a.ravel(),b.ravel()) if False else None
def poly2(c): return c
def build(Nd):
    
    funcs=[]
    for i in range(Nd+1):
        for j in range(Nd+1-i):
            c=np.zeros((Nd+5,Nd+5))
            # (1-x^2-y^2)^2 = 1 -2x^2 -2y^2 + x^4 + 2x^2y^2 + y^4
            for (a,b,v) in [(0,0,1),(2,0,-2),(0,2,-2),(4,0,1),(2,2,2),(0,4,1)]: c[i+a,j+b]+=v
            funcs.append(c)
    return funcs
funcs=build(Nd)
rg,rw=np.polynomial.legendre.leggauss(60); rg=(rg+1)/2; rw=rw/2
th=np.linspace(0,2*np.pi,128,endpoint=False); tw=2*np.pi/128
R,T=np.meshgrid(rg,th,indexing='ij'); W=(rw[:,None]*rg[:,None]*tw)*np.ones_like(R)
X=(R*np.cos(T)).ravel(); Y=(R*np.sin(T)).ravel(); W=W.ravel()
def ev(c,dx=0,dy=0):
    for _ in range(dx): c=P.polyder(c,axis=0)
    for _ in range(dy): c=P.polyder(c,axis=1)
    if c.size==0: return np.zeros_like(X)
    return P.polyval2d(X,Y,c)
Wf=np.array([ev(c) for c in funcs])
Gx=np.array([ev(c,1,0) for c in funcs]); Gy=np.array([ev(c,0,1) for c in funcs])
Lp=np.array([ev(c,2,0)+ev(c,0,2) for c in funcs])
M=(Wf*W)@Wf.T; Kb=(Lp*W)@Lp.T; Kt=(Gx*W)@Gx.T+(Gy*W)@Gy.T
# orthonormalise (SVD-based to handle ill-conditioning)
s,U=np.linalg.eigh(M); keep=s>1e-12*s.max(); Tm=U[:,keep]/np.sqrt(s[keep])
def freqs(tau2):
    K=Tm.T@(Kb+tau2*Kt)@Tm
    w=np.sort(np.linalg.eigvalsh(K)); return np.sqrt(w)
for tau in [0.0,5,10,20,40,80,160,1000]:
    f=freqs(tau**2)
    # degenerate pairs (m>=1) appear twice; extract unique
    u=[f[0]]
    for x in f[1:12]:
        if abs(x-u[-1])/u[-1]>1e-3: u.append(x)
    print("tau=%5g"%tau, np.round(np.array(u[:6])/u[0],3))
