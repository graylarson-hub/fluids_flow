import numpy as np
import matplotlib.pyplot as plt

from fluid_plots import source_or_sink, plot_streamlines


# Coordinate grid ####################

x = np.linspace(-5, 5, 301)
y = np.linspace(-4, 4, 301)

X, Y = np.meshgrid(x, y)


# Flow parameters ####################

U = 2.0         # Uniform flow speed (m/s)
m = 10.0         # Source strength (m^2/s)
a = 3.0          # Half the source-sink separation (m)


# Source and sink #####################

# Source at (-a, 0)
psi1, phi1, ur1, u1, v1 = source_or_sink(
    X, Y, m, -a, 0
)

# Sink at (+a, 0)
psi2, phi2, ur2, u2, v2 = source_or_sink(
    X, Y, -m, a, 0
)


# Superposition ######################

u = U + u1 + u2
v = v1 + v2

psi = U*Y + psi1 + psi2
phi = U*X + phi1 + phi2


# Stagnation points ##################

x_stag = np.sqrt(a**2 + m*a/(np.pi*U))

print(f"Stagnation points: x = +/- {x_stag:.3f} m")
print(f"Oval length: {2*x_stag:.3f} m")


# Velocity streamlines ###############

plot_streamlines(
    X, Y, u, v,
    title="Rankine Oval: Uniform Flow + Source + Sink",
    density=1.2,
    xlabel="x (m)",
    ylabel="y (m)",
    colorbar_label="Speed (m/s)"
)


# Dividing streamline ################

# The source-sink stream function has a branch cut
# between the two singularities. Mask that region
# to avoid drawing false contour lines.

cut = (np.abs(X) < a) & (np.abs(Y) < 0.06)
psi_plot = np.ma.masked_where(cut, psi)

fig, ax = plt.subplots(figsize=(9, 6))

# The zero streamline includes the oval boundary and
# the x-axis portions outside its stagnation points.
ax.contour(
    X, Y, psi_plot,
    levels=[0],
    colors="C0",
    linewidths=2
)

# Source and sink locations
ax.plot(-a, 0, "go", label="Source")
ax.plot(a, 0, "ro", label="Sink")

# Stagnation points
ax.plot(
    [-x_stag, x_stag], [0, 0],
    "ko", label="Stagnation points"
)

ax.set_title("Rankine Oval: Dividing Streamline")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_aspect("equal")
ax.legend()
ax.grid(True, alpha=0.2)

fig.tight_layout()
plt.show()
