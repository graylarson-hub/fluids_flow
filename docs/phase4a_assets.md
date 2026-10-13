# Phase 4A: Featured figure assets

Exported the six selected demonstrations as eight individual assets (two complementary Rankine views) using the finalized Phase 3 settings. All individual assets are white-background, 300 DPI PNGs with tight bounding boxes. Spatial plots retain equal aspect ratios and meter labels; velocity colorbars use m/s. No README rewrite was performed.

## Asset sources

| Source script | Export | Pixels | Selected presentation |
| --- | --- | --- | --- |
| `joukowski_airfoil.py` | [hero_joukowski_airfoil.png](../assets/hero_joukowski_airfoil.png) | 2692 x 2101 | Style A; actual transformed-airfoil panel, 61 contour levels over -12 to 12, 0.55-point navy lines, gray body and clear boundary |
| `rankine.py` | [rankine_oval.png](../assets/rankine_oval.png) | 3113 x 1834 | Style A dividing-streamline figure; source, sink and stagnation markers; exterior zero-streamfunction branches distinguished by dashes |
| `rankine.py` | [rankine_oval_streamlines.png](../assets/rankine_oval_streamlines.png) | 2368 x 1979 | Style A exterior velocity streamlines; polygon-masked light-gray interior with a dark dividing-streamline outline; clean version without point markers; no speed colorbar because color is constant |
| `rankine.py` | [rankine_oval_streamlines_explanatory.png](../assets/rankine_oval_streamlines_explanatory.png) | 2368 x 1979 | README-selected exterior-flow view with source, sink and stagnation markers; same polygon-masked interior and Style A settings |
| `lift_cyl.py` | [lifting_cylinder.png](../assets/lifting_cylinder.png) | 2256 x 2030 | Style B, original viridis, full finite unmasked field zero-to-P95 normalization, solid gray cylinder |
| `cyl_pressure_plot.py` | [cylinder_pressure_coefficient.png](../assets/cylinder_pressure_coefficient.png) | 2668 x 1768 | Engineering pressure plot; negative Cp upward, distinct circulation curves, degrees and circulation units |
| `vortex.py` | [free_vortex.png](../assets/free_vortex.png) | 2296 x 2030 | Style B, original viridis, zero-to-P95 normalization; dashed excluded singularity explicitly identified as non-solid |
| `uniform_source_sink.py` | [source_sink_superposition.png](../assets/source_sink_superposition.png) | 2296 x 2025 | Style B, original viridis, approved local P10-P95 normalization; point markers and dashed exclusions preserved |

The optional [gallery_overview.png](../assets/gallery_overview.png) is a 2705 x 2501 pixel, 150 DPI contact sheet. Use the individual figures for detailed inspection and README presentation.

## Rankine asset roles

`rankine_oval.png` is the clean geometry/dividing-streamline illustration, including source, sink and stagnation points. It remains unchanged from the original Phase 4A export. `rankine_oval_streamlines.png` shows only the exterior velocity-field flow pattern. The enclosed region is excluded for visualization and filled light gray with a dark outline; the analytical interior field is retained unchanged. The clean asset omits point markers. The [explanatory asset](../assets/rankine_oval_streamlines_explanatory.png) retains source, sink and stagnation markers and is selected for the README. It is an exact copy of the full-resolution explanatory review image; the clean version remains available. Both use the approved minimal scientific Style A, with equal spatial aspect and meter labels. The new asset is not speed-colored, so it has no quantitative colorbar. The overview now includes both views.

## Export method and changes

No permanent demonstration or library changes were needed. The ignored runner `figures/phase4a_review/export_assets.py` executes the existing scripts with the Agg backend and exports their actual Matplotlib figures. Concise standalone titles are changed in memory. The Rankine streamline asset extracts the upper and lower oval arcs from the existing zero-streamfunction contour using the corrected branch-cut mask (`corner_mask=False`). Unrelated zero-streamfunction axis branches are excluded. The arcs are joined at the validated analytical stagnation points to close the small gaps at the tips. A Matplotlib `Path.contains_points` polygon test masks interior grid points in copies of the plotting velocities before streamline tracing. Existing point-singularity masks are retained. The same path supplies the light-gray fill and dark outline, so the mask and drawn boundary agree. No rectangular mask, fixed-width interior exclusion, physical equation changes or artificial core is introduced. The hero is a tight crop of the existing airfoil panel, including its title and axes labels; the original two-panel demonstration remains unchanged. No field resampling was used; the Rankine polygon is derived from the existing masked streamfunction contour.

The new permanent deliverables are the PNGs in `assets/` and this report. The assets directory is eligible for version control; nothing was staged or committed. Export checks and 900-pixel preview copies are kept in the ignored `figures/phase4a_review/` directory. To reproduce from the portfolio root, run `python -B figures/phase4a_review/export_assets.py`.

## Verification

- All 10 existing demonstration/experiment scripts completed successfully headlessly. Numerical and rendering warnings were treated as errors; only the expected noninteractive-backend `show()` notice was suppressed for subprocess runs. Asset rendering produced no warnings.
- Assertions checked the approved airfoil contour count/range/line width, equal spatial aspect, negative Cp upward, viridis, physical velocity labels and full-field normalization limits.
- Source/sink limits are 7.658998 to 8.990441 m/s (P10-P95). Its colorbar has extensions at both ends; endpoint colors represent out-of-range speeds without changing calculated velocities. Other velocity assets retain global zero-to-P95 scaling.
- Rankine polygon checks confirmed the center is inside, an exterior point is outside, all interior velocity samples are masked, and the underlying velocity data are unchanged. Both clean and explanatory exterior-only versions were visually inspected at 900-pixel width.
- Hashes confirmed every existing root Python file was unchanged by export. Physics, grids, geometry and masks remain those of the finalized demonstrations.
- Inspected full-resolution figures, the overview and the original six 900-pixel-wide previews and the added Rankine streamline preview. Labels, pressure curves, airfoil boundary, geometry and legends remain readable. No labels are cropped.

## Image-quality limitations

Original viridis yellow has weaker contrast on white, especially on thin high-speed streamlines. Percentile saturation cannot distinguish speeds above the selected upper limit (or below the source/sink lower limit). Matplotlib streamline tracing retains some gaps/fragments. The source/sink exclusion circles are necessarily small on this full-domain grid; the markers and legend identify them, and full-resolution copies allow closer inspection. The airfoil cusp and Rankine boundary retain established finite-grid/sampled-boundary limitations.

The Rankine figure retains its approved outside legend and therefore a wider aspect than the other assets. No aesthetic redesign was introduced. Prefer individual images at approximately 800-1000 pixels wide when labels matter; small gallery thumbnails are for overview only.

No commits, pushes or publication. Phase 4A stops here for review.
