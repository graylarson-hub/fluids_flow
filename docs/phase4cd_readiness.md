# Phases 4C and 4D: documentation and release review

## Scope and outcome

Work was confined to `Fluids-Portfolio`, confirmed by `git rev-parse --show-toplevel`. Existing uncommitted changes were preserved. Added a [mathematical reference](mathematical_reference.md), [plotting API reference](plotting_api.md), and [minimal requirements](../requirements.txt). No Python equations, plotting defaults, styles, assets or source-file locations were changed. The README received only a small installation correction acknowledging the new manifest; its final editorial pass is deferred.

The working tree is ready for technical/editorial review, **not public release**: coursework remains reachable in local `main` history. License and scratchpad decisions also remain open. No commit, push, history rewrite, deletion or publication was performed.

## Dependencies and reproducibility

Only NumPy and Matplotlib are imported as runtime libraries; `fluid_plots` is a local module. `requirements.txt` specifies `numpy>=2.0` for `np.trapezoid` and `matplotlib>=3.8` for the Rankine contour object's collection-based clipping interface. This lower Matplotlib bound follows the [3.8 ContourSet API change](https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.8.0.html#contourset-is-now-a-single-collection); it is not a claim that every allowed version has been tested. Transitive packages are left to pip rather than individually pinned.

From the repository root, create an isolated environment and install:

```sh
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe joukowski_airfoil.py
```

