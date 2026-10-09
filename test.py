import numpy as np
import matplotlib.pyplot as plt

from fluid_plots import (
    plot_field,
    plot_vector,
    plot_streamlines,
    plot_combined,
    source_or_sink,
    source_sink_pair,
    plot_source_sink,
    plot_source_sink_pair,
)

# --------------------------------------------------
# Coordinate Grid
# --------------------------------------------------

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

# --------------------------------------------------
# Velocity Components
# --------------------------------------------------

# def u_uni(X, Y):
#     return a*np.cos(c)

# def v_uni(X, Y):
#     return a*np.sin(c)

def u(X, Y):
    return 3 * Y
def v(X, Y):
    return 2 * X


# --------------------------------------------------
# Stream Function and Velocity Potential
# --------------------------------------------------

def psi(X, Y):
    return 3/2 * Y**2 - X**2 

def phi(X, Y):
    return 

# psi_source, phi_source, ur_source, ux_source, uy_source = source_or_sink(X, Y, m, xr, yr)

# --------------------------------------------------
# Generate Plots
# --------------------------------------------------

# plot_field(
#     X, Y, phi_source, title="Source/Sink Velocity Potential"
# )

plot_vector(
    X, Y, u, v,
    title="Velocity Vector Field"
)

plot_streamlines(
    X, Y, u, v,
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