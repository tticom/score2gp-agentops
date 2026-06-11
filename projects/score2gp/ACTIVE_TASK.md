## Current Active Task

## Task 66 — Select next diagnostic-only evidence path after PR #239

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-66-next-diagnostic-evidence-path-v0.1`

PR title:
`docs(governance): add Task 66 decision on next diagnostic-only path`

Context:
Product PR #239 was audited and successfully merged, proving diagnostic-only rejection of negative TAB/blank/noise fixtures and providing a false-negative taxonomy. Despite this, semantic promotion of treble clef candidates remains explicitly blocked. We must now decide on the next purely diagnostic path to consolidate our evidence base before any semantic implementation is authorised.

Goal:
Create a governance decision document in `projects/score2gp/decisions/2026-06-11-next-diagnostic-evidence-path.md` summarizing the completed Task 65 evidence, explicitly blocking semantic promotion, and formally selecting Task 67 as a product task focused on a repeatable diagnostic gate report.

Non-goals:
- Do not implement ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise semantic promotion of `treble_clef_candidate`.
- Do not authorise pitch, rhythm, key signature, time signature, note, rest, voice, or musical inference.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not authorise vector-based treble clef candidate extraction.
- Do not implement product repo changes.
- Do not commit private/generated artifacts.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- A new decision document exists at `projects/score2gp/decisions/2026-06-11-next-diagnostic-evidence-path.md`.
- The document summarizes Task 65 as complete.
- The document explicitly blocks semantic promotion and vector/raster fusion.
- The document selects a new diagnostic-only Task 67 that implements a repeatable diagnostic gate report script.
- `ACTIVE_TASK.md` is updated to Task 66.
- A PR is raised for this governance task.

Stop conditions:
- Governance `main` is dirty before work starts.
- PR #119 is not merged.
- The task attempts to authorise semantic promotion or vector/raster fusion.
- Product repo files are modified.

Required validation:
- `git status --short`
- `git diff --check`
- `git ls-files | grep -Ei "(scratch|tmp|\.log$|screenshot|output|private_diagnostics|rendered|\.png$|\.jpg$|\.jpeg$|\.pdf$|\.gp$)" || true`
- `find . -path "./.git" -prune -o -type f -size +10M -print`

Reporting format:
- branch name
- PR link
- full commit hash
- exact files changed
- commands run
- validation results
- privacy/artifact check results
- summary of Task 66 decision
- selected next diagnostic-only path
- whether Task 67 is recommended
- known limitations
- whether PR is ready for review
