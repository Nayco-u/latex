# p1_imagenes.py
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, img_as_float

# === a) Cargar imagen RGB ===
img = io.imread("feliz_navidad.jpg")  # coloca aquí la ruta de tu imagen
img = img_as_float(img)
print(f"Tamaño: {img.shape} (alto, ancho, canales)")
print(f"Número de bits por canal: {img.dtype}")

# Mostrar imagen original
plt.figure()
plt.imshow(img)
plt.title("Imagen RGB original")
plt.axis("off")
plt.savefig("figs/p1a_imagen_rgb.png", dpi=200)

# === b) Mostrar cada canal ===
canales = ['Rojo', 'Verde', 'Azul']
colores = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # colores RGB

for i in range(3):
    # Crear una imagen con solo un canal
    canal_color = np.zeros_like(img)
    canal_color[:, :, i] = img[:, :, i]

    plt.figure()
    plt.imshow(canal_color)
    plt.title(f"Canal {canales[i]}")
    plt.axis("off")
    plt.savefig(f"figs/p1b_canal_{canales[i].lower()}.png", dpi=200)


# === c) Conversión a grises ===
# Usando función predefinida
img_gray_lib = color.rgb2gray(img)
plt.figure()
plt.imshow(img_gray_lib, cmap='gray')
plt.title("Escala de grises (rgb2gray)")
plt.axis("off")
plt.savefig("figs/p1c_grises_funcion.png", dpi=200)

# Por combinación lineal manual
img_gray_lin = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
plt.figure()
plt.imshow(img_gray_lin, cmap='gray')
plt.title("Escala de grises (combinación lineal)")
plt.axis("off")
plt.savefig("figs/p1c_grises_manual.png", dpi=200)

plt.show()
