# Active Task

**Task**: Task 101 — Conversion Recovery Evidence Adjudication and Architecture Review
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect and Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/conversion-recovery-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0043-conversion-recovery-architecture-review.md`

## Context

The master diagnosis concludes that Score2GP can either refuse real inputs or write musically corrupt output while a large synthetic test suite remains green. Several source reports conflict, and six related PRs are still open. Product main is not identical to any proposed workaround branch.

## Goal

Produce a full, evidence-backed recovery architecture and migration decision that adjudicates every material contradiction, traces the current call graph, defines deep target modules, identifies preservation and research needs, defines a real-source-only testing architecture, and selects bounded downstream research and implementation slices.

## Allowed Files

- `docs/design/2026-08-09-conversion-recovery-architecture.md`
- `docs/design/2026-08-09-real-source-testing-architecture.md`
- `docs/design/2026-08-09-conversion-module-migration-map.md`

## Non-goals

- No source, test, fixture, dependency, workflow, schema, or generated artifact may be changed.

## Acceptance

- Every non-obvious claim has exact repository or primary-source support.
- Every material report contradiction is resolved or explicitly blocks a task.
- The migration map contains an implementation-ready first-prompt specification.
- Product verification and artifact audit pass with docs-only changes.
