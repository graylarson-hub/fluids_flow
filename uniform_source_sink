import numpy as np

from fluid_plots import (
    source_or_sink,
    plot_vector,
    plot_streamlines,
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


# Visualizations/Plotting

plot_vector(
    X, Y, u, v,
    title="Combined Velocity Field",
    xlabel="x (m)", ylabel="y (m)",
    colorbar_label="Velocity Magnitude (m/s)"
)

plot_streamlines(
    X, Y, u, v,
    title="Uniform Flow + Two Sources/Sinks",
    density=1.5,
    xlabel="x (m)", ylabel="y (m)",
    colorbar_label="Velocity Magnitude (m/s)"
)

plot_field(
    X, Y, phi,
    title="Combined Velocity Potential",
    xlabel="x (m)", ylabel="y (m)",
    colorbar_label="Velocity Potential (m²/s)"
)