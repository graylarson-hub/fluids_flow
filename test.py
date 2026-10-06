import numpy as np

from fluid_plots import (
    plot_field,
    plot_vector,
    plot_streamlines,
    plot_combined,
    source_or_sink,
    plot_source_sink,
    source_sink_pair,
    plot_source_sink_pair
)

# --------------------------------------------------
# Coordinate Grid
# --------------------------------------------------

x = np.linspace(-2, 3, 151)
y = np.linspace(-1, 1, 101)

X, Y = np.meshgrid(x, y)

a = 2.0
c = 45*np.pi/180

# --------------------------------------------------
# Velocity Components
# --------------------------------------------------

def u(X, Y):
    return a*np.cos(c)

def v(X, Y):
    return a*np.sin(c)


# --------------------------------------------------
# Stream Function and Velocity Potential
# --------------------------------------------------

def psi(X, Y):
    return a * (Y*np.cos(c) - X*np.sin(c))

def phi(X, Y):
    return a*(X**3/3 - X*Y**2)

# Positive m creates a source; change to -1.0 for a sink.
m = 1.0
xr = 0.0
yr = 0.0
psi_source, phi_source, ur_source, ux_source, uy_source = source_or_sink(X, Y, m, xr, yr)

# --------------------------------------------------
# Generate Plots
# --------------------------------------------------

plot_field(
    X, Y, phi_source, title="Source/Sink Velocity Potential"
)

plot_vector(
    X, Y, u, v,
    title="Velocity Vector Field"
)

plot_streamlines(
    X, Y, u, v,
    title="Streamline Visualization",
    density=1.5
)

plot_combined(
    X, Y, psi, phi,
    title="Streamlines and Equipotential Lines",
    levels=25
)

plot_source_sink(
    X, Y, m, xr, yr,
    levels=24
)

# Equal source and sink: source at (-0.5, 0), sink at (0.5, 0).
# angle is in radians; negative m swaps source and sink.
psi_pair, phi_pair, ux_pair, uy_pair = source_sink_pair(
    X, Y, m=1.0, separation=1.0, xr=0.0, yr=0.0, angle=0.0
)

plot_source_sink_pair(
    X, Y, m=1.0, separation=1.0,
    levels=25, density=1.5
)
