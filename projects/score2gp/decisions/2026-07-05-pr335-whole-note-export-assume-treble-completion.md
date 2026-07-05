# PR #335 completion — whole-note export assumed-clef safety fix

## 1. Baseline
- Governance PR #234 approved Outcome B research.
- Product PR #335 implemented the authorised narrow fix.
- Product PR #335 was merged at corrected head `04a2ff083a2d42ec025d9e212bbe24609089bd15`.

## 2. Merge Evidence
- **Product PR URL**: https://github.com/tticom/score2gp/pull/335
- **Product Merge Commit**: `a4235ea55c45a513c671f2cc5f24c916bf58f865`
- **Merge Timestamp**: `2026-07-05T16:24:42Z`
- **Branch**: `feature/whole-note-export-assume-treble-clef-v0.1`
- **Branch Deletion Status**: Deleted (remote branch removed)
- **Post-Merge Verification Verdict**: VERIFIED

```text
PR readiness evidence:
- PR state: MERGED
- Head SHA: 04a2ff083a2d42ec025d9e212bbe24609089bd15
- Mergeable: MERGEABLE (before merge)
- Changed files: src/score2gp/cli.py, src/score2gp/whole_note_recogniser.py, tests/test_cli_notation_whole_note_export.py, tests/test_note_candidate_recognition_cli.py, tests/test_note_candidate_recognition_report.py
- CI/checks: passing (4 checks)
- Codex review submissions: 1 review submitted (COMMENTED state)
- Codex inline comments: 2 inline comments (PRRT_kwDOShNpkc6ObK9V, PRRT_kwDOShNpkc6ObK9Y)
- Review threads: 2 threads
- Unresolved threads: 0 threads
- Codex comment disposition:
  - Thread PRRT_kwDOShNpkc6ObK9V: accepted as blocker, fixed by replacing silent truncation with explicit validation error, regression tests added.
  - Thread PRRT_kwDOShNpkc6ObK9Y: accepted as blocker, fixed by propagating assumed-clef mode and counters to coverage reporting, regression tests added.
- Regression tests added/updated: test_notation_whole_note_export_fails_on_real_fixture_due_to_multiple_notes, test_notation_whole_note_export_fails_without_pitch_resolution, test_coverage_report_under_assume_treble_clef, test_coverage_report_without_assume_treble_clef, test_note_candidate_recognition_cli.py, test_note_candidate_recognition_report.py
- Known limitations: public two-note fixture rejects cleanly, positive export remains mock-only.
```

## 3. Capability Landed
- `notation-whole-note-export` command exposes an explicit opt-in `--assume-treble-clef` flag.
- The flag is propagated to recognition.
- `whole_note_candidate` can receive assumed-treble fallback pitch when the flag is enabled.
- Multiple whole-note candidates are rejected cleanly with a validation error instead of being silently truncated.
- No partial `.gp` is written on multi-candidate rejection.
- Assumed-clef coverage reporting distinguishes assumed-clef fallback resolution from detected-clef evidence, preventing misleading coverage analysis.

## 4. Tests and Validation
- Focused CLI tests pass (13/13).
- Full test suite passes (859/859).
- GitHub checks pass.
- Artifact hygiene verified clean.

## 5. Explicit Limitations
- This does not prove arbitrary PDF support.
- This does not prove broad whole-note recognition.
- This does not prove multi-note or multi-bar GP export.
- This does not prove positive real-fixture GP export from a true single-whole-note PDF.
- The existing public fixture (`tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`) contains two whole notes and now cleanly rejects under the single-note contract.
- Positive export remains mock-only until a safe single-whole-note real fixture is approved and added.

## 6. Governance Result
- Product PR #335 completion is recorded.
- The active product implementation loop is closed.
- Developer implementation is not currently authorised.
- Next work requires Supervisor selection.

## 7. Required Next Decision
Supervisor must choose one of the following paths:
- Stop or pause.
- Record and approve a new fixture strategy for a true single-whole-note real fixture.
- Select another bounded capability for development.
- Open an Architect research loop if uncertainty remains.
