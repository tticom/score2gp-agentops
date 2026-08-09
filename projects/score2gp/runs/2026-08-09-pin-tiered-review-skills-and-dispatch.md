# Pin Tiered Review Skills and Operational Dispatch

**Task**: Reviewer Role Firewall and Tiered Review Dispatch Integration
**Date**: 2026-08-09
**Status**: AWAITING_EXTERNAL_REVIEW
**Governance Author**: `tticom-codex`
**Repository**: `tticom/score2gp-agentops`
**Branch**: `codex/pin-tiered-review-skills`
**AgentOps Main SHA**: `ca8c4c9e1c74b87b48d1b08b9d96baaf1d453bd2`
**Product Main SHA**: `4a4f5c339e09987b9f41641397f1db7e8ab1be5d`
**Skills Lock SHA**: `439404f7342f4e324147efb6b0276f698fbf2bdb`

## Authority

The maintainer directed Codex to implement the reviewer-skill and instruction
changes after merging `tticom/agy-skills#14`. This is a bounded AgentOps
control-plane integration; it does not modify the active product task or any
product repository file.

## Implemented Contract

- Pin the merged `agy-skills` revision containing `code-review`, `hard-review`,
  and `devils-advocate-review`.
- Make `got` select a deterministic minimum review level from live changed
  paths, active authority, risk markers, and earlier-head trusted reviews.
- Materialize the exact live PR head in a detached, head-specific review
  worktree before authorizing review.
- Require an author comment pinning the exact live head before review dispatch.
- Limit reviewer mutations to formal review metadata, inline review comments,
  and one mandatory marked PR summary comment.
- Preserve the unconditional no-merge rule for `tticom-automation` and
  `tticom-gov`; require a separate exact current maintainer instruction before
  `tticom-codex` may merge.
- Replace synthetic domain-acceptance language with real-source provenance and
  fixture-independence requirements.

## Historical Audit Compatibility

No historical run record was rewritten. The governance audit now accepts the
existing strict re-approved-head syntax when both values are full SHAs and
accepts either REST numeric review IDs or GitHub `PRR_...` node IDs. Invalid,
short, non-hex, or unstructured metadata remains rejected.

## Validation

- Full AgentOps test suite: PASS (`124 passed`).
- Governance audit: PASS.
- Python compilation of changed scripts: PASS.
- `git diff --check`: PASS.
- Locked revision is contained in `agy-skills/origin/main`: PASS.
- All six installed skill links resolve below the immutable locked checkout:
  PASS.

The control-plane tests use invented GitHub payloads only as non-domain
infrastructure tests. They make no Score2GP recognition, conversion, timing,
geometry, grouping, or musical acceptance claim.

## Stop Condition

Publish one AgentOps PR and stop for independent review. Do not merge it.
