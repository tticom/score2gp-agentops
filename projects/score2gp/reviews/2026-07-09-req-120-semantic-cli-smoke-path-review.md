# Req-120 Implementation Conformance Review

Date: 2026-07-09
Reviewer role: Reviewer
Task: Req-120 / Task 52
Product PR: `tticom/score2gp` #354
Product main SHA after merge: `86ace6e6`

## Implementation Conformance Verdict

`approve implementation`

The product implementation satisfies Req-120. It successfully exposes semantic candidates (logical clefs and quarter rests) via the diagnostics CLI/reporting paths (`inspect-pdf` and `note-candidate-recognition` commands, and `scripts/note_candidate_recognition_report.py`).

## PR Readiness Status

`READY`

PR #354 was merged after verification checks and test validation passed.

## Evidence Reviewed

Product files changed:

- `src/score2gp/pdf.py`
- `src/score2gp/whole_note_recogniser.py`
- `tests/test_semantic_cli_reporting.py` [NEW]

Validation reviewed:

- `git diff --check`: passed
- focused tests: `tests/test_semantic_cli_reporting.py` passed
- artifact audit: passed
- full suite: `901 passed, 1 skipped` passed
- GitHub checks: PR merged successfully

## Claim-by-Claim Verification

### Claim 1: Smallest safe reporting path for current semantic candidates

Status: verified.

Semantic candidates (`logical_clef` and `quarter_rests`) are correctly extracted using the Req-119 snapshot logic and returned under the `"semantic_candidates"` key in the result of `run_recognition_on_file` and each page's `page_info` in `inspect_pdf_file`.

### Claim 2: Strict non-goals (no pitch/rhythm timeline inference, no ScoreIR changes, no private fixtures)

Status: verified.

No new semantic classes or conversion code were added. The new output key `"semantic_candidates"` is diagnostic-only and does not affect the translation flow to ScoreIR.

### Claim 3: Legacy ScoreIR/playable output is verified unchanged

Status: verified.

Tests in `tests/test_semantic_cli_reporting.py` run the `convert` command on standard public fixtures and assert that the generated GP summary/reports contain no leaked semantic candidate fields and that the output remains valid and unchanged.

## Tests Prove Wanted Behaviour

Yes. Focused unit tests verify that semantic candidates are exposed in the JSON outputs of both CLI paths and the reporting script.

## Unsupported Claims

- Pitch/rhythm duration guesses.
- Support for scanned/OCR PDF.

## Required Fixes

None.

## Suggested Next Action

Promote Req-121 (Task 53) / Fail-closed semantic coverage expansion.
