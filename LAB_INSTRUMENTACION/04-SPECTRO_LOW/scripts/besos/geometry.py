"""Curvatura de las líneas espectrales (imagen curva de la rendija) y rectificación."""
import numpy as np


def trace_line(img, x_guess, half_win=6, rows=(250, 800), step=5, band=2, deg=2):
    """Centroide de una línea fila a fila y ajuste polinomial x(y).

    Devuelve (coeficientes np.polyfit, filas, centroides, rms del ajuste)."""
    ys, xs = [], []
    x_c = int(round(x_guess))
    for y in range(rows[0], rows[1], step):
        prof = img[y - band:y + band + 1].mean(0)
        x_c = int(np.argmax(prof[x_c - half_win:x_c + half_win + 1])) + x_c - half_win
        sl = slice(x_c - half_win, x_c + half_win + 1)
        w = prof[sl] - np.median(prof)
        w[w < 0] = 0
        if w.sum() <= 0:
            continue
        ys.append(y)
        xs.append((w * np.arange(sl.start, sl.stop)).sum() / w.sum())
    ys, xs = np.array(ys), np.array(xs)
    coef = np.polyfit(ys, xs, deg)
    rms = float(np.std(xs - np.polyval(coef, ys)))
    return coef, ys, xs, rms


def rectify(img, coef, y_ref=None):
    """Desplaza cada fila para que la línea trazada quede vertical (interpolación lineal)."""
    ny, nx = img.shape
    if y_ref is None:                         # vértice de la parábola
        y_ref = -coef[1] / (2 * coef[0]) if len(coef) == 3 else ny / 2
    x = np.arange(nx, dtype=float)
    dx = np.polyval(coef, np.arange(ny)) - np.polyval(coef, y_ref)
    return np.array([np.interp(x + dx[y], x, img[y]) for y in range(ny)])


def tilt_deg(coef, rows):
    """Inclinación media de la línea respecto a la vertical (término lineal en el centro)."""
    y0 = np.mean(rows)
    slope = np.polyval(np.polyder(coef), y0)
    return float(np.degrees(np.arctan(slope)))
