import numpy as np
import p2_1
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 100)
f = np.sin(2 * np.pi * 5 * t) + 0.3 * np.random.normal(size=t.shape)
plt.plot(f)
plt.title("Senal de ejemplo")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()
plt.savefig("IEE3702/TAREA2/figs/senal_ejemplo.png")
plt.show()

pos = 50
N = 50
rf = p2_1.autocorr(f, pos, N)

plt.plot(rf)
plt.title("Autocorrelacion")
plt.xlabel("Desplazamiento")
plt.ylabel("Correlacion")
plt.grid()
plt.savefig("IEE3702/TAREA2/figs/autocorrelacion_seno.png")
plt.show()