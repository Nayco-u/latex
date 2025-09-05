import numpy as np
import matplotlib.pyplot as plt

# Potencia y parámetros de la antena
Pt = 20.0     # [W]
d0 = 10.0     # [m]
alphas = [2.0, 5.0]
heights = [12.0, 24.0, 36.0]

# Parámetros de la antena (1.7 GHz)
params = dict(Gm=17.8, GSSL=-18, theta_tilt=2, theta_HPBW=7.5)

def Gv_dB(theta_deg, pars):
    Gm, GSSL, tilt, HPBW = pars["Gm"], pars["GSSL"], pars["theta_tilt"], pars["theta_HPBW"]
    return Gm + np.maximum(-12 * ((theta_deg - tilt) / HPBW)**2, GSSL)

def theta_from_x(x, h):
    return np.degrees(np.arctan2(h, x))

def R_from_x(x, h):
    return np.sqrt(h**2 + x**2)

# Distancias horizontales
x = np.logspace(-1, 4, 2000)

plt.figure(figsize=(8,5))

for h in heights:
    theta_x = theta_from_x(x, h)
    Gv = Gv_dB(theta_x, params)
    Glin = 10**(Gv/10.0)
    R = R_from_x(x, h)
    for a in alphas:
        S = (Pt * Glin) / (4*np.pi * d0**2) * (d0 / R)**a   # W/m²
        plt.plot(x, 1e6*S, label=f"h={h} m, α={a}")

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Distancia horizontal x desde la base [m]")
plt.ylabel("Densidad de potencia [μW/m²]")
plt.title("Exposición vs distancia (f=1.7 GHz, Pt=20 W, d0=10 m)")
plt.grid(True, which='both', ls=':')
plt.legend(ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig("exposicion_vs_distancia2.png", dpi=300)
plt.show()
