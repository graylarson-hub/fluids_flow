"""Exploratory rotational-flow example, not an automated test suite.

u=3y, v=2x is incompressible, with vorticity -1 in consistent units.
The unused phi placeholder and commented experiments are unfinished.
"""

import numpy as np
import matplotlib.pyplot as plt

from fluid_plots import (
    plot_vector,
    plot_streamlines,
)

# Archived experiments below refer to removed specialized plotting functions.
# Their original implementations remain in Git history; they are not active API.

# Coordinate grid ####################

N = 400
xmin = -5
xmax = 5
ymin = -5
ymax = 5

x = np.linspace(xmin, xmax, N)
y = np.linspace(ymin, ymax, N)

X, Y = np.meshgrid(x, y)

a = 2.0
c = 0

# Positive m creates a source; change to -1 for sink.
m = 1
xr = -2.0
yr = 0.0

# Velocity components ################

# def u_uni(X, Y):
#     return a*np.cos(c)

# def v_uni(X, Y):
#     return a*np.sin(c)

def u(X, Y):
    return 3 * Y
def v(X, Y):
    return 2 * X


# Stream function and unfinished potential experiment ####################

def psi(X, Y):
    return 3/2 * Y**2 - X**2 

def phi(X, Y):
    return 

# psi_source, phi_source, ur_source, ux_source, uy_source = source_or_sink(X, Y, m, xr, yr)

# Generate plots #####################

U = u(X, Y)
V = v(X, Y)

# plot_field(
#     X, Y, phi_source, title="Source/Sink Velocity Potential"
# )

plot_vector(
    X, Y, U, V,
    title="Velocity Vector Field"
)

plot_streamlines(
    X, Y, U, V,
    title="Streamline Visualization",
    density=1.5
)

# plot_combined(
#     X, Y, psi, phi,
#     title="Streamlines and Equipotential Lines",
#     levels=25
# )

# plot_source_sink(
#     X, Y, m, xr, yr,
#     levels=24
# )

# plot_source_sink_pair(
#     X, Y, m, xr, yr,
#     levels=24
# )

# Stream-function contours
PSI = psi(X,Y)
plt.figure(figsize=(8, 6))
plt.contour(X, Y, PSI, levels=25)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Stream Function Contours")
plt.axis("equal")
plt.grid(True)
plt.show()
