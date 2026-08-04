# Active Task

**Task**: CR-06: Key-Signature Semantics Architecture
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr06-key-signature-semantics-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0030-cr06-key-signature-semantics-architecture.md`

## Context

Developer slice `CR-05A` completed and merged via PR #398 (`0529189e148e68c0adc0fb789d7d334a7322b5a5`). The project now promotes backlog task `CR-06` to determine a generic, testable architecture for key-signature evidence detection on notation staves.

## Goal

Determine a generic, testable architecture in `tticom/score2gp` for key-signature evidence detection on notation staves without defaulting unevidenced staves to recognized C-major / A-minor key signatures. Write the architectural design report at `docs/design/cr06-key-signature-semantics-architecture.md`.

## Allowed Files

- `docs/design/cr06-key-signature-semantics-architecture.md`

## Non-goals

- No product source code modifications in `src/` or `tests/`.
- No modifications to governance files in `score2gp-agentops`.

## Acceptance

Publish one product architecture PR on branch `agy/cr06-key-signature-semantics-architecture` in `tticom/score2gp` containing `docs/design/cr06-key-signature-semantics-architecture.md` for independent Codex review.
