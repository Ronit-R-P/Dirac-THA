"""Foam stress ball (3D view): COMPRESSION (fitted static curve) + RECOVERY (first-order damper) + 3D column animation.
Edit the DATA block, then run:  python stress_ball_model_3d.py
Fit, damper and recovery are identical to stress_ball_model.py. Only the geometry/drawing is 3D.
Geometry: nu ~ 0 foam => independent vertical columns, revolved about the vertical axis (axisymmetric).
          The plate crushes each column to thickness t(r); width = MEASURED bulge; rim roundness (NMAX) is visual only.
This is parametric curve fitting, not machine learning."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3D projection)
from matplotlib.widgets import Slider, Button
from scipy.optimize import curve_fit
trapz = getattr(np, 'trapezoid', None) or np.trapz

# ================= DATA (edit me) =================
H0, R0   = 70.0, 35.0
BOARD_KG = 0.30
KG       = np.arange(1, 15)
HEIGHT   = np.array([51, 46, 40.5, 35, 25, 22, 19, 12, 10, 9.5, 9.0, 9.0, 9.5, 9.5])
BULGE    = np.array([.9, 1.2, 1.5, 1.8, 2.2, 2.4, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5])   # mm per side
TRAIN_MAX_KG = 12
USE_PHYSICS_FLOOR = True
RHO_PU, M_BALL_G = 1.15, 40.0             # g/cm^3 (typical PU, VERIFY) and ball mass in g (weigh it)
C_DAMP   = 75.0
VIDEO_FPS = 59.8
OBS_FRAMES = {2: 15, 3: 15, 4: 15}        # CALIBRATION
VAL_FRAMES = {}                           # VALIDATION, e.g. {6: 15}
SLOWMO = 4
NMAX = 7.0                                # rim squareness at full compression (2 = ellipse). Visual only.
CUTAWAY = False                           
NG = 19                                   # particles per axis (lower, e.g. 15, if the animation is slow)
PLATE_R = 45.0                            # drawn plate radius (mm), visual only
# ==================================================
F  = (KG + BOARD_KG) * 9.81
DZ = H0 - HEIGHT
EPS_CAP = DZ.max() / H0 + 0.02
TOL = 0.02 * H0
V0 = 4.0 / 3.0 * np.pi * R0**3
SOLID_FRAC = (M_BALL_G / RHO_PU * 1000.0) / V0
D_PHYS = H0 - M_BALL_G / RHO_PU * 1000.0 / (np.pi * R0**2)

def knee(F, D, Fc, q):
    return D * F / (F**q + Fc**q) ** (1.0 / q)

def fit(mask):
    if USE_PHYSICS_FLOOR:
        f = lambda F, Fc, q: knee(F, D_PHYS, Fc, q)
        (Fc, q), _ = curve_fit(f, F[mask], DZ[mask], p0=[60, 4], bounds=([5, 1], [300, 30]), maxfev=40000)
        return np.array([D_PHYS, Fc, q])
    lo_D = max(DZ[mask].max(), 5.0)
    p, _ = curve_fit(knee, F[mask], DZ[mask], p0=[lo_D + 1, 60, 4],
                     bounds=([lo_D, 5, 1], [H0 - 1, 300, 30]), maxfev=40000)
    return p

print(f"Solid-polymer volume fraction {SOLID_FRAC*100:.0f}% | physics floor {H0-D_PHYS:.1f} mm (D={D_PHYS:.1f} mm)")
print("Extrapolation test (fit on loads <= cutoff, predict the heavier ones):")
for cut in (6, 8, 10, 12):
    msk = KG <= cut
    if msk.all(): continue
    pc = fit(msk); err = knee(F[~msk], *pc) - DZ[~msk]
    print(f"  train <= {cut:2d} kg: D={pc[0]:5.1f} mm | RMSE on heavier loads {np.sqrt(np.mean(err**2)):.2f} mm, worst {np.abs(err).max():.1f} mm")

tr = KG <= TRAIN_MAX_KG; te = ~tr
p = fit(tr); D, Fc, q = p
rmse = lambda s: np.sqrt(np.mean((knee(F[s], *p) - DZ[s]) ** 2))
print(f"\nChosen fit (train <= {TRAIN_MAX_KG} kg): D={D:.1f} mm  Fc={Fc:.1f} N  q={q:.2f}  initial k={Fc/D*1000:.0f} N/m")
print(f"train RMSE {rmse(tr):.2f} mm" + (f" | held-out RMSE {rmse(te):.2f} mm" if te.any() else ""))
for k, f, h in zip(KG[te], F[te], HEIGHT[te]):
    print(f"  {k} kg: predicted height {H0-knee(f,*p):5.1f} mm | measured {h:5.1f} mm")

Fg  = np.linspace(0, 170, 900); DZg = knee(Fg, *p)
KT  = np.gradient(Fg, DZg + 1e-12) * 1000
comp = lambda f: np.interp(f, Fg, DZg)
ktan = lambda f: np.interp(f, Fg, KT)

# ---- recovery ----
Fs = lambda z: np.interp(z, DZg, Fg)
C_USE = C_DAMP
def recover(z0, c=None, dt=0.001, tmax=3.0):
    c = C_USE if c is None else c
    t, z, out_t, out_z = 0.0, z0, [0.0], [z0]
    while z > 0.2 and t < tmax:
        z -= dt * 1000.0 * Fs(z) / c; t += dt; out_t.append(t); out_z.append(max(z, 0.0))
    return np.array(out_t), np.array(out_z)
def frames_to_tol(z0, c=None):
    tt, zz = recover(z0, c); hit = zz < TOL
    return tt[np.argmax(hit)] * VIDEO_FPS if hit.any() else np.nan
z0_of = lambda kg: float(comp((kg + BOARD_KG) * 9.81))
mod = np.mean([frames_to_tol(z0_of(k), C_DAMP) for k in OBS_FRAMES])
C_USE = C_DAMP * np.mean(list(OBS_FRAMES.values())) / mod
print(f"\nDamper fitted to {list(OBS_FRAMES)} kg video: c = {C_USE:.1f} N s/m  (2% of rest height = {TOL:.1f} mm)")
print("Recovery time (frames to within 2% of rest height):")
for kg in sorted(set(OBS_FRAMES) | set(VAL_FRAMES) | set(int(k) for k in KG[te])):
    obs = OBS_FRAMES.get(kg, VAL_FRAMES.get(kg))
    tag = "calibration" if kg in OBS_FRAMES else ("VALIDATION" if kg in VAL_FRAMES else "held-out load, not filmed: prediction")
    print(f"  {kg:2d} kg: model {frames_to_tol(z0_of(kg)):4.1f}" + (f" | observed {obs} ({tag})" if obs else f" ({tag})"))

# ---- 3D geometry: independent columns revolved about the vertical axis + convex superellipse profile ----
bulge_at = lambda dz: np.interp(dz, np.r_[0, np.maximum.accumulate(DZ)], np.r_[0, BULGE])
n_of = lambda dz: 2.0 + (NMAX - 2.0) * min(dz / D_PHYS, 1.0) ** 1.5
thick = lambda r, A_, B_, n_: 2.0 * B_ * np.clip(1.0 - (np.abs(r) / A_) ** n_, 0.0, None) ** (1.0 / n_)
def V_ratio(dz):
    A_, B_, n_ = R0 + bulge_at(dz), (H0 - dz) / 2.0, n_of(dz)
    rs = np.linspace(0, A_, 600)
    return trapz(2 * np.pi * rs * thick(rs, A_, B_, n_), rs) / V0

gl = np.linspace(-R0, R0, NG)
GX, GY, GZ = np.meshgrid(gl, gl, np.linspace(0, H0, NG))
inside = GX**2 + GY**2 + (GZ - R0)**2 <= R0**2
if CUTAWAY: inside &= (GY <= 0)
px, py, pz = GX[inside], GY[inside], GZ[inside]                  # original particle positions
pr  = np.sqrt(px**2 + py**2)
Lc  = 2.0 * np.sqrt(np.clip(R0**2 - pr**2, 1e-9, None))         # original column length at each radius
eta = np.clip((pz - R0) / (Lc / 2.0), -1, 1)                    # position inside the column, -1..1

def shape(dz):
    A_, B_, n_ = R0 + bulge_at(dz), (H0 - dz) / 2.0, n_of(dz)
    lam = A_ / R0                                               # lateral spread = measured bulge
    t = thick(lam * pr, A_, B_, n_)                             # column thickness under the plate
    zd = B_ + eta * t / 2.0                                     # uniform strain inside each column
    eps = np.clip(1.0 - t / Lc, 0.0, 1.0)
    return lam * px, lam * py, zd, eps, A_, B_, n_

thp = np.linspace(-np.pi / 2, np.pi / 2, 120); cp, sp = np.cos(thp), np.sin(thp)
phis = [ph for ph in np.linspace(0, 2 * np.pi, 13)[:-1] if (not CUTAWAY) or np.sin(ph) <= 1e-9]
ring_ph = np.linspace(np.pi, 2 * np.pi, 100) if CUTAWAY else np.linspace(0, 2 * np.pi, 200)
pl_ph = np.linspace(0, 2 * np.pi, 120)

fig = plt.figure(figsize=(13, 6.5)); plt.subplots_adjust(bottom=0.2, wspace=0.12)
ax = fig.add_subplot(1, 2, 1, projection='3d'); ax2 = fig.add_subplot(1, 2, 2)
ax.set_xlim(-50, 50); ax.set_ylim(-50, 50); ax.set_zlim(-5, 95); ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=18, azim=-60)
ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)"); ax.set_zlabel("height (mm)")
ax.set_title("Compression (independent columns, 3D, data-fitted)")
ax.plot(PLATE_R*np.cos(pl_ph), PLATE_R*np.sin(pl_ph), 0*pl_ph, 'k', lw=3)                 # table edge
mer_lines = [ax.plot([0, 1], [0, 1], [0, 1], color='indigo', lw=1.2)[0] for _ in phis]
ring_line, = ax.plot([0, 1], [0, 1], [0, 1], color='indigo', lw=1.5)
plate_line, = ax.plot([0, 1], [0, 1], [0, 1], color='crimson', lw=3)
scat = None
txt = ax.text2D(0.02, 0.98, "", transform=ax.transAxes, va='top', family='monospace', fontsize=9,
                bbox=dict(fc='lightyellow', ec='orange'))
ax2.plot(DZg, Fg, 'b-', label='fitted model'); ax2.plot(DZ[tr], F[tr], 'go', label='train')
if te.any(): ax2.plot(DZ[te], F[te], 'rs', label='held-out')
ax2.set_xlabel("compression (mm)"); ax2.set_ylabel("force incl. board (N)"); ax2.set_xlim(0, 70); ax2.set_ylim(0, 170)
ax2.grid(alpha=.3); ax2.legend(); mk, = ax2.plot([], [], 'k*', ms=15)

def draw_dz(dz, label):
    global scat
    xd, yd, zd, eps, A_, B_, n_ = shape(dz)
    if scat is not None: scat.remove()
    scat = ax.scatter(xd, yd, zd, c=eps, cmap='plasma', vmin=0, vmax=EPS_CAP, s=8, depthshade=False)
    r = A_ * np.abs(cp) ** (2.0 / n_); z = B_ + B_ * np.sign(sp) * np.abs(sp) ** (2.0 / n_)
    for line, ph in zip(mer_lines, phis):
        line.set_data(r * np.cos(ph), r * np.sin(ph)); line.set_3d_properties(z)
    ring_line.set_data(A_ * np.cos(ring_ph), A_ * np.sin(ring_ph)); ring_line.set_3d_properties(np.full_like(ring_ph, B_))
    h = H0 - dz
    plate_line.set_data(PLATE_R * np.cos(pl_ph), PLATE_R * np.sin(pl_ph)); plate_line.set_3d_properties(np.full_like(pl_ph, h))
    mk.set_data([dz], [float(Fs(dz))])
    txt.set_text(f"{label}\ncompress  {dz:4.1f} mm ({dz/H0*100:3.0f}%)\n"
                 f"k_tangent {float(ktan(float(Fs(dz)))):6.0f} N/m\nbulge     {A_-R0:4.1f} mm\n"
                 f"volume    {V_ratio(dz)*100:4.0f}% (solid floor {SOLID_FRAC*100:.0f}%)")
    fig.canvas.draw_idle()
def draw(kg):
    f = (kg + BOARD_KG) * 9.81; draw_dz(float(comp(f)), f"load {kg:4.1f} kg + board ({f:5.1f} N)")

busy = False
def release(_):
    global busy
    if busy: return
    zc = float(comp((sl.val + BOARD_KG) * 9.81))
    if zc < 3.0:
        txt.set_text("Move the load slider up first,\nthen press Release"); fig.canvas.draw_idle(); return
    busy = True
    try:
        tt, zz = recover(zc); step = max(1, int(round(1000.0 / VIDEO_FPS)))
        for i in range(0, len(zz), step):
            draw_dz(zz[i], f"RELEASED  t = {tt[i]*1000:4.0f} ms  (slow-mo x{SLOWMO})")
            plt.pause(step * 0.001 * SLOWMO)
        draw_dz(zz[-1], f"RECOVERED  t = {tt[-1]*1000:4.0f} ms")
    finally:
        busy = False

sl = Slider(plt.axes([0.15, 0.07, 0.6, 0.04]), 'Added load (kg)', 0, 14, valinit=0, valfmt='%.1f')
sl.on_changed(draw)
btn = Button(plt.axes([0.8, 0.07, 0.12, 0.04]), 'Release', color='lightgreen'); btn.on_clicked(release)
draw(0)
if __name__ == "__main__": plt.show()
