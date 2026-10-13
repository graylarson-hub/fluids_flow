import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import Normalize

from fluid_plots import (
    source_or_sink,
    plot_vector,
    plot_field,
)


x = np.linspace(-5, 5, 300)
y = np.linspace(-5, 5, 300)

X, Y = np.meshgrid(x, y)

# Flow parameters

U = 8        # Uniform flow velocity (m/s)
a = 111        # Flow angle in degrees
aplpha = np.radians(a)  # angle in radians

# Source 1
m1 = 10     # Source strength (m^2/s)
x1, y1 = 2.0, 0.0

# Source 2
m2 = -10      # Source strength (m^2/s)
x2, y2 = -1.0, 0.0


# Uniform flow

u_uniform = np.full_like(X, U * np.cos(aplpha))
v_uniform = np.full_like(Y, U * np.sin(aplpha))

psi_uniform = U * (Y * np.cos(aplpha) - X * np.sin(aplpha))
phi_uniform = U * (X * np.cos(aplpha) + Y * np.sin(aplpha))


# Point source/sink

psi1, phi1, ur1, u1, v1 = source_or_sink(X, Y, m1, x1, y1)
psi2, phi2, ur2, u2, v2 = source_or_sink(X, Y, m2, x2, y2)


# Superposition

u = u_uniform + u1 + u2
v = v_uniform + v1 + v2

psi = psi_uniform + psi1 + psi2
phi = phi_uniform + phi1 + phi2


# Stagnation point

# Along y = 0, the upstream velocity is:
# u = U + m/(2*pi*(x - xr))
# Set u = 0 to find the stagnation point.
# x_stag = xr - m / (2 * np.pi * U)
# y_stag = yr
# print(f"Stagnation point: ({x_stag:.3f}, {y_stag:.3f}) m")


# Visualization-only singularity masks ####################

# A cell diagonal marks the near-center region the grid cannot resolve.
# Keep the calculated fields unchanged; no finite or viscous core is invented.
plot_core = np.hypot(x[1] - x[0], y[1] - y[0])
near_centers = ((np.hypot(X - x1, Y - y1) <= plot_core)
                | (np.hypot(X - x2, Y - y2) <= plot_core))
u_plot = np.ma.masked_where(near_centers, u)
v_plot = np.ma.masked_where(near_centers, v)
phi_plot = np.ma.masked_where(near_centers, phi)

# Visualizations/Plotting

fig, ax = plt.subplots(figsize=(8, 7))
# Dashed circles show grid-sized exclusions; markers locate point flows.
for xc, yc, label, marker in [(x1, y1, "Source", "+"), (x2, y2, "Sink", "x")]:
    ax.add_patch(Circle((xc, yc), plot_core, facecolor="white",
                        edgecolor="#66717b", linestyle="--", linewidth=1, zorder=6))
    ax.plot(xc, yc, marker, color="#203345", markersize=7, label=label, zorder=7)
ax.legend(loc="upper right", title="Point flows; dashed exclusions", fontsize=9)
plot_vector(
    X, Y, u_plot, v_plot,
    ax=ax,
    title="Combined Velocity Field",
    xlabel="x (m)", ylabel="y (m)",
    colorbar_label="Velocity Magnitude (m/s)"
)

fig, ax = plt.subplots(figsize=(8, 7))
# Dashed circles show grid-sized exclusions; markers locate point flows.
for xc, yc, label, marker in [(x1, y1, "Source", "+"), (x2, y2, "Sink", "x")]:
    ax.add_patch(Circle((xc, yc), plot_core, facecolor="white",
                        edgecolor="#66717b", linestyle="--", linewidth=1, zorder=6))
    ax.plot(xc, yc, marker, color="#203345", markersize=7, label=label, zorder=7)
ax.legend(loc="upper right", title="Point flows; dashed exclusions", fontsize=9)
# Local color limits emphasize speed variation in this superposition only.
# Use the full finite, unmasked field; velocities and tracing are unchanged.
speed_plot = np.ma.masked_invalid(np.hypot(u_plot, v_plot))
vmin, vmax = np.percentile(speed_plot.compressed(), [10, 95])
norm = Normalize(vmin=vmin, vmax=vmax)
stream = ax.streamplot(x, y, u_plot, v_plot, color=speed_plot,
                       cmap="viridis", norm=norm, density=1.5,
                       linewidth=0.85, arrowsize=0.8)
# Triangles identify speeds outside the color interval, not clipped velocities.
fig.colorbar(stream.lines, ax=ax, extend="both", label="Speed (m/s)")
ax.set(title="Uniform Flow + Two Sources/Sinks", xlabel="x (m)", ylabel="y (m)")
ax.set_aspect("equal", adjustable="box")
ax.grid(True, alpha=0.2)
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8, 7))
# Dashed circles show grid-sized exclusions; markers locate point flows.
for xc, yc, label, marker in [(x1, y1, "Source", "+"), (x2, y2, "Sink", "x")]:
    ax.add_patch(Circle((xc, yc), plot_core, facecolor="white",
                        edgecolor="#66717b", linestyle="--", linewidth=1, zorder=6))
    ax.plot(xc, yc, marker, color="#203345", markersize=7, label=label, zorder=7)
ax.legend(loc="upper right", title="Point flows; dashed exclusions", fontsize=9)
plot_field(
    X, Y, phi_plot,
    ax=ax,
    title="Combined Velocity Potential",
    xlabel="x (m)", ylabel="y (m)",
    colorbar_label="Velocity Potential (m²/s)"
)