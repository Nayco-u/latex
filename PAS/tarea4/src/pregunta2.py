import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
import glob
import os

# --- 1. Definir carpeta donde están los archivos ---
data_path = "data/proc"  # ajusta esta ruta
fs = 100  # Hz, tasa de muestreo (ajústala según la info del curso)

# --- 2. Función para cargar archivos de una componente (EW, NS, UD) ---
def load_component_files(extension):
    files = glob.glob(os.path.join(data_path, f"*.{extension}"))
    signals = [np.loadtxt(f) for f in files]
    return signals

# --- 3. Calcular PSDs con Welch ---
def compute_psds(signals, fs, nperseg=1024):
    psds = []
    freqs = None
    for sig in signals:
        f, Pxx = welch(sig, fs=fs, nperseg=nperseg)
        psds.append(Pxx)
        freqs = f
    psds = np.array(psds)
    return freqs, psds

# --- 4. Procesar cada dirección ---
for comp in ["EW", "NS", "UD"]:
    signals = load_component_files(comp)
    freqs, psds = compute_psds(signals, fs)
    
    # PSD típica = promedio (o mediana) entre todas las señales
    psd_typical = np.mean(psds, axis=0)
    
    # Graficar ejemplos y PSD típica
    plt.figure()
    for i in range(min(3, len(psds))):  # graficar hasta 3 ejemplos
        plt.semilogy(freqs, psds[i], alpha=0.5, label=f"Ejemplo {i+1}")
    plt.semilogy(freqs, psd_typical, 'k', linewidth=2, label="PSD típica")
    plt.title(f"PSD {comp}")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("PSD [Power/Hz]")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"PSD_{comp}.png")
    plt.show()

def generate_signal_from_psd(psd_typical, freqs, N, fs):
    """
    Genera una señal sintética con PSD dada.
    psd_typical: array con la PSD típica
    freqs: frecuencias asociadas (Hz)
    N: largo de la señal deseada
    fs: frecuencia de muestreo
    """
    # --- 1. Amplitud espectral = sqrt(PSD) ---
    amp = np.sqrt(psd_typical)
    
    # --- 2. Generar fases aleatorias ---
    phases = np.exp(1j * 2 * np.pi * np.random.rand(len(freqs)))
    
    # --- 3. Espectro simétrico para ifft ---
    spectrum = amp * phases
    spectrum_full = np.concatenate([spectrum, np.conj(spectrum[-2:0:-1])])
    
    # --- 4. Transformada inversa para obtener señal en el tiempo ---
    signal = np.fft.ifft(spectrum_full).real
    
    # Ajustar longitud al tamaño N
    signal = np.tile(signal, int(np.ceil(N/len(signal))))[:N]
    return signal

# --- Generar un ejemplo de terremoto sintético ---
N = 5000  # duración en muestras
for comp in ["EW", "NS", "UD"]:
    signals = load_component_files(comp)
    freqs, psds = compute_psds(signals, fs)
    psd_typical = np.mean(psds, axis=0)
    
    synthetic = generate_signal_from_psd(psd_typical, freqs, N, fs)
    
    # Graficar señal en el tiempo
    plt.figure()
    plt.plot(synthetic)
    plt.title(f"Terremoto sintético {comp}")
    plt.xlabel("Muestra")
    plt.ylabel("Amplitud")
    plt.savefig(f"SismoSintetico_{comp}.png")
    plt.show()
    
    # Comparar PSD del sintético con la típica
    f, Pxx = welch(synthetic, fs=fs, nperseg=1024)
    plt.figure()
    plt.semilogy(freqs, psd_typical, 'k', linewidth=2, label="PSD típica")
    plt.semilogy(f, Pxx, 'r--', label="PSD sintético")
    plt.title(f"Comparación PSD {comp}")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("PSD [Power/Hz]")
    plt.legend()
    plt.savefig(f"PSD_comparacion_{comp}.png")
    plt.show()