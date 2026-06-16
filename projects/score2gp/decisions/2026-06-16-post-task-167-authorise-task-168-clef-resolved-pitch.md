# Product Task 167 Completion & Task 168 Authorisation

## Product Task 167 Handover Validation

- **Title**: Bridge deterministic raster treble-clef diagnostics into read-only clef candidate evidence
- **Product PR**: [feat(recognition): bridge deterministic raster treble-clef diagnostics #287](https://github.com/tticom/score2gp/pull/287)
- **Reported state**: merged
- **Final head SHA**: `27b37ffa1d440ad8bbaddab2e9253d162c5c5d15`
- **Merge commit**: `5ffbe0cf3627326a22ee0352e36ca99e80dcdb1c`
- **Merged at**: `2026-06-16T09:22:10Z`
- **Changed files**:
  - `src/score2gp/whole_note_recogniser.py`
  - `tests/test_raster_treble_clef_bridge.py`

## Product Task 167 Outcome Summary
- Bridged existing raster-derived treble-clef diagnostic evidence into the deterministic `extract_treble_clef_candidate_evidence(...)` boundary introduced by Product Task 166.
- Extended `extract_treble_clef_candidate_evidence(...)` to accept a `fitz.Page` object and build raster diagnostics through the existing raster diagnostics path.
- Preserved fail-closed behaviour when no page is supplied.
- Preserved fail-closed behaviour when raster diagnostics fail or do not report `status: success`.
- Added `source: raster_diagnostic_candidate_evidence` for bridged raster-derived clef candidates.
- Routed raster-derived candidates through the existing `map_treble_clef_candidates_to_read_only_outcomes(...)` validation boundary.
- Did not use `assume_treble_clef` as visual clef evidence.
- Did not infer clef from pitch outcomes.
- Did not infer clef from note positions.
- Did not infer clef from ledger-line placement.
- Did not implement new visual clef recognition.
- Did not implement pitch inference.

### Deterministic staff association
- The initial staff-index-only association was rejected as unsafe.
- Raster `staff_index` ordering was determined not to map directly to geometry `system_index` and `staff_index`.
- The final bridge un-scales raster `y_coords` and matches them to geometry staff `y0` and `y1`.
- The mapping requires exactly one matching geometry staff within the threshold.
- If zero or multiple geometry staves match, the evidence fails closed.
- If multiple raster candidates map to the same geometry staff, the evidence fails closed.
- The implementation avoids guessing system/staff association.

### Fail-closed raster validation
- `render_scale` must be numeric and greater than zero.
- Raster staff data must be shaped correctly.
- `bbox` must be list/tuple-like with exactly four numeric values.
- Malformed, missing, non-numeric, wrong-length, or uncastable bbox evidence is skipped.
- Non-treble raster classifications are skipped.
- Exceptions during raster diagnostic construction or coordinate conversion fail closed.

## Validation Commands and Results
- Command: `pytest tests/test_raster_treble_clef_bridge.py tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py`
- Result: `53 passed in 18.47s`
- `git diff --check` passed.
- `git ls-files | grep -Ei ...` hygiene check was recorded as safe. No new artifacts added.

## Behaviour Preservation
- Existing note extraction was preserved.
- Existing ledger-line extraction was preserved.
- Existing duplicate beam/ledger suppression was preserved.
- Existing `staff_position_index` behaviour was preserved.
- Existing `attached_ledger_line_candidate_ids` behaviour was preserved.
- Existing `assumed_treble_pitch` behaviour was preserved.
- Existing `map_clef_resolved_staff_pitch(...)` behaviour from Product Task 165 was preserved.
- Existing Product Task 166 clef evidence validation boundary was safely extended.
- Whole-note recognition compatibility was preserved.

## Codex Disposition
No unresolved Product PR #287 Codex comments or review threads were present before merge. Product PR #287 review comments and review threads were checked during supervision and no active threads were present.

## Known Limitations
- Mixed or overlapping systems may cause vertical staff association ambiguity.
- Ambiguous raster-to-geometry association fails closed and drops clef evidence rather than guessing.
- Clef-resolved pitch mapping is still not wired into the main recognition pipeline.

## Privacy/Artifact Hygiene
No private fixtures, diagnostic dumps, scratch JSON, logs, GP files, screenshots, credentials, PDFs, images, or unrelated artifacts were added.

---

## Authorised Next Product Task

**Product Task 168 — Apply clef-resolved staff pitch mapping from deterministic clef evidence**

### Goal
Use deterministic `treble_clef_candidate` evidence to apply read-only `clef_resolved_staff_pitch` mapping to note candidates through `map_clef_resolved_staff_pitch(...)`.

This is a controlled connection task. It must only emit clef-resolved pitch where explicit staff-associated clef evidence is present and unambiguous.

### Functional Requirements
- Verify that deterministic `treble_clef_candidate` outcomes exist only where evidence is explicit and staff-associated.
- Build or reuse a deterministic staff-level clef policy from `treble_clef_candidate` outcomes.
- Apply `map_clef_resolved_staff_pitch(...)` only to notes on staves with exactly one deterministic treble clef candidate.
- Do not apply clef-resolved pitch mapping to a staff with zero clef candidates.
- Do not apply clef-resolved pitch mapping to a staff with multiple clef candidates.
- Do not apply clef-resolved pitch mapping when clef evidence is malformed, ambiguous, unsupported, or missing.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes.
- Do not infer clef from note positions.
- Do not infer clef from ledger-line placement.
- Preserve existing `assumed_treble_pitch` behaviour.
- Do not replace `assumed_treble_pitch`.
- Keep `clef_resolved_staff_pitch` semantically distinct from `assumed_treble_pitch`.
- Use `staff_position_index` as the vertical pitch coordinate.
- Use `attached_ledger_line_candidate_ids` only as supporting evidence for out-of-staff notes, not as an independent pitch source.
- In-staff notes may receive `clef_resolved_staff_pitch` only when staff-level clef evidence is explicit and unambiguous.
- Out-of-staff notes may receive `clef_resolved_staff_pitch` only when staff-level clef evidence is explicit and unambiguous, and required ledger-line support is present.
- Preserve existing note extraction.
- Preserve existing ledger-line extraction.
- Preserve duplicate beam/ledger suppression.
- Preserve existing `staff_position_index`.
- Preserve existing `attached_ledger_line_candidate_ids`.
- Preserve existing `map_treble_clef_candidates_to_read_only_outcomes(...)` fail-closed validation.
- Preserve existing `extract_treble_clef_candidate_evidence(...)` fail-closed validation.
- Preserve whole-note recognition compatibility.

### Non-goals
- Do not implement new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes.
- Do not infer clef from note positions.
- Do not infer clef from ledger-line placement.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not implement OCR.
- Do not implement rests.
- Do not alter existing note-candidate extraction heuristics.
- Do not alter existing ledger-line extraction heuristics.
- Do not alter ledger-line grouping heuristics unless a blocker is reported.
- Do not alter raster clef detection heuristics unless a blocker is reported.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

### Boundary
Product Task 168 may connect deterministic `treble_clef_candidate` evidence to `map_clef_resolved_staff_pitch(...)`, but only where clef evidence is explicit, deterministic, staff-associated, and unambiguous. It must not guess clef context. It must not replace or alter `assumed_treble_pitch`.

**Implementation must wait until this governance PR is merged.**
