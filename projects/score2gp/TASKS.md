# Agent Execution Gate

This task queue is not permission to execute work.

Agents must not start any unchecked task from this file.

The only executable task source is:

`projects/score2gp/ACTIVE_TASK.md`

If `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`, the agent must stop after preflight and report.

Agents must not:

- merge PRs
- push directly to main
- delete branches
- force-push
- run `gh pr merge`
- run commands containing `--delete-branch`
- run `hgh`
- approve own PR
- bypass failing checks
- mark unmerged work as merged/done
- start unrelated backlog tasks
- modify files without explicit approval in `ACTIVE_TASK.md` or the current user session

Unchecked tasks below are backlog candidates only.

---

# Score2GP Task Queue

This file serves as a durable task queue to organize and track governance and product priorities for `score2gp`. It replaces scattered next-priority lists found in individual research documents.

## 1. Verified Baseline

**Current Baseline:** Post-PR #193
Product `main` passed the post-merge smoke tests:
- Full `pytest` passed (544 passing).
- `validate-ir` on `fixtures/public/tiny_score.ir.json` passed.
- `git diff --check` clean.
- Privacy checks clean (no leakages of semantic dumps, private PDFs, or raw paths).

## 2. Completed Items (Post-PR #191 Priority List)

- [x] PR #191: Added pure staff-position indexing.
- [x] PR #68: Researched staff-local primitive clustering.
- [x] PR #192: Implemented aggregate x-aligned primitive clustering diagnostics.
- [x] PR #69: Researched left-margin font/text/ink density diagnostics.
- [x] PR #193: Implemented aggregate left-margin diagnostics.
- [x] Researched post-PR #193 diagnostics boundary strictness (see `RESEARCH_POST_193_DIAGNOSTICS_BOUNDARY.md`).

*(Note: Both diagnostic paths implemented in PR #192 and PR #193 remain geometry-only and diagnostic-only.)*

## 3. Explicitly Deferred Capabilities

To maintain the project's strict architecture and safety boundaries, the following tasks remain explicitly **deferred**. Do not propose or implement them:

- Scanned / OCR PDF support (We remain strictly focused on born-digital PDF parsing).
- Pitch mapping / Pitch inference.
- Clef handling and parsing.
- Notehead classification.
- Rhythm inference / duration extraction.
- Voice assignment.
- Bar-local timing grids inference.
- ScoreIR event creation / integration into the pipeline.
- Direct integration of geometry clusters into the final playback mapping.

## 4. Next Safe Tasks

The following tasks represent the safe, geometry-first next steps for the project:

- [x] **Architecture Review:** Conducted a post-PR #193 architecture review focusing on the strictness of current diagnostics boundaries (Findings documented).
- [ ] **Import Boundary Hardening:** Research import-boundary hardening v0.2. Evaluate if the current geometry guardrails and PDF import boundaries are too narrow.
- [ ] **Diagnostics Schema Stability:** Research diagnostics schema stability and versioning specifically for the new geometry diagnostics components.
- [ ] **Fixture Expansion:** Research public fixture expansion for born-digital standard-staff diagnostics to increase coverage without violating privacy boundaries.
- [ ] **Documentation:** Consider drafting lightweight documentation explaining the diagnostics pipeline boundaries to future contributors and agents.
