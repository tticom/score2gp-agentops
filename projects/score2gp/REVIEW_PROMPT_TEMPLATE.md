# ScoreToGP Review Prompt Template

This template directs a reviewer/architect agent to evaluate a completed implementation PR before drafting the next prompt.

---

## 1. Governance Rule: Review First, Prompt Second

**You must complete the evaluation review before writing any implementation instructions.** 
Do not assume the implementation agent succeeded. Ground your assessment in local validation, visual verification, and coherent logs.

---

## 2. Review Role Contract — Adversarial Verification Mode

You must operate in **Adversarial Verification Mode**.
- Start from `cannot verify`.
- Approval must be earned from independently verified evidence (tests, diffs, outputs, hygiene). Self-reporting is not evidence.
- Test the strongest failure modes before approving.
- Reject summary-only approval.
- Verify that the proposed next task is the smallest safe task.
- Reject tasks that merely repeat prior evidence.
- You must find blockers, missing evidence, false progress, unsafe scope expansion, and unsupported readiness claims.

---

## 3. Review Instructions

### Task 1: Create Adversarial Review Evidence Ledger
You must produce a mandatory `Adversarial Review Evidence Ledger` for all key claims in the review. Missing evidence must be treated as a verdict-changing blocker.
For each key claim, provide:
- **Claim**: [State the key claim]
- **Evidence inspected**: [State the exact reproducible evidence reviewed, cross-referencing `summary.json`, `warnings.json`, and `roundtrip_report.json`. Ensure all artifacts are from the same, single-run execution and are completely consistent.]
- **Evidence classification**: `verified` / `partially verified` / `not verified` / `contradicted` / `out of scope`
- **Strongest failure mode**: [What is the strongest failure mode considered?]
- **Was the failure mode tested or ruled out**: [Yes/No, and how]
- **Verdict consequence**: [State the verdict consequence. Untested failure modes and any non-verified classification MUST result in a verdict consequence, not just missing evidence.]

### Task 2: Identify Contradictions
- Check if visual/source evidence contradicts diagnostic summaries. If a contradiction is found, assume the tool output is wrong and label the claim as `contradicted` in the ledger.

### Task 3: Execute Disconfirmation Gate
- You must actively check for false success by providing a `Disconfirmation Gate` block. List the main ways the PR could falsely appear successful, evidence checked against each, untested failure modes, whether they block approval, and the final blocker consequence.

### Task 4: Identify Architectural Risks
- Inspect the diff to confirm that MusicXML pitch/tuning data was not used to bypass PDF geometry gates or drive layout grouping.
- Ensure that the global warning filter remains tightly constrained and that no safety gates were loosened in strict mode.

---

## 3. Decision Matrix

Select a recommendation based on the evidence:
- **Approve**: Strict-mode conversion successfully passed on the active benchmark rung with >95% semantic match rates.
- **Keep Draft**: Mismatched arrangements, unproven claims, or research-isolation phases.
- **Request Changes**: Code style errors, safety gate bypasses, or inconsistent artifacts.
- **Close / Supersede**: Out of scope, redundant work, or unresolvable arrangement drift.

---

## 4. Next Implementation Prompt & Evidence Requirements

**Draft the next implementation prompt only after the decision above is finalized.**
Ensure that the mandatory run record under `projects/score2gp/runs/<date>-<slug>.md` has been successfully created and checked. Under the **Mandatory Evidence Record Rule**, if no report file was written to `score2gp-agentops`, the task is incomplete and cannot be approved.

Use the standard implementation template and specify:
- Current verified state.
- Progress Baseline (what specific evidence/PR is being built upon).
- Target branch name.
- Narrow, single-rung active goal.
- Incremental Progress Check (what new evidence/capability is produced).
- Non-goals (what must not be started).
- Verification commands.
