# Active Task

**Task**: FS-01: Runtime Provenance Baseline and Corpus Stabilisation Harness
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/fs01-runtime-provenance-baseline`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0036-fs01-runtime-provenance-baseline.md`

## Context

Developer slice `CR-07C` completed and merged via PR #408 (`20ee373e23afce1d97a8a296ceb2a00590dac8c9`). The project now promotes Developer task `FS-01` from the approved queue in `APPROVED_TASK_QUEUE.md` to establish a commandable, private-safe runtime provenance recording baseline and corpus stabilisation harness.

## Goal

Implement `src/score2gp/runtime_provenance.py` and integrate runtime provenance logging into `scripts/private_e2e_smoke.py` and `scripts/private_diagnostic_smoke.py`. Record git SHA, working tree status, executable/import paths, command line invocation, refusal codes, and sanitized structural counts without leaking private corpus data into Git.

## Allowed Files

- `src/score2gp/runtime_provenance.py`
- `scripts/private_e2e_smoke.py`
- `scripts/private_diagnostic_smoke.py`
- `tests/test_runtime_provenance.py`

## Non-goals

- Core OMR conversion changes are deferred until FS-02/FS-04.
- No private corpus fixtures or outputs may enter Git tracking.

## Acceptance

Pass validation commands (`pytest tests/test_runtime_provenance.py` and `python scripts/agent_verify.py`). Publish one Developer pull request on branch `agy/fs01-runtime-provenance-baseline` in `tticom/score2gp` for independent Codex review.
