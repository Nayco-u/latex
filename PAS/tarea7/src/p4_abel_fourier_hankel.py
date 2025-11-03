# p4_abel_fourier_hankel.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j0
import os

os.makedirs("figs", exist_ok=True)

# Definición de funciones radiales
r = np.linspace(0, 1, 400)
cup = 2 * np.sqrt(1 - 4 * r**2) * (np.abs(r) <= 0.5)
cone = np.maximum(0, 1 - r)

# Abel-Fourier-Hankel ciclo (conceptual)
A = np.cumsum(cup[::-1])[::-1]
F = np.fft.fftshift(np.abs(np.fft.fft(cup)))
H = np.abs(np.fft.fft(j0(2*np.pi*r)))

plt.figure()
plt.plot(r, cup, label='Copa f(r)')
plt.plot(r, cone, label='Cono g(r)')
plt.title("Funciones base radiales")
plt.legend(); plt.grid(True)
plt.savefig("figs/p4_funciones_base.png", dpi=200)

plt.figure()
plt.plot(F / F.max(), label='Fourier de f(r)')
plt.plot(H / H.max(), label='Hankel(J0)')
plt.legend(); plt.title("Ciclo Abel-Fourier-Hankel (numérico)")
plt.grid(True)
plt.savefig("figs/p4_ciclo_afh.png", dpi=200)
