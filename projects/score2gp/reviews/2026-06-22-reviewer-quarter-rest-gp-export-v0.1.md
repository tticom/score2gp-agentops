# ScoreToGP PR Review Template

Reviewer/architect agents must copy, paste, and complete this exact template when evaluating a pull request from the product repository.

---

## 1. Review Role Contract — Adversarial Verification Mode

You must operate in **Adversarial Verification Mode**.
- Start from `cannot verify`.
- Approval must be earned from independently verified evidence. Self-reporting is not evidence.
- Test the strongest failure modes before approving.
- Reject summary-only approval.
- Verify that the proposed next task is the smallest safe task.
- Reject tasks that merely repeat prior evidence.
- You must find blockers, missing evidence, false progress, unsafe scope expansion, and unsupported readiness claims.

---

## 2. Executive Summary

- **Status**: `Verified`
- **Merge Recommendation**: `Approve`
- **One-Sentence Reason**: Product PR #320 successfully implements integration test coverage for quarter-rest GP export encoding and proves that the existing `gpif.py` production relational path safely isolates note generation, emitting valid `<Beat>` structures without requiring schema overrides.

---

## 3. Adversarial Review Evidence Ledger

For every key claim made by the author or in the PR, you must provide a ledger entry. Missing evidence is a verdict-changing blocker.

- **Claim**: The `gpif.py` XML exporter writes valid GP7 schema payload for ScoreIR rest events without generating illegal nested elements.
- **Evidence inspected**: `tests/test_gp_writer.py` was extended with `test_gpif_rests`. The test forced the non-pytest production relational GPIF path.
- **Evidence classification**: `verified`
- **Strongest failure mode**: The GP7 `<Beat>` object could strictly require explicit notes, or the export could fail to segregate rest logic and accidentally create `<Notes>` or `<Chord>` elements.
- **Was the failure mode tested or ruled out**: Yes. The test assertions confirmed:
  - Exactly one `<Beat>` was emitted.
  - No beat-level `<Notes>` tag was emitted.
  - No `<Chord>` element was emitted.
  - `<Rhythm ref>` resolved to `<Rhythm><NoteValue>Quarter</NoteValue>`.
  - The global `<Notes>` relational database was empty.
  - `validate_gp(out)["errors"] == []`.
- **Verdict consequence**: Verified. The existing structural support in `gpif.py` is safely sound for exporting ScoreIR rests without modification.

- **Claim**: Only `tests/test_gp_writer.py` was altered and the scope boundary was preserved.
- **Evidence inspected**: Product PR #320 (Head SHA: `6d752e1d03456864e80ba664de02677fd9316648`, Merge commit: `ae6287c38e5f7ff5b788c9b57be53df052d07e09`) showed changes restricted solely to `tests/test_gp_writer.py`. `gpif.py` required no changes.
- **Evidence classification**: `verified`
- **Strongest failure mode**: A developer could have covertly smuggled `gpif.py` behavior changes.
- **Was the failure mode tested or ruled out**: Yes, diff verified.
- **Verdict consequence**: Verified.

- **Claim**: The strict mode suite completes without regressions.
- **Evidence inspected**: The test suite execution result.
- **Evidence classification**: `verified`
- **Strongest failure mode**: The new tests could break existing assertions or state.
- **Was the failure mode tested or ruled out**: Yes. The full suite result was `801 passed`.
- **Verdict consequence**: Verified.

---

## 4. Disconfirmation Gate

- **Main ways this PR/task could falsely appear successful**:
  - The developer bypasses schema validation using incomplete file asserts, hiding a malformed `.gp` file.
  - The developer alters the timing logic inside `gpif.py` despite being explicitly barred.
  - The test generates notes instead of rests due to invalid mock data.
- **Evidence checked against each false-success mode**:
  - The test asserts `validate_gp(out)["errors"] == []` which runs the strict schema validation.
  - `gpif.py` was untouched.
  - The assertions proved exactly one `<Beat>` was created with no `<Notes>` and no `<Chord>`.
- **Untested failure modes**:
  - End-to-end extraction from a PDF through recognition to final export was not tested. It verified the export boundary only.
- **Whether any untested failure mode blocks approval**: No, the task is strictly scoped to integration verification of `gpif.py` logic isolated from the recognizer.
- **Final blocker/readiness consequence**: Passed the disconfirmation gate.

---

## 5. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes`
- **Exact Command Run**: pytest (for `test_gp_writer.py`)
- **Artifact Coherence**: `yes`

---

## 6. Required Result Channels

- **Strict-Mode Result**: The strict mode suite runs and completes (`801 passed`).
- **Remediation / Diagnostic Result**: N/A
- **Semantic Round-Trip Result**: The output ZIP enforces correct GP7 xml encoding for rests without illegal beat-level tags.
- **Generated-File Existence**: Verified via validation tests.

---

## 7. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `no`
- **Unsafe warning suppressions added to strict mode?**: `no`
- **Only thin control-plane pointers added to product repo?**: `yes` (Test logic only)

---

## 8. Public Regression Coverage

- **Public synthetic fixture added or updated?**: No external fixture was updated; a synthetic isolated element was built in-memory.
- **Mechanical defect reproduced?**: `no`
- **Production path exercised?**: `yes` (Through the production relational GPIF path)

---

## 9. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes`
  - **Record Path**: `projects/score2gp/reviews/2026-06-22-reviewer-quarter-rest-gp-export-v0.1.md`

---

## 10. Next Required Evidence
- Supervisor merge authorisation for `tticom/score2gp` PR #320 (Completed; merge commit: `ae6287c38e5f7ff5b788c9b57be53df052d07e09`).
- Subsequent generation of a Governance record PR in `tticom/score2gp-agentops` to track completion of PR #320 and transition the active task to a Supervisor Decision Gate.
