# Completion Record: Post PR #324 Tab-Only Timing Policy

## Baselines & Merges
- **Product PR**: https://github.com/tticom/score2gp/pull/324
- **Product PR Title**: feat: enforce strict tab-only timing policy A+B+C
- **Product PR Merge Commit**: `67e31602eb280a225b0608e6bfd8255acdeacfc0`
- **Product PR Head SHA before merge**: `cabd0a786d311ad5e409ce7dc0408d5e61d56a79`
- **Product baseline before PR #324**: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`
- **Governance baseline**: PR #205 merged at `14caf6f05d84f03b1cc97463ae371d1b8c68e2e7`

## Files Changed in Product PR
- `src/score2gp/build_ir.py`
- `src/score2gp/cli.py`
- `tests/test_pdf_only_tab.py`

## Product Capability Now Present
- default approximate `--pdf-only-tab` behaviour remains available,
- strict mode flag `--require-precise-timing` exists,
- strict mode refuses tab-only missing timing evidence,
- refusal category is `pdf_only_tab_missing_timing_evidence`,
- strict refusal includes specific remediation guidance,
- no GP output is produced on strict refusal,
- no broad rhythm inference added,
- no ML added.

## Validation Evidence
- PR readiness verdict was READY.
- CI and Raster Diagnostics Gate were successful before merge.
- Reported focused test: `.venv/bin/pytest tests/test_pdf_only_tab.py -q` passed.
- Reported full suite: `PYTHONPATH=. .venv/bin/pytest tests -q` passed with 807 tests.
- Codex P2 thread was resolved after remediation hint fix.

## Known Limitations
- Precise tab-only rhythm inference is still not solved.
- Tab-only approximate/default timing remains approximate.
- Precise rhythm still requires reliable timing evidence such as MusicXML/sidecar or explicit supported timing evidence.
- ML-assisted extraction remains future/nice-to-have only.
- The next active blocker is not selected in this task.
