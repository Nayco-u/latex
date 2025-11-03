# p3_teorema_seccion_central.py
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon, iradon
import scipy.ndimage as nd
import os

os.makedirs("figs", exist_ok=True)

# a) Imagen analítica: suma de rectángulos
x = np.linspace(-1, 1, 256)
y = np.linspace(-1, 1, 256)
X, Y = np.meshgrid(x, y)
img = ((np.abs(X) < 0.4) & (np.abs(Y) < 0.2)).astype(float)
plt.imsave("figs/p3_imagen_base.png", img, cmap='gray')

# Transformada de Fourier 2D
F2 = np.fft.fftshift(np.abs(np.fft.fft2(img)))
plt.imsave("figs/p3_fourier2d.png", np.log1p(F2), cmap='inferno')

# Transformada de Radon
thetas = np.linspace(0, 180, 12, endpoint=False)
R = radon(img, theta=thetas, circle=True)
plt.figure(figsize=(10,10))
plt.plot(R[:, 0], label=f'\\theta={thetas[0]:.0f}')
plt.plot(R[:, 1], label=f'\\theta={thetas[1]:.0f}')
plt.plot(R[:, 2], label=f'\\theta={thetas[2]:.0f}')
plt.plot(R[:, 3], label=f'\\theta={thetas[3]:.0f}')
plt.legend(); plt.title("Transformada de Radon")
plt.savefig("figs/p3_radon.png", dpi=200)

# b) Comparar secciones centrales

for i, theta in enumerate(thetas):
    g = R[:, i]
    G = np.abs(np.fft.fftshift(np.fft.fft(g)))
    N = F2.shape[0]
    x = np.arange(-N//2, N//2)
    X, Y = np.meshgrid(x, x)

    # Coordenadas de línea (por interpolación)
    r_line = np.linspace(-N//2, N//2, N)
    x_line = N/2 + r_line * np.cos(np.deg2rad(theta))
    y_line = N/2 + r_line * np.sin(np.deg2rad(theta))

    F_section = nd.map_coordinates(F2, [y_line, x_line], order=1)
    F_section /= F_section.max()

    plt.figure()
    plt.plot(G / G.max(), label='FFT Radon')
    plt.plot(F_section, label='Sección central')
    plt.legend()
    plt.title(f"Comparación \\theta={theta:.0f}\\degree")
    plt.savefig(f"figs/p3_comparacion_theta{int(theta)}.png", dpi=200)

# ---------- Reconstrucción con iradon (FBP) ----------
recon_iradon = iradon(R, theta=thetas, circle=True)
plt.imsave("figs/p3c_recon_iradon.png", recon_iradon, cmap='gray')