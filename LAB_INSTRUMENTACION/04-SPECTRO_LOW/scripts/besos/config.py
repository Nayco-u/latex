"""Configuración central: rutas, parámetros del instrumento, fuentes e identificación de líneas.

Todo lo que es "dato de entrada" vive aquí; el resto de los módulos son genéricos.
"""
from pathlib import Path

# ----------------------------------------------------------------------------- rutas
ROOT = Path(__file__).resolve().parents[2]          # .../04-SPECTRO_LOW


def _raw_dir() -> Path:
    """Busca la carpeta de la sesión, ya sea en datos/ o en la raíz."""
    for cand in (ROOT / "datos" / "2026-10-06", ROOT / "2026-10-06"):
        if any(cand.rglob("*.fits")):
            return cand
    raise FileNotFoundError("No se encontraron FITS en datos/2026-10-06 ni en 2026-10-06")


RAW_DIR = _raw_dir()
FIG_DIR = ROOT / "figuras"
RES_DIR = ROOT / "resultados"
TEX_DIR = ROOT / "informe" / "generado"       # tablas y macros \newcommand para el informe

# ----------------------------------------------------------------------- detector
CAMERA = "DMK 41AU02.AS (Sony ICX205AL, CCD)"
PIXEL_UM = 4.65                 # tamaño de píxel [µm]
NX, NY = 1280, 960
BIAS_ROWS = (0, 100)            # filas sin luz, usadas para estimar el nivel de fondo
EXTRACT_ROWS = (450, 550)       # filas (a lo largo de la rendija) que se promedian: zona de mejor foco
ROW_BANDS = [(y, y + 50) for y in range(250, 800, 50)]   # bandas para estudiar el FWHM a lo largo de la rendija

# ------------------------------------------------------------- óptica (diseño BESOS)
OPTICS = dict(
    f_col=30.0,        # colimador E [mm]
    f_cam=40.0,        # cámara B [mm]
    slit_um=25.0,      # ancho de rendija [µm]
    apex_deg=60.0,     # ángulo del prisma
    prism_base=15.0,   # base del prisma [mm]
    glass="SF18",
    # Sellmeier SF18 (Schott, catálogo antiguo), λ en µm
    sellmeier_B=(1.56441, 0.291414, 0.960308),
    sellmeier_C=(0.0121864, 0.0535568, 111.451),
)

# ------------------------------------------------------------------------- fuentes
# folder: subcarpeta en RAW_DIR; color: color de los gráficos.
LEDS = {
    "Blue LED":  dict(folder="blue",      lam_nom=465.0, color="#1f4fd1"),
    "Green LED": dict(folder="green_150", lam_nom=525.0, color="#1b9e3e"),
    "Red LED":  dict(folder="red",       lam_nom=625.0, color="#d62728"),
}
LED_LAM_ERR = 10.0   # incertidumbre asumida de la λ nominal de los LEDs [nm]

FLASH = dict(folder="espect", label="Phone flash", color="#444444")
RANGE_THRESHOLD = 0.05   # fracción del máximo que define los bordes del rango espectral

# Trazado de la curvatura de las líneas: (fuente, x aproximada de una línea brillante)
TRACE = dict(folder="lamp2", x_guess=1081)

# Lámparas espectrales. Cada rasgo = (x_aprox [px], [λ de laboratorio en aire, nm], usar_en_calibración)
# Los rasgos con varias λ son mezclas no resueltas: se ajustan pero no se usan para calibrar.
# λ: NIST Atomic Spectra Database (Ar I, Kr I).
LAMPS = {
    "Kr": dict(folder="lamp2", label="Kr lamp", color="#6b6b6b", features=[
        (874.2,  [557.029], True),
        (920.5,  [587.092], True),
        (1081.0, [758.741, 760.155], False),
        (1110.0, [810.437, 811.290], False),
        (1119.0, [826.324, 829.811], False),
        (1141.0, [877.675], True),
        (1146.0, [892.869], True),
    ]),
    "Ar": dict(folder="lamp", label="Ar lamp", color="#d4a017", features=[
        (1037.0, [696.543], True),
        (1045.0, [706.722], True),
        (1084.0, [763.511, 772.376], False),
        (1110.0, [800.616, 801.479, 810.369, 811.531], False),
        (1125.0, [840.821, 842.465], False),
        (1154.0, [912.297, 922.450], False),
        (1172.0, [965.779], True),
    ]),
}
GROUP_GAP_PX = 16      # rasgos más cercanos que esto se ajustan juntos (multi-gaussiana)
