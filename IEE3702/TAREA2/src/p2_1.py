import numpy as np

def autocorr(f, pos, N):
    
    f = np.asarray(f)
    L = len(f)

    # indices de la ventana
    start = pos - N//2
    end = pos + N//2
    
    # senal ventana con ceros si excede
    window = np.zeros(N)
    for i in range(N):
        idx = start + i
        if 0 <= idx < L:
            window[i] = f[idx]

    # autocorrelacion usando np.correlate (modo 'full')
    rf = np.correlate(window, window, mode='full')
    return rf