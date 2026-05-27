# ScoreToGP Review Prompt Template

This template directs a reviewer/architect agent to evaluate a completed implementation PR before drafting the next prompt.

---

## 1. Governance Rule: Review First, Prompt Second

**You must complete the evaluation review before writing any implementation instructions.** 
Do not assume the implementation agent succeeded. Ground your assessment in local validation, visual verification, and coherent logs.

---

## 2. Review Instructions

### Task 1: Verify Claims
- Cross-reference the agent's claims against `summary.json`, `warnings.json`, and `roundtrip_report.json`.
- Ensure all artifacts are from the same, single-run execution and are completely consistent.

### Task 2: Identify Contradictions
- Check if visual/source evidence contradicts diagnostic summaries (e.g. check if a measure or system is visible in the original PDF but reported missing by the tool). 
- If a contradiction is found, assume the tool output is wrong and label the claim as `contradicted`.

### Task 3: Identify Architectural Risks
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

## 4. Next Implementation Prompt Generation

**Draft the next implementation prompt only after the decision above is finalized.**
Use the standard implementation template and specify:
- Current verified state.
- Target branch name.
- Narrow, single-rung active goal.
- Non-goals (what must not be started).
- Verification commands.
