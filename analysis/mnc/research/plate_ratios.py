import numpy as np
from numpy.polynomial import legendre as L
def free_plate(a_over_b, nu=0.3, N=14, nmodes=8):
    # plate x in [-1,1] (half-width a/2 scaled), y in [-1,1]; physical half-sizes ax, by
    ax, by = a_over_b/2.0, 0.5
    xg, wg = L.leggauss(40)
    def basis(deriv, half):
        out=[]
        for i in range(N):
            c=np.zeros(N); c[i]=1
            for _ in range(deriv): c=L.legder(c)
            out.append(L.legval(xg,c)/half**deriv)
        return np.array(out)  # N x ng
    B0x,B1x,B2x = basis(0,ax),basis(1,ax),basis(2,ax)
    B0y,B1y,B2y = basis(0,by),basis(1,by),basis(2,by)
    W=ax*by  # jacobian (dx dy) = ax*by du dv
    def I(Bx,By,Cx,Cy):
        # matrix over (i,j),(k,l): sum wg_x Bx_i Cx_k * sum wg_y By_j Cy_l
        Mx = (Bx*wg)@Cx.T; My=(By*wg)@Cy.T
        return np.kron(Mx,My)*W
    K = I(B2x,B0y,B2x,B0y)+I(B0x,B2y,B0x,B2y)+nu*(I(B2x,B0y,B0x,B2y)+I(B0x,B2y,B2x,B0y))+2*(1-nu)*I(B1x,B1y,B1x,B1y)
    M = I(B0x,B0y,B0x,B0y)
    Lc=np.linalg.cholesky(M); Li=np.linalg.inv(Lc)
    ev=np.linalg.eigvalsh(Li@K@Li.T)
    ev=ev[ev>1.0]
    ev=np.sort(ev)
    return np.sqrt(ev)
for ab in [1.0,1.1,1.25,1.5,2,3,4]:
    f=free_plate(ab)[:6]
    print("free rect a/b=%.2f  ratios:"%ab, np.round(f/f[0],3))
