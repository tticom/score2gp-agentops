## Current Active Task

## Task 128 — Discover safe next candidate boundary after quarter-note reporting

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 126 successfully exposed `quarter_note_candidates` evidence.

Goal:
Inspect existing diagnostics, models, fixtures, generated public fixtures, and recognition/reporting paths.
Determine the next smallest safe candidate-evidence boundary after quarter-note reporting.
Candidate areas to inspect may include:
- eighth-note-like candidates;
- rest-like candidates;
- stem/beam evidence;
- filled notehead plus beam evidence;
- other primitive-derived candidate boundaries already safely present in diagnostics.
Produce an evidence-based report. Stop and report if safe existing evidence or fixtures do not support a next boundary.

Non-goals:
* Do not implement product code unless safe existing support is explicit and governance later authorises implementation.
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not add rests as product-facing recognition output.
* Do not add eighth-note recognition as product-facing recognition output.
* Do not emit full notation events.
* Do not broaden into full notation recognition.
* Do not change governance records from the product repo.

Next Step:
Execute Product Task 128 discovery in the `score2gp` repository.
