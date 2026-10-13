# Phase 3C: final scientific visualization styles

## Changes by file

| File | Final presentation |
| --- | --- |
| `uniform.py` | Style A: navy vectors and 0.85 pt streamlines, 0.8-size arrows, meter axes, no speed colorbars. Existing stream-function/potential comparison retained. |
| `cylinder_flow.py` | Style A vectors/streamlines; an exact-radius gray cylinder and dark outline on all three plots. Existing equipotential comparison retained. |
| `rankine.py` | Style A streamlines with labeled point-flow exclusions. Navy dividing boundary, gray dashed exterior zero-streamfunction branches, distinct source/sink and stagnation markers; legend outside the boundary plot. |
| `joukowski_airfoil.py` | Both cylinder and airfoil panels retained, enlarged to an 18 x 7 inch figure. Selected 61 levels over the original -12 to +12 m^2/s range, 0.55 pt navy contours, gray geometry with 1.2 pt dark outline above contours, equal aspect, no grid/colorbar. |
| `uniform_source_sink.py` | Style B: original viridis, existing density 1.5, 0.85 pt streamlines and 0.8-size arrows. Source/sink markers and dashed grid-sized exclusions on vector, streamline and potential plots. |
| `vortex.py` | Style B: original viridis, existing density 1.2, 0.85 pt streamlines and 0.8-size arrows. Dashed exclusion, center marker and explicit non-solid-region note on all three plots. |
| `lift_cyl.py` | Style B: original viridis, existing density 1.5, 0.85 pt streamlines and 0.8-size arrows. Exact-radius gray cylinder/dark outline on vector, streamline and Cp plots. |
| `cyl_pressure_plot.py` | Conventional pressure graph retained: negative Cp upward. Distinct line patterns supplement circulation colors; legend includes circulation units. |
| `fluid_plots.py` | Small backward-compatible keyword additions described below. |

The actual tested navy (#203345), gray fill (#d6d8da), streamline weights and arrow sizes were reused. No scalar-background style was applied. Auxiliary scalar/combined plots retain their quantitative labels and established encodings.

Round 2's 0.55 pt airfoil sample was a larger standalone export; its numerical levels, range, color and line width are reproduced in the required two-panel demonstration. The gallery also supplies a 13 x 9 inch standalone detail, so thumbnail resizing is not the only way to judge thin contours.

## Plotting interface

All five public functions, existing argument defaults, array inputs and return forms remain compatible. `source_or_sink()` is unchanged. Optional `color` on vector/streamline plots chooses a constant color and omits the speed colorbar; `None` preserves the established viridis speed coloring. Streamline `linewidth` and `arrowsize` pass through to Matplotlib with its previous defaults.

Optional `ax` on the four plot functions supports a caller-prepared 2D axis. This lets demonstration scripts draw geometry/annotations before the library's blocking display or export, rather than adding invisible annotations after a window closes. Geometry stays in demonstrations. `plot_field(surface=True)` retains its existing 3D panel/return behavior; a supplied 2D `ax` is incompatible with that mode and raises a clear error. No styling framework, extra public functions or dependencies were added.

## Correctness and verification

- All original calculation assignments were compared structurally with the pre-Phase-3C source snapshots. Mathematical equations, grids, circulation conventions, complex potential, Kutta condition, transformation and sampled geometry are unchanged. The Rankine cut mask, resolution check and visualization-only point-flow masks are preserved.
- All ten demonstration/experiment scripts ran successfully in separate headless Python processes. Only Agg's expected noninteractive `show()` notice was suppressed; every other warning was treated as an error. Both exploratory scripts remain unchanged.
- The eight major demonstrations produced 19 figures before and after, with no captured numerical/rendering warnings. Final main and auxiliary contact sheets, transformation panels, and thin-oval detail were visually inspected.
- Library compatibility checks covered legacy defaults, supplied axes, monochrome colorbar omission, uniform/nonuniform/zero fields, NaNs, infinity, masked samples, full-field percentile limits, quiver values, and optional 3D scalar plotting.
- Twelve resolved Rankine cases passed on odd/even grids; four under-resolved cases were rejected. Thin-case U=2, m=0.2, a=1 height errors on n=401/800/1201 were 1.99e-10 / 3.59e-9 / 1.28e-11 m. The added boundary highlight clips only at analytical stagnation coordinates; it adds no sampled mask that could erase the narrow tips.
- The near-center source test retains raw maximum speed 6.758e15 m/s, plotted maximum 36.852 m/s and p95 8.446245 m/s. No velocities were capped. Relevant Phase 2 checks passed: source/sink flux, cylinder pressure-force integration for both circulation signs, vortex derivative diagnostic (0.00764978 1/s), and Kutta numerator (1.105e-15 m/s). This is not a rerun of all 225 historical cases.

## Review images

Original review artifacts are ignored under `figures/phase3_final_review/`. The public final exports linked below are tracked under `assets/`.

- [Final selected-example gallery](../assets/gallery_overview.png) (later Phase 4 exports)
- Auxiliary vector/scalar/combined review sheets remain local-only; the demonstration scripts retain those plots.
- The two-panel transformation review remains local-only; [joukowski_airfoil.py](../joukowski_airfoil.py) displays the original circle and transformed airfoil together.
- [Final standalone airfoil export](../assets/hero_joukowski_airfoil.png)
- The thin-oval review image remains local-only; its numerical results are recorded above. Public assets show the default [Rankine geometry](../assets/rankine_oval.png) and [explanatory exterior flow](../assets/rankine_oval_streamlines_explanatory.png).
- Individual 300 DPI figures: `after_<script>_<number>.png` (19 total).
- Seven 200 DPI before/after sheets: `compare_<script>.png`; individual baseline exports are also retained.
- Reproduction/check scripts and JSON results: `review.py`, `gallery.py`, `validate_styles.py`, `validate_rankine.py`, `validate_physics.py` and adjacent JSON files. Baseline Python copies/hashes are ignored review snapshots.

## Remaining limitations and stopping point

Original viridis is intentionally untrimmed: high-speed yellow thin lines have weaker contrast on white. Percentile saturation cannot distinguish speeds above the ceiling, and streamline fragments from Matplotlib tracing persist. Singular exclusions do not indicate solid objects or viscous cores. Rankine tips and the Joukowski cusp still have the established finite-grid/sampled-boundary limitations.

An artificial all-zero quiver produces inherited Matplotlib automatic-arrow-scaling warnings (also reproduced with the baseline library); its color normalization remains compatible. No demonstration uses that field, and no unrelated arrow-scaling correction was introduced.

No parent-coursework files, previous phase reports, README, dependencies, folder organization or exploratory scripts were changed. No commits, pushes or publication. Phase 3C stops here for review before README/GitHub presentation work.

## Final local source/sink color normalization

The source/sink demonstration's streamline plot now uses the 10th through 95th
percentiles of the full finite, unmasked speed field with original viridis.
For the existing 300 x 300 grid, the limits are 7.658998 to 8.990441 m/s.
The speed colorbar has extensions at both ends: speeds outside this interval
share endpoint colors, while their calculated values remain unchanged.
The vector plot and all global library normalization defaults retain zero-to-p95
scaling. Equations, grid, streamline paths/arrows, markers and dashed exclusions
are preserved. The final streamline export, final overview, and source/sink
before/after sheet were refreshed; the four-option comparison remains a review
artifact of the normalization choices.
