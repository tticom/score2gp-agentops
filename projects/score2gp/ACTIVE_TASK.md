# Active Task

Status: PR_OPEN

Current Permission Tier: Tier 2 branch and PR work.

## Title

Research: Public Fixture Expansion for Standard-Staff Diagnostics

## Context

Following the implementation of standard-staff diagnostics (PR #192 primitive clustering, PR #193 left-margin density), we need to expand our fixture set to thoroughly test these new diagnostics. The expansion must cover diverse standard-staff geometries (like large clusters, ties, accidentals, varying margin densities) without violating the strict rule against using real copyrighted PDF files (privacy boundary). 

## Current Verified State

* Product PR #194 was merged and the post-merge review is complete.
* Current fixtures heavily focus on tablature or paired-staff.
* We rely on python scripts (`fitz`) to generate synthetic PDFs from JSON to ensure zero copyright/privacy risk.

## Goal

Produce a research report analyzing how we can expand synthetic fixtures for born-digital standard-staff diagnostics.
Identify missing geometric patterns that need testing.
Propose specific JSON structures and generative python script additions to achieve this.

## Non-goals

* Do not modify product code in `src/score2gp/`.
* Do not attempt to parse real copyrighted PDFs.
* Do not merge any PRs.

## Forbidden Actions

* Modifying product implementation code.
* Pushing to `main` directly.
* Breaking the semantic firewall (do not introduce pitch/duration parsing).

## Allowed Repositories

Governance repo: `/home/tticom/work/score2gp-workspace/score2gp-agentops`
Product repo: `/home/tticom/work/score2gp-workspace/score2gp`

## Allowed Branches

Any task branch prefixed with `research/`.

## Allowed Files

Governance repo:
* A new research report in `projects/score2gp/research/`.
* `ACTIVE_TASK.md`
* `TASKS.md` (to update status if needed)

Product repo:
* Inspecting `tests/fixtures/pdf/`

## Constraints

* Fixtures must be entirely synthetic and algorithmically generated.
* No private or copyrighted PDFs may be used.

## Required Pre-flight Checks

* Ensure governance and product repos are on `main` and up-to-date.

## Implementation Guidance

* Analyze the current `make_*_pdfs.py` scripts.
* Propose a new script `make_standard_staff_diagnostics_pdfs.py` or similar in the research document.
* Document the JSON schema needed for simulating left margin elements and primitive clusters.

## Validation

* The research report accurately identifies missing fixture capabilities and provides a concrete plan to implement them.

## Acceptance Criteria

* A research report is created and pushed as a PR in the governance repo.

## Stop Conditions

* Blocked on needing human review or architectural decision on fixture strategy.

## Reporting Format

Report branch name, PR link, and summary of the research findings.
