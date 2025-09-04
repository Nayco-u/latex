import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

def densidad_espectral(data, rate, filename):
    # Calcular la densidad espectral
    freqs, psd = plt.psd(data, NFFT=1024, Fs=rate)
    plt.title("Densidad espectral")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Densidad espectral (dB/Hz)")
    plt.grid()
    plt.savefig(filename)
    plt.show()
    return freqs, psd

if __name__ == "__main__":
    # Ejemplo con seno ruidoso
    f = 440  # Frecuencia en Hz
    fs = 44100  # Frecuencia de muestreo
    t = np.linspace(0, 1, fs)
    ruido = np.random.normal(0, 0.5, t.shape)
    senal = np.sin(2 * np.pi * f * t) + ruido

    densidad_espectral(senal, fs, "IEE3702/TAREA2/figs/densidad_espectral_seno.png")

    # Ejemplo con audio
    rate, data = wav.read("IEE3702/TAREA2/data/song_for_fraser.wav")
    data = data[:,0] / np.max(np.abs(data[:,0]))
    densidad_espectral(data, rate, "IEE3702/TAREA2/figs/densidad_espectral_audio.png")
