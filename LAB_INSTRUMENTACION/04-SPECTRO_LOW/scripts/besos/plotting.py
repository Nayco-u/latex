"""Simple, consistent figures for the report (vector PDF + PNG preview).

Sizes follow the IEEEtran two-column layout: W1 = one column, W2 = full page width.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "0.88", "grid.linewidth": 0.6, "lines.linewidth": 1.3,
    "savefig.bbox": "tight", "savefig.dpi": 220, "legend.frameon": False,
})
W1, W2 = 3.45, 7.0     # [in]
INK = "0.25"
C_DESIGN = "#c44e52"


def save(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"))
    plt.close(fig)


def raw_images(images, titles, path, vmax=80):
    """Grid of combined raw frames."""
    n = len(images)
    cols = 3
    rows = int(np.ceil(n / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(W2, 1.6 * rows), sharex=True, sharey=True)
    for ax, im, t in zip(axs.flat, images, titles):
        ax.imshow(im, cmap="gray", vmin=0, vmax=vmax, origin="upper")
        ax.set_title(t, fontsize=8)
        ax.grid(False)
    for ax in axs.flat[n:]:
        ax.axis("off")
    for ax in axs[:, 0]:
        ax.set_ylabel("y [px]")
    for ax in axs[-1]:
        ax.set_xlabel("x [px]")
    save(fig, path)


def curvature(img, img_rect, ys, xs, coef, path, xlim=(1000, 1180), vmax=120):
    """Kr lines before and after rectification, with the traced centroids."""
    fig, axs = plt.subplots(1, 2, figsize=(W1, 1.9), sharey=True)
    for ax, im, t in zip(axs, (img, img_rect), ("(a) Raw", "(b) Rectified")):
        ax.imshow(im, cmap="gray", vmin=0, vmax=vmax, aspect="auto")
        ax.set_xlim(*xlim)
        ax.set_title(t, fontsize=8)
        ax.set_xlabel("x [px]")
        ax.grid(False)
    yy = np.arange(ys.min() - 30, ys.max() + 30)
    axs[0].plot(xs, ys, ".", ms=1.5, color="#e8590c", label="centroids")
    axs[0].plot(np.polyval(coef, yy), yy, "-", lw=0.9, color="#4c9be8", label="quadratic fit")
    axs[0].set_ylim(img.shape[0], 0)
    axs[0].set_ylabel("y [px]")
    axs[0].legend(loc="upper left", fontsize=6, handlelength=1, frameon=True, facecolor="white", framealpha=0.85)
    save(fig, path)


def fwhm_rows(yc, fw, extract_rows, path):
    """FWHM of isolated Kr lines along the slit."""
    fig, ax = plt.subplots(figsize=(W1, 1.8))
    ax.axvspan(*extract_rows, color="#4c72b0", alpha=0.12, label="extracted rows")
    shades = ["#222222", "#555555", "#888888", "#b0b0b0"]
    for (lam, v), c, mk in zip(sorted(fw.items()), shades, "osD^"):
        ax.plot(yc, v, "-", marker=mk, ms=3, lw=0.9, color=c, label=f"Kr {lam:.1f} nm")
    ax.set_xlabel("Row (band centre), y [px]")
    ax.set_ylabel("FWHM [px]")
    ax.legend(ncol=2, fontsize=6)
    save(fig, path)


def lines_gaussians(series, path, xlim=(420, 990)):
    """Normalized profiles (faint) and Gaussian fits (solid) vs wavelength, one plot.

    series: list of dict(label, color, lam, flux, norm, style, segments=[(lam_model, model), ...])."""
    fig, ax = plt.subplots(figsize=(W2, 2.2))
    for s in series:
        norm = s["norm"]
        if s.get("style", ".") == ".":
            ax.plot(s["lam"], s["flux"] / norm, ".", ms=1.5, color=s["color"], alpha=0.35)
        else:
            ax.plot(s["lam"], s["flux"] / norm, "-", lw=0.6, color=s["color"], alpha=0.35)
        for k, (lm, m) in enumerate(s["segments"]):
            ax.plot(lm, m / norm, "-", color=s["color"], label=s["label"] if k == 0 else None)
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.03, 1.08)
    ax.set_xlabel(r"$\lambda$ [nm]")
    ax.set_ylabel("Normalized intensity")
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.15), handlelength=1.5)
    save(fig, path)


def flash(lam, flux, lam_lo, lam_hi, thr, path):
    fig, ax = plt.subplots(figsize=(W1, 1.9))
    f = flux / np.max(flux)
    ax.plot(lam, f, color=INK)
    ax.axhline(thr, color="0.6", lw=0.7, ls="--")
    ax.text(805, thr + 0.03, f"{thr:.0%}", fontsize=6.5, color="0.4", ha="right")
    ax.axvspan(lam_lo, lam_hi, color="#4c72b0", alpha=0.08)
    for v, ha, dx in ((lam_lo, "left", 4), (lam_hi, "right", -4)):
        ax.axvline(v, color="#4c72b0", lw=0.9)
        ax.text(v + dx, 1.02, f"{v:.0f} nm", ha=ha, fontsize=7, color="#4c72b0")
    ax.set_xlim(380, 810)
    ax.set_ylim(-0.02, 1.12)
    ax.set_xlabel(r"$\lambda$ [nm]")
    ax.set_ylabel("Normalized intensity")
    save(fig, path)


def calibration(x_cal, lam_cal, colors, labels, x_grid, lam_grid, res, x_val, lam_val, val_colors, path):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(W1, 2.7), sharex=True, gridspec_kw=dict(height_ratios=[3, 1.3]))
    a1.plot(x_grid, lam_grid, "-", color=INK, lw=1, label="Hartmann fit")
    seen = set()
    for x, l, c, lab in zip(x_cal, lam_cal, colors, labels):
        a1.plot(x, l, "o", ms=4, mfc=c, mec="white", mew=0.5, label=lab if lab not in seen else None)
        seen.add(lab)
    for x, l, c in zip(x_val, lam_val, val_colors):
        a1.errorbar(x, l, yerr=10, fmt="s", ms=3.5, color=c, mfc="white", capsize=1.5, lw=0.7)
    a1.plot([], [], "s", mfc="white", mec="0.3", ms=3.5, label="LEDs (check, ±10 nm)")
    a1.set_ylabel(r"$\lambda$ [nm]")
    a1.legend(loc="upper left")
    a2.axhline(0, color="0.6", lw=0.7)
    for x, r, c in zip(x_cal, res, colors):
        a2.plot(x, r, "o", ms=3.5, mfc=c, mec="white", mew=0.5)
    a2.set_ylabel("Resid. [nm]")
    a2.set_xlabel("x [px]")
    save(fig, path)


def dispersion(lam, meas, theo, lam_pts, pts, pts_colors, path, theo_label):
    fig, ax = plt.subplots(figsize=(W1, 2.0))
    ax.plot(lam, meas, color=INK, label="Measured (calibration)")
    ax.plot(lam, theo, "--", color=C_DESIGN, label=theo_label)
    ax.scatter(lam_pts, pts, s=14, c=pts_colors, edgecolors="white", linewidths=0.5, zorder=3)
    ax.set_xlabel(r"$\lambda$ [nm]")
    ax.set_ylabel(r"$P=|d\lambda/dx|$ [nm/px]")
    ax.legend(loc="upper left")
    save(fig, path)


def resolution(lam_pts, R_pts, R_err, colors, lam, R_theo, path, theo_label):
    fig, ax = plt.subplots(figsize=(W1, 2.0))
    ax.plot(lam, R_theo, "--", color=C_DESIGN, label=theo_label)
    for l, r, e, c in zip(lam_pts, R_pts, R_err, colors):
        ax.errorbar(l, r, yerr=e, fmt="o", ms=4, color=c, mec="white", mew=0.5, capsize=1.5, lw=0.7)
    ax.plot([], [], "o", color="0.4", ms=4, label="Measured (Kr, Ar lines)")
    ax.set_xlabel(r"$\lambda$ [nm]")
    ax.set_ylabel(r"$R=\lambda/\Delta\lambda$")
    ax.set_ylim(top=max(R_theo.max(), max(R_pts)) * 1.35)
    ax.legend(loc="upper right")
    save(fig, path)
