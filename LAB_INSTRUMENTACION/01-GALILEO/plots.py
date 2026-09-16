import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE="tab:blue"; RED="tab:red"; INK="#2b2b2b"; MUTED="#6f6f6f"; GRID="#dedede"

plt.rcParams.update({
    "font.family":"serif","font.serif":["DejaVu Serif"],"font.size":8,
    "axes.edgecolor":MUTED,"axes.labelcolor":INK,"text.color":INK,
    "xtick.color":MUTED,"ytick.color":MUTED,"axes.linewidth":0.6,
    "xtick.major.width":0.6,"ytick.major.width":0.6,
    "figure.dpi":300,"savefig.dpi":300,
})

eye=np.array([33,32,34,32,33],float); tel=np.array([815,796,779,811,803],float)
M=tel/eye; sM=M*np.sqrt((1/tel)**2+(1/eye)**2)
n=np.arange(1,6); mbar=M.mean(); sem=M.std(ddof=1)/np.sqrt(5)

fig,ax=plt.subplots(figsize=(3.4,2.1))
ax.axhspan(mbar-sem,mbar+sem,color=BLUE,alpha=0.12,lw=0)
ax.axhline(mbar,color=BLUE,lw=1.2,label="mean")
ax.axhline(25,color=RED,lw=1.2,ls=(0,(4,2)),label="nominal")
ax.errorbar(n,M,yerr=sM,fmt="o",ms=4.5,mfc="white",mec=BLUE,mew=1.2,
            ecolor=BLUE,elinewidth=1.0,capsize=2.5,capthick=1.0,ls="none",
            label="trials",zorder=3)
ax.set_xticks(n); ax.set_xlabel("Trial"); ax.set_ylabel(r"Magnification")
ax.set_xlim(0.5,5.5); ax.set_ylim(21.8,26.4)
ax.grid(axis="y",color=GRID,lw=0.5); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False,fontsize=6.6,loc="lower right",ncol=1,handlelength=1.8)
fig.tight_layout(pad=0.3); fig.savefig("img/fig_magnification.pdf"); plt.close(fig)

# exit pupil
obj=np.array([47.1,47.0,47.2,47.3,47.1]); Do=obj.mean()
p25=np.array([1.0,0.9,0.8,1.0,1.0]); p50=np.array([0.5,0.4,0.6,0.66,0.52])
meas=[p25.mean(),p50.mean()]
err=[p25.std(ddof=1)/np.sqrt(5),p50.std(ddof=1)/np.sqrt(5)]
exp=[Do/25.0,Do/50.0]
x=np.arange(2); w=0.34
fig,ax=plt.subplots(figsize=(3.4,1.95))
b1=ax.bar(x-w/2,meas,w,yerr=err,color=BLUE,edgecolor="white",lw=0.8,
          error_kw=dict(ecolor=INK,elinewidth=0.9,capsize=2.5,capthick=0.9),label="measured")
b2=ax.bar(x+w/2,exp,w,color=RED,edgecolor="white",lw=0.8,label="expected")
for xx,v in zip(x-w/2,meas): ax.text(xx,v+0.13,f"{v:.2f}",ha="center",fontsize=6.6,color=INK)
for xx,v in zip(x+w/2,exp):  ax.text(xx,v+0.05,f"{v:.2f}",ha="center",fontsize=6.6,color=INK)
ax.set_xticks(x); ax.set_xticklabels([r"$25\times$",r"$50\times$"])
ax.set_ylabel(r"$D_{ex}$ [mm]"); ax.set_ylim(0,2.45)
ax.grid(axis="y",color=GRID,lw=0.5); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False,fontsize=6.6,loc="upper right",handlelength=1.4)
fig.tight_layout(pad=0.3); fig.savefig("img/fig_pupil.pdf"); plt.close(fig)
print("ok")
