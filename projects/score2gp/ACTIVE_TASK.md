## Current Active Task

## Product Task 148 — Implement read-only eighth-note candidate boundary composition

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 145 successfully added generated public fixture evidence (`generated_standard_staff_eighth_notes.pdf`) that emits `quarter_note_candidate`, `flag_candidate`, and `beam_candidate` evidence, all perfectly joined with explicit bounds (`page_index`, `system_index`, `staff_index`, `bbox`). This evidence enables safe boundary composition for eighth notes without altering extraction heuristics.

Goal:
Implement a conservative generic `eighth_note_candidate` composition boundary from existing `quarter_note_candidate` plus nearby `flag_candidate` or `beam_candidate` evidence.

Scope:
- Work in `tticom/score2gp`.
- Use only existing generic candidate outputs and evidence fields.
- Compose `eighth_note_candidate` from:
  - `quarter_note_candidate` + `flag_candidate`, or
  - `quarter_note_candidate` + `beam_candidate`.
- Require exact match on:
  - `page_index`
  - `system_index`
  - `staff_index`
- Require conservative bbox relationship:
  - overlap, touch, or tightly bounded local proximity;
  - avoid staff-space margins unless the value is available at the composition boundary and explicitly justified.
- Use `generated_standard_staff_eighth_notes.pdf` and `generated_standard_staff_eighth_notes.json` to prove the boundary.
- Include source component references in the emitted candidate, such as source candidate ids or component bboxes, if those fields already exist or can be added without changing extraction heuristics.
- Preserve all existing generic outputs:
  - `whole_note_candidate`
  - `half_note_candidate`
  - `quarter_note_candidate`
  - `x_aligned_cluster_candidate`
  - `left_margin_candidate`
  - `flag_candidate`
  - `beam_candidate`
- Preserve backward compatibility for `whole-note-recognition`.
- Add focused tests for:
  - flagged eighth-note composition;
  - beamed eighth-note composition;
  - no composition across different staff/system/page;
  - no composition where bbox relationship is absent or too loose.

Non-goals:
- Do not infer pitch.
- Do not infer playable rhythm or duration.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not add OCR.
- Do not implement rests.
- Do not implement full notation recognition.
- Do not alter existing extraction heuristics.
- Do not change staff association heuristics.
- Do not commit private PDFs, generated scratch dumps, screenshots, logs, credentials, or unrelated artifacts.

Next Step:
Execute Product Task 148 in the `score2gp` repository.
