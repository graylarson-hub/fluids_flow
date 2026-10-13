# Documentation, verification and final release review

## Current outcome (2026-10-13)

The final review was confined to the portfolio repository. The earlier final review began with a clean working tree; the subsequent approved license/scratchpad cleanup and documentation edits remain uncommitted. Local `main`, local `origin/main`, and the remote `main` hash read with `git ls-remote` all match **`c14c252392ff0b05d30aa0f2d0c9560130612b17`**. The previously reported reachable-coursework problem is now resolved for this branch. This report replaces its earlier unresolved-history assessment; the phase audit/validation reports remain historical records.

The README cleanup, approved MIT licensing, private scratchpad backup/removal and public-documentation link cleanup are complete. Final publication review remains pending. No source, figure, physics equation or visualization style was modified during this pass. No commit, push, history rewrite, remote change or visibility change was performed.

## README changes and first impression

- Removed the prominent Numerical Validation section, case count and detailed residual discussion. Replaced them with one short **Numerical verification** note and the [validation report](phase2_validation.md) link near the bottom.
- Added the missing [mathematical reference](mathematical_reference.md) and [plotting API](plotting_api.md) links. Retained the example-script links and approved image selection/layout.
- Made `python -m pip install -r requirements.txt` the primary setup command, avoiding a duplicate installation route that omitted the Matplotlib lower bound.
- Updated the stated fresh-environment versions to the actual Windows/Python 3.14.7, NumPy 2.5.4 and Matplotlib 3.11.2 results. Other platforms/version combinations remain unverified.
- Removed a repeated field-calculation explanation, linked the detailed API, and clarified that Rankine interior masking belongs to the featured export rather than the standalone calculation.

There were no literal TODO/TBD or unresolved placeholder fields in the README. Missing technical links and outdated setup wording were the items resolved. The source/sink local P10-P95 display choice is still documented once, with physics unchanged.

The opening identifies an educational analytical potential-flow visualization project immediately. The hero and gallery precede the detailed mathematics; setup and source tables provide practical entry points. The tone is suitable for an engineering portfolio without production-CFD claims. The remaining mathematical explanation gives technical readers enough context without leading with validation statistics.

## Documentation and link audit

The mathematical reference, exact-signature API reference, validation report, requirements file and all eight completed example references exist. README source, image and documentation links resolve to tracked repository files or the new LICENSE awaiting tracking. No local Windows/user-home paths were found in tracked public Markdown or Python; displayed environment/output paths remain only in ignored local verification JSON. Relative repository links are used for local content.

The nine links to ignored review images have been resolved in `phase3a_review.md` and `phase3c_review.md`. Where equivalent final presentation assets exist, links now point to the tracked gallery, airfoil and Rankine assets. Thin-oval tests, raw/masked arrows, auxiliary plots and the original review sheets have no equivalent public image; their broken links were removed while retaining the diagnostic explanations and explicit local-only context. Default Rankine assets are not presented as the thin test case. The two-panel transformation is referenced through its completed demonstration script.

All 55 README/documentation file and image references resolve to publication-eligible repository files, including the new LICENSE. The four external reference links were also checked and loaded successfully. Historical descriptions of masks, caches and earlier working-tree state remain audit records rather than current implementation claims.

The exact portfolio export runner remains ignored. A fresh checkout can run the demonstrations and display all assets, but cannot reproduce every approved crop/export-only Rankine mask from tracked source alone. Decide whether to include a small export runner later; this does not prevent the demonstrations from running.

## Python review: findings for approval

Reviewed `fluid_plots.py`, the eight completed demonstrations, and both scratchpads. Required third-party runtime imports are only NumPy and Matplotlib; `fluid_plots` is the adjacent local module. No broken imports or platform-specific filesystem assumptions were found in the completed calculations. Printed circulation, lift, stagnation dimensions and vortex residuals are useful diagnostics, not accidental debugger output. Physical spatial plots use meter labels, and velocity colorbars use m/s. The pressure coefficient is dimensionless and circulation legends include units.

The plotting module and eight completed demonstrations are unchanged and byte-identical to the source covered by the preceding fresh-environment verification. No accidental equation change was introduced by documentation work. The approved default P95 normalization, local source/sink P10-P95 limits, Rankine branch-cut treatment and airfoil settings remain intact.

Non-blocking comments/cleanup items, left unchanged for approval:

- `uniform_source_sink.py` retains misspelled `aplpha`, unused exploratory fields, and an inactive single-source/+x stagnation explanation that does not apply to its active angled two-point superposition. Remove or clarify that inactive block if doing a later code-comment cleanup.
- `cyl_pressure_plot.py`'s opening sentence says flow along +x gives negative lift without explicitly qualifying positive circulation; later code and documentation use the correct signed relation.
- The unfinished rotational scratchpads `fun.py` and `test.py` have now been backed up privately and removed from the active tree/index. They remain only in earlier Git history and private/local records.
- The known all-zero quiver automatic-scaling warning and existing streamline tracing gaps remain documented numerical limitations, not newly introduced failures.

## Assets and presentation

All nine PNGs are tracked, decode correctly and retain their approved styles. No images were regenerated or modified. The required selected assets are:

| Asset | Pixels | Approximate size |
| --- | --- | --- |
| `hero_joukowski_airfoil.png` | 2692 x 2101 | 0.74 MB |
| `rankine_oval_streamlines_explanatory.png` | 2368 x 1979 | 0.48 MB |
| `rankine_oval.png` | 3113 x 1834 | 0.13 MB |
| `lifting_cylinder.png` | 2256 x 2030 | 0.55 MB |
| `cylinder_pressure_coefficient.png` | 2668 x 1768 | 0.32 MB |
| `free_vortex.png` | 2296 x 2030 | 0.79 MB |
| `source_sink_superposition.png` | 2296 x 2025 | 1.03 MB |

