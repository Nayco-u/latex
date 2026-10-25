"""Ajustes gaussianos (simples y múltiples) de rasgos espectrales."""
import numpy as np
from scipy.optimize import curve_fit

FWHM_FACTOR = 2 * np.sqrt(2 * np.log(2))   # FWHM = 2.3548 σ


def gaussian(x, amp, mu, sigma):
    return amp * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def multi_gaussian(x, c0, c1, *p):
    """Fondo lineal + N gaussianas; p = (amp, mu, sigma) * N."""
    y = c0 + c1 * (x - x.mean())
    for i in range(0, len(p), 3):
        y = y + gaussian(x, *p[i:i + 3])
    return y


def fit_gaussians(x, y, guesses, half_win=10, sigma0=2.0, sigma_max=8.0, max_shift=4.0, yerr=None):
    """Ajusta simultáneamente una gaussiana por cada posición en `guesses`.

    Devuelve (lista de dict por componente, (x_ventana, modelo))."""
    guesses = np.atleast_1d(np.asarray(guesses, float))
    lo = max(int(guesses.min() - half_win), 0)
    hi = min(int(guesses.max() + half_win) + 1, len(x))
    xx, yy = x[lo:hi], y[lo:hi]
    ee = None if yerr is None else yerr[lo:hi]

    p0, lb, ub = [np.min(yy), 0.0], [-np.inf, -np.inf], [np.inf, np.inf]
    for g in guesses:
        a0 = max(yy[int(round(g)) - lo] - np.min(yy), 1e-3)
        p0 += [a0, g, sigma0]
        lb += [0.0, g - max_shift, 0.4]
        ub += [np.inf, g + max_shift, sigma_max]
    popt, pcov = curve_fit(multi_gaussian, xx, yy, p0=p0, bounds=(lb, ub),
                           sigma=ee, absolute_sigma=ee is not None, maxfev=50000)
    perr = np.sqrt(np.diag(pcov))
    # sin errores absolutos: escalar con el chi2 reducido (curve_fit ya lo hace)
    comps = []
    for i in range(2, len(popt), 3):
        a, mu, s = popt[i:i + 3]
        ea, emu, es = perr[i:i + 3]
        comps.append(dict(amp=a, amp_err=ea, mu=mu, mu_err=emu, sigma=s, sigma_err=es,
                          fwhm=FWHM_FACTOR * s, fwhm_err=FWHM_FACTOR * es))
    return comps, (xx, multi_gaussian(xx, *popt), popt)


def group_positions(xs, gap):
    """Agrupa posiciones ordenadas cuya separación es menor que `gap`."""
    order = np.argsort(xs)
    groups, cur = [], [order[0]]
    for i, j in zip(order[:-1], order[1:]):
        if xs[j] - xs[i] < gap:
            cur.append(j)
        else:
            groups.append(cur)
            cur = [j]
    groups.append(cur)
    return groups
