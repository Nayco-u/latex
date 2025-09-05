import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

audio_path = os.path.join('PAS','tarea3', 'data', 'audio.wav')
fs, data = wavfile.read(audio_path)

if data.ndim > 1:
    data = data[:, 0]

# Normalizar la señal
data = data.astype(np.float64)
data = (data - np.mean(data)) / np.std(data)

# Definir h(n)
a = 0.8
N = 200
n = np.arange(N)
h = (1 - a) * (a ** n)

# Convolución con FFT
L = len(data) + len(h) - 1
data_fft = np.fft.fft(data, n=L)
h_fft = np.fft.fft(h, n=L)
y_fft = data_fft * h_fft
y = np.fft.ifft(y_fft).real
y = y[:len(data)]
t_y = np.arange(len(y)) / fs

# Reproducir la salida
output_path = os.path.join('PAS','tarea3', 'data', 'output.wav')
wavfile.write(output_path, fs, y.astype(np.float32))