import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io
from scipy.signal import convolve2d
from scipy.fft import fft2, ifft2, fftshift, ifftshift
from scipy.ndimage import uniform_filter

os.makedirs("results", exist_ok=True)

# -----------------------------------------------------------
# 1) Cargar imagen
# -----------------------------------------------------------
def load_image(path):
    img = io.imread(path, as_gray=True)
    img = img.astype(np.float32) / 255.0
    return img

# -----------------------------------------------------------
# 2) Estimar ruido σ usando filtro de promedio - imagen original ≈ detalle
# -----------------------------------------------------------
def estimate_noise_sigma(img):
    """Estima sigma del ruido usando método de residual del promedio local."""
    smooth = uniform_filter(img, size=7)
    residual = img - smooth
    sigma = np.std(residual)
    return sigma

# -----------------------------------------------------------
# 3) Crear filtros H(u,v) según el tipo de blur
# -----------------------------------------------------------
def build_filter(img, h_type):
    M, N = img.shape
    u = np.arange(-M//2, M//2)
    v = np.arange(-N//2, N//2)
    U, V = np.meshgrid(u, v, indexing='ij')

    if h_type == "h1":  # blur gaussiano suave
        sigma = 8
        H = np.exp(-(U**2 + V**2) / (2 * sigma**2))

    elif h_type == "h2":  # movimiento lineal
        L = 25
        theta = np.deg2rad(15)
        H = np.sinc((U*np.cos(theta) + V*np.sin(theta)) * L / M)

    elif h_type == "h3":  # movimiento circular
        R = 20
        r = np.sqrt(U**2 + V**2)
        H = (r <= R).astype(float)

    return fftshift(H)

# -----------------------------------------------------------
# 4) Wiener clásico con parámetro gamma
# -----------------------------------------------------------
def wiener_gamma(img, H, gamma):
    G = fft2(img)
    W = np.conj(H) / (np.abs(H)**2 + gamma)
    F_hat = W * G
    f = np.real(ifft2(F_hat))
    return f

# -----------------------------------------------------------
# 5) Wiener usando densidades espectrales (pregunta 3)
# -----------------------------------------------------------
def wiener_full_psd(img, H, sigma):
    G = fft2(img)

    # Densidad espectral del ruido (plana)
    S_ww = sigma**2

    # Estimación de PSD de imagen usando |G|^2 suavizado
    S_gg = uniform_filter(np.abs(G)**2, size=15)

    # S_ff estimado usando relación S_gg = |H|^2 S_ff + S_ww
    S_ff = np.maximum(S_gg - S_ww, 1e-6)

    W = np.conj(H) * S_ff / (np.abs(H)**2 * S_ff + S_ww)
    F_hat = W * G
    f = np.real(ifft2(F_hat))
    return f

# -----------------------------------------------------------
# 6) Procesar TODAS las imágenes
# -----------------------------------------------------------
def process_image(name, h_type):
    print(f"\n=== Procesando {name} ({h_type}) ===")

    img = load_image(f"figs/{name}.png")
    sigma = estimate_noise_sigma(img)
    print(f"Sigma estimado = {sigma:.4f}")

    H = build_filter(img, h_type)

    # Wiener clásico con distintos gamma
    gammas = [1e-3, 1e-2, 1e-1, 0.5]
    for g in gammas:
        rec = wiener_gamma(img, H, g)
        plt.imsave(f"results/{name}_wiener_gamma_{g}.png",
                   np.clip(rec, 0, 1), cmap="gray")

    # Wiener completo usando PSD (pregunta 3)
    rec2 = wiener_full_psd(img, H, sigma)
    plt.imsave(f"results/{name}_wiener_psd.png",
               np.clip(rec2, 0, 1), cmap="gray")

    return sigma


# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------
if __name__ == "__main__":
    images = [
        ("bici_h1", "h1"),
        ("bici_h2", "h2"),
        ("road_h1", "h1"),
        ("road_h3", "h3")
    ]

    for name, h in images:
        process_image(name, h)

    print("\nListo! Resultados guardados en carpeta: results/")
