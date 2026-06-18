# ScoreToGP PR Review Template

Reviewer/architect agents must copy, paste, and complete this exact template when evaluating a pull request from the product repository.

---

## 1. Executive Summary

- **Status**: `Fix` / `Research-Isolation` / `Infrastructure` / `Blocked` / `Rejected`
- **Merge Recommendation**: `Approve` / `Keep Draft` / `Request Changes` / `Close-Supersede`
- **One-Sentence Reason**: A single, concise sentence explaining the recommendation based on the evidence.

---

## 2. Claims vs. Evidence

- **Claim**: [State the agent's claim]
  - **Evidence**: [State the reproducible evidence reviewed]
  - **Verified?**: `yes` / `no`
  - **Incremental Progress Verified?**: `yes` / `no` (Must not merely repeat the baseline)
  - **Contradictions**: [Identify any contradictions between visual/source files and tool output]

---

## 3. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes` / `no`
  - **Exact Command Run**: [State the CLI command]
- **Artifact Coherence**: `yes` / `no`
  - *Note: Do all generated artifacts (summary.json, warnings.json, roundtrip_report.json) agree on compiler status and generation? If not, stop and require reconciliation.*

---

## 4. Required Result Channels

- **Strict-Mode Result**: [Report strict compile results; list safety blockers]
- **Remediation / Diagnostic Result**: [Report permissive/debug/skipped compile results]
- **Semantic Round-Trip Result**: [Report notes count, string/fret match rates, and poor/unknown bars]
- **Generated-File Existence**: [Report if ScoreIR and GP packages were written]

---

## 5. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `yes` / `no`
- **Unsafe warning suppressions added to strict mode?**: `yes` / `no`
- **Only thin control-plane pointers added to product repo?**: `yes` / `no`

---

## 6. Public Regression Coverage

- **Public synthetic fixture added or updated?**: [Name of the fixture]
- **Mechanical defect reproduced?**: `yes` / `no`
- **Production path exercised?**: `yes` / `no`

---

## 7. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes` / `no`
  - **Record Path**: [e.g. projects/score2gp/runs/<date>-<slug>.md]
  - *Note: If no report file was written, the review status must remain Keeping Draft or Requesting Changes; the task is incomplete.*

---

## 8. Next Required Evidence
- [Define exactly what evidence is required to advance this PR or the next branch]
