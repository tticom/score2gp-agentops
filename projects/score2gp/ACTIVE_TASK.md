# Active Task: Supervisor Pivot Decision Gate — Tab-Only Timing Policy

## Repository
tticom/score2gp

## Current Governance State
Architect research for tab-only rhythm inference has completed with Outcome C.

Report:
`projects/score2gp/reports/2026-06-24-tab-only-rhythm-inference-viability.md`

## Product Baseline
- Product PR #323 is merged.
- Product baseline: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`
- Baseline capability: tab-only quarter-rest candidate support is wired into `--pdf-only-tab`.

## Outcome C Summary
No credible deterministic or non-ML path is currently viable for precise tab-only rhythm inference from tab-only PDFs where timing evidence is absent or insufficient.

## Supervisor Policy Direction
The selected direction for now is A+B+C:

A. Approximate/default-rhythm output may be allowed for tab-only input where timing evidence is insufficient, provided the output is clearly marked as approximate/defaulted.

B. Strict rejection must be available when the user or caller requires precise timing but the input lacks timing evidence.

C. Precise rhythm conversion requires MusicXML/sidecar, standard notation timing evidence, or explicit rhythm markers.

D. ML-assisted tab rhythm extraction is future/nice-to-have only. It is not active work and is not authorised now.

## Active Blocker
The next blocker is not architecture viability. That has been answered by Outcome C.

The next blocker is defining exact product behaviour and tests for approximate mode, strict mode, and precise mode requirements.

## Next Authorised Task
Supervisor must authorise a bounded Developer requirement before any product implementation.

The next valid task should define:
- user-facing mode behaviour,
- CLI/API flags or existing option behaviour,
- warnings/errors,
- acceptance tests,
- fixture scope,
- non-goals,
- artifact/privacy constraints.

## Developer Implementation Authorised
No.

## Reviewer Architecture Verification Required
Yes.

## Required Reviewer Verdict
stop or pivot / approve Outcome C as evidence-backed / return to Architect if not sufficiently supported.
Supervisor pivot decision remains blocked until Reviewer architecture verification is complete.

## Stop Conditions
Stop any agent that:
- tries to rerun the completed Architect research,
- authorises ML work,
- implements product code without a new Developer requirement,
- claims precise tab-only rhythm inference is solved,
- changes product files from this governance PR.
