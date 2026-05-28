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

## Durable Agent State & Mandatory Evidence Record Rule

Durable agent state and task run history for ScoreToGP live here in `score2gp-agentops`, not in the product repository:

- Handoffs live under [`handoffs/`](handoffs/).
- Review decisions live under [`reviews/`](reviews/).
- Run records live under [`runs/`](runs/).
- Task and benchmark state lives under [`tasks/`](tasks/).

> [!IMPORTANT]
> **Mandatory Evidence Record Rule**
> Every agent task must create or update one durable markdown file in `score2gp-agentops` before reporting completion.
>
> **Accepted Locations**:
> - `projects/score2gp/runs/<date>-<slug>.md`
> - `projects/score2gp/reviews/<date>-<slug>.md`
> - `projects/score2gp/research/<date>-<slug>.md`
> **Required Information**:
> The record must include: repo and branch, command(s) run, input availability (using private-safe basenames only), output directory path (if any), strict conversion status, remediation/diagnostic status, generated file existence, semantic round-trip status, exact blocker category, private-safe metrics, public tests run, private-safety audit, and next required evidence.
> If no report file was written, the task is incomplete.

> [!IMPORTANT]
> **Mandatory Prompt Chain Rule**
> Every agent run must record the exact explicit prompt chain used for that run.
>
> If the run includes multiple prompts, each prompt must be stored as a numbered immutable file under a `prompts/` directory.
>
> The final run/research/review record must state which prompt was operative for the final commit or conclusion.
>
> A PR body is not sufficient.
> A final chat response is not sufficient.
> Console output is not sufficient.
> A report without the prompt chain is incomplete.
>
> Agents cannot reliably record hidden platform/system instructions. They must record the explicit prompt text they received, plus the governance docs and repository refs they were instructed to read.


The product repository `AGENTS.md` is only a bootstrap pointer. It should identify `score2gp` as the product repository, route agents to this governance project, state local private-safety and verification commands, and stop if `score2gp-agentops` is unavailable.


---

## The Core Product Quality Principle

> [!IMPORTANT]
> **Generated GP or ScoreIR files are not conversion success.**
> An output file merely proves that generation occurred. Product success is achieved only when the **strict-mode semantic quality gate passes** and the generated notes match the original visual score perfectly without violating geometry or layout grouping rules. Permissive or remediation bypass modes are for diagnostics only and never represent a strict conversion pass.
