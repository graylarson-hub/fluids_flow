# Phase 3A plotting corrections and figure review - 2026-10-12

## Scope and changes

Work was confined to the cleaned `Fluids-Portfolio` Git repository, initially
clean. No parent repository work, moves, deletions, dependencies, commits, remote
changes, or publication were performed. `fluid_plots.py` and its five-function
public API are unchanged. Phase 2 remains the historical mathematical audit;
this report records corrections to its confirmed plotting limitations.

- `rankine.py`: replaced the fixed 0.06 m cut strip; added a conservative
  resolution check and visualization-only source/sink velocity masks.
- `uniform_source_sink.py`: added visualization-only masks to velocity components
  and the plotted potential around unresolved centers. Original arrays remain
  available as `u`, `v`, `psi`, and `phi`.
- `docs/phase3a_review.md`: this report.
- `figures/phase3_review/`: ignored PNGs, diagnostics, and small reproducible
  review scripts. These are review artifacts, not a new testing framework.

## Rankine correction

The branch cut lies on y=0 between -a and +a. Mask just the grid row nearest
zero, across that segment (with half an x-cell allowance for its endpoints).
Set `corner_mask=False`: every quad crossing the jump touches a masked vertex
and is excluded completely, so Matplotlib cannot interpolate a false contour
across it. The omitted band shrinks as the grid is refined. Both odd and even
sample counts are covered; the nearest row can be on either side for even grids.
The original stream function and other analytical equations are untouched.

The independent half-height H solves
`U*H - m/pi*atan(a/H) = 0`. Evaluating that expression at `3*dy` checks whether
H exceeds three vertical intervals, without adding a root-finding helper.
Also require `x_stag-a >= 2*dx` to resolve the narrow nose between each center
and stagnation point. Failure raises a refinement message before figures open.
These are conservative sampling checks for the example's positive U,m,a,
not formal guarantees of contour accuracy. Passing them still calls for refinement
if quantitative boundary coordinates matter.

The reported thin case U=2, m=0.2, a=1 has H=0.0484587168 m. It works with:

```python
x = np.linspace(-1.25, 1.25, 401)
y = np.linspace(-0.15, 0.15, 401)
```

The old strip erased most of its boundary even on that fine grid; the correction
shows both complete sides and their stagnation tips. Keeping a wide domain at a
low sample count is now explicitly identified as under-resolved.

## Singularity investigation

A 301-by-301 grid with a source nominally at (0.2,0.2) samples a representational
near-center rather than necessarily an exact singular point. In the quiver
comparison, automatic arrow scale went from approximately 5.068e14 with raw
samples to 46.91 after omitting unresolved near-center samples. The raw image
has nearly invisible ordinary arrows and one oversized diagonal arrow; its
95th-percentile color limit alone cannot fix arrow geometry.

Both affected source/sink demonstrations now mask samples within one cell diagonal
of either center only when plotting. That distance comes from coordinate resolution,
not viscosity or a prescribed physical core. No values are capped or replaced and
no flow equations are regularized. The mask shrinks with grid refinement.
For Rankine, the velocity mask is separate from the cut mask; the larger velocity
exclusion is not imposed on dividing-streamline contours.

The existing vortex 0.25 m exclusion was already clearly documented as a plotting
mask and showed no corresponding near-center failure, so it was not changed.
The generic plotting module still treats fields as supplied: caller scripts must
choose problem-specific exclusions. Velocity colors continue to use zero to the
95th percentile of the full finite, unmasked field, including quiver downsampling.
The percentile can shift slightly when omitted samples are excluded; the rule is
unchanged. Masked holes do not describe a finite-core fluid model.

## Verification

- All eight requested demonstrations ran at their original grids before and after;
  each set produced 19 figures, with no captured numerical or rendering warnings.
- Twelve resolved Rankine cases passed: (U,m,a)=(2,10,3), (1.5,4,1),
  (3,20,2), and (2,0.2,1), each on three grids. Counts include 101, 200, 201,
  301, 401, 800, and 1201. Four intentionally coarse cases were rejected.
- No cut-crossing false zero contour was found in the tested segment interior.
  Contour heights were compared with independent scalar bisection roots;
  their relative errors were below 1.5% for every resolved case.
- Stagnation velocities were below 1e-10 m/s. Original analytical assignment
  syntax matched the committed baseline, and all unedited demonstration sources
  and `fluid_plots.py` matched their committed contents. Syntax checks passed.
