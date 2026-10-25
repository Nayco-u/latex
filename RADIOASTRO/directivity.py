import numpy as np
import matplotlib.pyplot as plt

# Parámetros
D0 = 1074  # Directividad máxima (lineal)
sigma_az = 2.5191  # grados
sigma_el = 2.4361  # grados

# Conversión a radianes
sigma_az_rad = np.radians(sigma_az)
sigma_el_rad = np.radians(sigma_el)

# Rango angular
theta_deg = np.linspace(-15, 15, 500)
theta_rad = np.radians(theta_deg)

# Función de directividad
def directivity(theta, sigma):
    return D0 * np.exp(-(theta**2) / (2 * sigma**2))

# Calcular directividades
D_az = directivity(theta_rad, sigma_az_rad)
D_el = directivity(theta_rad, sigma_el_rad)

# Convertir a dBi
D_az_dBi = 10 * np.log10(D_az)
D_el_dBi = 10 * np.log10(D_el)

# Nivel de media potencia (-3 dB)
D0_dBi = 10 * np.log10(D0)
half_power_level = D0_dBi - 3

# FWHM (en grados)
fwhm_az = 2.355 * sigma_az
fwhm_el = 2.355 * sigma_el

# Plot
plt.figure(figsize=(8, 5))

# Curvas
plt.plot(theta_deg, D_az_dBi, label='Azimuth', linewidth=2)
plt.plot(theta_deg, D_el_dBi, linestyle='--', label='Elevation', linewidth=2)

# Línea de -3 dB
plt.axhline(half_power_level, linestyle=':', label='-3 dB level')

# Área FWHM AZ
mask_az = np.abs(theta_deg) <= fwhm_az / 2
plt.fill_between(theta_deg[mask_az], D_az_dBi[mask_az], half_power_level,
                 alpha=0.3, label='FWHM Azimuth')

# Área FWHM EL
mask_el = np.abs(theta_deg) <= fwhm_el / 2
plt.fill_between(theta_deg[mask_el], D_el_dBi[mask_el], half_power_level,
                 alpha=0.2, label='FWHM Elevation')

# Labels
plt.xlabel('Angular Offset (degrees)')
plt.ylabel('Directivity (dBi)')
plt.title('Antenna Directivity Pattern with FWHM')

plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.xlim(-12, 12)
plt.ylim(0, D0_dBi + 1)

plt.tight_layout()
plt.savefig('directivity_fwhm.png', dpi=150)
plt.show()