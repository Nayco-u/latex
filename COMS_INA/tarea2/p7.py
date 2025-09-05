import numpy as np
import matplotlib.pyplot as plt

# Parametros
sigma = 1.0

# funcion de densidad de probabilidad
def p(r):
    return (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2))

a, b = 0, 10  

x_vals = np.linspace(a, b, 1000)
f_max = np.max(p(x_vals))

def sample_f(n_samples):
    samples = []
    np.random.seed(0)  # Para reproducibilidad
    while len(samples) < n_samples:
        x = np.random.uniform(a, b)
        y = np.random.uniform(0, f_max)
        if y < p(x):
            samples.append(x)
    return np.array(samples)

# Simula N muestras
N = 10000
samples = sample_f(N)

print(f"Media muestral: {np.mean(samples)}")
print(f"Varianza muestral: {np.var(samples)}")
print(f"Moda muestral: {np.bincount(samples.astype(int)).argmax()}")
print(f"Mediana muestral: {np.median(samples)}")

# Grafica el histograma y la densidad teorica
plt.hist(samples, bins=50, density=True, alpha=0.5, label='Simulacion')
plt.plot(x_vals, p(x_vals), 'r-', label='Densidad teorica')
plt.legend()
plt.show()
