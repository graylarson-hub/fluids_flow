"""Uniform flow plus a doublet around an impermeable, nonlifting cylinder."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from fluid_plots import plot_vector, plot_streamlines, plot_combined


# Coordinate grid ####################

x = np.linspace(-5, 5, 300)
y = np.linspace(-5, 5, 300)
X, Y = np.meshgrid(x, y)


# Parameters #########################

U = 2.0                 # Freestream velocity (m/s)
alpha = np.radians(-66)     # Flow angle (degrees converted to radians)
R = 1.0                  # Cylinder radius (m)


# Polar coordinates ##################

r = np.hypot(X, Y)
theta = np.arctan2(Y, X)

# Angle relative to incoming flow
beta = theta - alpha

# Avoid division by zero at cylinder center
r_safe = np.where(r == 0, np.nan, r)


# Stream function and potential ######

psi = U * (r_safe - R**2 / r_safe) * np.sin(beta)
phi = U * (r_safe + R**2 / r_safe) * np.cos(beta)


# Velocity components ################

# Radial and tangential velocities
vr = U * (1 - R**2 / r_safe**2) * np.cos(beta)
vt = -U * (1 + R**2 / r_safe**2) * np.sin(beta)

# Convert from polar to Cartesian
u = vr * np.cos(theta) - vt * np.sin(theta)
v = vr * np.sin(theta) + vt * np.cos(theta)


# Mask cylinder interior #############

inside = r <= R
u = np.ma.masked_where(inside, u)
v = np.ma.masked_where(inside, v)
psi = np.ma.masked_where(inside, psi)
phi = np.ma.masked_where(inside, phi)


# Plot results #######################

fig, ax = plt.subplots(figsize=(8, 7))
ax.add_patch(Circle((0, 0), R, facecolor="#d6d8da",
                    edgecolor="#39434d", linewidth=1.2, zorder=6))
plot_vector(
    X, Y, u, v,
    ax=ax,
    color="#203345",
    title="Velocity Field Around a Cylinder",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

fig, ax = plt.subplots(figsize=(8, 7))
ax.add_patch(Circle((0, 0), R, facecolor="#d6d8da",
                    edgecolor="#39434d", linewidth=1.2, zorder=6))
plot_streamlines(
    X, Y, u, v,
    ax=ax,
    linewidth=0.85, arrowsize=0.8,
    color="#203345",
    title="Potential Flow Around a Cylinder",
    density=1.5,
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

fig, ax = plt.subplots(figsize=(8, 7))
ax.add_patch(Circle((0, 0), R, facecolor="#d6d8da",
                    edgecolor="#39434d", linewidth=1.2, zorder=6))
plot_combined(
    X, Y, psi, phi,
    ax=ax,
    title="Streamlines and Equipotential Lines",
    xlabel="x (m)",
    ylabel="y (m)"
)
