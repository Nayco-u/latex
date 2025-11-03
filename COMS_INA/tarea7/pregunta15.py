import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.fft import fft, fftshift, ifft, fftfreq

# ---------- CONFIG ----------
file_real = "trms_002_h_real_2025.txt"
file_imag = "trms_002_h_imag_2025.txt"
file_params = "trms_002_h_params_2025.txt"

# ---------- FUNCIONES ----------
def parse_params(filename):
    """Extrae parámetros básicos del archivo params."""
    params = {}
    with open(filename, 'r', encoding='utf-8') as f:
        txt = f.read()
    # Buscamos Frec. muestreo (MHz), Tasa de datos (Mbps), Modulación
    m = re.search(r"Frec\.?\s*muestreo\s*=\s*([0-9.+-eE]+)\s*\[?([^\]\n]+)?\]?", txt, re.I)
    if m:
        val = float(m.group(1))
        unit = m.group(2) or ""
        params['Fs_MHz'] = val
    m = re.search(r"Tasa de datos\s*=\s*([0-9.+-eE]+)\s*\[?([^\]\n]+)?\]?", txt, re.I)
    if m:
        params['bitrate_Mbps'] = float(m.group(1))
    m = re.search(r"Modulaci[oó]n\s*=\s*([^\n\r]+)", txt, re.I)
    if m:
        params['modulation'] = m.group(1).strip()
    m = re.search(r"Tipo de pulso\s*=\s*([^\n\r]+)", txt, re.I)
    if m:
        params['pulse'] = m.group(1).strip()
    return params

def read_vector(filename):
    """Lee un vector de texto, intentando columnas o una por línea."""
    data = np.loadtxt(filename)
    return data.flatten()

# ---------- LECTURA ----------
params = parse_params(file_params)
if 'Fs_MHz' not in params:
    raise ValueError("Error: No se pudo extraer Frecuencia de muestreo del archivo params.")
Fs = params['Fs_MHz'] * 1e6  # Hz
Ts = 1.0 / Fs

if 'bitrate_Mbps' in params:
    bitrate = params['bitrate_Mbps'] * 1e6  # bps
else:
    raise ValueError("Error: No se pudo extraer Tasa de datos del archivo params.")

if 'modulation' in params:
    mod = params['modulation']
else:
    mod = "64-QAM"  # fallback

# leer real e imag
h_real = read_vector(file_real)
h_imag = read_vector(file_imag)
if h_real.shape != h_imag.shape:
    raise ValueError("Los archivos real e imag tienen distinto largo.")
h = h_real + 1j * h_imag

N = len(h)
t = np.arange(N) * Ts  # vector tiempo (s)

# ---------- RESPUESTA EN FRECUENCIA ----------
Nfft = 2**int(np.ceil(np.log2(N)) + 6)
H = fftshift(fft(h, n=Nfft))
df = Fs / Nfft
f = fftshift(fftfreq(Nfft, d=Ts))

# ---------- PDP, retardo medio, rms ----------
P = np.abs(h)**2
P_sum = np.sum(P)
if P_sum <= 0:
    raise ValueError("PDP con energía cero.")
P_norm = P / P_sum

tau = t  # retardos en segundos
tau_mean = np.sum(tau * P_norm)
tau_rms = np.sqrt(np.sum(((tau - tau_mean)**2) * P_norm))

# ---------- Coherence bandwidth ----------
Wc_relax = 1.0 / (5.0 * tau_rms) if tau_rms > 0 else np.nan
Wc_estrict = 1.0 / (50.0 * tau_rms) if tau_rms > 0 else np.nan

# ---------- Comparación con tasa de símbolo ----------
# para 64-QAM: bits por símbolo = 6
M = None
m = re.search(r'(\d+)\s*-\s*QAM', mod.replace(" ", ""), re.I)
if m:
    M = int(m.group(1))
else:
    # si no se parsea, asumimos 64
    M = 64
bits_per_sym = int(np.log2(M))
symbol_rate = bitrate / bits_per_sym  # símbolos por segundo = baud

# ---------- Impresión y figuras ----------
print("==== RESULTADOS ====")
print(f"N muestras h(t): {N}")
print(f"Fs = {Fs/1e6:.6f} MHz, Ts = {Ts*1e9:.3f} ns")
print(f"Bitrate = {bitrate/1e6:.3f} Mbps, Modulación = {M}-QAM -> Rs = {symbol_rate/1e6:.3f} Msps")
print()
print(f"Retardo medio (mean excess delay): {tau_mean*1e9:.3f} ns")
print(f"RMS delay spread: {tau_rms*1e9:.3f} ns")
print()
print("Ancho de banda de coherencia:")
print(f" Bc (regla 1/(50*tau_rms)) = {Wc_relax/1e6 if not np.isnan(Wc_relax) else np.nan:.6f} MHz")
print(f" Bc (regla 1/(5*tau_rms)) = {Wc_estrict/1e6 if not np.isnan(Wc_estrict) else np.nan:.6f} MHz")

# --- Graficas ---
plt.figure(figsize=(10, 6))
plt.plot(t*1e9, np.abs(h), label='|h(t)|')
plt.xlabel("Retardo (ns)")
plt.ylabel("|h(t)|")
plt.title("Respuesta al impulso (magnitud)")
plt.grid(True)
plt.tight_layout()
plt.savefig("h_time_domain.png")

plt.figure(figsize=(10,6))
# magnitud de H vs frecuencia (dB)
Hmag_db = 20*np.log10(np.abs(H) + 1e-20)
plt.plot(f/1e6, Hmag_db)
plt.xlim(0, Fs/2/1e6)  # plot positive half para visual
plt.xlabel("Frecuencia (MHz)")
plt.ylabel("Magnitud H(f) (dB)")
plt.title("Respuesta en frecuencia H(f) (dB)")
plt.grid(True)
plt.tight_layout()
plt.savefig("H_freq_domain.png")