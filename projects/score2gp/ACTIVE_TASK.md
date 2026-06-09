## Current Active Task

## Task 47 — Define first read-only recogniser prerequisites and acceptance criteria

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-47-read-only-recogniser-prereqs-v0.1`

PR title:
`docs(score2gp): define first read-only recogniser prerequisites`

Context:
Governance PR #101 is merged, producing the candidate diagnostics consumption boundary note. Candidate diagnostics are explicitly limited to read-only geometry/evidence inspection, preserving `None`/`[]` semantics. Before any robust recognisers are implemented, we must define the first isolated read-only recogniser target, its allowed inputs, and strict stop conditions.

Goal:
Create a governance-only design note (`projects/score2gp/reviews/2026-06-09-first-read-only-recogniser-prerequisites.md`) that defines the first safe, read-only recogniser prerequisite boundary and acceptance criteria. This task does not authorise product implementation.

Non-goals:
- Do not modify the product repo.
- Do not implement any recogniser.
- Do not infer musical semantics or emit ScoreIR.
- Do not create or update fixtures, artifacts, private PDFs, or logs.

Acceptance criteria:
- Governance PR opened from `governance/task-47-read-only-recogniser-prereqs-v0.1` to `main`.
- Exactly one governance design note is added, alongside this `ACTIVE_TASK.md` update.
- No product repo files are changed.
- The design note selects one evidence-driven, read-only target.
- The note defines allowed evidence, fixture requirements, and stop conditions.

Stop conditions:
- Product repo would need modification.
- Private artifacts are needed.
- Inference requires semantic ScoreIR integration or fake geometry.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Test/check results
- Privacy/artifact check results
- Known limitations
- Whether PR is ready for review
- Recommended next smallest task after this PR is merged
