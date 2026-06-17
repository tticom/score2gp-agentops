# Decision Record: Post Task 174, Authorise Task 175 (Logical Clef Extraction Gap Diagnosis)
Date: 2026-06-17

## Context
Product Task 174 added a safe synthetic diagnostic-boundary proof showing that, once deterministic logical treble-clef evidence exists, a whole-note candidate with staff-position evidence can successfully receive `clef_resolved_staff_pitch` and is not counted as skipped for missing clef evidence.

## Governance PR #182 Verification
* State: MERGED
* Head SHA: 15d22ef1c74c73f440ea6adc488e0ed3f2193b29
* Date: 2026-06-17

## Product PR #292 Verification
* State: MERGED
* Head SHA: 83b8954f9128c4f692e97d7ee4a6876b58c0eda3
* Date: 2026-06-17

## Product PR #293 Live Merge Evidence
* State: MERGED
* Final head SHA: 3b97c9b9da2189165e4c201df5bdf0c96f74e47c
* Merge commit: c61b3799a2ae2d01d3943f1a017a5a7ae219f838
* Merged timestamp: 2026-06-17T19:20:05Z
* Base branch: main
* Changed files: 1 (`tests/test_logical_clef_coverage_proof.py`)

## Product Task 174 Completion Summary
Product Task 174 added `tests/test_logical_clef_coverage_proof.py`. The synthetic integration test provides deterministic logical clef and whole note evidence. It successfully simulates pipeline processing, ensuring `map_clef_resolved_staff_pitch` receives valid logical clef evidence and produces `A4` for the candidate.

## Product PR #293 Validation Evidence
* `PYTHONPATH=src pytest tests/test_logical_clef_coverage_proof.py`: 1 passed in 0.03s.
* `PYTHONPATH=src pytest tests/test_logical_clef_bridge.py`: 6 passed in 0.16s.
* `PYTHONPATH=src python3 scripts/run_coverage_analysis_task170.py`: public fixture aggregate remained unchanged (14 skipped candidates, 0 mapped).
* `git diff main...HEAD --check`: no formatting errors.
* `git diff main...HEAD --stat`: exactly 1 file changed, 72 insertions.
* `git status --short`: clean working tree.
* `git status --ignored`: only standard ignored files such as `.venv` and `.pytest_cache`.
* Hygiene grep found only existing tracked public fixtures, with no new or modified PDFs, private fixtures, or sensitive files.

## Safety/Privacy/Artifact Hygiene Result
Clean. No new PDFs, images, or sensitive artifacts were introduced. The hygiene grep returned only existing tracked public files.

## Current Limitation
* The synthetic diagnostic-boundary proof passes.
* The current generated public PDF aggregate remains unchanged.
* The generated public PDFs still do not yield deterministic logical treble-clef evidence that the bridge can consume.

## Evidence-Based Next Blocker
The next blocker is the extraction gap from generated public PDF primitives to deterministic logical clef evidence, not pitch mapping and not playable output.

## Reason for Product Task 175
Before expanding recognition or moving toward playable output, the project needs an empirical diagnosis of why generated public PDFs fail to produce usable logical clef evidence.

## Explicit Boundary
* Product Task 175 is strictly diagnostic/read-only.
* It may add a safe aggregate report or tests proving the extraction gap.
* It must not implement broad visual recognition, playable output, canonical pitch adoption, or private fixture use.
