"""Modelo teórico de primer orden del espectrógrafo de prisma.

Ecuaciones (ver Marco Teórico del informe):
  n(λ)        Sellmeier
  δ(λ)        = θ1 + arcsin[n sin(A - arcsin(sin θ1 / n))] - A
  dδ/dλ       derivada numérica de δ a θ1 fijo
  dx/dλ       = f_cam dδ/dλ
  Δλ          = w' |dλ/dx|,  w' = w (f_cam/f_col) · M_anam
  R           = λ/Δλ
"""
import numpy as np


class Prism:
    def __init__(self, sellmeier_B, sellmeier_C, apex_deg=60.0, lam_c=550.0, theta1_deg=None):
        self.B, self.C = np.array(sellmeier_B), np.array(sellmeier_C)
        self.A = np.radians(apex_deg)
        # ángulo de incidencia: por defecto, desviación mínima a la longitud de onda central
        if theta1_deg is None:
            self.theta1 = np.arcsin(self.n(lam_c) * np.sin(self.A / 2))
        else:
            self.theta1 = np.radians(theta1_deg)

    def n(self, lam_nm):
        l2 = (np.asarray(lam_nm, float) / 1000.0) ** 2
        return np.sqrt(1 + np.sum(self.B[:, None] * l2 / (l2 - self.C[:, None]), axis=0)).squeeze()

    def dn_dlam(self, lam_nm, h=0.05):
        return (self.n(np.asarray(lam_nm) + h) - self.n(np.asarray(lam_nm) - h)) / (2 * h)

    def angles(self, lam_nm):
        n = self.n(lam_nm)
        r1 = np.arcsin(np.sin(self.theta1) / n)
        r2 = self.A - r1
        theta2 = np.arcsin(n * np.sin(r2))
        return r1, r2, theta2

    def deviation(self, lam_nm):
        """δ(λ) [rad]."""
        _, _, theta2 = self.angles(lam_nm)
        return self.theta1 + theta2 - self.A

    def angular_dispersion(self, lam_nm, h=0.05):
        """dδ/dλ [rad/nm] (valor absoluto)."""
        lam = np.asarray(lam_nm, float)
        return np.abs(self.deviation(lam + h) - self.deviation(lam - h)) / (2 * h)

    def anamorphic(self, lam_nm):
        """Magnificación anamórfica del prisma (=1 en desviación mínima)."""
        r1, r2, theta2 = self.angles(lam_nm)
        return (np.cos(self.theta1) * np.cos(r2)) / (np.cos(r1) * np.cos(theta2))


def performance(prism, lam_nm, f_col, f_cam, slit_um, pixel_um, base_mm):
    """Dispersión, resolución y poder resolutivo teóricos en función de λ."""
    lam = np.asarray(lam_nm, float)
    lin = f_cam * 1e3 * prism.angular_dispersion(lam)            # µm/nm
    recip_px = pixel_um / lin                                     # nm/px
    w_img = slit_um * f_cam / f_col * prism.anamorphic(lam)       # µm
    w_eff = np.maximum(w_img, 2 * pixel_um)                       # muestreo de Nyquist
    dlam = w_eff / lin                                            # nm
    return dict(lam=lam, lin_um_nm=lin, recip_nm_px=recip_px, recip_nm_mm=1e3 / lin,
                slit_img_um=w_img, slit_img_px=w_img / pixel_um, dlam=dlam, R=lam / dlam,
                R_diff=base_mm * 1e6 * np.abs(prism.dn_dlam(lam)))


def detector_range(prism, f_cam, width_mm, lam_center, lam_grid=np.arange(350, 1000, 0.1)):
    """λ que caen dentro del detector si λ_center cae en su centro."""
    x = f_cam * np.tan(prism.deviation(lam_grid) - prism.deviation(lam_center))  # mm
    inside = np.abs(x) <= width_mm / 2
    return float(lam_grid[inside].min()), float(lam_grid[inside].max())
