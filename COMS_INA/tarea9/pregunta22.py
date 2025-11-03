import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

def Ps_16qam_mrc_avg(Nr, gamma_bar):
    M = 16
    g = 3/(M-1)
    # integrands
    integrand1 = lambda theta: (1 + g * gamma_bar / np.sin(theta)**2)**(-Nr)
    integrand2 = lambda theta: (1 + g * gamma_bar / np.sin(theta)**2)**(-Nr)
    I1, _ = integrate.quad(integrand1, 0, np.pi/2, epsabs=1e-12, epsrel=1e-9, limit=200)
    I2, _ = integrate.quad(integrand2, 0, np.pi/4, epsabs=1e-12, epsrel=1e-9, limit=200)
    A = 4 / np.pi * (1 - 1 / np.sqrt(M))
    B = 4 / np.pi * (1 - 1 / np.sqrt(M))**2
    Ps = A * I1 - B * I2
    return Ps

# Rango de SNR en dB
gamma_db = np.linspace(0, 30, 31)
gamma_lin = 10**(gamma_db/10)

plt.figure(figsize=(8,6))
for Nr in range(1,9):
    Ps_vals = [Ps_16qam_mrc_avg(Nr, gbar) for gbar in gamma_lin]
    plt.plot(gamma_db, Ps_vals, label=f'N_r={Nr}')
plt.grid(True, which='both')
plt.xlabel('SNR media por rama $\\bar\\gamma$ (dB)')
plt.ylabel('Prob. media de error de símbolo $\\overline{P_s}$')
plt.legend()
plt.title('16-QAM con MRC - $N_r=1..8$')
plt.ylim(1e-5,1)
plt.savefig('fig1')
plt.show()
