"""Genera la carta Gantt del proyecto BIFROST a partir de 13-Carta Gantt.xlsx."""
import datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import openpyxl

XLSX = "/mnt/user-data/uploads/PRACTICA2/13-Carta Gantt.xlsx"
OUT = "/root/informe/img/gantt.png"

PHASE_COLORS = ["#2B6BB5", "#C4622D", "#118A73", "#8B5FBF", "#B03A5B"]
INK = "#1f2328"
MUTED = "#6b7280"
GRID = "#e5e7eb"

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb["Ligero"]

rows = []
for r in ws.iter_rows(min_row=7, max_row=55, min_col=2, max_col=7, values_only=True):
    name, cat, _who, _prog, start, days = r
    if not name or "inserte filas" in str(name):
        continue
    name = str(name).strip()
    is_phase = name.startswith(("Pre-Phase", "Phase"))
    if is_phase:
        rows.append((name, cat, None, None))
    elif isinstance(start, dt.datetime):
        rows.append((name.replace("Contrucción", "Construcción"), cat, start, days))

# Agrupar en fases
phases, current = [], None
for name, cat, start, days in rows:
    if start is None:                      # fila de encabezado de fase
        current = {"title": name, "tasks": []}
        phases.append(current)
    elif current is not None:
        current["tasks"].append((name, cat, start, days))

# --- dibujo -----------------------------------------------------------------
n = sum(len(p["tasks"]) for p in phases)
fig, ax = plt.subplots(figsize=(13.5, 0.215 * n + 1.4))

y = 0
yticks, ylabels = [], []
for pi, ph in enumerate(phases):
    color = PHASE_COLORS[pi % len(PHASE_COLORS)]
    for name, cat, start, days in ph["tasks"]:
        end = start + dt.timedelta(days=int(days or 1))
        if str(cat).strip() == "Hito":
            ax.plot(start, y, marker="D", markersize=7, color=color,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=4)
            ylabels.append(name + "  ◆")
        else:
            ax.barh(y, end - start, left=start, height=0.55, color=color,
                    edgecolor="white", linewidth=1.0, zorder=3)
            ylabels.append(name)
        yticks.append(y)
        y -= 1
    y -= 0.6                                # separación entre fases

# Periodo de práctica profesional
p0 = dt.datetime(2026, 1, 5)
p1 = dt.datetime(2026, 2, 28)
ax.axvspan(p0, p1, color="#2B6BB5", alpha=0.07, zorder=0)
ax.axvline(p1, color=MUTED, linestyle="--", linewidth=1.1, zorder=2)
ax.text(p1, 1.6, "  Término de la práctica profesional (28-02-2026)",
        color=MUTED, fontsize=8.5, va="center", ha="left")

ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=8.2, color=INK)
ax.set_ylim(y + 0.4, 2.4)

ax.xaxis.set_major_locator(mdates.MonthLocator())
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul",
         "ago", "sep", "oct", "nov", "dic"]
ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%m\n%Y"))
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda x, _: "{}\n{}".format(MESES[mdates.num2date(x).month - 1],
                                 mdates.num2date(x).year)))
ax.tick_params(axis="x", labelsize=8.5, colors=MUTED, length=0)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=1)
ax.set_axisbelow(True)
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)

handles = [Patch(facecolor=PHASE_COLORS[i % len(PHASE_COLORS)], label=ph["title"])
           for i, ph in enumerate(phases)]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.08),
          ncol=3, frameon=False, fontsize=8.5, labelcolor=INK)

fig.tight_layout()
fig.savefig(OUT, dpi=220, bbox_inches="tight", facecolor="white")
print("ok ->", OUT, "tareas:", n)
