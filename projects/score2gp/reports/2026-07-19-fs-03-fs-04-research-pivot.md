# FS-03 and FS-04: Research Pivot

**Date**: 2026-07-19
**Programme**: Runtime-Provenance and Functional-Stabilisation
**Role**: Developer

## Objective
Run the selected corpus, identify the first shared source/output divergence, and repair one behaviour class per PR.

## Observation
To trace the first shared divergence on the canonical path, the pipeline was run against the private corpus (`Lesson-3` through `Lesson-7`, plus additional files). 

The canonical pipeline (`score2gp convert`) depends on an external MusicXML sidecar to provide timing, rhythmic alignment, and rest inference data alongside the vector PDF tab geometry.

However, the private fixtures directory (`score2gp-private-fixtures/fixtures/private/`) contains only `.pdf` inputs and their reference `.gp` output targets. It contains **no** `.mxl` or `.musicxml` sidecars.

## Missing Observation
The pipeline blocked at the Orchestration Gate (`missing_musicxml` / `provide-matching-musicxml-before-build-ir`). Because the required external MusicXML sidecars are missing, the pipeline correctly refuses to build the ScoreIR. Consequently, it is impossible to trace the "first shared source/output divergence" on the canonical product route.

## Pivot Decision
The missing observation is the lack of external MusicXML sidecars in the private fixtures, which are necessary to exercise the canonical `score2gp convert` pipeline. 

Without the ability to generate or access the MusicXML representations of these private fixtures, no structural divergences (like ghost rests or timing issues) can be empirically traced through the pipeline for FS-03/FS-04.

Since the programme requires not stopping unless no credible task or pivot remains, and FS-03/FS-04 are blocked, I must proceed to evaluate FS-05 (Baseline Decision) in light of these missing dependencies.
