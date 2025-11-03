import numpy as np
from scipy import integrate, optimize
from math import sin, pi
from scipy.special import erfc, erfcinv

P_b = 1e-3
Q_inv = erfcinv(P_b)
print("Q_inv:", Q_inv)
gamma_awgn = (Q_inv**2)/2   # lineal

def Pb_mrc_avg(Nr, gamma_bar):
    # integrand for the formula
    integrand = lambda theta: (1.0 + gamma_bar/(sin(theta)**2))**(-Nr)
    val, _ = integrate.quad(integrand, 0, pi/2, limit=200)
    return (1.0/pi) * val

def Pb_sc_avg(L, gamma_bar):
    # integrand for the formula
    integrand = lambda theta: erfc(np.sqrt(2 * theta)) * L * np.exp(-theta/gamma_bar) / gamma_bar * (1 - np.exp(-theta/gamma_bar))**(L-1)
    val, _ = integrate.quad(integrand, 0, pi/2, limit=200)
    return val

# find gamma_bar such that Pb_mrc_avg(Nr, gamma_bar)=1e-3
def find_gamma_for_target(Nr, target=1e-3):
    # search in gamma_bar in linear scale
    lo, hi = 1e-4, 1e2
    for _ in range(50):
        mid = (lo+hi)/2
        pb = Pb_mrc_avg(Nr, mid)
        if pb > target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

def find_gamma_sc_for_target(L, target=1e-3):
    # search in gamma_bar in linear scale
    lo, hi = 1e-4, 1e2
    for _ in range(50):
        mid = (lo+hi)/2
        pb = Pb_sc_avg(L, mid)
        if pb > target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

for Nr in range(1,9):
    gamma_req = find_gamma_for_target(Nr, 1e-3)
    print("Nr", Nr, "gamma_req (dB):", 10*np.log10(gamma_req))
    if gamma_req < gamma_awgn:
        print(" -> MRC with Nr={} needs lower SNR than AWGN reference".format(Nr))
        break

for L in range(1,9):
    gamma_req_sc = find_gamma_sc_for_target(L, 1e-3)
    print("L", L, "gamma_req_sc (dB):", 10*np.log10(gamma_req_sc))
    if gamma_req_sc < gamma_awgn:
        print(" -> SC with L={} needs lower SNR than AWGN reference".format(L))
        break

print("AWGN needed (dB):", 10*np.log10(gamma_awgn))
