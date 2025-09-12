import spectrum
import pylab
import os
import numpy as np

# --- 1. Cargar la señal incognito1 ---
path = os.path.join("data", "incognito1.txt")
f = np.loadtxt(path)

# --- 2. Estimar el orden del filtro AR con AIC---
order = pylab.arange(1, 30)
rho = [spectrum.aryule(f, i, norm='biased')[1] for i in order]
aic = spectrum.AIC(len(f), rho, order)
pylab.plot(order, aic, label='AIC')
pylab.savefig("AIC_order_estimation_1")
pylab.show()

# --- 3. Determinar estimadores optimos ---
best_p = 4 # Estimado desde el grafico
print("Orden AR estimado:", best_p)

rho, sigma, coeff = spectrum.aryule(f, order=best_p)
print("Coeficientes AR:", rho)
print("Varianza del ruido:", sigma)

# --- 4. Generar señal AR con parámetros encontrados ---
n = len(f)
noise = np.random.normal(0, np.sqrt(sigma), n)
f_sim = np.zeros(n)
for i in range(best_p, n):
    f_sim[i] = -np.dot(rho, f_sim[i-best_p:i][::-1]) + noise[i]

# --- 5. Comparar autocorrelaciones ---
def autocorr(x, lags=50):
    result = np.correlate(x - np.mean(x), x - np.mean(x), mode='full')
    result = result[result.size//2:]
    return result[:lags+1] / result[0]

lags = 40
r_orig = autocorr(f, lags)
r_sim  = autocorr(f_sim, lags)

pylab.figure()
pylab.stem(range(lags+1), r_orig, linefmt='b-', markerfmt='bo', basefmt=' ')
pylab.stem(range(lags+1), r_sim, linefmt='r--', markerfmt='ro', basefmt=' ')
pylab.legend(["Original", "Simulada"])
pylab.xlabel("Lag")
pylab.ylabel("Autocorrelación")
pylab.title("Comparación autocorrelaciones")
pylab.savefig("AutoCorr_1")
pylab.show()