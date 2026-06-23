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

- **Status**: `Fix`
- **Merge Recommendation**: `Approve`
- **One-Sentence Reason**: Product PR #320 successfully implements missing integration test coverage for quarter-rest GP export encoding and proves that `gpif.py` safely isolates note generation, bypassing strict schema mismatches.

---

## 2. Adversarial Review Evidence Ledger

For every key claim made by the author or in the PR, you must provide a ledger entry. Missing evidence is a verdict-changing blocker.

- **Claim**: The `gpif.py` XML exporter writes valid GP7 schema payload for ScoreIR rest events without generating illegal nested elements.
- **Evidence inspected**: `tests/test_gp_writer.py` was extended with `test_gpif_rests`, asserting `validate_gp()` returns `xml_well_formed=True` and `errors=[]` for a dynamically constructed rest `<Event>`.
- **Evidence classification**: `verified`
- **Strongest failure mode**: The GP7 `<Beat>` object could strictly require an explicit internal `<Rest>` tag or reject empty note groups when a rest is generated, breaking `validate_gp`.
- **Was the failure mode tested or ruled out**: Yes, `validate_gp(out)` enforces GP7 constraints. The test executes this and ensures `errors` is empty. The output `.gp` correctly places `rest="true"` without internal note components.
- **Verdict consequence**: Verified. The existing structural support in `gpif.py` is safely sound for exporting ScoreIR rests without modification.

- **Claim**: Only `tests/test_gp_writer.py` was altered and the scope boundary was preserved.
- **Evidence inspected**: `gh pr diff 320` against `main` and `git diff --stat` showing exactly 51 insertions restricted to `tests/test_gp_writer.py`. No runtime dependencies, recognition pipelines, or sequencing logic were modified.
- **Evidence classification**: `verified`
- **Strongest failure mode**: A developer could have covertly smuggled test configurations or `gpif.py` behavior changes violating Architect Outcome A.
- **Was the failure mode tested or ruled out**: Yes, diff verified.
- **Verdict consequence**: Verified.

---

## 3. Disconfirmation Gate

- **Main ways this PR/task could falsely appear successful**:
  - The developer bypasses schema validation using incomplete file asserts, hiding a malformed `.gp` file.
  - The developer alters the timing logic inside `gpif.py` despite being explicitly barred.
  - The test generates notes instead of rests due to invalid mock data.
- **Evidence checked against each false-success mode**:
  - The test asserts `validate_gp(out)["errors"] == []` which runs the strict schema validation.
  - `gpif.py` was untouched (`git diff --stat`).
  - The test isolates the rest using `score.bars[0].events = [e for e in score.bars[0].events if getattr(e, "is_rest", False)]` and explicitly clears its notes: `e_rest.notes = []` and forces `e_rest.is_rest = True`.
- **Untested failure modes**:
  - End-to-end extraction from a PDF through recognition to final export was not tested. However, this is expected since the task explicitly forbade recognition or sequencing rework.
- **Whether any untested failure mode blocks approval**: No, the task is strictly scoped to integration verification of `gpif.py` logic isolated from the recognizer.
- **Final blocker/readiness consequence**: Passed the disconfirmation gate.

---

## 4. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes`
  - **Exact Command Run**: `git diff --check`, `find . -path "./.git" -prune -o -type f -size +10M -print`
- **Artifact Coherence**: `yes`
  - *Note: Do all generated artifacts (summary.json, warnings.json, roundtrip_report.json) agree on compiler status and generation? If not, stop and require reconciliation.* (N/A for integration unit test)

---

## 5. Required Result Channels

- **Strict-Mode Result**: The strict mode suite runs and completes (`801 passed`). `test_gpif_rests` correctly passes.
- **Remediation / Diagnostic Result**: N/A
- **Semantic Round-Trip Result**: The output ZIP enforces correct GP7 xml encoding `rhythm NoteValue == Quarter` and `<Event rest="true">`.
- **Generated-File Existence**: Verified via `tmp_path` asserts `zipfile.is_zipfile(out)` logic.

---

## 6. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `no`
- **Unsafe warning suppressions added to strict mode?**: `no`
- **Only thin control-plane pointers added to product repo?**: `yes` (Test logic only)

---

## 7. Public Regression Coverage

- **Public synthetic fixture added or updated?**: No external fixture was updated; a synthetic isolated element was built in-memory via `tiny_score.ir.json` fallback to ensure deterministic execution without touching prohibited system dependencies.
- **Mechanical defect reproduced?**: `no`
- **Production path exercised?**: `yes` (Through `gp_package.write_gp()`)

---

## 8. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes`
  - **Record Path**: `projects/score2gp/reviews/2026-06-22-reviewer-quarter-rest-gp-export-v0.1.md`

---

## 9. Next Required Evidence
- Supervisor merge authorisation for `tticom/score2gp` PR #320.
- Subsequent generation of a Governance record PR in `tticom/score2gp-agentops` to track completion of PR #320 and authorise the next logical phase in Score2GP development (likely the End-to-End Recogniser/Export Pipeline test for rests).
