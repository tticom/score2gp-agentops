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

- **Status**: `Fix` / `Research-Isolation` / `Infrastructure` / `Blocked` / `Rejected`
- **Merge Recommendation**: `Approve` / `Keep Draft` / `Request Changes` / `Close-Supersede`
- **One-Sentence Reason**: A single, concise sentence explaining the recommendation based on the evidence.

---

## 2. Adversarial Review Evidence Ledger

For every key claim made by the author or in the PR, you must provide a ledger entry. Missing evidence is a verdict-changing blocker.

- **Claim**: [State the agent's claim]
- **Evidence inspected**: [State the exact reproducible evidence reviewed]
- **Evidence classification**: `verified` / `partially verified` / `not verified` / `contradicted` / `out of scope`
- **Strongest failure mode**: [What is the strongest failure mode considered?]
- **Was the failure mode tested or ruled out**: [Yes/No, and how]
- **Verdict consequence**: [State the verdict consequence. Untested failure modes and any non-verified classification MUST result in a verdict consequence, not just missing evidence.]

---

## 3. Disconfirmation Gate

- **Main ways this PR/task could falsely appear successful**: [List failure modes]
- **Evidence checked against each false-success mode**: [What evidence ruled them out]
- **Untested failure modes**: [List any failure modes that were not tested]
- **Whether any untested failure mode blocks approval**: [Yes/No, with rationale]
- **Final blocker/readiness consequence**: [Does this PR pass the disconfirmation gate?]

---

## 4. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes` / `no`
  - **Exact Command Run**: [State the CLI command]
- **Artifact Coherence**: `yes` / `no`
  - *Note: Do all generated artifacts (summary.json, warnings.json, roundtrip_report.json) agree on compiler status and generation? If not, stop and require reconciliation.*

---

## 5. Required Result Channels

- **Strict-Mode Result**: [Report strict compile results; list safety blockers]
- **Remediation / Diagnostic Result**: [Report permissive/debug/skipped compile results]
- **Semantic Round-Trip Result**: [Report notes count, string/fret match rates, and poor/unknown bars]
- **Generated-File Existence**: [Report if ScoreIR and GP packages were written]

---

## 6. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `yes` / `no`
- **Unsafe warning suppressions added to strict mode?**: `yes` / `no`
- **Only thin control-plane pointers added to product repo?**: `yes` / `no`

---

## 7. Public Regression Coverage

- **Public synthetic fixture added or updated?**: [Name of the fixture]
- **Mechanical defect reproduced?**: `yes` / `no`
- **Production path exercised?**: `yes` / `no`

---

## 8. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes` / `no`
  - **Record Path**: [e.g. projects/score2gp/runs/<date>-<slug>.md]
  - *Note: If no report file was written, the review status must remain Keeping Draft or Requesting Changes; the task is incomplete.*

---

## 9. Next Required Evidence
- [Define exactly what evidence is required to advance this PR or the next branch]
