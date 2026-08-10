# Active Task

**Task**: Task 97 — Paired-Staff Evidence Fusion (CRP-09)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-09-paired-staff-evidence-fusion`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0052-paired-staff-evidence-fusion.md`

## Context

Task 96 (CRP-08) implemented typed candidate adapters and evidence records (`CandidateAdapter`, `EvidenceRecord`, `SourceModality`) in `src/score2gp/notation_omr/evidence.py`.
Task 97 (CRP-09) is the ninth stage of the Conversion Recovery Programme. It associates notation, TAB, bars, and techniques by document topology (`SystemTopology` / `PairedStaffTopology`) rather than global measure-index coincidence, proving one-to-one ownership or explicit ambiguity across pages and systems without cross-system snapping.

## Goal

Implement `tests/test_paired_staff_evidence_fusion.py` and refine `src/score2gp/notation_omr/evidence.py` and `pipeline.py` to perform topology-bound evidence fusion across notation and TAB staves within system bounds without cross-system snapping.

## Allowed Files

- `src/score2gp/notation_omr/evidence.py`
- `src/score2gp/notation_omr/pipeline.py`
- `tests/test_paired_staff_evidence_fusion.py`

## Non-goals

- Do not snap evidence or candidates across system boundaries.
- Do not pass reference `.gp` files to the evidence fusion pipeline.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_paired_staff_evidence_fusion.py` passes cleanly and verifies paired-staff evidence fusion, system-boundary isolation, and explicit ambiguity tracking.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` preserves topology-bound paired-staff evidence.
- `python3 scripts/agent_verify.py` passes with zero regression.
