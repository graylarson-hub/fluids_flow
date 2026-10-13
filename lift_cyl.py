
import numpy as np

from fluid_plots import plot_vector, plot_streamlines, plot_field


# Coordinate grid ####################

x = np.linspace(-5, 5, 301)
y = np.linspace(-5, 5, 301)
X, Y = np.meshgrid(x, y)


# Parameters #########################

U = 4.5                 # Freestream velocity (m/s)
alpha = np.radians(0)    # Flow angle (degrees)
R = 1.4                  # Cylinder radius (m)
Gamma = -20.0             # Circulation (m^2/s)
rho = 1.333              # Air density (kg/m^3)


# Polar coordinates ##################

r = np.hypot(X, Y)
theta = np.arctan2(Y, X)

beta = theta - alpha

# No fluid exists inside the solid cylinder.
r_safe = np.where(r <= R, np.nan, r)


# Velocity components ################

# Uniform flow + doublet + free vortex

vr = U * (1 - R**2 / r_safe**2) * np.cos(beta)

vt = (-U * (1 + R**2 / r_safe**2) * np.sin(beta)
      + Gamma / (2 * np.pi * r_safe))

# Convert polar velocity to Cartesian
u = vr * np.cos(theta) - vt * np.sin(theta)
v = vr * np.sin(theta) + vt * np.cos(theta)


# Stream function ####################

psi = (U * (r_safe - R**2 / r_safe) * np.sin(beta)
       - Gamma / (2 * np.pi) * np.log(r_safe / R))



# Pressure coefficient ###############

# Bernoulli: lower pressure where velocity is higher
speed = np.hypot(u, v)

Cp = 1 - (speed / U)**2



# Lift calculation ###################

# Positive Gamma is counterclockwise.
# With flow along +x, positive Gamma gives downward lift.

lift_x = rho * U * Gamma * np.sin(alpha)
lift_y = -rho * U * Gamma * np.cos(alpha)

print(f"Circulation: {Gamma:.2f} m^2/s")
print(f"Lift per unit length, x: {lift_x:.3f} N/m")
print(f"Lift per unit length, y: {lift_y:.3f} N/m")


# Visualizations #####################

plot_vector(
    X, Y, u, v,
    title="Cylinder with Circulation: Velocity Field",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

plot_streamlines(
    X, Y, u, v,
    title="Potential Flow Around a Lifting Cylinder",
    density=1.5,
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)

plot_field(
    X, Y, Cp,
    title="Pressure Coefficient Around Cylinder",
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Pressure Coefficient, Cp"
)
