## Current Active Task

## Task 53 — Define read-only treble-clef candidate classifier boundary

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-53-read-only-treble-clef-candidate-classifier-boundary-v0.1`

PR title:
`docs(score2gp): define read-only treble-clef candidate classifier boundary`

Context:
Task 53 defines a read-only treble-clef candidate classifier boundary.
Task 53 is governance-only.
Task 53 does not authorise product implementation.
Task 53 depends on merged PR #106.
The next likely task, after this PR is merged and reviewed, may be a product implementation task for diagnostic-only classifier output, but only if this note explicitly authorises that boundary.

Goal:
Create a governance PR in `tticom/score2gp-agentops` that defines a read-only treble-clef candidate classifier boundary.

Non-goals:
- Do not modify the product repo.
- Do not implement classifier code.
- Do not emit ScoreIR.
- Do not infer full musical semantics.
- Do not convert `raster_opening_symbol_candidate` into a recognised clef.

Acceptance criteria:
- Governance PR opened from `governance/task-53-read-only-treble-clef-candidate-classifier-boundary-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated.
- `projects/score2gp/reviews/2026-06-10-read-only-treble-clef-candidate-classifier-boundary.md` is added.
- The note defines allowed inputs and outputs for a read-only treble-clef candidate classifier.
- The note blocks ScoreIR and full recogniser implementation.
- The note requires `unknown` handling and empirical validation.

Stop conditions:
- PR #106 is not merged.
- Repo is dirty before work starts.
- The task requires product repo changes or new fixtures.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results
- Privacy/artifact check results
- How PR #106 merge was verified
- Boundary summary
- Known limitations
- Whether PR is ready for review
- Recommended next smallest task after this PR is merged
