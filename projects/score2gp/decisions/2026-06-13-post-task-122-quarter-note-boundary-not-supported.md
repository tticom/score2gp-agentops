# Decision: Product Task 122 Stop and Authorise Filled Notehead Diagnostics

**Date:** 2026-06-13

## Context
Product Task 122 ("Add read-only quarter-note candidate evidence boundary") was authorised by Governance PR #149.

The product agent conducted a discovery step and correctly concluded that the task must stop (Path B — Not supported). No product PR was opened, and no product files were changed.

## Verified Product Evidence
Local source inspection on `main` verified the product agent's report:
- `src/score2gp/pdf_staff_notation_diagnostics.py::_extract_note_candidates()` derives note candidates only inside the `is_hollow = not draw.get("fill")` branch.
- Hollow noteheads without stems are appended as `WholeNoteCandidateDiagnostics`.
- Hollow noteheads with stems are appended as `HalfNoteCandidateDiagnostics`.
- Filled noteheads are currently ignored and not classified into note candidates by this function.
- `src/score2gp/pdf_staff_geometry.py` only defines `WholeNoteCandidateDiagnostics` and `HalfNoteCandidateDiagnostics`.
- The public schema `fixtures/public/pdf_staff_geometry_diagnostics_schema.json` only exposes `whole_note_candidates` and `half_note_candidates`.
- There is no verified `QuarterNoteCandidateDiagnostics` model or `quarter_note_candidates` schema field.

## Decision
The stop for Product Task 122 was correct. Exposing a quarter-note reporting boundary now would require speculative classification logic and unverified fixture updates. 

We must authorise a narrower precursor task to establish safe diagnostic evidence first.

## Authorised Next Task
**Product Task 124 — Add read-only filled/stemmed notehead diagnostic support**

**Scope:**
* Work in `tticom/score2gp`.
* Add the smallest safe diagnostic support for filled/stemmed notehead-like candidates, if existing public/generated fixtures can support it.
* Prefer generated public fixtures if fixture changes are needed.
* Keep the output diagnostic and read-only.
* Add or update schema/model/tests only as needed to expose diagnostic evidence.
* Preserve existing `whole_note_candidate` and `half_note_candidate` outputs.
* Preserve generic `note-candidate-recognition`.
* Preserve compatibility `whole-note-recognition`.
* Stop and report if safe fixtures cannot be created or used without committing inappropriate artifacts.

**Non-goals:**
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR, MusicXML, GP output, OCR, rests, eighth-note recognition, or full notation events.
* Do not broaden into full notation recognition.
