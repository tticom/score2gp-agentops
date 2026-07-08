# Active Task

**Task**: Req-113 / Task 44: Implement logical clef recognition integration
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must integrate the existing `classify_logical_clef_candidate` logic into the `evaluate_logical_clef_gate` function to populate the `clef_kind` field.

## 1. Baseline
- The Architect's proposal for logical clef recognition was merged in PR #349.
- The Reviewer approved the proposal in PR #265.
- We have a functioning `evaluate_logical_clef_gate` that currently returns `clef_kind="unknown"`.
- We have a functioning `classify_logical_clef_candidate` in `logical_clef_candidate_classifier.py` that identifies treble clefs via bounding box proportions.

## 2. Context
We now have approval to bind the geometric classifier to the semantic gate. This will allow the system to definitively extract a Treble Clef from standard standard-staff PDFs, unlocking subsequent pitch inference tasks.

## 3. Goal
Update `evaluate_logical_clef_gate` (or its calling context) to pass `left_margin_primitives` and staff geometry to `classify_logical_clef_candidate`. Map the classifier's output to the `SemanticGateResult`'s `clef_kind` field (`"treble"` or `"unknown"`).

## 4. Non-goals
- Do not add text payload OCR extraction.
- Do not implement Bass Clef heuristics if the public fixtures don't require them to pass.
- Do not infer pitch or duration.

## 5. Required Output & Outcome
A product PR with the integration implemented and tests proving the `dense_margin` fixture (and others with treble clefs) correctly resolve to `clef_kind="treble"`.

## 6. Next Steps
- Promote the next Epic C task (Quarter rest extraction) after merging.
