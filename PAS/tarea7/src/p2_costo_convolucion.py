# p2_costo_convolucion.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import time
import os

os.makedirs("figs", exist_ok=True)

img = np.random.rand(512, 512)

def conv_espacial(img, h):
    return convolve2d(img, h, mode='same')

def conv_freq(img, h):
    pad_shape = [img.shape[0] + h.shape[0] - 1, img.shape[1] + h.shape[1] - 1]
    F = np.fft.fft2(img, pad_shape)
    H = np.fft.fft2(h, pad_shape)
    conv = np.real(np.fft.ifft2(F * H))
    return conv[:img.shape[0], :img.shape[1]]

sizes = [3, 7, 15, 31, 63, 127, 255]
t_espacial, t_freq = [], []

for n in sizes:
    h = np.ones((n, n)) / n**2
    t0 = time.time(); conv_espacial(img, h); t1 = time.time()
    t_espacial.append(t1 - t0)
    t0 = time.time(); conv_freq(img, h); t1 = time.time()
    t_freq.append(t1 - t0)

plt.figure()
plt.semilogy(sizes, t_espacial, 'o-', label='Espacio')
plt.semilogy(sizes, t_freq, 's--', label='Frecuencia')
plt.xlabel("Tamaño del kernel (nxn)")
plt.ylabel("Tiempo [s]")
plt.legend()
plt.grid(True)
plt.title("Costo de convolución: espacio vs frecuencia")
plt.savefig("figs/p2_tiempos_convolucion.png", dpi=200)
