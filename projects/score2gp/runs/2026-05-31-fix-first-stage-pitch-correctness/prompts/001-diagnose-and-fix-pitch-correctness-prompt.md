# Antigravity Task: Diagnose and Fix First Stage Pitch Correctness Defect

## Context

The `score2gp` project has completed a research-and-test-foundation phase.

User-provided current status:
* `docs/domain/` now contains verified domain documentation.
* `intermediate-products.md` maps the 5 actual pipeline stages:
  * `inspect-pdf`
  * `extract-tab`
  * `align-ascii-musicxml`
  * `build-ir`
  * `write-gp`
* `domain-test-matrix.md` maps verified domain facts to test scenarios.
* `unresolved-questions.md` records open questions without guessing.
* Immutable stage integration tests now exist under:
```text
tests/integration/domain_contracts/
  test_guitar_pitch_validation.py
  test_timing_and_voices.py
  test_tablature_semantics.py
  test_intermediate_products.py
```
* The user reports that the full test suite currently passes: `python -m pytest` -> `404 passed`.
* The user reports the private-safety invariant:
```text
git ls-files fixtures/private work
```
returns only:
```text
fixtures/private/.gitkeep
```
* The last generated `smoke.gp` had a serious musical correctness problem: unrealistic pitch.

Treat the above as user-provided state. Verify it before relying on it.

The purpose of this task is not to expand the domain foundation. The purpose is to use the new domain-contract foundation to diagnose and fix the first real musical correctness defect in the pipeline.

## Goal

Find the earliest pipeline stage where unrealistic pitch or invalid string/fret/pitch semantics are introduced, then implement the smallest safe fix for that stage.
