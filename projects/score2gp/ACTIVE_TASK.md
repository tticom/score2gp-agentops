# Active Task

**Task**: Architect research — design a safe single-prompt autonomous cycle workflow
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops`

## Status

APPROVED

## Executable Task

Yes

## Completion Evidence
The Architect must publish an architecture report (`projects/score2gp/research/2026-07-08-single-prompt-autonomous-cycle-architecture.md`) analyzing the safety, role compliance, and workflow feasibility of the single-prompt autonomous loop, detailing Outcome A, B, or C, and specifying exact stop gates and data flow mechanics.

## 1. Baseline
- Product PR #338: squash-merged at `ff241fbc0c714eb62acc14f5171f61cefa9c30ea`
- Governance PR #247: squash-merged at `c3b129a9514dd0e137d627f4a89fd1e81d081cf8`
- Decision record: `projects/score2gp/decisions/2026-07-08-pr338-completion-and-single-prompt-cycle-architecture-authorisation.md`

## 2. Context
Product PR #338 successfully implemented multi-staff parallel timing in `notation_bridge.py`. PR #247 implemented a cross-repo status bootstrap utility and updated startup rules. The Supervisor has reprioritized workflow turnaround efficiency and safety, overriding the next queue item (Task 14) to remain queued. This task authorises the Architect to design a safe, gated, multi-agent autonomous loop that can be launched from a single human prompt.

## 3. Active Blocker
Turnaround times are constrained by manual human copy-pasting of evidence, prompt generation, and step-by-step triggers between the Architect, Developer, Reviewer, and Integrator roles.

## 4. Goal
Analyze and design a single-prompt, multi-agent orchestration cycle that:
- Runs bootstrap first as a mandatory startup summary;
- Sequences agents (Architect, Developer, Reviewer) securely;
- Preserves explicit role boundaries and prevents self-approval;
- Employs strict evidence verification gates (fails closed);
- Passes status/evidence outputs between agents without manual copy-paste;
- Handles PR creation, review, merge, expected-head protection, and post-merge recording;
- Defines stop/pivot triggers and Supervisor approval gates.

## 5. Non-goals
- No product logic modifications.
- No developer implementation work is authorised.
- No automatic merge policies without head-matching and verification.
- No removal of Reviewer or PR readiness review gates.

## 6. Repo Scope
- **Allow**:
  - `projects/score2gp/research/2026-07-08-single-prompt-autonomous-cycle-architecture.md`
- **Stop before changing**:
  - `ACTIVE_TASK.md` or any other governance policy files;
  - any files in the product repository.

## 7. Branch Suggestion
`architect/single-prompt-autonomous-cycle-architecture-v0.1`

## 8. Required Output & Outcome
Architect must select exactly one:
- **Outcome A**: Cycle is viable for Tier B only, with Tier A pauses.
- **Outcome B**: Cycle is viable for both Tier A and Tier B with explicit stop gates.
- **Outcome C**: Full cycle is not safe; propose a smaller assistant/orchestrator improvement.

And define:
- Exact data flow mechanics between agents (preventing copy/paste).
- Concrete stop/pivot gates.
- Safety enforcement (e.g. expected-head check, artifact checks).

## 9. Next Steps
- Required next review: Reviewer architecture verification.
