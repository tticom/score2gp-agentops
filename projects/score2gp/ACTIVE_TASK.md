# Active Task

**Task**: CR-06A: Key Signature Evidence Contract & Fallback Removal
**Status**: PROMOTED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr06a-key-signature-evidence-contract`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0031-cr06a-key-signature-evidence-contract.md`

## Context

Architecture task `CR-06` completed and merged via PR #402 (`8bd870e4a7b56f81713c7a3afcb975265acb89b0`). The project now promotes Developer slice `CR-06A` to introduce explicit `logical_key_signature` status handling (`EVIDENCED`, `UNKNOWN`, `AMBIGUOUS`) in `pitch.py` and `cli.py`, removing the hardcoded `"C Major"` default fallback for unevidenced notation staves.

## Goal

Introduce explicit `logical_key_signature` status handling in `src/score2gp/notation_omr/pitch.py` and `src/score2gp/cli.py`. Remove the hardcoded `"C Major"` fallback for unevidenced staves so that unevidenced staves apply 0 key alterations without asserting a recognized C Major key signature in CLI or report metadata.

## Allowed Files

- `src/score2gp/notation_omr/pitch.py`
- `src/score2gp/cli.py`
- `tests/test_cr06_key_signature_semantics.py`

## Non-goals

- Visual accidental glyph extraction near clefs is deferred to follow-up slice CR-06B.
- Multi-staff key signature synchronization across grand staves is deferred.

## Acceptance

Pass validation commands (`pytest tests/test_cr06_key_signature_semantics.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/cr06a-key-signature-evidence-contract` in `tticom/score2gp` for independent Codex review.
