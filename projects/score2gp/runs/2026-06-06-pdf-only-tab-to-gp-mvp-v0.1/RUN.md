# ScoreToGP Run Record - PDF-Only Tab-to-GP MVP Pathway v0.1

## Repo and Branches
- **Repository**: tticom/score2gp / tticom/score2gp-agentops
- **Product Branch**: `feature/pdf-only-tab-to-gp-mvp-v0.1` (merged via Product PR #176)
- **Agentops Branch**: `run/pdf-only-tab-to-gp-mvp-v0.1`
- **Product PR**: #176 (https://github.com/tticom/score2gp/pull/176)
- **Product Head SHA**: `4e4f7d540a7f0dc5cd4fda8d4384e84d014a06d8`
- **Product Merge Commit**: `70e03a587b4b471e22c84d00d3a99a75c81aeaaa`
- **Merged Timestamp**: `2026-06-06T21:56:47Z`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-pdf-only-tab-to-gp-mvp-v0.1.md](prompts/001-pdf-only-tab-to-gp-mvp-v0.1.md)

## Plan Evidence
- **Agentops PR**: #50 (https://github.com/tticom/score2gp-agentops/pull/50)
- **Agentops Merge Commit**: `03644ec08b00556a9e96310f554668cfcc114e38`
- **Merged Timestamp**: `2026-06-06T21:55:42Z`
- **File Added**: `projects/score2gp/ACTIVE_PLAN.md`

## Files Changed

### Product Repository (`score2gp`):
- `src/score2gp/build_ir.py` (MODIFY)
- `src/score2gp/cli.py` (MODIFY)
- `tests/test_pdf_only_tab.py` (NEW)

### Agentops Repository (`score2gp-agentops`):
- `projects/score2gp/runs/2026-06-06-pdf-only-tab-to-gp-mvp-v0.1/RUN.md` (MODIFY)
- `projects/score2gp/runs/2026-06-06-pdf-only-tab-to-gp-mvp-v0.1/prompt-manifest.json` (UNCHANGED)
- `projects/score2gp/runs/2026-06-06-pdf-only-tab-to-gp-mvp-v0.1/prompts/001-pdf-only-tab-to-gp-mvp-v0.1.md` (UNCHANGED)

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (PDF-only pathway builds valid GP structure but suffers from a global ordering defect that merges unrelated pages, systems, and local bars into false chords)
- **Remediation / Diagnostic Status**: `pass` (All unit and integration tests pass cleanly)
- **Generated File Existence**: `yes` (A structurally valid `.gp` package is written for Lesson 3 Page 1 and Full-score)
- **Semantic Round-Trip Status**: `blocked` (Generated output is musically invalid due to incorrect bar/event ordering and duplicate strings)

## Key Implementation Summary
- **Direct Conversion Build**: Added `build_ir_from_tabraw_only` to parse a PDF's `TabRaw` candidate coordinates directly.
- **Timing Bypass**: Added `--pdf-only-tab` to the `convert` CLI command to bypass MusicXML sidecar preflight checking entirely.
- **Rhythm Inference Policy**: Implemented deterministic rhythmic alignment by grouping fret candidates by bar and horizontal x-position. Rhythm grid spacing (eighths, 16ths, 32nds, 64ths) is calculated dynamically from bar candidate density, and the final event duration is stretched to fill the measure.
- **Diagnostic Reports**: Added a distinct `pdf_only_diagnostics` block to the JSON report to track PDF-only status and output.
- **Optional Comparison evaluation**: Added `--ref-gp` to allow semantic GP comparison at the end of a run without treating the reference GP as an input dependency.
- **Inferred-Timing Warning**: Added the warning item code `pdf_only_tab_inferred_timing` to warn that timing is layout-inferred.

## Non-Goals Kept
- No OCR
- No Audiveris dependency
- No scanned PDF support
- No perfect rhythm guarantee
- No dependency on reference GP as input
- No private/generated artifacts committed to either repository

