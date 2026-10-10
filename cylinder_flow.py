import numpy as np
import matplotlib.pyplot as plt

from fluid_plots import plot_vector, plot_streamlines, plot_field, plot_combined


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

plot_vector(
    X, Y, u, v,
    title="Velocity Field Around a Cylinder",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Velocity (m/s)"
)

plot_streamlines(
    X, Y, u, v,
    title="Potential Flow Around a Cylinder",
    density=1.5,
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Velocity (m/s)"
)

plot_combined(
    X, Y, psi, phi,
    title="Streamlines and Equipotential Lines",
    xlabel="x (m)",
    ylabel="y (m)"
)