# REC-10 — Rhythm Evidence

Status: SKELETON — depends on REC-04 and REC-06
Role: Developer
Repository: `score2gp`

## Objective

Produce typed notehead, stem, beam, flag, rest, dot and tuplet hypotheses with
relationships and provenance, without assigning final duration or voice.

## Required work

1. Adapt existing morphology code behind one rhythm-evidence interface.
2. Emit attachment and grouping alternatives rather than finalized events.
3. Combine modalities without erasing disagreement.
4. Preserve missing-object and conflicting-object diagnostics.
5. Exclude measure-capacity repair and equal-spacing duration fabrication.

## Acceptance and falsification

- Stems without supported noteheads do not become accepted notes.
- Beams crossing unrelated staff regions cannot group events.
- TAB-only and paired notation/TAB input classes remain distinguishable.

## Validation

Use provenance-linked real-source cases and the REC-01 rhythm layer; include
known difficult rests, beams and tuplets as negative or ambiguity controls.

