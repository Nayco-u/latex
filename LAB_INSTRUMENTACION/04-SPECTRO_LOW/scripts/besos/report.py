"""Escritura de resultados: CSV en resultados/ y tablas/macros LaTeX en informe/generado/."""
import csv

from . import config


def write_csv(name, rows, header):
    config.RES_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.RES_DIR / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def write_macros(values: dict, name="valores.tex"):
    """\\newcommand{\\Nombre}{valor} para citar números en el informe sin copiarlos a mano."""
    config.TEX_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["% Archivo generado por scripts/run_all.py -- no editar a mano"]
    lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in values.items()]
    (config.TEX_DIR / name).write_text("\n".join(lines) + "\n")


def write_table(name, header, rows, colspec, caption=None):
    """Cuerpo de una tabla booktabs (tabular), para usar con \\input dentro de un table."""
    config.TEX_DIR.mkdir(parents=True, exist_ok=True)
    out = [f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", " & ".join(header) + " \\\\", "\\midrule"]
    out += [" & ".join(str(c) for c in r) + " \\\\" for r in rows]
    out += ["\\bottomrule", "\\end{tabular}"]
    (config.TEX_DIR / name).write_text("\n".join(out) + "\n")
