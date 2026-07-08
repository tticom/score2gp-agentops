# Active Task

**Task**: Reviewer architecture verification for single-prompt loop
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## Status

APPROVED

## Executable Task

Yes

## Completion Evidence
A Reviewer architecture verification report with adversarial evidence ledger and verdict, saved in the appropriate governance directory (e.g., `projects/score2gp/reviews/`).

## 1. Baseline
- The Architect has completed the single-prompt autonomous cycle workflow research (`Req-101`) and produced the architecture report.
- The control-plane orchestration flow remains constrained by manual handoff.

## 2. Context
The Architect was previously authorised to design a single-prompt, multi-agent autonomous cycle to improve turnaround times. The Architect has produced an architecture proposal detailing the loop mechanics, stop gates, and data flow. As mandated by `AGENT_PR_READINESS.md` and the Single-Task Loop Rule, the Reviewer must now independently verify the Architect's research before any Developer implementation is authorised.

## 3. Active Blocker
Developer implementation of the single-prompt cycle cannot begin until the Architect's plan is explicitly verified and approved by a Reviewer, ensuring the design is safe and measurable.

## 4. Goal
Verify the Architect's single-prompt autonomous cycle research before Developer implementation begins.

## 5. Non-goals
- No Developer implementation.
- No product code changes.

## 6. Repo Scope
- **Allow**:
  - Creation of a new review report in `projects/score2gp/reviews/`
- **Stop before changing**:
  - `ACTIVE_TASK.md` or any other governance policy files.
  - any files in the product repository `tticom/score2gp`.

## 7. Branch Suggestion
`review/single-prompt-cycle-architecture-v0.1`

## 8. Required Output & Outcome
Produce a Reviewer architecture verification report using Mode 1 (Architecture / research review) defined in `skills/reviewer/SKILL.md`.

The report must include:
- An adversarial evidence ledger independently testing the Architect's claims.
- A disconfirmation gate identifying ways the proposed loop could fail or become unsafe.
- A final Reviewer verdict (e.g., `approve architecture`, `return to architect`, etc.).

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: An independent architectural verdict detailing whether the proposed loop is safe to implement.
- **Which prior result must it not merely repeat?**: Must not just summarize the Architect's report. It must actively probe the proposed gates for failure modes.
- **How will we know the task moved the project forward?**: A conclusive verdict will clear or block the path for implementation.
- **What is the smallest next decision this task enables?**: Whether `Req-103` (Developer implementation of the loop) is safe to execute.

## 10. Next Steps
- Promote `Req-103` only after Reviewer verification passes (`approve architecture`).
