## Current Active Task

## Task 46 — Candidate diagnostics consumption boundary review

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`review/candidate-diagnostics-consumption-boundary-v0.1`

PR title:
`docs(score2gp): define candidate diagnostics consumption boundary review`

Context:
Product PR #234 is merged (commit `7dabc59ac120dfc726ccb72c47586eb1af37392f`). This completed Task 45: Implement read-only candidate diagnostics integration. The product repository now exposes `left_margin_candidates` and `x_aligned_cluster_candidates` as optional read-only supplementary fields on `NotationStaffDiagnostics`.

Before any recogniser work can begin, we must review the newly merged candidate diagnostics output and define the next safe boundary. This review determines how these diagnostics should be consumed downstream while strictly preserving evidence boundaries and explicitly rejecting semantic inference.

Goal:
Produce a governance-only review/design note under `projects/score2gp/reviews/` that inspects the candidate diagnostics contract and recommends the next smallest evidence-preserving step. The review must define what downstream consumers may read, what they must not infer yet, what evidence must be preserved, and what prerequisite diagnostics are still missing.

Non-goals:
- Do not modify the product repo (`tticom/score2gp`).
- Do not implement recogniser logic.
- Do not infer musical semantics.
- Do not classify notes, rests, clefs, pitch, rhythm, duration, voices, bars, or ScoreIR events.
- Do not create fixtures, snapshots, PDFs, GP files, logs, or generated artifacts.
- Do not promote product implementation until the boundary review is complete and merged.

Required pre-flight checks:
From the governance repo:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp-agentops
git status --short
git branch --show-current
git fetch --all --prune
```

From the product repo:
```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
git branch --show-current
git fetch --all --prune
git switch main
git pull --ff-only
gh pr view 234 --json state,mergedAt,mergeCommit,headRefOid,baseRefName
```

Implementation guidance:
- Produce a new markdown document under `projects/score2gp/reviews/` (e.g., `candidate_diagnostics_consumption_boundary.md`).
- Review the candidate diagnostics contract implemented in Task 45.
- Identify how downstream processing should safely consume `left_margin_candidates` and `x_aligned_cluster_candidates`.
- Explicitly block any semantic inference and ScoreIR integration at this stage.
- Define the evidence required before any future recogniser implementation.
- Recommend the next smallest safe step.

Acceptance criteria:
- A governance PR is opened from `review/candidate-diagnostics-consumption-boundary-v0.1` to `main`.
- Only governance files are changed.
- No product files are changed.
- No private/generated artifacts are committed.
- Task 46 is clearly design/review-only.
- Task 46 explicitly blocks semantic inference and ScoreIR integration.
- Task 46 defines the evidence required before any future recogniser implementation.

Reporting format:
The governance agent must report:
- Governance branch name.
- Governance PR link.
- Exact files changed.
- Commit hash.
- Commands run.
- Summary of the boundary review conclusions.
- The recommended next task.
- Known limitations.