## Test Coverage
- **Fret and Layout Safety Gates**: Tests assert that unsafe geometries (e.g., missing system, string, or bar line coordinates) trigger appropriate refusals.
- **Rhythm Inference Policy**: Asserts that spacing density boundaries are mapped to correct musical grid tick intervals.
- **CLI Orchestration & JSON Report**: Asserts that `convert` outputs correct fields, warnings, and exit codes under both successful and refused conversions.

## Exact Verification Commands Run

### 1. Focused PDF-Only Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_pdf_only_tab.py
```
* **Result**: **PASS** (4/4 passed).

### 2. Focused CLI Convert Test Suite:
```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
```
* **Result**: **PASS** (13/13 passed).

### 3. Public Test Suite:
```bash
PYTHONPATH=. .venv/bin/pytest
```
* **Result**: **PASS** (491/491 passed).

### 4. Private-Safety Audit:
```bash
git ls-files fixtures/private work
```
* **Result**: Outputs exactly:
  ```text
  fixtures/private/.gitkeep
  ```
  No private files, generated `.gp` packages, or inspection reports are tracked in the repository.

### 5. Git Diff Check:
```bash
git diff --check
```
* **Result**: Clean.

---

## Private Lesson 3 Smoke Test Summaries

### Page-1 Smoke Test (Structural Success)
The PDF-only convert pipeline was executed locally on Page 1 of the private Lesson 3 score with the `--pdf-only-tab` flag and no MusicXML sidecar input.
- **Exit Code**: `0`
- **Status**: `success`
- **Output Written**: `true` (valid GP file successfully written)
- **GP Validate**: `pass` (structure validation has no errors)
- **Playable Candidate Count**: `461` (mapped to 461 notes across 395 events in 21 bars)
- **Inferred Timing Warning Present**: `true` (warning code `pdf_only_tab_inferred_timing` is recorded in warnings)

### Full-Score Smoke Test & Ordering Defect
The PDF-only convert pipeline was executed on the full Lesson 3 score, successfully producing a structurally valid GP package.
- **Exit Code**: `0`
- **Status**: `success`
- **GP Validate**: `pass` (XML well-formed and package valid zip)
- **Findings**:
  - Full-score inspection exposed a **serious global ordering defect**:
    - Events merge notes from multiple source pages, systems, and local bars (e.g. `bar-1-event-1` contains notes from pages 1, 2, 3, and 4 collapsed into the same event).
    - Events contain duplicate strings (multiple notes on the same string in a single event).
    - The generated score is musically unacceptable.
- **Conclusion**:
  - This run is **not a finished MVP success**.
  - It represents a structural breakthrough plus a newly identified blocker.

### Evidence Caveat
> [!NOTE]
> The `report.json` uploaded during the initial review step reflected an earlier pre-fix conversion attempt where a MusicXML timing sidecar was required but not provided (`musicxml_not_found` refusal). It is not indicative of the successful PDF-only execution.

---

## Current Status and Limitations

### Current Status
The direct PDF-only pathway successfully bypasses the MusicXML requirement and compiles structurally valid GP packages, but the musical output is currently invalid due to global ordering collapsing.

### Known Limitations
- **Global Bar Ordering**: Fret candidates from different pages, systems, and local bars are collapsed into the same bars/events because the builder groups by local bar index and x-coordinate without preserving page and system vertical reading order.
- **Duplicate Strings**: Multiple candidates on the same string are incorrectly stacked into single events.
- **Approximate Timing**: Rhythmic durations are approximate and inferred from visual horizontal placement density.
- **Rhythm Policy**: The density-grid mapping does not capture musical spacing nuances and needs layout-aware refinement.
- **Techniques**: Expressive guitar technique support remains limited.

---

## Next Recommended Task
Develop a product fix in the `feature/pdf-only-global-bar-ordering-v0.1` branch under the task `fix: preserve PDF-only source bar ordering`. The fix must group and sort candidates by page index, vertical system vertical order, and local bar index before assigning global output bars 1..N. Duplicate-string candidates in the same x-group should be split into adjacent events or trigger a clean refusal.
