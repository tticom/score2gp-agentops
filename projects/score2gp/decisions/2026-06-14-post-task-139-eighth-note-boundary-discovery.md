# Decision: Post Task 139 Eighth-Note Boundary Discovery

## Product Task 139 Discovery Summary
Product Task 139 was a discovery-only task in `tticom/score2gp` aimed at investigating whether a safe, conservative `eighth_note_candidate` composition boundary could be defined from existing generic read-only candidate evidence (quarter notes, flags, beams). 

**Conclusion:** `eighth_note_candidate` reporting is **not yet safe** to implement.
**Code changes:** Explicitly, no product code was changed by Product Task 139.

## Discovery Evidence
* **Missing Note Candidate Staff Identity:** Whole, half, and quarter generic note candidate outputs currently lack `system_index` and `staff_index`. `shape_candidate_evidence` only emits `candidate_id`, `page_index`, and `bbox`, and the mapping functions corresponding to these candidates drop or do not propagate staff identities.
* **Flag/Beam Staff Identity:** In contrast, flag and beam candidates now carry full staff identity (`page_index`, `system_index`, `staff_index`).
* **Join Safety Unattainable:** A staff-local join rule to associate notehead/stems with flags/beams is unsafe and impossible to perform conservatively until note candidates consistently preserve their staff identity.
* **Fixture Evidence:** No existing public fixture currently produces both quarter-like notehead/stem evidence and flag/beam evidence in a way that can be used to reliably test a conservative composition rule. 

## Product Task 141 Authorisation Summary
**Authorised Task:** `Product Task 141 — Add staff identity to generic note candidate evidence`

**Scope Summary:**
* Work in `tticom/score2gp`.
* Ensure `whole_note_candidate`, `half_note_candidate`, and `quarter_note_candidate` generic outputs include `page_index`, `system_index`, `staff_index`, and `bbox`.
* Prefer using existing diagnostic extraction to propagate this identity safely.
* Include minimal public eighth-note fixture work strictly to support future composition-boundary testing, avoiding fixture churn.
* Add regression tests ensuring that `system_index` and `staff_index` are populated.
* Preserve all existing generic candidate reporting elements, compatibilities (`score2gp whole-note-recognition`), and `scripts/note_candidate_recognition_report.py`.

**Non-Goals:**
* Do not implement `eighth_note_candidate` reporting.
* Do not implement eighth-note recognition, rests, pitch inference, staff position inference, rhythm, ScoreIR, MusicXML, GP output, or OCR.
* Do not alter flag/beam diagnostic heuristics.

## Known Limitations
* `eighth_note_candidate` reporting is explicitly not yet implemented and remains unauthorised until note candidate staff identity is fully propagated.
* All broader musical logic (pitch, rhythm, duration, semantics) remains unimplemented.
