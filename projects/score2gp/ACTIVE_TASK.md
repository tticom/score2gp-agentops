## Current Active Task

## Task 68 — Select next diagnostic-only evidence path after PR #240

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-68-next-diagnostic-evidence-path-v0.1`

PR title:
`docs(governance): add Task 68 decision on next diagnostic-only path`

Context:
Product PR #240 (Task 67) was audited and successfully merged, providing a repeatable raster diagnostics gate report. The next step is to further consolidate our baseline confidence before allowing semantic logic to take effect. We must formally select the next product task to address the false-negative taxonomy.

Goal:
Create a governance decision document in `projects/score2gp/decisions/2026-06-11-raster-diagnostics-false-negative-manifest.md` summarizing the completed Task 67 evidence and formally selecting Task 69 as a product task focused on classifying the false-negative categories into a machine-readable manifest.

Non-goals:
- Do not implement ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise semantic promotion of `treble_clef_candidate`.
- Do not authorise pitch, rhythm, key signature, time signature, note, rest, voice, or musical inference.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not implement product repo changes.
- Do not commit private/generated artifacts.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- A new decision document exists at `projects/score2gp/decisions/2026-06-11-raster-diagnostics-false-negative-manifest.md`.
- The document summarizes Task 67 as complete.
- The document explicitly blocks semantic promotion and vector/raster fusion.
- The document selects a new diagnostic-only Task 69 that implements a machine-readable manifest for false negatives.
- `ACTIVE_TASK.md` is updated to Task 68.
- A PR is raised for this governance task.

Stop conditions:
- Governance `main` is dirty before work starts.
- Product repo files are modified.
- The task attempts to authorise semantic promotion or vector/raster fusion.

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
- summary of Task 68 decision
- selected next diagnostic-only path
- known limitations
- whether PR is ready for review