On a POSIX shell (commands provided for convenience; not tested on Linux/macOS):

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python joukowski_airfoil.py
```

A new virtual environment was created without `--system-site-packages`. Dependencies were installed using the manifest into the ignored `figures/phase4d_review/venv/`, independently of the active interpreter. Initial sandboxed network access failed; the permitted download run succeeded. `pip check` reported no broken requirements.

A separate `figures/phase4d_review/working_copy/` contains current root source files, README, manifest, documentation and assets, with no `.git`, cached modules, inherited review files or coursework. This tests the **current uncommitted working tree**, not a GitHub checkout or the published state. The module import resolved to that copy. The historical committed HEAD does not yet include these final assets/documentation/styles.

Tested environment: Windows x64, Python **3.14.7**, NumPy **2.5.4**, Matplotlib **3.11.2**, Agg backend. No Linux/macOS or interactive GUI compatibility claim is made. Unbounded upper version constraints allow future releases; recheck after dependency upgrades.

## Demonstration checks

| Completed demonstration | Rendered figures |
| --- | --- |
| `uniform.py` | 3 |
| `uniform_source_sink.py` | 3 |
| `rankine.py` | 2 |
| `cylinder_flow.py` | 3 |
| `vortex.py` | 3 |
| `lift_cyl.py` | 3 |
| `cyl_pressure_plot.py` | 1 |
| `joukowski_airfoil.py` | 1 (two panels) |

The eight examples rendered **19 figures**, including labels and colorbars, without captured numerical or rendering warnings. Separate subprocess entry points also ran with the copy imported normally, from a different working directory. Only Agg's expected noninteractive `show()` notice was suppressed for those runs; other warnings were errors. The README and API usage examples were exercised, including saving a PNG into a newly created local output directory.

Checks retained the pressure-integrated final-case lift/theory agreement and negligible ideal drag, Rankine analytical stagnation locations, the 61 airfoil contour levels and finite mapped coordinates. No source was changed, so the 225 historical mathematical cases were not unnecessarily repeated. [Phase 2](phase2_validation.md) remains the source for tested physics ranges and [Phase 3C](phase3c_review.md) for broader style/API verification.

All nine PNGs in `assets/` decode successfully. The final overview and explanatory Rankine image were reviewed in the current session/history; the README points to `rankine_oval_streamlines_explanatory.png`, which retains source, sink and stagnation-point markers and a polygon-masked gray interior. The standalone Rankine script still shows its original full superposition; exterior-only masking is an asset-export procedure, documented in [Phase 4A](phase4a_assets.md).

Evidence and generated comparison renders are kept locally under ignored `figures/phase4d_review/`: `verify_fresh.py`, `fresh_environment_results.json`, `history_check.json`, `preservation.json` and `rendered/`. They are review evidence, not a newly advertised public test framework.

## Repository hygiene and links

- The current tracked tree contains source, README, `.gitignore` and documentation. No tracked `.pyc`, `__pycache__`, virtual environment or generated review directory was found. Phase 1's cache finding is historical, not the current state.
- `.gitignore` excludes caches, local environments, `figures/`, temporary/log files and named coursework directories. `assets/` and `docs/` are intentionally eligible for tracking. No ignore changes were necessary.
- No unwanted coursework/private files were found in the current public-facing file inventory. This is a filename/import review, not a comprehensive secrets or authorship audit.
- All 56 local README/documentation links were checked and resolve in the working tree. Public source/document/asset targets resolve in the clean copy. Nine links in historical review reports deliberately target ignored `figures/` artifacts: those exist locally but are absent from a fresh public copy. They should be labelled local-only or replaced with public evidence during the final documentation review.
- Phase reports contain historical claims superseded by later phases. Keep them as audit records; avoid treating old mask/style/cache findings as current implementation descriptions.
- The asset export runner remains ignored, so a fresh copy can run the demonstrations and view assets but cannot reproduce every exact portfolio crop/mask solely from tracked source. Decide whether a small export runner should later be included. The runner also currently saves the explanatory Rankine review image locally; its promotion to `assets/` was a separate copy step.
- `fun.py` and `test.py` overlap on rotational incompressible flow (`u=3y`, `v=2x`, vorticity -1), not potential flow. `test.py` has a `phi` placeholder returning `None` and obsolete commented calls, and is not a test suite. Recommendation: exclude both from the public release, retaining local copies if useful; alternatively keep them clearly labelled exploratory. No move/deletion/exclusion was performed.

## Reachable-history finding: unresolved

Read-only checks inspected all **10 commits** reachable from local `main` at `79897d8089f0992f260e238e7b13f3b5fa2be735`. Both local `main` and local remote-tracking `origin/main` point there. No remote fetch or live GitHub verification was performed.

`git log main --name-only`, every reachable commit's `git ls-tree -r --name-only`, and `git log main -- 'HW 2.pdf' 'Homework 2.docx'` show:

- `HW 2.pdf`
- `Homework 2.docx`
- Relevant commits: `abbbb63` (first commit) and `8855ccc` (later deletion).

No lecture directories were found in the inspected reachable trees, but the two homework files are enough to fail the requested clean-history criterion. Deletion from HEAD and ignore rules do not remove historical copies. The stated prior cleanup cannot be confirmed for this local branch. **Resolve the intended public branch/history before release**; no history operation was authorized or performed here. If the cleaned branch exists elsewhere, compare it explicitly before choosing any corrective action.

## License decision

No license file is present. Choose the intended reuse policy and copyright-holder details before adding one:

- [MIT](https://choosealicense.com/licenses/mit/): short permissive terms, allowing reuse and closed-source redistribution with copyright/license notices retained; no warranty.
- [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/): permissive reuse with an express contributor patent grant, notice retention and change-marking obligations; more detailed terms.
- [GPLv3](https://choosealicense.com/licenses/gpl-3.0/): copyleft; distributing covered modified works requires corresponding source and the same licensing freedoms. Appropriate if reciprocal openness is the goal rather than unrestricted downstream licensing.
- [No license](https://choosealicense.com/no-permission/): does not grant general reuse/modification/distribution rights, even if code is publicly viewable. GitHub's platform-specific viewing/forking rights do not make it open source.

Decide whether the chosen license also covers original documentation and figures, and verify ownership of included material. No license was selected or added.

## Actionable final-release checklist

- [x] Add concise mathematical and exact-signature API references.
- [x] Declare current runtime dependencies and test isolated installation.
- [x] Run the eight completed examples, render figures and check public links.
- [x] Confirm the README uses the explanatory Rankine streamline asset and matching caption.
- [ ] Resolve the reachable homework history; verify the actual intended public branch and remote state. Do not publish with this finding unresolved.
- [ ] Decide whether `fun.py` and `test.py` should remain publicly included; approve any move/removal separately.
- [ ] Choose a license, copyright-holder information and scope for code/docs/figures.
- [ ] Decide whether to include an exact asset-export runner and replace/label links to local-only review artifacts.
- [ ] During the deferred README pass, shorten Numerical Validation to approximately one sentence linking to `docs/phase2_validation.md`, near the bottom.
- [ ] Resolve remaining README placeholders/decisions, link the new technical references and manifest, check technical wording and remove repetition.
- [ ] Review GitHub rendering, image sizing and final captions; interactive GUI behavior was not rechecked here.
- [ ] Review all intended source/docs/assets for the future release commit; existing work remains uncommitted. Recheck links against the intended tracked tree rather than only local files.
- [ ] Complete the final publication review and obtain explicit authorization before committing, pushing or changing visibility.
