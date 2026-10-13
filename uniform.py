"""Uniform, incompressible, irrotational flow at an arbitrary angle."""

import numpy as np

from fluid_plots import (
    plot_vector,
    plot_streamlines,
    plot_combined,
)

# Coordinate grid (meters)
x = np.linspace(-5, 5, 150)
y = np.linspace(-5, 5, 150)
X, Y = np.meshgrid(x, y)

# Uniform flow
U = 2.0          # m/s
angle = np.radians(30)

# Velocity components
u = np.full_like(X, U * np.cos(angle))
v = np.full_like(Y, U * np.sin(angle))

# Stream function and velocity potential
psi = U * (Y * np.cos(angle) - X * np.sin(angle))
phi = U * (X * np.cos(angle) + Y * np.sin(angle))

# Plots
plot_vector(X, Y, u, v, title="Uniform Velocity Field")

plot_streamlines(X, Y, u, v, title="Uniform Flow Streamlines")

plot_combined(
    X, Y, psi, phi,
    title="Stream Function and Velocity Potential",
    levels=20,
    xlabel="x (m)",
    ylabel="y (m)",
)
