# Active Task

**Task**: Task 88 — Conversion Recovery Evidence Adjudication & Architecture Review
**Status**: ACTIVE
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/conversion-recovery-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0043-conversion-recovery-architecture-review.md`

## Context

The source reports conflict, three competing product PRs remain open, and the
existing M6 implementation prompts assume unverified constants and counts.
Before product behaviour changes, perform the full evidence adjudication,
architecture review, sidecar decision, and real-source testing design required
by the conversion-recovery programme.

## Goal

Produce an evidence-backed target architecture and migration decision that
preserves verified working behaviour, replaces destructive paths, defines
real-source-only acceptance, and completes the first unblocked downstream
prompt.

## Allowed Files

- docs/design/2026-08-09-conversion-recovery-architecture.md
- docs/design/2026-08-09-real-source-testing-architecture.md
- docs/design/2026-08-09-conversion-module-migration-map.md

## Non-goals

- Do not modify product source, tests, fixtures, dependencies, schemas, or workflows.
- Do not merge, close, or rewrite open investigation PRs.
- Do not promote downstream implementation from an unresolved report claim.

## Acceptance

- Material report contradictions and open PR hunks are dispositioned at exact revisions.
- Current and target module seams, interfaces, invariants, and migration order are explicit.
- Sidecar generation receives an A, B, or C decision using Lesson 6 4/4 triplets as a mandatory discriminator.
- Real-source test architecture isolates generation from reference GP data and does not accept skipped private tests as evidence.
- A preserve, wrap, replace, and delete matrix and dependency graph are complete.
- The migration map contains an implementation-ready specification for the
  first downstream prompt; publishing that prompt requires a separate
  AgentOps governance promotion. Dependent prompts remain skeletons.
