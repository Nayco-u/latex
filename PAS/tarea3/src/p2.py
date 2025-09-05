import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def autocorrelacion_fft(x, rango, sesgada=True):
    N = len(x)
    # FFT y cálculo de autocorrelación
    Xf = np.fft.fft(x, n=2*N)
    r = np.fft.ifft(np.abs(Xf)**2).real[:N]
    r = np.concatenate((r[::-1][:-1], r))

    mid = len(r) // 2
    r = r[mid + rango[0]: mid + rango[-1] + 1]

    if not sesgada:
        lag = np.arange(rango[0], rango[-1] + 1)
        r = r / (N - np.abs(lag))
    else:
        r = r / N
    return r

if __name__ == "__main__":
    # Cargar audios
    fs1, x1 = wavfile.read('PAS\\tarea3\\data\\audio.wav')
    fs2, x2 = wavfile.read('PAS\\tarea3\\data\\output.wav')

    if x1.ndim > 1:
        x1 = x1[:, 0]
    if x2.ndim > 1:
        x2 = x2[:, 0]

    x1 = x1[:100000]
    x2 = x2[:100000]

    x1 = (x1 - np.mean(x1)) / np.std(x1)
    x2 = (x2 - np.mean(x2)) / np.std(x2)

    rango = np.arange(-500, 501)

    auto_sesgada_1 = autocorrelacion_fft(x1, rango, sesgada=True)
    auto_no_sesgada_1 = autocorrelacion_fft(x1, rango, sesgada=False)
    auto_sesgada_2 = autocorrelacion_fft(x2, rango, sesgada=True)
    auto_no_sesgada_2 = autocorrelacion_fft(x2, rango, sesgada=False)

    # Autocorrelación predicha
    alpha = 0.8
    Lh = 200
    h = (1 - alpha) * alpha**np.arange(Lh+1)

    # Predicción: h * h* * rf
    rh = np.convolve(h, h[::-1], mode='full')
    rg_pred = np.convolve(rh, auto_sesgada_1, mode='full')
    rg_est = auto_no_sesgada_2
    rg_pred = rg_pred[len(rg_pred)//2 + rango[0] : len(rg_pred)//2 + rango[-1] + 1]
    error_rel = np.linalg.norm(rg_pred - rg_est) / np.linalg.norm(rg_est)
    print(f"Error relativo: {error_rel:.4f}")

    # Gráfico 1: Sesgada vs No Sesgada
    plt.figure(figsize=(10,8))

    plt.subplot(2,1,1)
    plt.plot(rango, auto_sesgada_1, label='Sesgada audio.wav')
    plt.plot(rango, auto_no_sesgada_1, label='No Sesgada audio.wav', linestyle="--")
    plt.title('Autocorrelación de audio.wav')
    plt.xlabel('Desplazamiento (muestras)')
    plt.ylabel('Autocorrelación')
    plt.legend(); plt.grid()

    plt.subplot(2,1,2)
    plt.plot(rango, auto_sesgada_2, label='Sesgada output.wav')
    plt.plot(rango, auto_no_sesgada_2, label='No Sesgada output.wav', linestyle="--")
    plt.title('Autocorrelación de output.wav')
    plt.xlabel('Desplazamiento (muestras)')
    plt.ylabel('Autocorrelación')
    plt.legend(); plt.grid()

    plt.tight_layout()
    plt.savefig('PAS\\tarea3\\data\\autocorrelacion_sesgada_vs_nosesgada.png')
    plt.show()

    # Gráfico 2: Estimada vs Predicha
    plt.figure(figsize=(8,6))
    plt.plot(rango, rg_est, label='Estimación Sesgada')
    plt.plot(rango, rg_pred, label='Predicha', linestyle="--")
    plt.title('Autocorrelación de output.wav (estimada vs predicha)')
    plt.xlabel('Desplazamiento (muestras)')
    plt.ylabel('Autocorrelación')
    plt.legend(); plt.grid()

    plt.tight_layout()
    plt.savefig('PAS\\tarea3\\data\\autocorrelacion_predicha.png')
    plt.show()