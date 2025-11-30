import numpy as np
import matplotlib.pyplot as plt
from skimage import io, filters, measure, morphology
from scipy.ndimage import binary_opening, binary_closing
from scipy.optimize import curve_fit

# ============================
# Parámetros
# ============================

OFFSET = 100
MIN_AREA = 40       # eliminar objetos demasiado pequeños
MAX_AREA = 2000     # eliminar objetos demasiado grandes
MIN_CIRC = 0.65     # circularidad mínima aceptable


# ============================
# Funciones auxiliares
# ============================

def gaussian(x, A, x0, sigma, C):
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + C


def plot_raw_offset(raw, corrected):
    fig, ax = plt.subplots(1, 2, figsize=(11, 5))
    ax[0].imshow(raw, cmap='gray')
    ax[0].set_title("RAW")
    ax[1].imshow(corrected, cmap='gray')
    ax[1].set_title("RAW - OFFSET")
    plt.show()


def circularity(region):
    """ Circularidad = 4πA / P^2 """
    area = region.area
    per = region.perimeter if region.perimeter > 0 else 1
    return 4 * np.pi * area / (per ** 2)


# ============================
# Procesamiento principal
# ============================

def load_and_preprocess(path):
    raw = io.imread(path).astype(float)
    corrected = raw - OFFSET

    # Mostrar RAW y OFFSET juntos
    plot_raw_offset(raw, corrected)

    return raw, corrected


def segment_beads(img):

    # Umbral global
    th = filters.threshold_otsu(img)
    mask = img > th

    # Limpieza morfológica
    mask = morphology.remove_small_objects(mask, MIN_AREA)
    mask = binary_opening(mask, structure=np.ones((3,3)))
    mask = binary_closing(mask, structure=np.ones((3,3)))

    # Mostrar máscara
    plt.figure(figsize=(5,5))
    plt.imshow(mask, cmap='gray')
    plt.title("Máscara Post-Procesada")
    plt.show()

    # Etiquetado
    labels = measure.label(mask)
    regions = measure.regionprops(labels, intensity_image=img)

    # Filtrado geométrico (área + circularidad)
    filtered = []
    for r in regions:
        A = r.area
        C = circularity(r)

        if MIN_AREA < A < MAX_AREA and C > MIN_CIRC:
            filtered.append(r)

    print(f"Microesferas detectadas: {len(filtered)}")

    # Dibujar bounding boxes sobre imagen original
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(img, cmap='gray')

    for r in filtered:
        minr, minc, maxr, maxc = r.bbox
        ax.add_patch(
            plt.Rectangle((minc, minr),
                          maxc-minc, maxr-minr,
                          edgecolor='red', facecolor='none', linewidth=1.5)
        )
    plt.title("Microesferas detectadas")
    plt.show()

    return filtered


# ============================
# MAIN
# ============================

def main():
    raw, img = load_and_preprocess("img.tif")

    beads = segment_beads(img)

    # Aquí continuarías con el análisis: FWHM, NA, potencia, etc.
    return beads


if __name__ == "__main__":
    main()
