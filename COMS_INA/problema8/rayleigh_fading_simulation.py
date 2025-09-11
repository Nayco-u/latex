import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.special import j0
from math import pi
import os

# ---------------- Helper functions -----------------
def clarke_psd(f, fD, eps=1e-9):
    S = np.zeros_like(f, dtype=float)
    mask = np.abs(f) < fD
    x = f[mask] / (fD + 0.0)
    denom = np.sqrt(np.maximum(1.0 - x**2, eps))
    S[mask] = 1.0/(pi * fD * denom)
    return S

def fading_rayleigh_fd(v, fc, Ts, Td, seed=0, Nfreq=None):
    c = 3e8
    fD = (v * fc) / c
    N = int(np.round(Td / Ts))
    if Nfreq is None:
        Nfft = 1 << (int(np.ceil(np.log2(N))) + 2)
    else:
        Nfft = int(Nfreq)
    Fs = 1.0 / Ts
    freqs = np.fft.fftfreq(Nfft, d=Ts)
    S = clarke_psd(freqs, fD)
    rng = np.random.default_rng(seed)
    spec_real = rng.normal(size=Nfft)
    spec_imag = rng.normal(size=Nfft)
    spec = (spec_real + 1j*spec_imag) * np.sqrt(S/2.0)
    h_time = np.fft.ifft(np.fft.ifftshift(spec))
    h = h_time[:N]
    power = np.mean(np.abs(h)**2)
    h /= np.sqrt(power)
    t = np.arange(N) * Ts
    return h, fD, t

def plot_time_db(h, t, title):
    plt.figure()
    magdb = 20.0 * np.log10(np.abs(h) + 1e-12) # dB

    # Plot
    plt.plot(t, magdb)
    plt.xlabel("Time (s)")
    plt.ylabel("Magnitude (dB)")
    plt.title(title)
    plt.grid(True)
    plt.savefig("fading_trace.png", dpi=300)
    plt.show()

def plot_histogram_rayleigh(r, title, bins=60):
    plt.figure()

    # Histogram and Rayleigh PDF
    counts, edges = np.histogram(r, bins=bins, density=True)
    centers = 0.5*(edges[:-1] + edges[1:])
    plt.bar(centers, counts, width=edges[1]-edges[0], alpha=0.6)
    omega = np.mean(r**2)
    sigma2 = omega/2.0
    r_axis = np.linspace(0, r.max()*1.05, 400)
    pdf = (r_axis / sigma2) * np.exp(-r_axis**2 / (2.0*sigma2))

    #Plot
    plt.plot(r_axis, pdf, linewidth=2)
    plt.xlabel("Envelope |h|")
    plt.ylabel("PDF")
    plt.title(title)
    plt.grid(True)
    plt.savefig("histogram_rayleigh.png", dpi=300)
    plt.show()

def compute_mean_rms(r):
    mean_r = np.mean(r)
    rms = np.sqrt(np.mean(r**2))
    return mean_r, rms

def plot_psd_and_clarke(h, Fs, fD, title="PSD vs Clarke"):
    # Welch PSD
    f, Pxx = signal.welch(h, fs=Fs, return_onesided=False)
    f_shift = np.fft.fftshift(f)
    P_shift = np.fft.fftshift(Pxx)

    # Normalizar el área de la PSD empírica a 1
    area_emp = np.trapezoid(P_shift, f_shift)
    if area_emp > 0:
        P_shift /= area_emp

    # Clarke teórica
    f_th = np.linspace(-fD*1.2, fD*1.2, 2001)  # eje centrado en 0
    S_th = clarke_psd(f_th, fD)
    S_th /= np.trapezoid(S_th, f_th)  # normalizar área a 1

    # Plot
    plt.figure(figsize=(7,4))
    plt.semilogy(f_shift, Pxx, label="Welch PSD (empirical)")
    plt.semilogy(f_th, S_th, 'r--', linewidth=2, label="Clarke theoretical PSD")
    plt.xlim(-2*fD, 2*fD)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized PSD")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig("psd_clarke.png", dpi=300)
    plt.show()


def autocorr_empirical(h):
    N = len(h)
    R = np.zeros(N, dtype=complex)
    R = np.correlate(h, h, mode='full') / N
    R = R[N-1:]  # Keep non-negative lags
    return R

def plot_autocorr_vs_j0(h, Ts, fD, title):
    R = autocorr_empirical(h)
    lags = np.arange(len(R))
    taus = lags * Ts
    plt.figure()
    plt.plot(taus, np.real(R), label="Empirical Re{Rhh}")
    plt.plot(taus, j0(2*pi*fD*taus), linewidth=2, label="J0 theory")
    plt.xlabel("Lag (s)")
    plt.ylabel("Autocorrelation")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig("autocorr_j0.png", dpi=300)
    plt.show()

def estimate_LCR_AFD(r, Ts, Td, levels_dB=[10,20]):
    results = {}
    rms = np.sqrt(np.mean(r**2))
    omega = np.mean(r**2)
    for L in levels_dB:
        R = 10**(-L/20.0) * rms
        crossings = 0
        durations = []
        in_fade = False
        cur_len = 0
        for n in range(1, len(r)):
            if (r[n-1] > R) and (r[n] <= R):
                crossings += 1
            if r[n] < R:
                cur_len += 1
                in_fade = True
            else:
                if in_fade:
                    durations.append(cur_len * Ts)
                in_fade = False
                cur_len = 0
        if in_fade and cur_len>0:
            durations.append(cur_len * Ts)
        LCR_emp = crossings / Td
        AFD_emp = np.mean(durations) if len(durations)>0 else 0.0
        results[L] = {"R":R, "LCR_emp":LCR_emp, "AFD_emp":AFD_emp}
    return results

# ---------------- Example usage -----------------
if __name__ == "__main__":
    v = 60.0/3.6
    fc = 1.8e9
    Ts = 100e-6
    Td = 0.5
    seed = 10

    h, fD, t = fading_rayleigh_fd(v, fc, Ts, Td, seed)
    Fs = 1.0/Ts

    plot_time_db(h, t, f"Fading trace (seed={seed}, fD={fD:.2f} Hz)")

    r = np.abs(h)
    plot_histogram_rayleigh(r, "Envelope histogram vs Rayleigh PDF")
    mean_r, rms_r = compute_mean_rms(r)
    print("Empirical mean:", mean_r, "Empirical RMS:", rms_r)

    plot_psd_and_clarke(h, Fs, fD, "PSD vs Clarke")

    plot_autocorr_vs_j0(h, Ts, fD, "Autocorrelation vs J0")

    results = estimate_LCR_AFD(r, Ts, Td)
    print("LCR/AFD results:", results)
