"""
FLUID_PLOTS.PY
==============

Reusable plotting functions for engineering and fluid mechanics.

REQUIRED LIBRARIES:
    numpy
    matplotlib

HOW TO IMPORT:
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

BASIC SETUP:
    import numpy as np

    x = np.linspace(-5, 5, 201)
    y = np.linspace(-5, 5, 201)

    X, Y = np.meshgrid(x, y)

    # Define a scalar function
    def f(X, Y):
        return X**2 - Y**2

    # Define velocity components
    def u(X, Y):
        return 2 * X

    def v(X, Y):
        return -2 * Y
    
    
    # Stream function
    def psi(X, Y):
        return 2 * X * Y

    # Velocity potential
    def phi(X, Y):
        return X**2 - Y**2

FUNCTION REFERENCE:
    plot_field(X, Y, f)
        3D surface + 2D contour plot.

    plot_vector(X, Y, u, v)
        Velocity vector field (quiver plot).

    plot_streamlines(X, Y, u, v)
        Streamlines calculated from velocity components.

    plot_combined(X, Y, psi, phi)
        Overlay stream function and velocity potential.

    source_or_sink(X, Y, m, xr=0, yr=0)
        Return psi, phi, radial velocity, x velocity, and y velocity.

    plot_source_sink(X, Y, m, xr=0, yr=0)
        Plot radial streamlines and circular equipotential lines.

    source_sink_pair(X, Y, m, separation=1, xr=0, yr=0, angle=0)
        Return psi, phi, ux, uy for an equal source and sink.

    plot_source_sink_pair(X, Y, m, separation=1, xr=0, yr=0, angle=0)
        Overlay pair streamlines (with flow arrows) and equipotentials.

EXAMPLES:
    plot_field(X, Y, f, title="Scalar Field")

    plot_vector(X, Y, u, v, title="Velocity Field")

    plot_streamlines(X, Y, u, v, density=1.5)

    plot_combined(X, Y, psi, phi, levels=25)

    plot_source_sink(X, Y, m=1.0)   # Positive strength: source
    plot_source_sink(X, Y, m=-1.0)  # Negative strength: sink

    plot_source_sink_pair(X, Y, m=1.0, separation=1.0)

NOTES:
    - X and Y must be matching 2D meshgrids.
    - Functions should use NumPy-compatible operations.
    - All four plotting functions accept mathematical functions
      or precomputed NumPy arrays.
    - Use save="filename.png" to export figures at 300 DPI.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def source_or_sink(X, Y, m, xr=0.0, yr=0.0):
    """Evaluate a 2D point source (m > 0) or sink (m < 0).

    X, Y are matching 2D meshgrids; (xr, yr) is the center.
    m is volume flow rate per unit depth (length squared / time).
    Returns (psi, phi, ur, ux, uy), each with the meshgrid shape:

        psi = m / (2*pi) * atan2(Y - yr, X - xr)
        phi = m / (2*pi) * log(r / r_ref)
        ur  = m / (2*pi*r)

    r_ref is one coordinate unit; changing it only adds a constant
    to phi. The convention is ux = d(phi)/dx = d(psi)/dy and
    uy = d(phi)/dy = -d(psi)/dx. All fields are NaN at the singular
    center. psi has a branch cut along the negative x direction
    from the center; use plot_source_sink for a combined plot that
    avoids interpolating contours across that discontinuity.
    """
    X, Y = _check_grid(X, Y)
    if not all(np.isscalar(value) and np.isfinite(value)
               for value in (m, xr, yr)):
        raise ValueError("m, xr, and yr must be finite scalars.")
    if m == 0:
        raise ValueError("m must be nonzero: positive for a source, negative for a sink.")

    dx, dy = X - xr, Y - yr
    r = np.hypot(dx, dy)
    safe_r = np.where(r == 0, np.nan, r)
    factor = m / (2 * np.pi)
    psi = np.where(r == 0, np.nan, factor * np.arctan2(dy, dx))
    phi = factor * np.log(safe_r)
    ur = factor / safe_r
    ux = ur * (dx / safe_r)
    uy = ur * (dy / safe_r)
    return psi, phi, ur, ux, uy


def plot_source_sink(X, Y, m, xr=0.0, yr=0.0, title=None,
                     levels=20, save=None):
    """Plot stream-function and potential contours for a point source/sink.

    Positive m gives outward flow; negative m gives inward flow.
    levels is the number of radial streamlines and the approximate
    number of potential contours. Streamlines are drawn analytically
    as rays to avoid false contours at the atan2 branch cut.
    Blue solid rays have constant psi; orange dashed contours have
    constant phi. Returns (fig, ax), like plot_combined. Optional save
    exports at 300 DPI. Use source_or_sink with plot_field to inspect
    the individual scalar fields (psi is discontinuous at its cut).
    """
    X, Y = _check_grid(X, Y)
    if (min(X.shape) < 2 or not np.all(np.isfinite(X))
            or not np.all(np.isfinite(Y))
            or np.ptp(X) == 0 or np.ptp(Y) == 0):
        raise ValueError("The plot needs a finite grid spanning both axes.")
    if not isinstance(levels, (int, np.integer)) or levels < 2:
        raise ValueError("levels must be an integer of at least 2.")
    _, phi, _, _, _ = source_or_sink(X, Y, m, xr, yr)

    fig, ax = plt.subplots(figsize=(9, 7))
    # Each ray is a constant angle, hence a constant stream function.
    radius = np.max(np.hypot(X - xr, Y - yr))
    for theta in np.linspace(-np.pi, np.pi, levels, endpoint=False):
        ax.plot([xr, xr + radius * np.cos(theta)],
                [yr, yr + radius * np.sin(theta)],
                color="royalblue", linewidth=1.2)
    ax.contour(X, Y, phi, levels=levels, colors="darkorange",
               linewidths=1.2, linestyles="dashed")
    kind = "Source" if m > 0 else "Sink"
    ax.plot(xr, yr, "o", color="black", markersize=5)
    ax.legend(handles=[
        Line2D([0], [0], color="royalblue", lw=2,
               label="Streamlines (constant psi)"),
        Line2D([0], [0], color="darkorange", lw=2, linestyle="--",
               label="Equipotential lines (constant phi)")
    ])
    direction = "outward" if m > 0 else "inward"
    ax.set_title(title if title is not None else
                 f"{kind}: m = {m:g}, flow {direction}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xlim(np.min(X), np.max(X))
    ax.set_ylim(np.min(Y), np.max(Y))
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")
    plt.show()
    return fig, ax

def _pair_centers(separation, xr, yr, angle):
    if not all(np.isscalar(value) and np.isfinite(value)
               for value in (separation, xr, yr, angle)):
        raise ValueError("separation, xr, yr, and angle must be finite scalars.")
    if separation <= 0:
        raise ValueError("separation must be positive; zero needs an ideal-doublet formula.")
    dx = 0.5 * separation * np.cos(angle)
    dy = 0.5 * separation * np.sin(angle)
    return (xr - dx, yr - dy), (xr + dx, yr + dy)


def source_sink_pair(X, Y, m, separation=1.0, xr=0.0, yr=0.0, angle=0.0):
    """Evaluate an equal-strength source/sink pair (a finite doublet).

    (xr, yr) is the midpoint; separation is the distance between centers.
    angle is in radians, counterclockwise from +X toward the sink for
    positive m. At angle=0, +m is on the left and -m is on the right.
    Negative m reverses the flow. m has units of length squared / time.

    Returns (psi, phi, ux, uy) arrays, by superposition:
        phi = m/(2*pi) * log(r_source/r_sink)
        psi = m/(2*pi) * (theta_source - theta_sink)
    psi uses the principal angle difference, with a branch cut on the
    segment joining the centers. All fields are NaN at either center.
    Velocity follows ux = phi_x = psi_y, uy = phi_y = -psi_x.

    The ideal doublet is the limit separation -> 0 with m*separation
    fixed. This function evaluates the finite pair, not that limit.
    Use plot_source_sink_pair to avoid false contours across psi's cut.
    """
    X, Y = _check_grid(X, Y)
    first, second = _pair_centers(separation, xr, yr, angle)
    psi_a, phi_a, _, ux_a, uy_a = source_or_sink(X, Y, m, *first)
    psi_b, phi_b, _, ux_b, uy_b = source_or_sink(X, Y, -m, *second)
    # Wrap the angle difference so the cut lies only between the centers.
    theta = (psi_a + psi_b) * (2 * np.pi / m)
    psi = m / (2 * np.pi) * np.arctan2(np.sin(theta), np.cos(theta))
    return psi, phi_a + phi_b, ux_a + ux_b, uy_a + uy_b


def plot_source_sink_pair(X, Y, m, separation=1.0, xr=0.0, yr=0.0,
                          angle=0.0, title="Source-Sink Pair (Finite Doublet)",
                          levels=20, density=1.2, save=None):
    """Plot pair streamlines and equipotentials; return (fig, ax).

    X, Y must be increasing, equally spaced rectangular meshgrids.
    Parameters m, separation, xr, yr, angle follow source_sink_pair.
    Blue streamlines are integrated from velocity (constant psi), with
    arrows from source to sink. This avoids psi's angular branch cut.
    Orange dashed lines are constant phi; levels controls their count.
    density controls streamline density. save exports a 300 DPI image.
    """
    X, Y = _check_grid(X, Y)
    x, y = _streamplot_grid(X, Y)
    if not isinstance(levels, (int, np.integer)) or levels < 2:
        raise ValueError("levels must be an integer of at least 2.")
    _, phi, ux, uy = source_sink_pair(X, Y, m, separation, xr, yr, angle)
    first, second = _pair_centers(separation, xr, yr, angle)
    # Omit the unresolved cores even when a center falls between samples.
    core = np.hypot(x[1] - x[0], y[1] - y[0])
    mask = ((np.hypot(X - first[0], Y - first[1]) <= core)
            | (np.hypot(X - second[0], Y - second[1]) <= core))
    if np.all(mask):
        raise ValueError("Use a finer or wider grid to resolve the pair.")
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.streamplot(x, y, np.ma.masked_where(mask, ux),
                  np.ma.masked_where(mask, uy), color="royalblue",
                  density=density, linewidth=1.2, arrowsize=1.2,
                  broken_streamlines=False)
    ax.contour(X, Y, np.ma.masked_where(mask, phi), levels=levels,
               colors="darkorange", linewidths=1.2, linestyles="dashed")
    source, sink = (first, second) if m > 0 else (second, first)
    source_marker, = ax.plot(*source, "o", color="green", label="Source")
    sink_marker, = ax.plot(*sink, "o", color="crimson", label="Sink")
    ax.legend(handles=[
        Line2D([0], [0], color="royalblue", lw=2,
               label="Streamlines (constant psi)"),
        Line2D([0], [0], color="darkorange", lw=2, linestyle="--",
               label="Equipotential lines (constant phi)"),
        source_marker, sink_marker
    ], loc="upper right")
    ax.set(title=title, xlabel="X", ylabel="Y",
           xlim=(x[0], x[-1]), ylim=(y[0], y[-1]))
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")
    plt.show()
    return fig, ax


# ============================================================
# INTERNAL HELPER
# ============================================================

def _streamplot_grid(X, Y):
    """Validate a streamplot grid and return its coordinate axes."""
    x, y = X[0, :], Y[:, 0]
    if len(x) < 2 or len(y) < 2:
        raise ValueError("The grid needs at least 2 points per axis.")
    if not np.all(np.isfinite(X)) or not np.all(np.isfinite(Y)):
        raise ValueError("Grid coordinates must be finite.")
    if not np.allclose(X, x[None, :]) or not np.allclose(Y, y[:, None]):
        raise ValueError("Streamplot requires a rectangular meshgrid.")
    if not np.all(np.diff(x) > 0) or not np.all(np.diff(y) > 0):
        raise ValueError("X and Y coordinates must be increasing.")
    if (not np.allclose(np.diff(x), np.diff(x)[0])
            or not np.allclose(np.diff(y), np.diff(y)[0])):
        raise ValueError("Streamplot requires equally spaced coordinates.")
    return x, y


def _evaluate(field, X, Y):
    """
    Evaluate a function or accept an existing array.
    Ensures the result has the same shape as the meshgrid.
    """

    if callable(field):
        Z = field(X, Y)
    else:
        Z = field

    Z = np.asarray(Z, dtype=float)

    try:
        return np.broadcast_to(Z, X.shape)
    except ValueError:
        raise ValueError(
            "Field dimensions must match the meshgrid."
        )


def _check_grid(X, Y):
    """Check that X and Y are matching 2D arrays."""

    X = np.asarray(X)
    Y = np.asarray(Y)

    if X.ndim != 2 or Y.ndim != 2 or X.shape != Y.shape:
        raise ValueError("X and Y must be matching 2D meshgrids.")

    return X, Y


# ============================================================
# SCALAR FIELD / 3D SURFACE + CONTOUR
# ============================================================

def plot_field(X, Y, func, title="Scalar Field",
               levels=20, cmap="viridis", save=None):
    """
    Plot a 3D surface and 2D contour of a scalar function.

    Parameters
    ----------
    X, Y : numpy.ndarray
        2D coordinate arrays generated by np.meshgrid().

    func : callable or numpy.ndarray
        Mathematical function or precomputed scalar field.

    title : str
        Figure title.

    levels : int
        Number of contour levels.

    cmap : str
        Matplotlib colormap.

    save : str or None
        Optional filename for exporting a 300 DPI image.

    Returns
    -------
    fig, axes
        Matplotlib figure and axes objects.
    """

    X, Y = _check_grid(X, Y)
    Z = _evaluate(func, X, Y)

    fig = plt.figure(figsize=(14, 6))

    # 3D Surface
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")

    surf = ax1.plot_surface(
        X, Y, Z,
        cmap=cmap,
        edgecolor="none",
        rcount=100,
        ccount=100
    )

    ax1.set_title("3D Surface")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("f(X,Y)")

    fig.colorbar(surf, ax=ax1, shrink=0.6)

    # 2D Contour
    ax2 = fig.add_subplot(1, 2, 2)

    filled = ax2.contourf(
        X, Y, Z,
        levels=levels,
        cmap=cmap
    )

    lines = ax2.contour(
        X, Y, Z,
        levels=filled.levels,
        colors="black",
        linewidths=0.6
    )

    ax2.clabel(lines, inline=True, fontsize=8)

    ax2.set_title("2D Contour")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_aspect("equal", adjustable="box")

    fig.colorbar(filled, ax=ax2, label="f(X,Y)")

    fig.suptitle(title, fontsize=14)

    fig.tight_layout(rect=[0, 0, 1, 0.95])

    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")

    plt.show()

    return fig, (ax1, ax2)


# ============================================================
# VECTOR FIELD / QUIVER PLOT
# ============================================================

def plot_vector(X, Y, u, v, title="Velocity Field",
                max_arrows=25, cmap="viridis", save=None):
    """
    Plot a 2D velocity vector field using arrows.

    Parameters
    ----------
    X, Y : numpy.ndarray
        2D coordinate arrays generated by np.meshgrid().

    u, v : callable or numpy.ndarray
        Horizontal and vertical velocity components.

    title : str
        Figure title.

    max_arrows : int
        Approximate maximum number of arrows per axis.

    cmap : str
        Matplotlib colormap.

    save : str or None
        Filename for exporting a 300 DPI image.

    Returns
    -------
    fig, ax
        Matplotlib figure and axes objects.

    Example
    -------
    >>> plot_vector(X, Y, u, v, title="Velocity Field")
    """

    X, Y = _check_grid(X, Y)

    U = _evaluate(u, X, Y)
    V = _evaluate(v, X, Y)

    speed = np.sqrt(U**2 + V**2)

    # Downsample arrows for readability
    sx = max(1, int(np.ceil(X.shape[1] / max_arrows)))
    sy = max(1, int(np.ceil(X.shape[0] / max_arrows)))

    fig, ax = plt.subplots(figsize=(9, 7))

    q = ax.quiver(
        X[::sy, ::sx],
        Y[::sy, ::sx],
        U[::sy, ::sx],
        V[::sy, ::sx],
        speed[::sy, ::sx],
        cmap=cmap,
        angles="xy",
        pivot="mid"
    )

    fig.colorbar(q, ax=ax, label="Velocity Magnitude")

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")

    plt.show()

    return fig, ax


# ============================================================
# STREAMLINE PLOT
# ============================================================

def plot_streamlines(X, Y, u, v, title="Streamlines",
                     density=1.2, cmap="viridis", save=None):

    """
    Plot streamlines calculated from a 2D velocity field.

    Parameters
    ----------
    X, Y : numpy.ndarray
        Regular, equally spaced 2D coordinate meshgrids.

    u, v : callable or numpy.ndarray
        Horizontal and vertical velocity components.

    title : str
        Figure title.

    density : float
        Controls streamline density (default 1.2).

    cmap : str
        Matplotlib colormap for velocity magnitude.

    save : str or None
        Optional filename for exporting a 300 DPI image.

    Returns
    -------
    fig, ax
        Matplotlib figure and axes objects.

    Notes
    -----
    Streamlines are calculated numerically from the velocity
    components. A stream function is not required.
    """
    
    X, Y = _check_grid(X, Y)

    U = _evaluate(u, X, Y)
    V = _evaluate(v, X, Y)

    speed = np.sqrt(U**2 + V**2)

    x, y = _streamplot_grid(X, Y)

    fig, ax = plt.subplots(figsize=(9, 7))

    stream = ax.streamplot(
        x, y, U, V,
        color=speed,
        cmap=cmap,
        density=density,
        linewidth=1.3,
        arrowsize=1.2
    )

    fig.colorbar(
        stream.lines,
        ax=ax,
        label="Velocity Magnitude"
    )

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")

    plt.show()

    return fig, ax



# ============================================================
# COMBINED STREAM FUNCTION + VELOCITY POTENTIAL
# ============================================================



def plot_combined(X, Y, psi, phi, title="Flow Visualization",
                  levels=20, save=None):

    
    """
    Overlay streamlines and equipotential lines.

    Parameters
    ----------
    X, Y : numpy.ndarray
        2D coordinate arrays generated by np.meshgrid().

    psi : callable or numpy.ndarray
        Stream function.

    phi : callable or numpy.ndarray
        Velocity potential.

    title : str
        Figure title.

    levels : int
        Approximate number of contour levels (default 20).

    save : str or None
        Optional filename for exporting a 300 DPI image.

    Returns
    -------
    fig, ax
        Matplotlib figure and axes objects.

    Notes
    -----
    Blue solid lines represent streamlines.
    Orange dashed lines represent equipotential lines.

    For a consistent 2D incompressible, irrotational flow,
    these two contour families are orthogonal wherever
    velocity is nonzero.
    """

    X, Y = _check_grid(X, Y)

    PSI = _evaluate(psi, X, Y)
    PHI = _evaluate(phi, X, Y)

    fig, ax = plt.subplots(figsize=(9, 7))

    # Stream function contours
    ax.contour(
        X, Y, PSI,
        levels=levels,
        colors="royalblue",
        linewidths=1.2
    )

    # Velocity potential contours
    ax.contour(
        X, Y, PHI,
        levels=levels,
        colors="darkorange",
        linewidths=1.2,
        linestyles="dashed"
    )

    # Legend
    legend_elements = [
        Line2D(
            [0], [0],
            color="royalblue",
            lw=2,
            label="Streamlines"
        ),
        Line2D(
            [0], [0],
            color="darkorange",
            lw=2,
            linestyle="--",
            label="Equipotential Lines"
        )
    ]

    ax.legend(handles=legend_elements)

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.2)

    fig.tight_layout()

    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")

    plt.show()

    return fig, ax

