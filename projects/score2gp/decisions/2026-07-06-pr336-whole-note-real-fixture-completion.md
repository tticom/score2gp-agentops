# PR #336 completion — whole-note real-fixture E2E validation

## 1. Baseline
- Governance PR #236 approved Outcome B research and strategy.
- Product PR #336 implemented the authorised E2E validation path using a programmatic vector PDF fixture.
- Product PR #336 was merged at exact head `3004cbb980dcb70663f01bdbf6223217d8159811`.

## 2. Merge Evidence
- **Product PR URL**: https://github.com/tticom/score2gp/pull/336
- **Product Merge Commit**: `cae6a416076e66f6b84940ad0cbf3061beb241d9`
- **Merge Timestamp**: `2026-07-06T06:23:43Z`
- **Branch**: `feature/single-whole-note-real-fixture-e2e-v0.1`
- **Branch Deletion Status**: Deleted (remote branch removed)
- **Post-Merge Verification Verdict**: VERIFIED

```text
PR readiness evidence:
- PR state: MERGED
- Head SHA: 3004cbb980dcb70663f01bdbf6223217d8159811
- Mergeable: MERGEABLE (before merge)
- Changed files: 4
  - fixtures/public/generated_standard_staff_single_whole_note.json
  - tests/fixtures/pdf/generated_standard_staff_single_whole_note.pdf
  - tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
  - tests/test_cli_notation_whole_note_export.py
- CI/checks: passing (4 checks)
- Review threads: 0 threads
- Regression / E2E tests added: test_notation_whole_note_export_success_real_fixture
- Artifact hygiene: clean (no private or gp files tracked, PDF is acceptable under existing tracked generated PDF fixture convention)
```

## 3. Capability Landed
- Positive real-fixture E2E validation path for `notation-whole-note-export` with `--assume-treble-clef` verified end-to-end.
- Synthesized a single-staff, single-note vector PDF fixture `generated_standard_staff_single_whole_note.pdf` containing exactly one whole-note candidate.
- Verified unmocked CLI execution returning exit code `0` and successfully outputting a valid Guitar Pro (`.gp`) package.
- Verified output GP package structure containing exactly 1 track and 1 note, and validated the package integrity using `validate_gp` and `inspect_gp`.

## 4. Tests and Validation
- Focused E2E integration tests pass (14/14).
- Broader test subset passes (418 passed, 442 deselected).
- Full product test suite passes (860 passed).
- GitHub PR checks/CI pass.
- Artifact hygiene verified clean.

## 5. Explicit Limitations
- The single whole-note shape is compiled from PyMuPDF vector primitive ovals and lines rather than standard music font glyphs (`Emmentaler-20`).
- This validates the geometry parsing, candidate extraction, clef fallback, CLI export, and GP package structure but does not exercise standard-notation font glyph subset mapping.
- This does not prove arbitrary PDF support or broad whole-note recognition.
- This does not prove multi-note or multi-bar GP export.

## 6. Governance Result
- Product PR #336 completion is recorded.
- The active product implementation loop is closed.
- Developer implementation is not currently authorised.
- Next work requires Supervisor selection.

## 7. Required Next Decision
Supervisor must choose the next task from a clean, no-active-task baseline.
