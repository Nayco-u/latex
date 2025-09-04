import numpy as np
import p2_1
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# Cargar archivo de audio
rate, data = wav.read("IEE3702/TAREA2/data/song_for_fraser.wav")
print(f"Tasa de muestreo: {rate} Hz, Largo de la senal: {len(data)} muestras")

# Normalizar a +-1
data = data[:,0] / np.max(np.abs(data[:,0]))

# Graficar senal de audio
plt.plot(data)
plt.title("Senal de audio")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()
plt.savefig("IEE3702/TAREA2/figs/senal_audio.png")
plt.show()

# Calcular autocorrelacion
pos = 400000  # Ejemplo de posicion
N = 50000   # Largo de la ventana
rf = p2_1.autocorr(data, pos, N)

# Graficar autocorrelacion
plt.plot(rf)
plt.title("Autocorrelacion")
plt.xlabel("Desplazamiento")
plt.ylabel("Correlacion")
plt.grid()
plt.savefig("IEE3702/TAREA2/figs/autocorrelacion.png")
plt.show()