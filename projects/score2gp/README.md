# ScoreToGP Agent-Ops Governance Project

This directory contains the canonical agent-governance, review rubrics, prompt templates, and benchmark policies for the **ScoreToGP** project.

## Project Repositories

- **Product Repository**: [score2gp](https://github.com/tticom/score2gp)
  - Owns all product logic (`src/`), unit and integration tests (`tests/`), schemas, and public fixtures. It is focused strictly on code correctness, validation, and CLI execution.
- **Governance Repository**: [score2gp-agentops](https://github.com/tticom/score2gp-agentops)
  - Owns the control-plane rules, benchmark policies, prompt templates, and ADRs. It governs how reviewer and implementation agents coordinate work safely without polluting the product repository.

---

## Role & Coordination Workflows

1. **Implementation Agents**:
   - Work exclusively in the **product repository** (`score2gp`).
   - Receive a scoped implementation prompt from the governance repository and make targeted code changes to resolve active benchmark failures.
   - Stage, test, and push commits to isolated feature branches, keeping the working tree clean.
2. **Reviewer / Architect Agents**:
   - Work in the **governance repository** (`score2gp-agentops`) to evaluate product pull requests.
   - Strictly evaluate all claims, checks, and artifacts before drafting the next implementation instructions.
   - Judge whether changes should be trusted and verify strict safety gates.
3. **Human Maintainer**:
   - Acts as the final decider for the project.
   - Approves, rejects, merges, or redirects pull requests.
   - Audits private assets locally and determines benchmark ladder progression.

---

## Durable Agent State and Recording

Durable agent state for ScoreToGP lives here in `score2gp-agentops`, not in the product repository. [`TASK_RECORDING_CONVENTION.md`](TASK_RECORDING_CONVENTION.md) defines the single method:

- **Requirements:** [`requirements/`](requirements/).
- **Task authority and the single backlog:** [`ORCHESTRATION_STATE.json`](ORCHESTRATION_STATE.json), with the generated view [`ACTIVE_TASK.md`](ACTIVE_TASK.md).
- **Task prompts:** [`prompts/next/`](prompts/next/). The prompt at the authority revision that promoted a task is its operative instruction.
- **Evidence:** the pull request (exact-head handback, independent review and checks), plus one dated governance reconciliation record per completed task in [`handoffs/`](handoffs/). Research findings go in the requirement they serve, or in [`research/`](research/).

Dated record directories from earlier methods (`runs/`, `reviews/`, `reports/`, `decisions/`, `archive/`, `audits/`) are history. They are not written to for new work.

The product repository `AGENTS.md` is only a bootstrap pointer. It should identify `score2gp` as the product repository, route agents to this governance project, state local private-safety and verification commands, and stop if `score2gp-agentops` is unavailable.


---

## The Core Product Quality Principle

> [!IMPORTANT]
> **Generated GP or ScoreIR files are not conversion success.**
> An output file merely proves that generation occurred. Product success is achieved only when the **strict-mode semantic quality gate passes** and the generated notes match the original visual score perfectly without violating geometry or layout grouping rules. Permissive or remediation bypass modes are for diagnostics only and never represent a strict conversion pass.
