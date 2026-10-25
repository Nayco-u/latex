"""Lectura de los FITS de AstroDMx y de sus logs."""
import re
from pathlib import Path

import numpy as np
from astropy.io import fits

from . import config


def frames(folder: str) -> list[Path]:
    """Todos los FITS de una fuente (todas las subcarpetas de captura)."""
    return sorted((config.RAW_DIR / folder).rglob("*__data.fits"))


def load_stack(folder: str) -> np.ndarray:
    """Cubo (n_frames, ny, nx) en ADU como float."""
    return np.array([fits.getdata(f).astype(float) for f in frames(folder)])


def master(folder: str, combine: str = "median") -> np.ndarray:
    """Imagen combinada de una fuente."""
    cube = load_stack(folder)
    return np.median(cube, 0) if combine == "median" else cube.mean(0)


def read_log(folder: str) -> dict:
    """Parámetros de captura (exposición, ganancia, ...) desde el primer log."""
    logs = sorted((config.RAW_DIR / folder).rglob("*__log.txt"))
    out = {"n_frames": len(frames(folder))}
    if not logs:
        return out
    txt = logs[0].read_text(errors="ignore")
    for key, pat in {"camera": r"Camera Name\s*=\s*(.+)",
                     "exposure_ms": r"Exposure\s*=\s*([\d.]+)",
                     "gain": r"Gain\s*=\s*(\d+)",
                     "gamma": r"Gamma\s*=\s*(\d+)",
                     "format": r"Pixel Format\s*=\s*(.+)"}.items():
        m = re.search(pat, txt)
        if m:
            out[key] = m.group(1).strip()
    return out


def saturated_fraction(folder: str, sat: float = 255) -> float:
    return float((load_stack(folder) >= sat).mean())
