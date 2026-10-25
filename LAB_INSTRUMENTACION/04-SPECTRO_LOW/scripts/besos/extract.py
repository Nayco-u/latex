"""Extracción del espectro 1D."""
import numpy as np

from . import config


def background(img, rows=config.BIAS_ROWS):
    """Nivel de fondo (bias + luz difusa) y ruido, de filas sin luz."""
    reg = img[rows[0]:rows[1]]
    return float(np.median(reg)), float(np.std(reg))


def spectrum_1d(img, rows=config.EXTRACT_ROWS):
    """Promedio a lo largo de la rendija, con el fondo restado. Devuelve (x_px, flujo, sigma)."""
    bkg, noise = background(img)
    sub = img[rows[0]:rows[1]] - bkg
    flux = sub.mean(0)
    sigma = np.full_like(flux, noise / np.sqrt(rows[1] - rows[0]))
    return np.arange(img.shape[1], dtype=float), flux, sigma
