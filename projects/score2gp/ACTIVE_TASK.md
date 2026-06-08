# Active Task

Status: APPROVED

Current Permission Tier: Tier 2 branch and PR work.

## Title

Document: Standard-Staff Fixture Expansion Plan

## Context

Following the implementation of standard-staff diagnostics (PR #192 primitive clustering, PR #193 left-margin density), we need to expand our fixture set to thoroughly test these new diagnostics. The research content generated previously must be added to the product repository, where architecture and testing plans belong, rather than the governance repository.

## Current Verified State

* Post-merge review for PR #194 is complete.
* The previous governance research PR (#79) is abandoned because product documentation belongs in the product repo.

## Goal

Draft the standard-staff fixture expansion plan in the `score2gp` product repository.

## Non-goals

* Do not modify actual source code in `src/score2gp/`.
* Do not merge PRs.

## Forbidden Actions

* Modifying product implementation code.
* Pushing to `main` directly.

## Allowed Repositories

Governance repo: `/home/tticom/work/score2gp-workspace/score2gp-agentops`
Product repo: `/home/tticom/work/score2gp-workspace/score2gp`

## Allowed Branches

Any task branch prefixed with `docs/`.

## Allowed Files

Governance repo:
* `projects/score2gp/ACTIVE_TASK.md`

Product repo write access:
* `docs/testing/standard-staff-fixtures.md`

## Constraints

* Documentation must be clear and focus on algorithmic generation of synthetic test fixtures without private content.

## Required Pre-flight Checks

* Ensure product repo is up-to-date on `main`.

## Implementation Guidance

* Create `docs/testing/standard-staff-fixtures.md` in the product repo, detailing the JSON schemas and synthetic fixture goals for standard staff tests (e.g. dense accidentals, multiple voices, wide curves).

## Validation

* Confirm the markdown file is well-formatted and located correctly.

## Acceptance Criteria

* A PR is opened in the `score2gp` product repository containing the documentation.

## Stop Conditions

* Blocked on human review.

## Reporting Format

Report product branch name and PR link.
