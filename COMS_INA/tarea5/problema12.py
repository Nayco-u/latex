import numpy as np
from scipy.special import erfc
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Q-function via erfc
def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

# (a) AWGN analytical for BPSK
def Pb_awgn(EbN0_lin):
    return Q(np.sqrt(2*EbN0_lin))

# (b) Rayleigh closed-form
def Pb_rayleigh_closed(gamma_bar_b):
    return 0.5 * (1.0 - np.sqrt(gamma_bar_b / (1.0 + gamma_bar_b)))

# (c) numerical integration
def Pb_rayleigh_numeric(gamma_bar_b):
    integrand = lambda g: Q(np.sqrt(2*g)) * (1.0/gamma_bar_b) * np.exp(-g/gamma_bar_b)
    val, _ = quad(integrand, 0, np.inf, epsabs=1e-8, epsrel=1e-6)
    return val

# (d) quick-and-dirty simulation
def simulate_pb_rayleigh(EbN0_lin, Nsym=2000, Nchan=200):
    pb_list = []
    for _ in range(Nchan):
        s = 2*(np.random.rand(Nsym) > 0.5) - 1.0
        h = (np.random.randn() + 1j*np.random.randn())/np.sqrt(2)
        N0 = 1.0 / EbN0_lin
        noise = np.sqrt(N0/2.0) * (np.random.randn(Nsym) + 1j*np.random.randn(Nsym))
        r = h * s + noise
        r_eq = r / h
        s_hat = np.real(r_eq) > 0
        s_bits = s > 0
        pb = np.mean(s_hat != s_bits)
        pb_list.append(pb)
    return np.mean(pb_list)

# Range of Eb/N0 in dB
EbN0_dB = np.arange(0, 31, 2)
EbN0_lin = 10**(EbN0_dB/10.0)

# (a)
Pb_awgn_vals = np.array([Pb_awgn(x) for x in EbN0_lin])

# (b) and (c)
gamma_bar_b = EbN0_lin
Pb_rayleigh_closed_vals = np.array([Pb_rayleigh_closed(g) for g in gamma_bar_b])
Pb_rayleigh_numeric_vals = np.array([Pb_rayleigh_numeric(g) for g in gamma_bar_b])

# (d)
Pb_rayleigh_sim = np.zeros_like(EbN0_lin, dtype=float)
for i, g in enumerate(gamma_bar_b):
    Pb_rayleigh_sim[i] = simulate_pb_rayleigh(g)

# Plot
plt.figure(figsize=(8,6))
plt.semilogy(EbN0_dB, Pb_awgn_vals, label='BPSK AWGN (teo)')
plt.semilogy(EbN0_dB, Pb_rayleigh_closed_vals, label='BPSK Rayleigh (cerrada)')
plt.semilogy(EbN0_dB, Pb_rayleigh_numeric_vals, '--', label='BPSK Rayleigh (num)')
plt.semilogy(EbN0_dB, Pb_rayleigh_sim, 'o-', label='BPSK Rayleigh (sim)')
plt.grid(True, which='both')
plt.xlabel('$E_b/N_0$ [dB]')
plt.ylabel('Probabilidad de error de bit $P_b$')
plt.ylim(1e-6, 1)
plt.legend()
plt.title('Problema 12: BPSK en AWGN y Rayleigh')
plt.tight_layout()
plt.savefig('problema12_fig.png', dpi=300)
plt.show()