The optional overview is approximately 1.65 MB; the clean alternative Rankine flow view is 0.47 MB. These are reasonable full-resolution PNG sizes; no optimization is necessary for this pass.

The README preserves its 720-pixel hero, 560-pixel gallery panels and expandable source/sink example. The hero has thin navy contours and a clear airfoil boundary. Rankine uses the explanatory version with source/sink/stagnation markers, gray masked interior and dark outline. Lifting-cylinder/vortex/source-sink assets retain viridis and physical speed labels; the pressure plot keeps negative Cp upward. Equal spatial aspect, solid-body outlines and singularity exclusions remain distinguishable.

Prior full-resolution/README-width inspections were reviewed, and the explanatory Rankine image was reinspected. Small colorbar/legend text benefits from the full-resolution assets, and viridis yellow still has weaker white-background contrast. These were approved style tradeoffs; no redesign was introduced. Markdown/HTML structure and file paths were checked locally; this pass did not render the uncommitted README on live GitHub or retest interactive GUI behavior.

## Reproducibility

[requirements.txt](../requirements.txt) declares `numpy>=2.0` for `np.trapezoid` and `matplotlib>=3.8` for the contour collection/clipping interface. Exact lower versions were not tested; the previous isolated installation resolved NumPy 2.5.4 and Matplotlib 3.11.2 under Windows/Python 3.14.7. The full earlier fresh-environment test used a separate copy of the then-uncommitted working tree and rendered **19 figures** from eight completed examples. It was not a GitHub-commit test.

This final pass reused that isolated environment for a lightweight check: `pip check` passed, and all eight completed scripts ran from a different working directory with Agg. Only its expected noninteractive `show()` notice was suppressed; every other warning was treated as an error. The README example was also exercised. No compatibility beyond the tested Windows/Python combination is claimed.

Local evidence is in ignored `figures/phase4d_review/` and `figures/final_release_review/`; it is deliberately not linked as public downloadable test infrastructure.

## Git hygiene and cleaned history

Read-only checks covered Git status, branch/ref hashes, remote URL, `.gitignore`, tracked filenames, text markers and every tree in the **11 commits reachable from `main`**. No `Lectures/`, `Quizzes_HW/`, `Quizes_HW/`, root `HW 2.pdf` or `Homework 2.docx` was found in that history. No coursework PDFs/DOCX files or compiled Python artifacts were found in the inspected reachable trees. The remote branch hash matches the local audited graph.

No cache, virtual environment, review output or temporary file is tracked. `.gitignore` appropriately excludes those outputs and coursework directories; assets/documentation remain tracked. Pending changes are limited to the approved scratchpad deletions, LICENSE, `.gitignore`, README, and the three documentation reports updated for final review. The only staged paths are the two scratchpad deletions; no scratchpad content, coursework, cache or ignored review figure is staged for publication. Remote configuration is unchanged.

No obvious hard-coded credential/private-key markers were found in reviewed tracked source/text or the reachable scratchpad versions. This is a focused source/history review, not an exhaustive secrets or authorship audit. Ordinary Git author attribution remains part of the history.

Branch-reachable history is clean for the specified coursework paths. That does not prove that GitHub has erased cached/unreachable objects, pull-request references, forks or other clones. [GitHub's removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) explains these limits. No server-side purge or other destructive action was attempted.

## Scratchpads and MIT License: complete

`fun.py` and `test.py` were copied to a private Documents backup directory outside the portfolio and any Git repository. Backup lengths (1,141 and 2,072 bytes) and SHA-256 hashes matched the originals before deletion and were reverified afterward. Both are absent from the working tree and Git index; their deletion is staged. Exact root-file ignore rules `/fun.py` and `/test.py` prevent accidental recommit. Private backup paths and full hashes are retained in local verification records rather than public documentation.

Three reachable versions of `fun.py` and four of `test.py` were checked for obvious sensitive markers, with no findings requiring historical removal. Earlier versions remain in history by design. No history rewrite was performed.

The approved [MIT License](../LICENSE) has been added with `Copyright (c) 2026 Gray Larson`. Its complete legal wording was verified against the standard MIT text; no custom restrictions were added. The README links to LICENSE. The file remains untracked until a separately authorized staging/commit step.

## Final-release checklist

- [x] Shorten README validation to a bottom note; preserve its report link without emphasizing case counts.
- [x] Resolve setup wording and add mathematical/API documentation links.
- [x] Preserve the approved explanatory Rankine asset, matching caption and gallery layout.
- [x] Verify tracked README links, PNG validity, runtime dependencies and lightweight example execution.
- [x] Verify the cleaned intended `main` history and matching remote branch hash.
- [x] Back up and verify both scratchpads privately; remove them from the active tree/index and add exact ignore rules. Historical copies remain unchanged.
- [x] Add the approved standard MIT License with the specified copyright and README reference.
- [x] Replace the nine local-only image links with suitable public references or preserve their explanations without broken hyperlinks.
- [ ] Decide whether exact asset-export reproduction should be available from tracked files.
- [ ] Optionally approve the small Python comment cleanup identified above; physics and styles need no change.
- [ ] Review final GitHub rendering/captions and the intended tracked diff after these edits.
- [ ] Authorize any final commit/push/publication separately. No such action was performed in this pass.
