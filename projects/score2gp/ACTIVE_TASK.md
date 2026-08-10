# Active Task

**Task**: Task 95 — Document Topology Module (CRP-07)
**Status**: MERGED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/crp-07-document-topology-module`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0050-document-topology-module.md`

## Context

Task 94 (CRP-06) implemented fret limit merge prevention (> 24) in `src/score2gp/pdf.py` and established `tests/test_tab_digit_recognition.py`.
Task 95 (CRP-07) is the seventh stage of the Conversion Recovery Programme. It establishes page, system, paired-staff, physical bar, and stable global measure identity in `src/score2gp/notation_omr/staff_geometry.py` behind a unified document topology module interface.

## Goal

Implement `tests/test_document_topology.py` and refine `src/score2gp/notation_omr/staff_geometry.py` to organize PDF layout candidates into page, system, paired-staff, physical bar, and global measure structures without cross-system barline snapping or musical timing inference.

## Allowed Files

- `src/score2gp/notation_omr/staff_geometry.py`
- `tests/test_document_topology.py`

## Non-goals

- Do not infer musical timing or duration assignments inside the topology module.
- Do not pass reference `.gp` files to the topology extractor.
- Do not introduce fixture-specific coordinate bounds or hash checks.

## Acceptance

- `pytest tests/test_document_topology.py` passes cleanly and verifies page/system/staff topology extraction on multi-page scores.
- `python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf` preserves system and barline topology.
- `python3 scripts/agent_verify.py` passes with zero regression.
