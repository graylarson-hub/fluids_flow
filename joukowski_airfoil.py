"""Map circulating cylinder flow to a Joukowski airfoil using a complex potential.

The circulation enforces zero tangential cylinder velocity at the trailing edge.
This example plots stream-function contours, not airfoil pressure or lift."""

import numpy as np
import matplotlib.pyplot as plt


# Flow parameters ####################

U = 3.0                  # Freestream velocity (m/s)
alpha = np.radians(10)     # Flow direction (degrees)


# Airfoil geometry ###################

a = 1.0                    # Transformation parameter (m)
zc = -0.05 + 0.10j       # Circle center (complex coordinates)

# Radius chosen so the circle passes through z = a
R = abs(a - zc)


# Circulation (Kutta condition) ######

theta_te = np.angle(a - zc)
Gamma = 4 * np.pi * R * U * np.sin(theta_te - alpha)

print(f"Circle radius: {R:.3f} m")
print(f"Circulation: {Gamma:.3f} m^2/s")


# Cylinder and airfoil geometry ######

theta = np.linspace(0, 2*np.pi, 600)

circle = zc + R * np.exp(1j * theta)

# Joukowski transformation
airfoil = circle + a**2 / circle


# Flow calculation grid ##############

# Polar grid outside the circle
radius = np.linspace(R * 1.002, 5*a, 220)
angles = np.linspace(0, 2*np.pi, 500)

r, t = np.meshgrid(radius, angles)

z = zc + r * np.exp(1j * t)
w = z - zc


# Complex potential ##################

# Uniform flow + doublet
W = U * (np.exp(-1j*alpha)*w
         + R**2*np.exp(1j*alpha)/w)

# Free vortex
W += Gamma/(2j*np.pi) * np.log(w/R)

# Imaginary part of W is the stream function
psi = W.imag


# Transform flow coordinates #########

zeta = z + a**2/z


# Plot streamlines ####################

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

levels = np.linspace(-4*U*a, 4*U*a, 41)

# Original cylinder flow
axes[0].contour(
    z.real, z.imag, psi,
    levels=levels, colors="C0", linestyles="solid"
)
axes[0].fill(
    circle.real, circle.imag,
    color="lightgray", edgecolor="black"
)
axes[0].set_title("Original Cylinder Flow")

# Transformed airfoil flow
axes[1].contour(
    zeta.real, zeta.imag, psi,
    levels=levels, colors="C0", linestyles="solid"
)
axes[1].fill(
    airfoil.real, airfoil.imag,
    color="lightgray", edgecolor="black"
)
axes[1].set_title("Joukowski Airfoil Flow")

for ax in axes:
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)

fig.tight_layout()
plt.show()
