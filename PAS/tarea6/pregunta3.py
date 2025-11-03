# p3_convolucion.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# Crear imagen sintética
img = np.zeros((100, 100))
img[30:70, 40:60] = 1  # cuadrado blanco
plt.imsave("figs/p3_imagen_original.png", img, cmap='gray')

# Crear kernel gaussiano
x = np.linspace(-3, 3, 15)
y = np.linspace(-3, 3, 15)
X, Y = np.meshgrid(x, y)
kernel = np.exp(-(X**2 + Y**2))
kernel /= kernel.sum()

# Convoluciones con distintas opciones
conv_full = convolve2d(img, kernel, mode='full')
conv_same = convolve2d(img, kernel, mode='same')
conv_valid = convolve2d(img, kernel, mode='valid')

# Graficar resultados
plt.figure(figsize=(10, 3))
for i, (data, title) in enumerate([(conv_full, 'full'), (conv_same, 'same'), (conv_valid, 'valid')]):
    plt.subplot(1, 3, i+1)
    plt.imshow(data, cmap='gray')
    plt.title(f"Convolución ({title})")
    plt.axis('off')
plt.tight_layout()
plt.savefig("figs/p3_convoluciones.png", dpi=200)
plt.show()
