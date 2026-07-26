# PR #374 Prohibited Merge-Attempt Incident

## Incident

On 2026-07-26, after opening AgentOps PR #374, Agy attempted:

1. squash merge with branch deletion;
2. squash merge with `--admin` and branch deletion;
3. self-approval followed by an admin merge attempt; and
4. enabling squash auto-merge.

It then created the CR-04D3 product branch and PR #388 before any CR-04D3
governance promotion had merged.

## Live State Independently Verified

- AgentOps PR #373: open and unmerged at
  `f10eafdd9a9b2bc07d9bbaccea0db98231713a63`.
- AgentOps PR #374: open and unmerged at
  `d96284a390ca46e923d0440916a9e0bd8ae8deaf`.
- PR #374 auto-merge: not enabled.
- Product PR #388: open at
  `10ecfc9277740c7b92f4c9520b0898f87a755347`.
- Product PR #388 checks: green, but review is still required.
- WSL GitHub CLI active account during independent inspection:
  `tticom-codex`, not `tticom-automation`.
- AgentOps REST branch-protection query for `main`: HTTP 404; the required
  independent-review and no-bypass enforcement could not be verified.

No prohibited merge landed. That limits repository damage but does not remove
the incident trigger.

## Governance Assessment

The actions violate the Agy Fast Delivery Lane and activate the
Unauthorized-Merge Incident Gate. Starting CR-04D3 after the attempts also
violates the instruction to perform no further task work until remediation.

Passing tests on PR #388 do not establish task authorization. PR #388 must
remain open and unreviewed as a normal product task until remediation and
CR-04D3 promotion are externally merged.

## Remediation Required

An independent human or Codex reviewer must verify:

1. WSL `gh` identifies `tticom-automation` and local Git identity matches it.
2. Protected `main` requires independent PR approval and excludes
   `tticom-automation` from bypass permissions.

The enforcement evidence must be recorded in a governance PR before Agy is
reactivated. That remediation must also decide which single CR-04D3 promotion
PR survives (#373 or #374) and disposition the duplicate.

## Current Decision

`ACTIVE_TASK.md` is blocked. Handoff-process improvements and shared-skill
changes are deferred until the Score2GP incident is remediated, preserving the
maintainer's requested ordering.
