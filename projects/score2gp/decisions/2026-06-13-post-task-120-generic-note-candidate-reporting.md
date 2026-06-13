# 2026-06-13: Post Task 120 — Generic Note-Candidate Reporting

## Task 120 Completion Summary

Product Task 120 added a generic read-only note-candidate reporting CLI and script alias to the `score2gp` product repository. 

* **Product PR:** https://github.com/tticom/score2gp/pull/267
* **Final Head SHA:** `4c4d39c2c9b45389d624a69cb9c4a7759cf2807b`
* **Merge Commit SHA:** `15faad90fbab5c6fa0da6033d3d8c9487f1dd331`
* **Changed Files:**
  * `src/score2gp/cli.py`
  * `scripts/note_candidate_recognition_report.py`
  * `tests/test_note_candidate_recognition_cli.py`
  * `tests/test_note_candidate_recognition_report.py`

## User-Visible Capability

* The `whole-note-recognition` CLI command and script remain available as backwards-compatibility aliases.
* The generic `note-candidate-recognition` CLI command and script are now available.
* Current recognition remains read-only candidate evidence only (`whole_note_candidate` and `half_note_candidate`).

## Codex Comment Disposition

* Codex source-checkout script import issue was accepted as a blocker.
* The issue was fixed by prepending `src` to `sys.path` in `scripts/note_candidate_recognition_report.py`.
* The fix commit was `4c4d39c2c9b45389d624a69cb9c4a7759cf2807b`.
* A direct Codex-thread reply was made with disposition and evidence.
* The Codex inline thread was resolved before or at merge.

## Authorisation

**Product Task 122 — Add read-only quarter-note candidate evidence boundary** is now authorised.

The authorised scope is:
* Add or expose a narrow read-only candidate-evidence boundary for quarter-note-like filled noteheads/stemmed candidates only if safe existing diagnostics and fixtures support it.
* Stop and report if safe existing evidence or fixtures do not support it.
* Preserve existing `whole_note_candidate` and `half_note_candidate` outputs.
* Preserve the generic `note-candidate-recognition` path.
* Preserve the compatibility `whole-note-recognition` path.
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR, MusicXML, GP output, OCR, rests, eighth-note recognition, or full notation events.
* Do not broaden recognition beyond candidate evidence.
