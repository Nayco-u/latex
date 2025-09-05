import numpy as np
import sympy as sp

# Definición de variables simbólicas
r, d = sp.symbols('r d')

# Matrices elementales
P = sp.Matrix([[1, d], [0, 1]])  # Propagación libre
L = sp.Matrix([[1, 0], [-2/r, 1]])  # Espejo esférico

# Matriz total del sistema
M = P * L * P * L
M = sp.simplify(M)

# Mostrar la matriz resultante
print(sp.latex(M))