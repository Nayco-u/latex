import numpy as np

eye  = np.array([33, 32, 34, 32, 33], float)
tel  = np.array([815, 796, 779, 811, 803], float)
sig_px = 1.0   # +-1 px reading uncertainty

M = tel/eye
sM_ind = M*np.sqrt((sig_px/tel)**2 + (sig_px/eye)**2)

print("per-trial M:", np.round(M,3))
print("per-trial sigma_M (px prop):", np.round(sM_ind,3))
Mbar = M.mean(); s = M.std(ddof=1); sem = s/np.sqrt(len(M))
print(f"M mean={Mbar:.3f} s={s:.3f} sem={sem:.3f}  rel s={100*s/Mbar:.2f}%")
print(f"dev from nominal 25: {100*(Mbar-25)/25:.2f}%")

# pupils
obj = np.array([47.1,47.0,47.2,47.3,47.1])
p25 = np.array([1.0,0.9,0.8,1.0,1.0])
p50 = np.array([0.5,0.4,0.6,0.66,0.52])
def stat(a,n):
    m=a.mean(); sd=a.std(ddof=1); se=sd/np.sqrt(len(a))
    print(f"{n}: mean={m:.4f} s={sd:.4f} sem={se:.4f} rel_s={100*sd/m:.2f}%")
    return m,sd,se
Do,sDo,seDo = stat(obj,"D_obj")
d25,s25,se25 = stat(p25,"exit25")
d50,s50,se50 = stat(p50,"exit50")

for (d,se,n,nom) in [(d25,se25,"25x",25),(d50,se50,"50x",50)]:
    Mp = Do/d
    sMp = Mp*np.sqrt((seDo/Do)**2 + (se/d)**2)
    print(f"M_pupil {n} = {Mp:.2f} +- {sMp:.2f}   (nominal {nom}, ratio {Mp/nom:.2f})")
print("ratio M_pupil50/M_pupil25 =", round((Do/d50)/(Do/d25),3))
print("expected exit pupil from photographic M:", round(Do/Mbar,3), "mm")
print("ratio expected/measured 25x:", round((Do/Mbar)/d25,3))

# FOV: 30 cm ruler assumed to fill the field, L = 18.7 m
W = 0.300; sW = 0.010
L = 18.7;  sL = 0.30
FOV = 2*np.arctan(W/(2*L))
dW = (1/(L*(1+(W/(2*L))**2)))*sW
dL = (W/(L**2*(1+(W/(2*L))**2)))*sL
sFOV = np.sqrt(dW**2+dL**2)
print(f"FOV = {FOV:.6f} +- {sFOV:.6f} rad = {np.degrees(FOV):.4f} +- {np.degrees(sFOV):.4f} deg = {FOV*206265:.1f} +- {sFOV*206265:.1f} arcsec")
print(f"arcmin: {np.degrees(FOV)*60:.2f} +- {np.degrees(sFOV)*60:.2f}")

AFOV = Mbar*np.degrees(FOV)
sAFOV = AFOV*np.sqrt((sem/Mbar)**2+(sFOV/FOV)**2)
print(f"apparent FOV = {AFOV:.2f} +- {sAFOV:.2f} deg")

# nominal exit pupils
print("nominal exit pupil 25x:", 50/25, "50x:", 50/50)
# Rayleigh
lam=550e-9; D=Do/1000
print("Rayleigh:", 1.22*lam/D*206265, "arcsec")
