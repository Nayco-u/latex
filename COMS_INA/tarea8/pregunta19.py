import re
import numpy as np
import matplotlib.pyplot as plt

with open("Problema_19/diversity_003_params_2025.txt", "r") as f:
    params = {}
    for line in f:
        line = line.strip()
        if '=' in line and line:
            key, value = line.split('=', 1)
            value = value.strip()
            # Extrae el primer número (float o int) de la cadena
            match = re.search(r"[-+]?\d*\.\d+|\d+", value)
            if match:
                num_str = match.group()
                if '.' in num_str:
                    params[key.strip()] = float(num_str)
                else:
                    params[key.strip()] = int(num_str)
            else:
                params[key.strip()] = value  # Si no hay número, guarda el texto
    
with open("Problema_19/diversity_003_h_real_2025.txt", "r") as f:
    h_real = np.array([float(x) for x in f.readlines()])

with open("Problema_19/diversity_003_h_imag_2025.txt", "r") as f:
    h_imag = np.array([float(x) for x in f.readlines()])

h = h_real + 1j * h_imag

u = np.conjugate(h) / np.linalg.norm(h)

print("Pesos óptimos (u):" , u)

gamma = 10**(params['gamma_bar'] / 10) * np.abs(h)**2

print("Relación señal a ruido (gamma):", gamma)

gamma_out = 10 * np.log10(sum(gamma))

print("Relación señal a ruido de salida (gamma_out):", gamma_out)

array_gain = np.sum(np.abs(h)**2)

print("Ganancia de arreglo:", array_gain)