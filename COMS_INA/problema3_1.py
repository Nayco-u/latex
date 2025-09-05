import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la antena
Gm = 18      # ganancia máxima en dBi
GSSL = -18   # supresión de lóbulos laterales en dB
theta_tilt = 2  # inclinación en grados
theta_HPBW = 6.4 # ancho a media potencia en grados

# Rango angular
theta = np.linspace(-180, 179, 2000)

# Modelo de Gunnarsson
Gv = Gm + np.maximum(-12*((theta - theta_tilt)/theta_HPBW)**2, GSSL)

# Gráfico polar
plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)

theta_rad = np.radians(theta)
ax.plot(theta_rad, Gv)

ax.set_theta_zero_location("E")
ax.set_theta_direction(-1)
ax.set_title("Patrón de radiación vertical (dB)", va='bottom')
plt.savefig("patron_vertical.png", dpi=300)
