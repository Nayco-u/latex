import os
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def parse_temperature(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, str):
        value = value.strip().lower().replace(',', '.')
        if value.endswith('k'):
            return float(value[:-1])
        if value.endswith('m'):
            return float(value[:-1]) * 1e-3
        return float(value)
    return float(value)


def gaussian_1d(x, amplitude, x0, sigma, offset):
    return amplitude * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + offset


def fit_gaussian_1d(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    valid = np.isfinite(x) & np.isfinite(y)
    x = x[valid]
    y = y[valid]
    if x.size < 4:
        raise ValueError('Not enough valid points for fitting')

    amplitude_guess = np.max(y) - np.min(y)
    offset_guess = np.min(y)
    x0_guess = x[np.argmax(y)]
    sigma_guess = max(np.ptp(x) / 4.0, 1e-3)
    p0 = [amplitude_guess, x0_guess, sigma_guess, offset_guess]

    popt, pcov = curve_fit(gaussian_1d, x, y, p0=p0, maxfev=10000)
    return popt, pcov


def load_dataset(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Archivo no encontrado: {file_path}')

    df = pd.read_csv(file_path)
    if 'T' not in df.columns:
        raise ValueError(f'Columna T no encontrada en {file_path}')

    df['T'] = df['T'].apply(parse_temperature)
    return df


def plot_scan(file_path, x_col, title, filename, correct_by=None):
    df = load_dataset(file_path)
    if x_col not in df.columns:
        raise ValueError(f'Columna {x_col} no encontrada en {file_path}')

    x_values = df[x_col].astype(float).to_numpy()
    if correct_by:
        if correct_by not in df.columns:
            raise ValueError(f'Columna de corrección {correct_by} no encontrada en {file_path}')
        correction = np.cos(np.radians(df[correct_by].astype(float).to_numpy()))
        x_values = x_values * correction

    y_values = df['T'].to_numpy()

    popt, _ = fit_gaussian_1d(x_values, y_values)
    amplitude, x0, sigma, offset = popt
    fwhm = 2.355 * sigma

    print(f'Fit results para {title}:')
    print(f'  Amplitud: {amplitude:.4f}')
    print(f'  Centro: {x0:.4f}')
    print(f'  Sigma: {sigma:.4f}')
    print(f'  Offset: {offset:.4f}')
    print(f'  FWHM: {fwhm:.4f}\n')

    x_fit = np.linspace(np.min(x_values), np.max(x_values), 300)
    y_fit = gaussian_1d(x_fit, *popt)

    plt.figure(figsize=(8, 5))
    plt.scatter(x_values, y_values, c='tab:blue', edgecolor='k', s=60, label='Datos')
    plt.plot(x_fit, y_fit, 'r-', linewidth=2, label='Ajuste Gaussiano')
    plt.axvline(x0, color='gray', linestyle='--', label=f'Centro = {x0:.2f}')
    plt.xlabel(x_col)
    plt.ylabel('Temperatura [K]')
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


if __name__ == '__main__':
    plot_scan(
        'az_data.csv',
        x_col='Daz',
        title='Azimuth Beamwidth',
        filename='azimuth_fit.png',
        correct_by='el'
    )

    plot_scan(
        'el_data.csv',
        x_col='Del',
        title='Elevation Beamwidth',
        filename='elevation_fit.png',
    )
