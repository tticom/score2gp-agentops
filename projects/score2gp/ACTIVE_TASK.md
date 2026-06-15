# Active Product Task

## Product Task 162 — Implement read-only ledger-line candidate extraction

### Scope
- Work in `tticom/score2gp`.
- Implement read-only `ledger_line_candidate` extraction from existing diagnostic evidence.
- Use `docs/design/read-only-ledger-line-candidate-boundary.md` as the controlling design.
- Emit `ledger_line_candidate` objects in the read-only recognition/reporting boundary.
- Add or update public generated fixtures only if required and safe.
- Add tests proving ledger-line candidates are emitted.
- Add tests proving a promoted ledger-line primitive is not also emitted as `beam_candidate`.
- Add tests proving eighth-note composition is not changed by ledger-line promotion.
- Preserve existing `staff_position_index`.
- Preserve existing `assumed_treble_pitch` behaviour.
- Preserve existing whole-note compatibility.
- Preserve default CLI/report behaviour except for the newly authorised read-only candidate exposure.

### Non-Goals
- Do not implement pitch inference.
- Do not implement ledger-line pitch mapping.
- Do not alter `staff_position_index` logic.
- Do not alter assumed-treble mapping.
- Do not implement clef recognition.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR, MusicXML, Guitar Pro, GP output, OCR, or rests.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
