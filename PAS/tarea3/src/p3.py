import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from p2 import autocorrelacion_fft

def correlacion_cruzada_fft(x, y, rango, sesgada=True):
    """
    Correlación cruzada de x e y
    """
    N = len(x)
    Xf = np.fft.fft(x)
    Yf = np.fft.fft(y)
    r = np.fft.ifft(Xf * np.conj(Yf)).real[:N]  # correlación cruzada
    r = np.concatenate((r[::-1][:-1], r))

    mid = len(r) // 2
    r = r[mid + rango[0]: mid + rango[-1] + 1]

    if not sesgada:
        lag = np.arange(rango[0], rango[-1] + 1)
        r = r / (N - np.abs(lag))
    else:
        r = r / N
    return r

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

# Correlaciones cruzadas
rango = np.arange(-500, 501)

cross_sesgada = correlacion_cruzada_fft(x1, x2, rango, sesgada=True)
cross_no_sesgada = correlacion_cruzada_fft(x1, x2, rango, sesgada=False)


# Parte 3b: Correlación cruzada predicha
alpha = 0.8
Lh = 200
h = (1 - alpha) * alpha**np.arange(Lh+1)

rf = autocorrelacion_fft(x1, rango, sesgada=True)
h_conj = h[::-1]
rfg_pred = np.convolve(h_conj, rf, mode="full")
mid = len(rf) // 2 + len(h) - 1
rfg_pred = rfg_pred[mid + rango[0] : mid + rango[-1] + 1]

# Error relativo
error_rel = np.linalg.norm(rfg_pred - cross_sesgada) / np.linalg.norm(cross_sesgada)
print(f"Error relativo parte 3b: {error_rel:.4f}")


# Gráfico 1: Sesgada vs No Sesgada
plt.figure(figsize=(10,6))
plt.plot(rango, cross_sesgada, label='Cruzada Sesgada f-g')
plt.plot(rango, cross_no_sesgada, label='Cruzada No Sesgada f-g', linestyle="--")
plt.title('Correlación Cruzada entrada-salida')
plt.xlabel('Desplazamiento (muestras)')
plt.ylabel('Correlación cruzada')
plt.legend(); plt.grid()

plt.tight_layout()
plt.savefig('PAS\\tarea3\\data\\correlacion_cruzada.png')
plt.show()


# Gráfico 2: Estimada vs Predicha (parte 3b)
plt.figure(figsize=(8,6))
plt.plot(rango, cross_sesgada, label='Estimación Sesgada')
plt.plot(rango, rfg_pred, label='Predicha', linestyle="--")
plt.title('Correlación Cruzada (estimada vs predicha)')
plt.xlabel('Desplazamiento (muestras)')
plt.ylabel('Correlación cruzada')
plt.legend(); plt.grid()

plt.tight_layout()
plt.savefig('PAS\\tarea3\\data\\correlacion_cruzada_predicha.png')
plt.show()