- The affected near-center source/sink example retained its raw extreme velocities,
  excluded them from plotted arrays, restored readable quiver scaling, and matched
  the zero/95th-percentile limits in both artists and colorbars.
- Relevant Phase 2 checks were repeated: positive/negative source flux, cylinder
  pressure integration for Gamma=-20,0,+20 at 30 degrees, the existing vortex
  derivative diagnostic, and the Joukowski Kutta numerator. This was not a rerun
  of all 225 Phase 2 cases.

Measured results: thin-case height errors for n=401,800,1201 were
1.986e-10, 3.590e-09, and 1.281e-11 m.
The near-center example kept raw maximum speed 6.758e+15 m/s;
its plotted maximum was 36.852 m/s and color vmax was
8.446245 m/s. Cylinder force errors were at most
4.263e-14 N/m;
the vortex diagnostic remained 0.00764978 1/s,
a finite-difference residual; Kutta numerator error was
1.105e-15 m/s.

## Visual review and remaining limitations

The before/after overviews, detailed scalar/combined overview, and both diagnostic
comparisons were visually inspected. Native figure sizes and equal spatial aspect
ratios were preserved; the pressure plot correctly keeps negative Cp upward.

| Model | Review outcome / remaining issue |
| --- | --- |
| Uniform flow | Straight streamlines and orthogonal contours; uniform speed correctly has one color. Velocity-axis/colorbar labels lack explicit units. |
| Source/sink superposition | No potential branch-cut artifact; grid cores omit unresolved samples. Default plots do not explicitly label centers or excluded regions. |
| Rankine oval | Default shape preserved; thin boundary restored. Exterior x-axis zero-streamfunction branches remain and are not solid body edges. |
| Nonlifting cylinder | Exterior contours and velocities look consistent; masked interior is a white hole without an explicit solid boundary. |
| Free vortex | Circular streamlines and radial scalar contours; existing excluded core is a white hole, not a physical vortex core. Some numerical streamline fragments stop early. |
| Lifting cylinder | Expected asymmetric velocity/Cp patterns; geometry remains implicit, and the sampled mask edge is slightly stepped. |
| Cylinder surface Cp | Opposite circulation signs shift the distributions consistently. Legend and units are readable at original size. |
| Joukowski airfoil | Circle and airfoil outlines are present; no obvious angular-seam or branch-cut artifact in the reviewed plot. Subplots/near-cusp detail are small in the overview; inspect the full figure. |

Streamplot interruptions can also result from its default streamline termination
and spacing algorithm. Blank regions near masks must not be read as viscous flow.
The nearest-row method assumes the example's increasing uniform mesh contains y=0
and the source-sink segment; it is not a general contour-grid validator. Contour
accuracy, particularly at thin noses, still depends on resolution. Extreme values
can remain in raw arrays by design. Uniform or general arrays passed directly to
`fluid_plots` do not acquire automatic point-flow masks.

## Review artifacts and Phase 3B

Original comparison/diagnostic artifacts remain ignored under `figures/`. The public final assets linked below are tracked under `assets/`:

- [Final selected-example gallery](../assets/gallery_overview.png) (later Phase 4 exports, not the original eight-model review sheet)
- Scalar/vector/combined detail sheets remain local-only; their findings are summarized in the visual review above.
- The thin-oval before/after comparison remains local-only; the Rankine correction above records its parameters and results. The [final geometry asset](../assets/rankine_oval.png) shows the default oval rather than that thin test case.
- The near-center raw/masked arrow comparison remains local-only; the singularity investigation above explains the demonstrated arrow-scaling problem and correction.
- Full-resolution examples: `after_<script>_<figure-number>.png` (300 DPI), with
  corresponding `before_...` files. Examples include `after_cyl_pressure_plot_1.png`
  and `after_joukowski_airfoil_1.png`.
- Reproduction/validation scripts: `review.py`, `validate_rankine.py`,
  `validate_physics.py`; numeric results are in adjacent JSON files. Run from the
  repository root using the project's NumPy/Matplotlib environment.

For Phase 3B, first review these figures together. Then decide on explicit geometry
and source/sink/core labels, consistent units, viewport choices for thin shapes,
and a common presentation style. Consider annotation of saturated velocity colors
and denser sampling near the Joukowski cusp. No broad aesthetic changes were made.
