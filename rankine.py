"""Rankine oval from uniform flow plus an equal-strength source/sink pair."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from fluid_plots import source_or_sink, plot_streamlines


# Coordinate grid ####################

x = np.linspace(-5, 5, 301)
y = np.linspace(-4, 4, 301)

X, Y = np.meshgrid(x, y)


# Flow parameters ####################

U = 2.0         # Uniform flow speed (m/s)
m = 10.0         # Source strength (m^2/s)
a = 3.0          # Half the source-sink separation (m)


# Source and sink #####################

# Source at (-a, 0)
psi1, phi1, ur1, u1, v1 = source_or_sink(
    X, Y, m, -a, 0
)

# Sink at (+a, 0)
psi2, phi2, ur2, u2, v2 = source_or_sink(
    X, Y, -m, a, 0
)


# Superposition ######################

u = U + u1 + u2
v = v1 + v2

psi = U*Y + psi1 + psi2
phi = U*X + phi1 + phi2


# Stagnation points ##################

x_stag = np.sqrt(a**2 + m*a/(np.pi*U))

# Require a few cells across the half-height and the short nose region.
# At x=0, psi(y)=U*y-m/pi*atan(a/y); its positive root is the half-height.
dx, dy = x[1] - x[0], y[1] - y[0]
if (U * (3 * dy) >= m / np.pi * np.arctan2(a, 3 * dy)
        or x_stag - a < 2 * dx):
    raise ValueError(
        "Rankine oval is under-resolved. Refine x and y or use a tighter domain "
        "to resolve its half-height and the distance from each center to its nose."
    )

# Exclude one cell diagonal around unresolved point-flow centers for plotting.
# These masks do not regularize or modify the analytical fields above.
plot_core = np.hypot(dx, dy)
near_centers = ((np.hypot(X + a, Y) <= plot_core)
                | (np.hypot(X - a, Y) <= plot_core))
u_plot = np.ma.masked_where(near_centers, u)
v_plot = np.ma.masked_where(near_centers, v)

print(f"Stagnation points: x = +/- {x_stag:.3f} m")
print(f"Oval length: {2*x_stag:.3f} m")


# Velocity streamlines ###############

fig, ax = plt.subplots(figsize=(8, 7))
# The point-flow exclusions are numerical regions, not solid geometry.
for xc, label, marker in [(-a, "Source", "+"), (a, "Sink", "x")]:
    ax.add_patch(Circle((xc, 0), plot_core, facecolor="white",
                        edgecolor="#66717b", linestyle="--", linewidth=1, zorder=6))
    ax.plot(xc, 0, marker, color="#203345", markersize=7, label=label, zorder=7)
ax.legend(title="Point flows; dashed exclusions", fontsize=9)
plot_streamlines(
    X, Y, u_plot, v_plot,
    ax=ax,
    title="Rankine Oval: Uniform Flow + Source + Sink",
    density=1.2, color="#203345", linewidth=0.85, arrowsize=0.8,
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)


# Dividing streamline ################

# Mask only the sampled row nearest y=0 over the source-sink segment.
# Every cell crossing the cut then has a masked corner. corner_mask=False
# drops those whole cells, preventing interpolation across the angular jump.
cut = np.zeros(X.shape, dtype=bool)
cut[np.argmin(np.abs(y)), np.abs(x) <= a + dx / 2] = True
psi_plot = np.ma.masked_where(cut, psi)

fig, ax = plt.subplots(figsize=(12, 6), layout="constrained")

# The zero streamline includes the oval boundary and
# the x-axis portions outside its stagnation points.
ax.contour(
    X, Y, psi_plot,
    levels=[0],
    colors="#79818a",
    linewidths=0.85, linestyles="dashed",
    corner_mask=False
)

# The same zero contour contains exterior axis branches, not body edges.
# Clip the highlight at the analytical stagnation points, rather than adding
# a sampled mask that could hide the narrow tips. Keep the cut mask unchanged.
oval_contour = ax.contour(X, Y, psi_plot, levels=[0], colors="#203345",
                          linewidths=1.3, corner_mask=False)
oval_contour.set_clip_path(Rectangle((-x_stag, y[0]), 2 * x_stag,
                                    y[-1] - y[0], transform=ax.transData))
ax.plot([], [], color="#203345", linewidth=1.3, label="Dividing streamline")
ax.plot([], [], color="#79818a", linestyle="--", linewidth=0.85,
        label="Exterior zero-streamfunction branches")

# Source and sink locations
ax.plot(-a, 0, "+", color="#203345", markersize=8, label="Source")
ax.plot(a, 0, "x", color="#203345", markersize=6, label="Sink")

# Stagnation points
ax.plot(
    [-x_stag, x_stag], [0, 0],
    "o", color="#203345", markersize=4, label="Stagnation points"
)

ax.set_title("Rankine Oval: Dividing Streamline")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_aspect("equal")
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=9)
ax.grid(True, alpha=0.2)

plt.show()
