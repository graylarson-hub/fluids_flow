"""Simple array-based engineering plots using NumPy and Matplotlib.

Coordinates and fields must be matching 2D arrays. Units depend on the
problem; use axis and colorbar labels to state them. save exports at 300 DPI.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

__all__ = ["plot_field", "plot_vector", "plot_streamlines", "plot_combined",
           "source_or_sink"]


def _check_grid(X, Y):
    """Require finite, matching 2D coordinate arrays."""
    X, Y = np.asarray(X, dtype=float), np.asarray(Y, dtype=float)
    if X.ndim != 2 or Y.shape != X.shape or min(X.shape) < 2:
        raise ValueError("X and Y must be matching 2D arrays with at least 2 points per axis.")
    if not np.all(np.isfinite(X)) or not np.all(np.isfinite(Y)):
        raise ValueError("Grid coordinates must be finite.")
    return X, Y


def _check_field(field, shape):
    """Require a precomputed field, allowing NaNs to mark singularities."""
    if callable(field):
        raise ValueError("Pass a precomputed 2D array, not a callable.")
    field = np.ma.asarray(field, dtype=float)
    if field.shape != shape:
        raise ValueError("Field arrays must have the same 2D shape as X and Y.")
    if not np.any(np.isfinite(field)):
        raise ValueError("Field arrays must contain at least one finite value.")
    return np.ma.masked_invalid(field)


def _streamplot_grid(X, Y):
    """Matplotlib streamplot requires increasing, evenly spaced mesh axes."""
    x, y = X[0, :], Y[:, 0]
    if not np.allclose(X, x[None, :]) or not np.allclose(Y, y[:, None]):
        raise ValueError("Streamplot requires a rectangular meshgrid.")
    dx, dy = np.diff(x), np.diff(y)
    if not np.all(dx > 0) or not np.all(dy > 0):
        raise ValueError("X and Y coordinates must be increasing.")
    if not np.allclose(dx, dx[0]) or not np.allclose(dy, dy[0]):
        raise ValueError("Streamplot requires equally spaced coordinates.")
    return x, y


def _finish(fig, axes, title, xlabel, ylabel, save):
    """Apply shared 2D labels and finish displaying or saving a figure."""
    for ax in axes:
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.2)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=300, bbox_inches="tight")
    plt.show()


def source_or_sink(X, Y, m, xr=0.0, yr=0.0):
    """Evaluate a 2D point source (m > 0) or sink (m < 0).

    X, Y are matching 2D arrays; (xr, yr) is the center, in coordinate
    length units. m is volume flow per unit depth (length squared/time).
    Returns (psi, phi, ur, ux, uy) arrays matching X: psi and phi have
    units length squared/time; velocities have units length/time.
    phi = m/(2*pi)*log(r/r_ref), with r_ref one coordinate unit.
    ux = psi_y = phi_x and uy = -psi_x = phi_y away from the center/cut.
    All fields are NaN at the singular center. psi has an atan2 branch
    cut along the negative x direction; contouring across it is misleading.
    """
    X, Y = _check_grid(X, Y)
    if not all(np.isscalar(value) and np.isfinite(value)
               for value in (m, xr, yr)):
        raise ValueError("m, xr, and yr must be finite scalars.")
    if m == 0:
        raise ValueError("m must be nonzero: positive for a source, negative for a sink.")
    dx, dy = X - xr, Y - yr
    r = np.hypot(dx, dy)
    # The point-flow model is undefined at r=0; do not invent a finite core.
    safe_r = np.where(r == 0, np.nan, r)
    factor = m / (2 * np.pi)
    psi = np.where(r == 0, np.nan, factor * np.arctan2(dy, dx))
    phi = factor * np.log(safe_r)
    ur = factor / safe_r
    ux = ur * (dx / safe_r)
    uy = ur * (dy / safe_r)
    return psi, phi, ur, ux, uy


def plot_field(X, Y, field, title="Scalar Field", levels=20,
               cmap="viridis", save=None, *, surface=False,
               xlabel="X", ylabel="Y", colorbar_label="Field", ax=None):
    """Plot a precomputed scalar field on matching 2D X, Y arrays.

    levels is a contour count or increasing sequence; surface adds a 3D
    panel. Labels may include problem-specific units; save exports at
    300 DPI. Returns (fig, ax), or (fig, (surface_ax, contour_ax)) when
    surface=True. Nonfinite field values are masked. Supply ax for prepared
    2D axes; ax cannot be combined with surface=True.
    """
    X, Y = _check_grid(X, Y)
    field = _check_field(field, X.shape)
    if surface:
        if ax is not None:
            raise ValueError("A supplied ax cannot be used with surface=True.")
        fig = plt.figure(figsize=(14, 6))
        surface_ax = fig.add_subplot(1, 2, 1, projection="3d")
        ax = fig.add_subplot(1, 2, 2)
        surf = surface_ax.plot_surface(X, Y, field.filled(np.nan), cmap=cmap)
        surface_ax.set(title="3D Surface", xlabel=xlabel, ylabel=ylabel,
                       zlabel=colorbar_label)
        fig.colorbar(surf, ax=surface_ax, shrink=0.6, label=colorbar_label)
        fig.suptitle(title)
    elif ax is None:
        fig, ax = plt.subplots(figsize=(9, 7))
    else:
        fig = ax.figure
    filled = ax.contourf(X, Y, field, levels=levels, cmap=cmap)
    fig.colorbar(filled, ax=ax, label=colorbar_label)
    _finish(fig, [ax], "2D Contour" if surface else title, xlabel, ylabel, save)
    return fig, (surface_ax, ax) if surface else ax


def plot_vector(X, Y, u, v, title="Velocity Field", max_arrows=25,
                cmap="viridis", save=None, *, xlabel="X", ylabel="Y",
                colorbar_label="Velocity Magnitude", color=None, ax=None):
    """Quiver plot of precomputed u, v arrays matching 2D X, Y.

    Arrows are colored by magnitude, with at most max_arrows per axis.
    color selects a constant arrow color without a colorbar; None keeps the
    established speed coloring. Supply ax to draw on prepared 2D axes.
    Labels may include units; save exports at 300 DPI. Returns (fig, ax).
    """
    X, Y = _check_grid(X, Y)
    u, v = _check_field(u, X.shape), _check_field(v, X.shape)
    if not isinstance(max_arrows, (int, np.integer)) or max_arrows < 1:
        raise ValueError("max_arrows must be a positive integer.")
    speed = np.hypot(u, v)
    finite_speed = np.ma.masked_invalid(speed).compressed()
    # Use the full field, so downsampling and singularities do not set the colors.
    vmax = np.percentile(finite_speed, 95) if finite_speed.size else 0
    norm = Normalize(vmin=0, vmax=vmax) if vmax > 0 else None
    sx = max(1, int(np.ceil(X.shape[1] / max_arrows)))
    sy = max(1, int(np.ceil(X.shape[0] / max_arrows)))
    sample = (slice(None, None, sy), slice(None, None, sx))
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 7))
    else:
        fig = ax.figure
    if color is None:
        arrows = ax.quiver(X[sample], Y[sample], u[sample], v[sample],
                           speed[sample], cmap=cmap, norm=norm,
                           angles="xy", pivot="mid")
        fig.colorbar(arrows, ax=ax, label=colorbar_label)
    else:
        ax.quiver(X[sample], Y[sample], u[sample], v[sample],
                  color=color, angles="xy", pivot="mid")
    _finish(fig, [ax], title, xlabel, ylabel, save)
    return fig, ax


def plot_streamlines(X, Y, u, v, title="Streamlines", density=1.2,
                     cmap="viridis", save=None, *, xlabel="X", ylabel="Y",
                     colorbar_label="Velocity Magnitude", color=None,
                     linewidth=None, arrowsize=1, ax=None):
    """Streamlines of precomputed u, v arrays matching 2D X, Y.

    X, Y must form an increasing, equally spaced rectangular meshgrid.
    density controls line spacing; color shows speed. Labels may include
    units; save exports at 300 DPI. Returns (fig, ax). Masked singularities
    interrupt numerical streamlines; no stream function is required.
    color selects a constant line color and omits the colorbar;
    None preserves speed coloring. linewidth/arrowsize pass through to Matplotlib.
    Supply ax to prepare geometry/annotations before display or saving.
    """
    X, Y = _check_grid(X, Y)
    u, v = _check_field(u, X.shape), _check_field(v, X.shape)
    x, y = _streamplot_grid(X, Y)
    speed = np.hypot(u, v)
    finite_speed = np.ma.masked_invalid(speed).compressed()
    # Limit colors, not velocities; fall back to automatic scaling for zero speed.
    vmax = np.percentile(finite_speed, 95) if finite_speed.size else 0
    norm = Normalize(vmin=0, vmax=vmax) if vmax > 0 else None
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 7))
    else:
        fig = ax.figure
    stream = ax.streamplot(x, y, u, v, color=speed if color is None else color,
                           cmap=cmap, norm=norm, density=density,
                           linewidth=linewidth, arrowsize=arrowsize)
    if color is None:
        fig.colorbar(stream.lines, ax=ax, label=colorbar_label)
    _finish(fig, [ax], title, xlabel, ylabel, save)
    return fig, ax


def plot_combined(X, Y, psi, phi, title="Flow Visualization", levels=20,
                  save=None, *, xlabel="X", ylabel="Y", ax=None):
    """Overlay precomputed psi and phi arrays matching 2D X, Y.

    Blue contours show psi; orange dashed contours show phi. levels is
    a count or increasing sequence; save exports at 300 DPI. Returns
    (fig, ax). Fields are not calculated or checked for physical consistency.
    Use u=psi_y=phi_x, v=-psi_x=phi_y; a potential requires irrotational
    flow locally, whereas a stream function requires 2D incompressibility.
    Mask angular branch cuts before contouring discontinuous fields.
    Supply ax to add physical geometry before display or saving.
    """
    X, Y = _check_grid(X, Y)
    psi, phi = _check_field(psi, X.shape), _check_field(phi, X.shape)
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 7))
    else:
        fig = ax.figure
    ax.contour(X, Y, psi, levels=levels, colors="royalblue", linewidths=1.2)
    ax.contour(X, Y, phi, levels=levels, colors="darkorange",
               linewidths=1.2, linestyles="dashed")
    ax.legend(handles=[
        Line2D([0], [0], color="royalblue", label="Streamlines (constant psi)"),
        Line2D([0], [0], color="darkorange", linestyle="--",
               label="Equipotential lines (constant phi)")
    ])
    _finish(fig, [ax], title, xlabel, ylabel, save)
    return fig, ax

