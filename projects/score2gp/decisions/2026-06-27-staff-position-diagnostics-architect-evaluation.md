# 2026-06-27 Architect Evaluation: Staff Position Diagnostics Viability

## Baseline Context

- **Product PR**: #330
- **Product Merge Commit**: dc511e6f663c08c180e1beae473c5b0d31f31bc4
- **Governance PR**: #224
- **Governance Merge Commit**: b78c9c306d41ee5b045ae7bb308807be5555a787
- **Capability Evaluated**: `StaffPositionDiagnostics` (Geometric position mapping from bounding boxes)

## Fixture Set Evaluated

The evaluation was performed against committed safe fixtures only:

- `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_half_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_ledger_lines.pdf`: evaluated
- `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`: evaluated

## Diagnostic Metrics

Evaluation of the fixtures yielded the following structured metrics via the read-only extraction path:

- total fixtures evaluated: 5
- total pages evaluated: 5
- total candidate records: 8
- positioned: 0
- ledger_positioned: 2
- ambiguous_notehead_center: 4
- ambiguous_vertical_position: 2
- malformed_candidate_data: 0
- missing_staff_geometry: 0
- missing_staff_lines: 0
- off_grid_candidate_center: 6

### Fixture-level Observations

- `generated_standard_staff_quarter_note.pdf`: 2 `quarter_note` candidates (both `ambiguous_notehead_center`)
- `generated_standard_staff_half_note.pdf`: 2 `half_note` candidates (both `ambiguous_notehead_center`)
- `generated_standard_staff_whole_note.pdf`: 2 `whole_note` candidates (both `ambiguous_vertical_position`)
- `generated_standard_staff_ledger_lines.pdf`: 2 `quarter_note` candidates (both `ledger_positioned`)
- `generated_standard_staff_multi_staff.pdf`: 0 candidates

## Analysis

### Facts

- Zero candidates on the staff successfully mapped to an unambiguous `positioned` status.
- All quarter and half notes mapped to `ambiguous_notehead_center`.
- All whole notes mapped to `ambiguous_vertical_position` (and triggered `off_grid_candidate_center`).
- The diagnostic safely propagates `ambiguous_notehead_center` and `ambiguous_vertical_position` rather than overclaiming geometric certainty.
- The diagnostic successfully ran without crashes on the committed safe fixture set.

### Inferences

- The geometric center of a full note bounding box is structurally unreliable for determining vertical pitch placement, especially for notes with stems (quarter and half notes), because the stem skews the `center_y` off the notehead.
- Even for whole notes (which lack stems), the bounding box center failed to snap to the `0.25` grid tolerance. This implies that glyph padding, aspect ratios, or rendering artifacts naturally offset the center beyond our rigid geometric grid constraints.
- The `StaffPositionDiagnostics` capability operates exactly as intended by identifying and isolating this geometric ambiguity, proving that raw bounding box position is insufficient for semantic pitch mapping without further refinement.

### Hypotheses

- To resolve `ambiguous_notehead_center`, a subsequent diagnostic or architecture phase must introduce morphology analysis (e.g., separating the notehead from the stem within the bounding box) to calculate a true notehead center.
- To resolve `ambiguous_vertical_position` for whole notes, the grid tolerance might need re-evaluation or morphology analysis must identify the optical center of the notehead.

### Unknowns

- Whether morphology analysis alone will be sufficient to resolve all vertical position ambiguities across all clefs and notation styles.
- How complex the morphology extraction will be for beamed notes or chords.

## Architect Outcome

**Outcome B — Useful but insufficient alone**

## Outcome Justification

The `StaffPositionDiagnostics` capability provides highly useful and stable evidence by successfully bounding and categorising geometric ambiguity (e.g., distinguishing stem-induced ambiguity from off-grid ambiguity). It correctly prevents false semantic overclaims. However, the 0% `positioned` success rate on basic standard staff fixtures proves that raw bounding box center geometry is strictly insufficient to authorise semantic pitch inference. We cannot map these candidates to logical pitches until we can resolve the notehead center ambiguity.

## Next Recommended Task

**Task**: Perform an Architect diagnostic phase to evaluate optical/morphological notehead center extraction for candidates flagged as `ambiguous_notehead_center` or `ambiguous_vertical_position`.

## Stop / Pivot Conditions

- Stop if morphology extraction requires complex, unbound CV/ML approaches that violate the deterministic geometric pipeline.
- Pivot if bounding boxes provided by the upstream bucket diagnostics do not tightly contain the notehead.

## Explicitly Still Blocked

- semantic pitch implementation: yes
- G-clef inference implementation: yes
- rhythm implementation: yes
- whole-note recognition implementation: yes
- ScoreIR semantic changes: yes
- GP export changes: yes
