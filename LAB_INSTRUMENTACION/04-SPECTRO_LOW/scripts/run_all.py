"""Pipeline completo de reducción del espectrógrafo BESOS.

Uso:  python3 scripts/run_all.py

  1. Imágenes combinadas (mediana) de cada fuente.
  2. Curvatura de las líneas: traza de una línea de Kr y rectificación.
  3. Espectros 1D (filas de mejor foco).
  4. Ajuste gaussiano de las líneas de las lámparas (Kr, Ar) y de los LEDs.
  5. Calibración λ(x) con la fórmula de Hartmann (solo líneas aisladas).
  6. Dispersión, resolución y rango medidos.
  7. Modelo teórico de primer orden y comparación.
  8. Figuras (figuras/), CSV (resultados/), tablas y macros LaTeX (informe/generado/).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from besos import calibration as cal  # noqa: E402
from besos import config as cfg  # noqa: E402
from besos import extract, fitting, geometry, io, plotting, prism, report  # noqa: E402


def fmt(v, d=1, sign=False):
    """Número para LaTeX (punto decimal, signo menos tipográfico)."""
    s = f"{v:+.{d}f}" if sign else f"{v:.{d}f}"
    return "$-$" + s[1:] if s.startswith("-") else s


# ------------------------------------------------------------------ 1-3. reducción
def reduce_sources():
    folders = {k: v["folder"] for k, v in cfg.LEDS.items()}
    folders.update({k: v["folder"] for k, v in cfg.LAMPS.items()})
    folders["Flash"] = cfg.FLASH["folder"]
    masters = {k: io.master(f) for k, f in folders.items()}

    ref = masters[next(k for k, f in folders.items() if f == cfg.TRACE["folder"])]
    coef, ys, xs, rms = geometry.trace_line(ref, cfg.TRACE["x_guess"])
    y_ref = float(np.mean(cfg.EXTRACT_ROWS))       # las posiciones x quedan referidas a esta fila
    rect = {k: geometry.rectify(m, coef, y_ref) for k, m in masters.items()}
    spectra = {k: extract.spectrum_1d(r) for k, r in rect.items()}
    trace = dict(coef=coef, ys=ys, xs=xs, rms=rms,
                 sagitta=float(np.ptp(np.polyval(coef, np.arange(250, 800)))),
                 tilt=geometry.tilt_deg(coef, cfg.EXTRACT_ROWS))
    return folders, masters, rect, spectra, trace


def fwhm_along_slit(rect):
    """FWHM de líneas aisladas de Kr en bandas de filas (dónde está el mejor foco)."""
    feats = [f for f in cfg.LAMPS["Kr"]["features"] if f[2]]
    out = {f[1][0]: [] for f in feats}
    centers = []
    xs = np.array([f[0] for f in feats])
    for band in cfg.ROW_BANDS:
        x, y, _ = extract.spectrum_1d(rect["Kr"], band)
        centers.append(np.mean(band))
        for grp in fitting.group_positions(xs, cfg.GROUP_GAP_PX):
            comps, _ = fitting.fit_gaussians(x, y, xs[grp], half_win=9, sigma_max=7.0)
            for i, c in zip(grp, comps):
                out[feats[i][1][0]].append(c["fwhm"])
    return np.array(centers), {k: np.array(v) for k, v in out.items()}


# ------------------------------------------------------------- 4. ajustes gaussianos
def fit_lamps(spectra):
    rows = []
    for lamp, d in cfg.LAMPS.items():
        x, y, _ = spectra[lamp]
        feats = d["features"]
        xs = np.array([f[0] for f in feats])
        for grp in fitting.group_positions(xs, cfg.GROUP_GAP_PX):
            comps, _ = fitting.fit_gaussians(x, y, xs[grp], half_win=9, sigma0=2.0, sigma_max=7.0, max_shift=4.0)
            for i, c in zip(grp, comps):
                rows.append(dict(lamp=lamp, lams=feats[i][1], use=feats[i][2], **c))
    return rows


def fit_leds(spectra):
    out = {}
    for led in cfg.LEDS:
        x, y, _ = spectra[led]
        comps, _ = fitting.fit_gaussians(x, y, [float(np.argmax(y))], half_win=90, sigma0=20,
                                         sigma_max=80, max_shift=30)
        out[led] = comps[0]
    return out


def main():
    folders, masters, rect, spectra, trace = reduce_sources()
    logs = {k: io.read_log(f) for k, f in folders.items()}
    sat_flash = io.saturated_fraction(cfg.FLASH["folder"])
    yc, fw_rows = fwhm_along_slit(rect)

    # --------------------------------------------------------- 5. calibración
    lines = fit_lamps(spectra)
    leds = fit_leds(spectra)
    used = [l for l in lines if l["use"]]
    sol = cal.fit([l["mu"] for l in used], [l["lams"][0] for l in used])
    for l in lines:
        l["lam_fit"] = float(cal.wavelength(l["mu"], sol))
        l["disp"] = float(cal.dispersion(l["mu"], sol))
        l["dlam"] = l["fwhm"] * l["disp"]
        l["dlam_err"] = l["fwhm_err"] * l["disp"]
        l["R"] = l["lams"][0] / l["dlam"]
        l["R_err"] = l["R"] * l["dlam_err"] / l["dlam"]
    for d in leds.values():
        d["lam"] = float(cal.wavelength(d["mu"], sol))
        d["lam_err"] = float(cal.wavelength_err(d["mu"], sol)[0])
        d["fwhm_nm"] = d["fwhm"] * float(cal.dispersion(d["mu"], sol))

    # ------------------------------------------------------------- 6. rango
    xf, ff, _ = spectra["Flash"]
    lam_f = cal.wavelength(xf, sol)
    ok = xf < sol["p"][2] - 60            # lejos del polo de la fórmula de Hartmann
    fn = ff / ff[ok].max()
    above = np.where(ok & (fn >= cfg.RANGE_THRESHOLD))[0]
    lam_lo, lam_hi = float(lam_f[above.min()]), float(lam_f[above.max()])
    lam_det_lo = float(cal.wavelength(0, sol))
    lam_last = max(l["lams"][0] for l in used)

    # ------------------------------------------------------- 7. modelo teórico
    o = cfg.OPTICS
    width = cfg.NX * cfg.PIXEL_UM / 1e3
    P = prism.Prism(o["sellmeier_B"], o["sellmeier_C"], o["apex_deg"], lam_c=550.0)
    lam_grid = np.arange(440, 970, 1.0)
    perf = lambda pr, fcol=o["f_col"], fcam=o["f_cam"]: prism.performance(   # noqa: E731
        pr, lam_grid, fcol, fcam, o["slit_um"], cfg.PIXEL_UM, o["prism_base"])
    th = perf(P)
    meas_disp = cal.dispersion(cal.pixel(lam_grid, sol), sol)
    ratio = meas_disp / th["recip_nm_px"]                       # P_med / P_diseño
    f_eff = float(o["f_cam"] / np.median(ratio))
    lam_th_lo, lam_th_hi = prism.detector_range(P, o["f_cam"], width, 550)

    # Hipótesis: prisma fuera de desviación mínima (θ1 mayor). Se busca el θ1 cuya
    # imagen anamórfica de la rendija iguala el FWHM medido de las líneas de Kr.
    fwhm_kr = float(np.median([l["fwhm"] for l in used if l["lamp"] == "Kr"]))
    thetas = np.arange(np.degrees(P.theta1), 85, 0.1)
    img_px = np.array([perf(prism.Prism(o["sellmeier_B"], o["sellmeier_C"], o["apex_deg"], theta1_deg=t))
                       ["slit_img_px"][110] for t in thetas])          # a 550 nm
    t_off = float(thetas[np.argmin(np.abs(img_px - fwhm_kr))])
    P_off = prism.Prism(o["sellmeier_B"], o["sellmeier_C"], o["apex_deg"], theta1_deg=t_off)
    th_off = perf(P_off)
    ratio_off = float(np.median(meas_disp / th_off["recip_nm_px"]))

    # ================================================================ figuras
    F = cfg.FIG_DIR
    plotting.curvature(masters["Kr"], rect["Kr"], trace["ys"], trace["xs"], trace["coef"],
                       F / "curvatura_lineas.pdf")
    plotting.fwhm_rows(yc, fw_rows, cfg.EXTRACT_ROWS, F / "fwhm_vs_fila.pdf")
    order = ["Blue LED", "Green LED", "Red LED", "Flash", "Kr", "Ar"]
    titles = {"Flash": "Phone flash", "Kr": "Kr lamp", "Ar": "Ar lamp"}
    plotting.raw_images([masters[k] for k in order], [titles.get(k, k) for k in order],
                        F / "imagenes_crudas.pdf")

    series = []
    for led, d in cfg.LEDS.items():
        x, y, _ = spectra[led]
        c = leds[led]
        sl = slice(int(c["mu"] - 3 * c["fwhm"]), int(c["mu"] + 3 * c["fwhm"]))
        xm = np.linspace(sl.start, sl.stop, 600)
        series.append(dict(label=led, color=d["color"], lam=cal.wavelength(x[sl], sol), flux=y[sl],
                           norm=y[sl].max(), style=".",
                           segments=[(cal.wavelength(xm, sol), fitting.gaussian(xm, c["amp"], c["mu"], c["sigma"]))]))
    for lamp, d in cfg.LAMPS.items():
        x, y, _ = spectra[lamp]
        xm = np.linspace(850, 1180, 3000)
        m = sum(fitting.gaussian(xm, l["amp"], l["mu"], l["sigma"]) for l in lines if l["lamp"] == lamp)
        sl = slice(850, 1180)
        series.append(dict(label=d["label"], color=d["color"], lam=cal.wavelength(x[sl], sol), flux=y[sl],
                           norm=y[sl].max(), style="-", segments=[(cal.wavelength(xm, sol), m)]))
    plotting.lines_gaussians(series, F / "gaussianas_leds_lamparas.pdf")
    plotting.flash(lam_f[ok], ff[ok], lam_lo, lam_hi, cfg.RANGE_THRESHOLD, F / "flash_rango.pdf")

    xg = np.linspace(0, 1180, 600)
    plotting.calibration(
        [l["mu"] for l in used], [l["lams"][0] for l in used],
        [cfg.LAMPS[l["lamp"]]["color"] for l in used], [cfg.LAMPS[l["lamp"]]["label"] for l in used],
        xg, cal.wavelength(xg, sol), sol["res"],
        [leds[k]["mu"] for k in cfg.LEDS], [cfg.LEDS[k]["lam_nom"] for k in cfg.LEDS],
        [cfg.LEDS[k]["color"] for k in cfg.LEDS], F / "calibracion.pdf")
    lab_th = r"First order, design ($f_{col}$=30, $f_{cam}$=40 mm)"
    cols_used = [cfg.LAMPS[l["lamp"]]["color"] for l in used]
    plotting.dispersion(lam_grid, meas_disp, th["recip_nm_px"], [l["lams"][0] for l in used],
                        [l["disp"] for l in used], cols_used, F / "dispersion.pdf", lab_th)
    plotting.resolution([l["lams"][0] for l in used], [l["R"] for l in used], [l["R_err"] for l in used],
                        cols_used, lam_grid, th["R"], F / "resolucion.pdf", lab_th)

    # ================================================================ CSV
    report.write_csv("lineas_lamparas.csv",
                     [[l["lamp"], "/".join(f"{v:.3f}" for v in l["lams"]), int(l["use"]), f"{l['mu']:.2f}",
                       f"{l['mu_err']:.2f}", f"{l['fwhm']:.2f}", f"{l['fwhm_err']:.2f}", f"{l['lam_fit']:.2f}",
                       f"{l['disp']:.4f}", f"{l['dlam']:.3f}", f"{l['R']:.1f}"] for l in lines],
                     ["lamp", "lambda_lab_nm", "calibration", "x_px", "x_err", "fwhm_px", "fwhm_err",
                      "lambda_fit_nm", "disp_nm_px", "dlambda_nm", "R"])
    report.write_csv("leds.csv", [[k, cfg.LEDS[k]["lam_nom"], f"{d['mu']:.2f}", f"{d['lam']:.2f}",
                                   f"{d['fwhm']:.2f}", f"{d['fwhm_nm']:.2f}"] for k, d in leds.items()],
                     ["led", "lambda_nom_nm", "x_px", "lambda_meas_nm", "fwhm_px", "fwhm_nm"])
    report.write_csv("teoria.csv", np.c_[lam_grid, th["recip_nm_px"], th["slit_img_px"], th["dlam"], th["R"],
                                         meas_disp].round(4).tolist(),
                     ["lambda_nm", "P_design_nm_px", "slit_img_px", "dlam_design_nm", "R_design", "P_meas_nm_px"])

    # ================================================================ tablas LaTeX
    report.write_table(
        "tab_lines.tex",
        ["Lamp", r"$\lambda_{\rm lab}$", "$x$ [px]", "Resid.", "FWHM [px]", "$P$ [nm/px]",
         r"$\Delta\lambda$ [nm]", "$R$"],
        [[l["lamp"], fmt(l["lams"][0], 1), fmt(l["mu"], 1), fmt(l["lams"][0] - l["lam_fit"], 2, sign=True),
          fmt(l["fwhm"], 1), fmt(l["disp"], 2), rf"{fmt(l['dlam'], 1)}$\pm${fmt(l['dlam_err'], 1)}",
          f"{l['R']:.0f}"] for l in sorted(used, key=lambda r: r["lams"][0])],
        "@{}lrrrrrrr@{}")
    report.write_table(
        "tab_leds.tex", ["Source", r"$\lambda_{\rm nom}$", r"$\lambda_{\rm meas}$ [nm]", "FWHM [nm]"],
        [[k, f"{cfg.LEDS[k]['lam_nom']:.0f}", rf"{fmt(d['lam'], 1)}$\pm${fmt(d['lam_err'], 1)}",
          fmt(d["fwhm_nm"], 1)] for k, d in leds.items()], "@{}lccc@{}")

    def at(arr, lam):
        return float(np.interp(lam, lam_grid, arr))

    def meas_at(lam):
        return float(cal.dispersion(cal.pixel(lam, sol), sol))

    kr = {l["lams"][0]: l for l in used if l["lamp"] == "Kr"}
    r557, r878 = kr[557.029], kr[877.675]
    summary = [
        [r"$P$ at 500 nm [nm/px]", fmt(at(th["recip_nm_px"], 500), 2), fmt(meas_at(500), 2)],
        [r"$P$ at 600 nm [nm/px]", fmt(at(th["recip_nm_px"], 600), 2), fmt(meas_at(600), 2)],
        [r"$P$ at 800 nm [nm/px]", fmt(at(th["recip_nm_px"], 800), 2), fmt(meas_at(800), 2)],
        ["Slit image FWHM [px]", fmt(at(th["slit_img_px"], 550), 1), fmt(fwhm_kr, 1)],
        [r"$\Delta\lambda$ at 557 nm [nm]", fmt(at(th["dlam"], 557), 1), fmt(r557["dlam"], 1)],
        [r"$R$ at 557 nm", f"{at(th['R'], 557):.0f}", f"{r557['R']:.0f}"],
        [r"$R$ at 878 nm", f"{at(th['R'], 877.7):.0f}", f"{r878['R']:.0f}"],
        ["Range [nm]", rf"{lam_th_lo:.0f}--$>${lam_th_hi:.0f}$^a$",
         rf"{lam_lo:.0f}--{lam_hi:.0f}$^b$"],
    ]
    report.write_table("tab_summary.tex", ["Parameter", "Design", "Measured"], summary, "@{}lcc@{}")

    p = sol["p"]
    Rs = np.array([l["R"] for l in used])
    vals = dict(
        NFrames=logs["Kr"].get("n_frames", ""), PixelUm=fmt(cfg.PIXEL_UM, 2), DetWidthMm=fmt(width, 2),
        HartLamZero=fmt(p[0], 2), HartC=fmt(p[1], 0), HartXzero=fmt(p[2], 1),
        CalRMS=fmt(sol["rms"], 2), CalN=sol["n"], NFeatures=len(lines),
        CurvSagitta=fmt(trace["sagitta"], 0), CurvRMS=fmt(trace["rms"], 2), CurvTilt=fmt(trace["tilt"], 1),
        RangeMin=fmt(lam_lo, 0), RangeMax=fmt(lam_hi, 0), RangeThr=f"{cfg.RANGE_THRESHOLD*100:.0f}",
        RangeDetMin=fmt(lam_det_lo, 0), RangeLastLine=fmt(lam_last, 0),
        RangeThMin=fmt(lam_th_lo, 0), RangeThMax=fmt(lam_th_hi, 0),
        FlashSat=fmt(100 * sat_flash, 1),
        DispMeasFiveH=fmt(meas_at(500), 2), DispMeasSixH=fmt(meas_at(600), 2), DispMeasEightH=fmt(meas_at(800), 2),
        DispThFiveH=fmt(at(th["recip_nm_px"], 500), 2), DispThSixH=fmt(at(th["recip_nm_px"], 600), 2),
        DispRatio=fmt(float(np.median(ratio)), 2), DispRatioSpread=fmt(100 * np.ptp(ratio) / np.median(ratio), 0),
        FCamEff=fmt(f_eff, 1),
        RMin=f"{Rs.min():.0f}", RMax=f"{Rs.max():.0f}",
        RThFFS=f"{at(th['R'], 557):.0f}", RThEES=f"{at(th['R'], 877.7):.0f}",
        RDiffFiveH=f"{at(th['R_diff'], 500):.0f}",
        SlitImgUm=fmt(at(th["slit_img_um"], 550), 1), SlitImgPx=fmt(at(th["slit_img_px"], 550), 1),
        FWHMKr=fmt(fwhm_kr, 1), FWHMAr=fmt(np.median([l["fwhm"] for l in used if l["lamp"] == "Ar"]), 1),
        ThetaInc=fmt(np.degrees(P.theta1), 1), DevMin=fmt(np.degrees(P.deviation(550)), 1),
        NSF=fmt(float(P.n(550)), 4),
        ThetaOff=fmt(t_off, 0), DevOff=fmt(float(np.degrees(P_off.deviation(550))), 1),
        AnamOff=fmt(float(P_off.anamorphic(550)), 2), DispRatioOff=fmt(ratio_off, 2),
        FCamEffOff=fmt(o["f_cam"] / ratio_off, 1),
        LEDBlue=fmt(leds["Blue LED"]["lam"], 1), LEDGreen=fmt(leds["Green LED"]["lam"], 1),
        LEDRed=fmt(leds["Red LED"]["lam"], 1), XFiveFifty=f"{cal.pixel(550, sol):.0f}",
        NPxNIR=f"{cal.pixel(970, sol) - cal.pixel(700, sol):.0f}",
    )
    report.write_macros(vals)

    print(f"Curvature: sagitta {trace['sagitta']:.1f} px, rms {trace['rms']:.2f} px, tilt {trace['tilt']:.2f} deg")
    print(f"Hartmann: {p}  rms={sol['rms']:.3f} nm (N={sol['n']})")
    for l in sorted(lines, key=lambda r: r["mu"]):
        print(f"  {l['lamp']} {l['lams']} x={l['mu']:.2f} FWHM={l['fwhm']:.2f}px lam={l['lam_fit']:.2f} "
              f"R={l['R']:.0f} use={l['use']}")
    for k, d in leds.items():
        print(f"  {k}: lam={d['lam']:.1f}±{d['lam_err']:.1f} (nom {cfg.LEDS[k]['lam_nom']}) FWHM={d['fwhm_nm']:.1f} nm")
    print(f"Range flash {lam_lo:.1f}-{lam_hi:.1f}; det from {lam_det_lo:.1f}; theory {lam_th_lo:.0f}-{lam_th_hi:.0f}")
    print(f"P_meas/P_design median {np.median(ratio):.3f} (spread {100*np.ptp(ratio)/np.median(ratio):.1f}%), f_eff {f_eff:.2f}")
    print(f"Off-min-dev: theta1={t_off:.1f} dev={np.degrees(P_off.deviation(550)):.1f} anam={P_off.anamorphic(550):.2f} "
          f"ratio={ratio_off:.3f}")
    print("Logs:", {k: (v.get('exposure_ms'), v.get('gain')) for k, v in logs.items()})


if __name__ == "__main__":
    main()
