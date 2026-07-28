# Active Task

**Task**: PDFTAB-DUR-04: PDF-Tab Duration Types & Spatial Associator Primitive
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Primitive Author
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-associator-primitive`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0021-pdf-tab-duration-associator-primitive.md`

## Context

Architecture PR #392 merged at `44ab38ca0ad8e0460469360f7ab3e9db29f98aa8`, publishing the durable specification at `docs/design/pdf-tab-duration-candidate-extraction.md`. This task implements Slice 1 (Duration Types & Spatial Associator Primitive) as defined in Section 7 of the architecture document, treating proposed tolerance constants as provisional hypotheses to be empirically validated against test bounds.

## Goal

Create `src/score2gp/pdf_tab_duration_types.py` and `src/score2gp/pdf_tab_duration_associator.py` in `tticom/score2gp`.
Implement data structure `TabDurationEvidence` and spatial association functions matching `docs/design/pdf-tab-duration-candidate-extraction.md`.
Acknowledge that proposed tolerance constants ($\Delta x_{\text{stem\_tol}} \le \max(6.0\text{ pt}, 0.6 \times \text{staff\_space})$, $\epsilon = 4.0\text{ pt}$, $r \le 8.0\text{ pt}$) are provisional hypotheses until validated.
Implement comprehensive unit tests in `tests/test_pdf_tab_duration_associator.py` covering:
- Measured coordinates and margins from public fixture `generated_pdf_tab_duration.pdf`;
- Positive and negative association cases;
- Just-inside and just-outside boundary tests for all tolerances;
- Barline and staff-line stroke rejection;
- Neighbouring-event and ambiguous-candidate tests;
- At least one scaled synthetic geometry test case;
- Fail-closed behavior when candidate association is ambiguous.

## Allowed Files

- `src/score2gp/pdf_tab_duration_types.py` (in `score2gp`)
- `src/score2gp/pdf_tab_duration_associator.py` (in `score2gp`)
- `tests/test_pdf_tab_duration_associator.py` (in `score2gp`)

## Non-goals

No edits to existing assemblers (`pdf_tab_bar_assembler.py`), TabRaw models (`tabraw.py`), private inputs, reference GP leakage, automatic merge, branch deletion, or premature assembly pipeline wiring.

## Acceptance

`pdf_tab_duration_types.py` and `pdf_tab_duration_associator.py` are implemented in `score2gp`. Unit tests in `tests/test_pdf_tab_duration_associator.py` pass 100%, covering boundary, rejection, ambiguity, and scaled geometry tests. `agent_verify.py` passes all unit tests and checks cleanly, product PR is opened, and handback comment is published.
