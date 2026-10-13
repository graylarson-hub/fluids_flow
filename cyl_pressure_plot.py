"""Cylinder surface pressure and pressure-integrated forces per unit span.

Positive circulation is counterclockwise; flow along +x gives negative lift.
"""

import numpy as np
import matplotlib.pyplot as plt


# Cylinder parameters ################

U = 2.0         # Freestream velocity (m/s)
R = 1.0           # Cylinder radius (m)
rho = 1.225      # Air density (kg/m^3)

# Compare different circulation strengths (m^2/s)
gamma_values = [0.0, 8.0, -8.0, 20.0, -20.0]


# Surface coordinates ################

# Angle measured counterclockwise from +x
theta = np.linspace(0, 2*np.pi, 721)
theta_deg = np.degrees(theta)


# Pressure distribution ##############

fig, ax = plt.subplots(figsize=(9, 6))

for Gamma in gamma_values:

    # Tangential velocity on the cylinder surface
    vt = -2*U*np.sin(theta) + Gamma/(2*np.pi*R)

    # Pressure coefficient from Bernoulli
    Cp = 1 - (vt/U)**2

    # Gauge pressure relative to freestream
    pressure = 0.5*rho*U**2*Cp

    # Integrate surface pressure to find force per unit length
    drag = -R*np.trapezoid(pressure*np.cos(theta), theta)
    lift = -R*np.trapezoid(pressure*np.sin(theta), theta)

    # Analytical lift from Kutta-Joukowski
    lift_theory = -rho*U*Gamma

    print(f"\nCirculation = {Gamma:.1f} m^2/s")
    print(f"Lift (integrated): {lift:.3f} N/m")
    print(f"Lift (theoretical): {lift_theory:.3f} N/m")
    print(f"Drag (integrated): {drag:.3f} N/m")

    ax.plot(theta_deg, Cp, label=f"Gamma = {Gamma:g}")


# Plot formatting ####################

ax.set_title("Cylinder Surface Pressure Distribution")
ax.set_xlabel("Surface Angle (degrees)")
ax.set_ylabel("Pressure Coefficient, Cp")

ax.set_xticks(np.arange(0, 361, 45))
ax.axhline(0, color="gray", linewidth=0.8)
ax.legend()
ax.grid(True, alpha=0.3)

# Conventional aerodynamic Cp plots have negative Cp upward
ax.invert_yaxis()

fig.tight_layout()
plt.show()
