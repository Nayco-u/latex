"""Solución de longitud de onda λ(x) con la fórmula de Hartmann (adecuada para prismas).

    λ(x) = λ0 + C / (x - x0)
"""
import numpy as np
from scipy.optimize import curve_fit


def hartmann(x, lam0, C, x0):
    return lam0 + C / (np.asarray(x, float) - x0)


def fit(x, lam, x_err=None, p0=(250.0, -1.6e5, 1400.0)):
    """Ajuste por mínimos cuadrados. Devuelve dict con parámetros, covarianza y residuos."""
    x, lam = np.asarray(x, float), np.asarray(lam, float)
    popt, pcov = curve_fit(hartmann, x, lam, p0=p0, maxfev=50000)
    res = lam - hartmann(x, *popt)
    dof = max(len(x) - 3, 1)
    return dict(p=popt, cov=pcov, res=res, rms=float(np.sqrt(np.sum(res ** 2) / dof)), n=len(x))


def wavelength(x, sol):
    return hartmann(x, *sol["p"])


def wavelength_err(x, sol):
    """Incertidumbre de λ(x) propagada desde la covarianza del ajuste."""
    lam0, C, x0 = sol["p"]
    x = np.atleast_1d(np.asarray(x, float))
    J = np.stack([np.ones_like(x), 1 / (x - x0), C / (x - x0) ** 2], axis=1)
    return np.sqrt(np.einsum("ij,jk,ik->i", J, sol["cov"], J))


def pixel(lam, sol):
    """Inversa: x(λ)."""
    lam0, C, x0 = sol["p"]
    return x0 + C / (np.asarray(lam, float) - lam0)


def dispersion(x, sol):
    """Dispersión recíproca |dλ/dx| [nm/px]."""
    lam0, C, x0 = sol["p"]
    return np.abs(C) / (np.asarray(x, float) - x0) ** 2
