# Plotting API reference

The public API is the five functions in [fluid_plots.py](../fluid_plots.py). The four plotters accept **precomputed arrays, not callables**, and display fields rather than solving flow equations. [Mathematical reference](mathematical_reference.md) describes their physical conventions.

## Shared input and display behavior

Coordinates `X`, `Y` must be finite, matching 2D arrays with at least two samples per dimension. Fields must match that shape and contain usable finite data; NumPy masked arrays are accepted and NaN/infinity values are masked. Plotters convert data to floating-point arrays. They do not infer physical boundaries, angular branch cuts or singularity exclusions. Choose those masks in the calling calculation.

All four plotters accept `save=None`: a supplied filename exports at 300 DPI with a tight bounding box before display. Create the destination directory first. They call `plt.show()`, apply equal spatial aspect and a light grid to 2D axes, and return Matplotlib objects for inspection. Supplied `ax` allows geometry to be prepared before display; `surface=True` creates its own axes.

For speed-colored vectors/streamlines, normalization is zero to P95 of the full finite unmasked magnitude field. Values outside the color range keep their velocities but share endpoint colors. Zero-only speed fields fall back to Matplotlib normalization. The local P10-P95 source/sink example uses Matplotlib directly and does not change this API default. Constant-color figures have no speed colorbar.

## `plot_field()`

```python
plot_field(X, Y, field, title='Scalar Field', levels=20, cmap='viridis', save=None, *, surface=False, xlabel='X', ylabel='Y', colorbar_label='Field', ax=None)
```

Plot a precomputed scalar field. Required: `X`, `Y`, `field`, all matching `(ny, nx)` arrays.

- `title="Scalar Field"`, `levels=20` (count or increasing levels), `cmap="viridis"`.
- `surface=False`: filled contours with a colorbar. `surface=True`: additional 3D surface and separate colorbars; returns `(fig, (surface_ax, contour_ax))`.
- Otherwise returns `(fig, ax)`. `ax=None` creates a new axis; a supplied axis cannot be combined with `surface=True`.
- Default labels are `"X"`, `"Y"`, `"Field"`. Nonfinite scalar samples are masked. Contour interpolation near masks remains resolution-dependent.

## `plot_vector()`

```python
plot_vector(X, Y, u, v, title='Velocity Field', max_arrows=25, cmap='viridis', save=None, *, xlabel='X', ylabel='Y', colorbar_label='Velocity Magnitude', color=None, ax=None)
```

Plot quiver arrows from precomputed `u`, `v` on matching `(ny, nx)` `X`, `Y` arrays. Returns `(fig, ax)`.

- `title="Velocity Field"`, `max_arrows=25`: positive integer limiting samples to at most this count per axis. The complete field sets the color normalization before downsampling.
- `cmap="viridis"`, `color=None`: speed-colored arrows and speed colorbar. A constant `color` omits the colorbar.
- Defaults: `xlabel="X"`, `ylabel="Y"`, `colorbar_label="Velocity Magnitude"`, `ax=None`.
- Nonfinite/masked velocity samples are omitted. Arrow scaling is Matplotlib's automatic scaling; percentile colors do not prevent extreme unmasked velocities from affecting arrow lengths. An artificial all-zero quiver can emit inherited automatic-scaling warnings.

## `plot_streamlines()`

```python
plot_streamlines(X, Y, u, v, title='Streamlines', density=1.2, cmap='viridis', save=None, *, xlabel='X', ylabel='Y', colorbar_label='Velocity Magnitude', color=None, linewidth=None, arrowsize=1, ax=None)
```

Numerically trace streamlines from matching precomputed `(ny, nx)` `X`, `Y`, `u`, `v`. Coordinates must be an increasing, evenly spaced rectangular meshgrid. Returns `(fig, ax)`.

- `title="Streamlines"`, `density=1.2` controls tracing density, not grid resolution.
- `cmap="viridis"`, `color=None`: color by local speed with a colorbar. Constant `color` omits the colorbar.
- `linewidth=None` and `arrowsize=1` pass through to Matplotlib.
- Default labels: `"X"`, `"Y"`, `"Velocity Magnitude"`; `ax=None` creates a new axis.
- Masked/nonfinite velocities interrupt tracing. No stream function is required; no automatic body geometry or singularity radius is inferred.

## `plot_combined()`

```python
plot_combined(X, Y, psi, phi, title='Flow Visualization', levels=20, save=None, *, xlabel='X', ylabel='Y', ax=None)
```

Overlay constant-streamfunction and equipotential contours. Required: matching `(ny, nx)` `X`, `Y`, `psi`, `phi` arrays. Returns `(fig, ax)`.

- `title="Flow Visualization"`, `levels=20` (count or increasing sequence).
- Stream-function contours are blue and potential contours orange/dashed.
- Default labels: `xlabel="X"`, `ylabel="Y"`; `ax=None` creates a new axis.
- Each field's nonfinite values are masked. Caller must mask angular branch cuts before contouring; the function cannot recognize their physical location.

## `source_or_sink()`

```python
source_or_sink(X, Y, m, xr=0.0, yr=0.0)
```

Evaluate a point flow on matching finite `(ny, nx)` coordinate arrays. Required scalar `m` is finite and nonzero; `m>0` is a source, `m<0` a sink. Optional finite center coordinates `xr=0.0`, `yr=0.0` use the same length units as the grid.

Returns `(psi, phi, ur, ux, uy)`, each matching the grid. Stream function and potential have units length squared/time, velocities length/time. The logarithmic reference distance is one coordinate unit. All five outputs are NaN at exactly zero radius. Near-center finite samples can be extremely large; this function introduces no finite core or grid-sized mask. `psi` uses a principal `atan2` branch cut along the negative x direction from the center. No figures are created.

## Example: precomputed uniform flow

```python
from pathlib import Path
import numpy as np
from fluid_plots import plot_streamlines, source_or_sink

x = np.linspace(-2, 2, 81)
X, Y = np.meshgrid(x, x)
u = np.full_like(X, 2.0)
v = np.zeros_like(Y)
Path("figures").mkdir(exist_ok=True)
fig, ax = plot_streamlines(
    X, Y, u, v, color="#203345", linewidth=0.85,
    xlabel="x (m)", ylabel="y (m)",
    save="figures/uniform_example.png",
)
psi, phi, ur, ux, uy = source_or_sink(X, Y, m=2.0, xr=0.0, yr=0.0)
```

The uniform example has constant speed, so a quantitative colorbar is unnecessary. The separate point-source arrays have NaNs at the center; do not contour their angular cut without a suitable mask. For interactive demonstrations, close each figure window to continue. For batch verification, set `MPLBACKEND=Agg` before starting Python; this renders without GUI windows but does not save figures unless `save` is provided.

See [Phase 3C](phase3c_review.md) for approved styling and [Phase 4A](phase4a_assets.md) for export-only geometry choices. This reference is not a compatibility guarantee for every Matplotlib backend.
