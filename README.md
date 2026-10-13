# Two-dimensional fluid-flow visualizations

NumPy and Matplotlib demonstrations of ideal two-dimensional flow, with a small
shared plotting module. The scripts keep the governing equations visible so
engineering students can connect calculations to their plots.

## Requirements and running

Use Python 3 with NumPy **2.0 or newer** and Matplotlib. NumPy 2.0 is required
by the pressure-integration example's `np.trapezoid` call. The Phase 1 checks
used Python 3.14, NumPy 2.5.3, and Matplotlib 3.11.2.

From this directory, using your chosen Python environment:

```powershell
python -m pip install numpy matplotlib
python uniform.py
python cylinder_flow.py
python cyl_pressure_plot.py
```

In VS Code, open this folder, select the Python interpreter containing those
packages, and use **Run Python File in Terminal**. Keep the scripts beside
`fluid_plots.py` so local imports work. Figures open in Matplotlib windows;
close them to continue through scripts with multiple plots. Scripts execute
when run or imported; they are demonstrations, not importable physics APIs.

For a headless run in PowerShell:

```powershell
$env:MPLBACKEND = "Agg"
python cylinder_flow.py
Remove-Item Env:MPLBACKEND
```

A headless run does not open windows. Examples do not save figures by default.

## Demonstrations

| Script | Model or purpose |
| --- | --- |
| `uniform.py` | Uniform flow at an arbitrary angle; velocity, stream function, and potential |
| `uniform_source_sink.py` | Angled uniform flow plus a source and sink, using superposition |
| `rankine.py` | Rankine oval, stagnation-point locations, and dividing streamline |
| `cylinder_flow.py` | Uniform flow plus doublet; nonlifting cylinder with masked interior |
| `vortex.py` | Free vortex with excluded core and finite-difference vorticity check |
| `lift_cyl.py` | Cylinder with circulation, pressure coefficient, and analytical lift per span |
| `cyl_pressure_plot.py` | Cylinder surface pressure and pressure-integrated lift and drag |
| `joukowski_airfoil.py` | Conformal mapping of circulating cylinder streamlines to an airfoil |
| `fun.py`, `test.py` | Overlapping rotational-flow experiments; `test.py` retains unfinished comments and a potential placeholder |

The current superposition script is not a dedicated Rankine half-body demo.
The Joukowski example does not calculate airfoil pressure or lift.

## Shared plotting module

`fluid_plots.py` exports:

- `plot_field(X, Y, field, ...)`: 2D scalar contours; `surface=True` adds a 3D panel.
- `plot_vector(X, Y, u, v, ...)`: magnitude-colored quiver plot with downsampling.
- `plot_streamlines(X, Y, u, v, ...)`: magnitude-colored numerical streamlines.
- `plot_combined(X, Y, psi, phi, ...)`: blue stream-function and orange dashed potential contours.
- `source_or_sink(X, Y, m, xr=0, yr=0)`: returns `(psi, phi, ur, ux, uy)`.

Pass precomputed, matching 2D arrays, not functions. Streamplots require an
increasing, equally spaced rectangular meshgrid. Plot functions return the
figure and axis; scalar plots with `surface=True` return two axes.

Velocity colors span zero to the full field's 95th-percentile finite speed;
NaNs and masks are excluded. Higher velocities retain their numerical values
and use the upper colormap color. Zero fields use automatic normalization.

Labels can state problem-specific units. To save a plot at 300 DPI, create a
local output folder and pass its path:

```python
from pathlib import Path
import numpy as np
from fluid_plots import plot_vector

x = np.linspace(-2, 2, 41)
X, Y = np.meshgrid(x, x)
u, v = np.ones_like(X), np.zeros_like(Y)
Path("figures").mkdir(exist_ok=True)
fig, ax = plot_vector(X, Y, u, v, xlabel="x (m)", ylabel="y (m)",
                      colorbar_label="Speed (m/s)", save="figures/uniform.png")
```

## Assumptions and limitations

These are ideal-flow calculations, not viscous CFD simulations. Potential-flow
examples assume incompressibility and local irrotationality outside singularities.
They do not resolve boundary layers, separation, or viscous drag.

The convention is `u = psi_y = phi_x`, `v = -psi_x = phi_y`. A stream function
can also describe rotational incompressible flow: `fun.py` and `test.py` use
`u=3y`, `v=2x`, which has vorticity -1 and no consistent velocity potential.
Their coordinate/coefficient units are unspecified but must be consistent.

Positive source strength means outward flow; negative means inward flow.
Strength and circulation have units m?/s when coordinates are meters and
velocities m/s. Positive circulation is counterclockwise. For uniform flow
along +x, cylinder lift per span is `-rho * U * Gamma` in the y direction.

Point-source and vortex centers are singular. NaNs and excluded cores prevent
undefined values from being plotted; core masks do not change the ideal-flow
model. Angular stream functions/potentials can have branch cuts; naive contours
across a cut can draw false lines. Masking and grid sensitivity need care.

See [Phase 1 audit](docs/phase1_audit.md) for remaining review items. Coursework
may remain in historical Git commits and requires review before public release.
