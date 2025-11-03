import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Parámetros de simulación
# ===============================
np.random.seed(1234)        # Semilla reproducible
Ntrials = 10000             # Número de realizaciones
Nr_list = np.arange(1, 19)  # Número de ramas (1 a 18)
gamma_bar_dB = 17.8         # SNR media por rama en dB
gamma_bar = 10**(gamma_bar_dB/10)  # Escala lineal

# ===============================
# Simulación Monte Carlo
# ===============================
G_mean = []   # Ganancia promedio (lineal)
G_std  = []   # Desviación estándar

for Nr in Nr_list:
    # Generar Ntrials realizaciones de Nr canales independientes: h ~ CN(0,1)
    h = (np.random.randn(Ntrials, Nr) + 1j*np.random.randn(Ntrials, Nr)) / np.sqrt(2)

    # Potencia instantánea combinada (sum |h_r|^2)
    sum_abs2 = np.sum(np.abs(h)**2, axis=1)

    # SNR de salida (MRC): gamma_out = gamma_bar * sum |h|^2
    gamma_out = gamma_bar * sum_abs2

    # Ganancia de arreglo (lineal)
    G = sum_abs2
    G_mean.append(np.mean(G))
    G_std.append(np.std(G)/np.sqrt(Ntrials))  # error estándar de la media

G_mean = np.array(G_mean)
G_std  = np.array(G_std)

# Curva teórica
G_theo = Nr_list
G_theo_dB = 10 * np.log10(G_theo)

# ===============================
# Resultados y Gráficas
# ===============================

plt.figure(figsize=(8,5))
plt.errorbar(Nr_list, G_mean, yerr=2*G_std, fmt='o', capsize=4, label='Simulación (media +- 2 sigma)')
plt.plot(Nr_list, G_theo, 'r--', linewidth=2, label='Teórico: G = N_r')
plt.xlabel("Número de ramas N_r")
plt.ylabel("Ganancia de arreglo promedio (lineal)")
plt.title("Ganancia de arreglo MRC - Monte Carlo")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("ganancia_lineal.png", dpi=200)

plt.figure(figsize=(8,5))
plt.plot(Nr_list, 10*np.log10(G_mean), 'bo-', label='Simulado')
plt.plot(Nr_list, G_theo_dB, 'r--', linewidth=2, label='Teórico: 10log10(N_r)')
plt.xlabel("Número de ramas N_r")
plt.ylabel("Ganancia de arreglo promedio (dB)")
plt.title("Ganancia de arreglo MRC - Escala dB")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("ganancia_dB.png", dpi=200)

print("=== Resultados promedio ===")
for i, Nr in enumerate(Nr_list):
    print(f"N_r={Nr:2d} |  G_sim={G_mean[i]:6.3f} |  G_theo={G_theo[i]:6.3f} |  error={(G_mean[i]-G_theo[i])/G_theo[i]*100:5.2f}%")

print("\nFiguras guardadas: ganancia_lineal.png y ganancia_dB.png")
