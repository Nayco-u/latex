# p1_convolucion_lineal_vs_ciclica.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from skimage import io, color, img_as_float
import os

os.makedirs("figs", exist_ok=True)

# a) Imagenes a utilizar y filtros

def circ(N=256, R=60):
    """
    Genera una imagen circular (circ function) de tamaño NxN y radio R.
    """
    x = np.linspace(-N/2, N/2, N)
    y = np.linspace(-N/2, N/2, N)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    img = np.where(r <= R, 1.0, 0.0)
    return img

# Imagen analítica circular
img_simple = circ(N=256, R=50)

# Imagen real
img_real = img_as_float(io.imread("figs/feliz_navidad.jpg"))
img_gray = color.rgb2gray(img_real)

# Filtros
filtro_suavizado = np.ones((25, 25)) / 25**2
filtro_sobel = np.array([[1, 0, -1],
                         [2, 0, -2],
                         [1, 0, -1]])

# b) Convolución lineal vs cíclica
def conv_lineal(f, h):
    return convolve2d(f, h, mode='same', boundary='fill', fillvalue=0)

def conv_ciclica(f, h):
    F = np.fft.fft2(f)
    H = np.fft.fft2(h, s=f.shape)
    return np.real(np.fft.ifft2(F * H))

# Ejemplo con imagen simple
cl_simple_suave = conv_lineal(img_simple, filtro_suavizado)
cc_simple_suave = conv_ciclica(img_simple, filtro_suavizado)

cl_simple_sobel = conv_lineal(img_simple, filtro_sobel)
cc_simple_sobel = conv_ciclica(img_simple, filtro_sobel)

cl_gray_suave = conv_lineal(img_gray, filtro_suavizado)
cc_gray_suave = conv_ciclica(img_gray, filtro_suavizado)

cl_gray_sobel = conv_lineal(img_gray, filtro_sobel)
cc_gray_sobel = conv_lineal(img_gray, filtro_sobel)

plt.figure(figsize=(8, 7))
plt.subplot(2, 3, 1); plt.imshow(img_simple, cmap='gray'); plt.title("Original"); plt.axis('off')
plt.subplot(2, 3, 2); plt.imshow(cl_simple_suave, cmap='gray'); plt.title("Lineal")
plt.subplot(2, 3, 3); plt.imshow(cc_simple_suave, cmap='gray'); plt.title("Cíclica")
plt.subplot(2, 3, 4); plt.imshow(img_gray, cmap='gray'); plt.title("Original");plt.axis('off')
plt.subplot(2, 3, 5); plt.imshow(cl_gray_suave, cmap='gray'); plt.title("Lineal")
plt.subplot(2, 3, 6); plt.imshow(cc_gray_suave, cmap='gray'); plt.title("Cíclica")
plt.tight_layout()
plt.savefig("figs/p1_convolucion_suave.png", dpi=200)

plt.figure(figsize=(8, 7))
plt.subplot(2, 3, 1); plt.imshow(img_simple, cmap='gray'); plt.title("Original"); plt.axis('off')
plt.subplot(2, 3, 2); plt.imshow(cl_simple_sobel, cmap='gray'); plt.title("Lineal")
plt.subplot(2, 3, 3); plt.imshow(cc_simple_sobel, cmap='gray'); plt.title("Cíclica")
plt.subplot(2, 3, 4); plt.imshow(img_gray, cmap='gray'); plt.title("Original");plt.axis('off')
plt.subplot(2, 3, 5); plt.imshow(cl_gray_sobel, cmap='gray'); plt.title("Lineal")
plt.subplot(2, 3, 6); plt.imshow(cc_gray_sobel, cmap='gray'); plt.title("Cíclica")
plt.tight_layout()
plt.savefig("figs/p1_convolucion_sobel.png", dpi=200)

# c) Aplicar a canales RGB y HSV
img_hsv = color.rgb2hsv(img_real)
img_ycbcr = color.rgb2ycbcr(img_real)
for espacio, datos in zip(['RGB', 'HSV', 'YCbCr'], [img_real, img_hsv, img_ycbcr]):
    filtrada = np.zeros_like(datos)
    for i in range(3):
        filtrada[:, :, i] = conv_ciclica(datos[:, :, i], filtro_suavizado)
    if espacio == 'HSV':
        filtrada = color.hsv2rgb(filtrada)
    if espacio == 'YCbCr':
        filtrada = color.ycbcr2rgb(filtrada)
    plt.imsave(f"figs/p1_convolucion_{espacio.lower()}.png", filtrada)
