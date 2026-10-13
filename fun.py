"""Rotational incompressible flow: u=3y, v=2x; no velocity potential.

Coordinates and coefficients use a consistent, unspecified unit system.
This overlaps the exploratory test.py script and is retained for comparison.
"""

import numpy as np
import matplotlib.pyplot as plt

from fluid_plots import (
    plot_vector,
    plot_streamlines,
)

# Grid
N = 400
xmin, xmax = -4, 4
ymin, ymax = -4, 4

x = np.linspace(xmin, xmax, N)
y = np.linspace(ymin, ymax, N)

X, Y = np.meshgrid(x, y)

# Velocity components
def u(X, Y):
    return 3 * Y

def v(X, Y):
    return 2 * X

# Stream function
def psi(X, Y):
    return 1.5 * Y**2 - X**2

# Evaluate
U = u(X, Y)
V = v(X, Y)
PSI = psi(X, Y)

# Velocity vectors
plot_vector(
    X, Y, U, V,
    title="Velocity Vector Field"
)

# Streamlines
plot_streamlines(
    X, Y, U, V,
    title="Streamline Visualization",
    density=1.5
)

# Stream-function contours
plt.figure(figsize=(8, 6))
plt.contour(X, Y, PSI, levels=25)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Stream Function Contours")
plt.axis("equal")
plt.grid(True)
plt.show()
