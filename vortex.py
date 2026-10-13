"""Ideal free vortex with an excluded core and a numerical vorticity check.

The excluded region is a plotting mask, not a finite-core vortex model."""

import numpy as np
from fluid_plots import plot_vector, plot_streamlines, plot_field


# Coordinate grid ####################

x = np.linspace(-5, 5, 301)
y = np.linspace(-5, 5, 301)
X, Y = np.meshgrid(x, y)

# Vortex parameters ##################

Gamma = -7.0        # Circulation (m^2/s)
xc, yc = 1.0, 0.5    # Vortex center (m)

core_radius = 0.25   # Excluded region near singularity (m)


# Radial distance ####################

dx = X - xc
dy = Y - yc

r = np.hypot(dx, dy)

# Ideal vortex velocity is undefined at the center.
# Exclude a small region for numerical plotting.
r_safe = np.where(r <= core_radius, np.nan, r)


# Velocity components ################

# Positive Gamma = counterclockwise circulation

factor = Gamma / (2 * np.pi)

u = -factor * dy / r_safe**2
v = factor * dx / r_safe**2


# Stream function ####################

# Reference radius is 1 meter.
psi = -factor * np.log(r_safe / 1.0)


# Vorticity calculation ##############

# NumPy gradient returns derivatives in y, x order.
du_dy, du_dx = np.gradient(u, y, x)
dv_dy, dv_dx = np.gradient(v, y, x)

vorticity = dv_dx - du_dy

# Check away from the unresolved vortex center.
outside = r > 0.75

print("Maximum absolute vorticity away from core:")
print(f"{np.nanmax(np.abs(vorticity[outside])):.5f} 1/s")


# Visualizations/Plots ###############

plot_vector(
    X, Y, u, v,
    title="Free Vortex: Velocity Vectors",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

plot_streamlines(
    X, Y, u, v,
    title="Free Vortex: Streamlines",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

plot_field(
    X, Y, psi,
    title="Free Vortex: Stream Function",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Stream Function (m²/s)"
)
