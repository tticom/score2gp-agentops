## Current Active Task

## Task 52 — Record raster diagnostics merge and define opening-symbol diagnostics consumption boundary

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-52-raster-opening-symbol-consumption-boundary-v0.1`

PR title:
`docs(score2gp): define raster opening-symbol diagnostics consumption boundary`

Context:
Task 52 records Product PR #235 as merged.
Task 52 reconciles PR #105 as closed-unmerged historical negative vector-path evidence.
Task 52 defines the raster opening-symbol diagnostics consumption boundary.
Task 52 does not authorise product recogniser implementation.
The next likely task is governance-only unless the boundary explicitly authorises implementation.

Goal:
Create a governance PR that records the raster diagnostics merge, reconciles closed-unmerged PR #105 as historical negative evidence, and defines the opening-symbol diagnostics consumption boundary before any recogniser or classifier implementation.

Non-goals:
- Do not modify the product repo.
- Do not implement any recogniser.
- Do not emit ScoreIR.
- Do not infer pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.

Acceptance criteria:
- Governance PR opened from `governance/task-52-raster-opening-symbol-consumption-boundary-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated.
- `projects/score2gp/reviews/2026-06-10-raster-opening-symbol-diagnostics-consumption-boundary.md` is added.
- The note records Product PR #235 merge and PR #105 closure.
- The note defines a clear consumption boundary for raster diagnostics and explicitly blocks ScoreIR and recogniser implementation until authorised.

Stop conditions:
- Repo is dirty before work starts.
- PR #235 is not merged or PR #105 is unexpectedly merged.
- The task requires product repo modifications.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results
- Privacy/artifact check results
- Known limitations
- Whether PR is ready for review
- Recommended next smallest task after this PR is merged
