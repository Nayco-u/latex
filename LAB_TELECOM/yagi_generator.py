# Generador de archivo .nec parametrizado para una antena Yagi simple (driven + reflector + N directors)
# El script crea '/mnt/data/yagi.nec' con los parámetros modificables en la sección "PARÁMETROS".
# Ejecuta este script y luego descarga el archivo generado desde el enlace que aparece en la respuesta.

import math
from pathlib import Path

# ---------------------- PARÁMETROS (edítalos) ----------------------
params = {
    "freq_mhz": 144.0,            # frecuencia en MHz (cámbiala según necesites)
    "num_directors": 3,           # número de directores
    "wire_radius_m": 0.002,       # radio de alambre (m) --> diámetro ≈ 4 mm
    "segments_per_element": 11,   # segmentos por elemento (debe ser impar para alimentación centrada)
    # Longitudes relativas (fracciones de lambda)
    "reflector_length_frac": 0.52,   # reflector longitud relativa a lambda (L_reflector)
    "driven_length_frac": 0.48,      # driven (dipolo)
    "director_length_frac": 0.46,    # each director
    # Espaciados (fracciones de lambda)
    "spacing_reflector_driven_frac": 0.2,
    "spacing_driven_director_frac": 0.15,
    "spacing_between_directors_frac": 0.15,
    # coordenada Y (elementos se orientan a lo largo del eje Y, boom a lo largo de X)
    "boom_height_m": 0.0,  # si quieres elevar el centro de los elementos sobre el plano XZ (normalmente 0)
    # tags
    "reflector_tag": 1,
    "driven_tag": 2,
    "first_director_tag": 3,
}

# ---------------------- CÁLCULOS ----------------------
f = params["freq_mhz"]
wl = 300.0 / f               # longitud de onda en metros (c = 300 Mm/s)
half_wl = wl / 2.0
r = params["wire_radius_m"]
seg = params["segments_per_element"] if params["segments_per_element"] % 2 == 1 else params["segments_per_element"] + 1

# longitudes en metros (full element length)
L_ref = params["reflector_length_frac"] * wl
L_drv = params["driven_length_frac"] * wl
L_dir = params["director_length_frac"] * wl

# posiciones (x) a lo largo del boom (reflector a la izquierda, driven en x=0, directors a la derecha)
x_ref = - params["spacing_reflector_driven_frac"] * wl
x_drv = 0.0
x_positions = [x_ref, x_drv]

# primer director
x = x_drv + params["spacing_driven_director_frac"] * wl
x_positions.append(x)
for i in range(1, params["num_directors"]):
    x += params["spacing_between_directors_frac"] * wl
    x_positions.append(x)

lengths = [L_ref, L_drv] + [L_dir] * params["num_directors"]
tags = [params["reflector_tag"], params["driven_tag"]] + [params["first_director_tag"] + i for i in range(params["num_directors"])]

# ---------------------- GENERACIÓN DE LÍNEAS NEC ----------------------
lines = []
lines.append("CM Yagi parametrizada generada por script")
lines.append(f"CM Fecha: parametros: freq_mhz={f} MHz, num_directors={params['num_directors']}, wire_radius_m={r} m")
lines.append("CE")  # end comments
lines.append(f"FR 0 1 0 0 {f:.6f} 0")  # frecuencia

# GW lines for each element (elementos a lo largo del eje Y, centrados en y=0)
for tag, x_pos, L in zip(tags, x_positions, lengths):
    half = L / 2.0
    y1 = -half
    y2 =  half
    # GW: tag, segments, x1,y1,z1, x2,y2,z2, radius
    lines.append(f"GW {tag} {seg} {x_pos:.6f} {y1:.6f} {params['boom_height_m']:.6f} {x_pos:.6f} {y2:.6f} {params['boom_height_m']:.6f} {r:.6f}")

# Fuente: Excitación en el elemento driven (dipolo, centro)
driven_tag = params["driven_tag"]
driven_seg = (seg + 1) // 2  # segmento central
lines.append(f"EX 0 {driven_tag} {driven_seg} 0 1 0")  # excitación de voltaje unidad

# Plano de tierra (libre en espacio)
lines.append("GN 1")  # sin plano de tierra

# Solicitud de patrón de radiación (RP)
# RP: distancia, theta, phi, número de puntos, etc.
# Ejemplo: patrón en el plano XZ (phi=90), 37 puntos de theta de 0 a 180 grados
lines.append("RP 0 37 1 1000 0 0 0 0 90 0")

# Fin del archivo NEC
lines.append("EN")

# Escribir archivo .nec
output_path = Path("yagi.nec")
with output_path.open("w") as f:
    for line in lines:
        f.write(line + "\n")

print(f"Archivo NEC generado: {output_path.resolve()}")