# Active Task

**Task**: Req-129 / Task 72: Apply clef-aware pitch mapping to read-only note diagnostics
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must wire the approved clef-aware pitch mapping helper into read-only note-candidate diagnostics, commit focused tests, push the branch, and open a product PR. After the product PR is merged, the Reviewer must complete Task 73 and promote the next credible continuation rather than resetting to `NO_ACTIVE_TASK_APPROVED`.

## 1. Baseline
- Req-127 pitch mapping schema and implementation are complete.
- Product PR #361 added `src/score2gp/pdf_pitch_mapper.py` and focused unit tests.
- Existing read-only recognition code already computes `staff_position_index` and has legacy treble-only `clef_resolved_staff_pitch` enrichment.
- Existing semantic diagnostics expose logical clef candidates with `clef_kind` values for treble, bass, alto, and unknown.

## 2. Context
The project now has a verified pitch mapper, but the read-only diagnostic enrichment path still needs to consume it consistently. This is the smallest safe continuation before any ScoreIR or Guitar Pro mapping is considered.

## 3. Goal
Use `map_staff_step_to_midi_pitch` to enrich eligible read-only note candidates with clef-aware diagnostic pitch information.

The diagnostic enrichment must support:

- treble clef;
- bass clef;
- alto clef;
- ledger-line-supported staff positions already accepted by the current diagnostic path.

The output should remain diagnostic/read-only.

## 4. Non-goals
- Do not create ScoreIR events from standard-staff notes.
- Do not change GP writer output.
- Do not infer rhythm timelines.
- Do not infer voice assignment.
- Do not add accidental/key-signature handling beyond natural-note baseline mapping.
- Do not use MusicXML or GP oracle data to drive PDF pitch diagnostics.
- Do not broaden into final playable conversion.

## 5. Product Scope
Allowed likely files:

- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/pdf_pitch_mapper.py` only if a small helper is needed
- `tests/test_note_candidate_recognition_report.py`
- `tests/test_logical_clef_coverage_proof.py`
- `tests/test_pdf_pitch_mapper.py`
- CLI/report tests only if existing output paths require assertion updates
- no-ScoreIR leakage tests if new diagnostic keys need explicit coverage

Stop before changing:

- `build_ir.py`
- `notation_bridge.py`
- GP writer or GP package code
- MusicXML matching logic
- rhythm/timeline/voice assignment code

## 6. Suggested Product Work Branch
`feature/req-129-read-only-clef-aware-pitch-diagnostics-v0.1`

## 7. Required Validation

Run at minimum:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git diff --check
.venv/bin/python -m pytest -q tests/test_pdf_pitch_mapper.py tests/test_note_candidate_recognition_report.py tests/test_logical_clef_coverage_proof.py tests/test_no_scoreir_leakage_gate.py
.venv/bin/python scripts/artifact_audit.py
```

Run `make verify` if practical before merging.

## 8. Acceptance Criteria
- Read-only note candidates can be enriched using `map_staff_step_to_midi_pitch`.
- Treble, bass, and alto clef evidence are each covered by tests.
- Diagnostic output includes stable pitch evidence, preferably both MIDI pitch and note name if existing output contracts allow it.
- Unknown, missing, or ambiguous clef evidence fails closed without pitch enrichment.
- Ledger-line support remains bounded by existing staff-position/ledger validation rules.
- No ScoreIR, GP writer, MusicXML oracle, rhythm, timeline, or voice behavior changes.
- No-ScoreIR leakage tests pass.
- Artifact audit passes.

## 9. Next Steps
- After this product PR is merged and reviewed, perform the required continuation audit.
- Likely next candidates are accidental/key-signature diagnostic research, notehead-to-clef association hardening, or a real-corpus pitch-diagnostic audit depending on what Task 72 exposes.
