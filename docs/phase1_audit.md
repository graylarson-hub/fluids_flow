# Phase 1 audit ? 2026-10-12

## Initial state and preservation

- Existing repository on `main`; no README or dependency manifest.
- Initial working-tree changes: tracked `uniform_source_sink` deleted and
  untracked `uniform_source_sink.py` present. This pending rename was preserved;
  the new script was not edited and the old path was not restored.
- Shared plotting API already has the five intended public functions,
  arrays-only fields, optional 3D scalar panel, and percentile velocity colors.
  `fluid_plots.py` was left unchanged.
- Only NumPy and Matplotlib are needed. `np.trapezoid` requires NumPy >=2.0.
- A compiled `__pycache__/fluid_plots.cpython-314.pyc` is already tracked.
  Ignore rules do not untrack existing files; it was not deleted or unstaged.
- Ignored local `Quizzes_HW/` contains coursework and was not touched.
  Git history includes lecture/homework commits and later deletion commits.

## Conservative organization

The shared module and standalone scripts remain at the root to preserve simple
imports and VS Code execution. README identifies each demonstration; documentation
is in `docs/`. Optional future exports go in ignored `figures/`; existing scripts
still display plots without saving. No files were moved or deleted.

Fixed a stray bracket preventing `uniform.py` from parsing. `fun.py` and `test.py`
now evaluate velocity arrays before plotting. Removed obsolete/unused active
imports from `test.py` and unused imports from `cylinder_flow.py`. Added brief
model descriptions to the committed demonstrations and shortened section comments
in `test.py`. Working physics equations and plot choices were preserved.

## Decisions required before further cleanup

1. Whether to consolidate or rename `fun.py` and `test.py`. Both demonstrate
   the same rotational velocity field; `test.py` is not a test suite. Its unused
   `phi` returns `None`, and inactive comments reference removed specialized APIs.
   Keep these experiments until their intended future use is decided.
2. Whether to untrack the compiled Python cache in a later cleanup. Adding
   `.gitignore` entries alone cannot remove it from Git.
3. How to handle copyrighted coursework in repository history before release.
   This audit did not restore coursework, rewrite history, change remotes,
   commit, push, or publish. Historical deletion does not remove prior copies.
4. Whether to move examples into a folder later. That would need a simple,
   tested import/run approach; no packaging framework is needed for Phase 1.

## Prioritized mathematical and plotting review

1. Validate analytical derivatives, no-penetration boundaries, stagnation points,
   circulation orientation, and pressure-integrated lift for all sample parameters.
   Checks here are smoke checks, not complete validation of the physical models.
2. Examine near-singularity resolution. `source_or_sink` masks only exact `r=0`;
   floating-point grids may approach a center without hitting it exactly. Percentile
   colors improve contrast but do not remove very large velocities or integration
   sensitivity. The vortex core and cylinder interiors are already excluded.
3. Review Rankine dividing-streamline contours and branch-cut masks as grids or
   parameters change. The current Rankine mask uses a fixed 0.06 m half-width;
   that width is not tied to grid spacing. Superposed angular fields can be
   discontinuous, and singularities must not be interpreted as ordinary samples.
4. Check Joukowski trailing-edge and polar-grid seam behavior. The script avoids
   the circle surface by starting at 1.002 R and plots mapped contours only.
   Validate mapped velocities and Kutta behavior before adding pressure/lift.
5. Improve label consistency incrementally. Uniform velocity plots retain default
   labels without units; rotational examples have unspecified units. The pending
   superposition script retains the misspelled variable `aplpha` and unused
   exploratory fields. These do not require speculative physics changes.
6. Add a dedicated Rankine half-body or doublet example only if desired; the
   current oval and cylinder scripts already demonstrate related superposition.

## Verification

- Parsed all 11 Python files successfully and imported the unchanged plotting module.
- Ran all 10 demonstration/experiment scripts at their original grid sizes using
  Matplotlib Agg, with `plt.show` disabled for automation. Rendered all 25 figures
  to their canvases. All completed with no captured warnings.
- Verified matching coordinate/velocity array shapes where the scripts expose
  array-valued velocity components, and the presence of finite unmasked values.
- Cylinder pressure output agrees with theoretical lift for all printed cases;
  an automated check of the last case confirms lift and negligible drag.
- Joukowski trailing-edge cylinder tangential velocity is zero within 1e-12;
  mapped grid coordinates are finite. This is not a full mapped-flow validation.
- The vortex finite-difference check reports maximum absolute vorticity
  0.00765 1/s outside 0.75 m, a discretization residual rather than exact zero.
- Additional independent checks passed: uniform-flow derivative convention,
  pressure forces for all five circulation values, and the Rankine stagnation formula.
- Confirmed `fluid_plots.py` matches its committed contents.

Interactive window behavior and visual aesthetics were not manually inspected.
Numerical execution does not establish physical correctness for every parameter.
