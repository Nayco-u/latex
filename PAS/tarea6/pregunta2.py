# p2_impulso_linea.py
import numpy as np
import matplotlib.pyplot as plt

def delta_aprox(x, tau):
    return (1/tau) * np.where(np.abs(x/tau) < 0.5, 1, 0)

# Definimos f(x, y) = x + y - 1 (por ejemplo)
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
f = X + Y - 1
grad_f = np.sqrt(1**2 + 1**2)

for tau in [0.5, 0.2, 0.1]:
    delta_f = delta_aprox(f, tau)
    plt.figure()
    plt.imshow(delta_f, extent=[-2, 2, -2, 2], origin='lower', cmap='hot')
    plt.title(f"$\\delta(f(x,y))$ con $\\tau={tau}$")
    plt.colorbar(label="Magnitud")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(f"figs/p2_impulso_tau{tau}.png", dpi=200)

plt.show()
