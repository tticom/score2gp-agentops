# Raster Diagnostics Summary Merge and Next Boundary

## Verified Prerequisites
- Product PR #237 is merged (`https://github.com/tticom/score2gp/pull/237`), completing Task 57. The final head SHA is `67a54b847cffcf28a46d9800cd014439cce1d07a` and the merge commit is `55e5717d23c547dc0b45ab1b877df58a0b21ce17`.
- Governance PR #110 is merged, establishing the diagnostic consumer contract.

## Purpose
This note records the successful implementation of the read-only raster diagnostics summary helper and defines the next safe reporting/export boundary before any further product work.

## Merge Record
Task 57 introduced `summarize_raster_treble_clef_diagnostics`, which safely consumes the `raster_opening_symbol_classification` field without mutating the product objects, producing semantic inferences, or emitting `ScoreIR`. The implementation handles missing, malformed, or unexpected summary inputs safely, returning `"unknown"` as a first-class result.

## Next Safe Reporting Boundary
The next authorized step must remain a governance boundary definition. Task 59 should define whether and how a CLI, smoke script, JSON report, or governance run record may expose the summary data without committing artifacts, leaking private fixtures, or implying semantic recognition. 

### What remains explicitly unauthorised
The following actions are strictly prohibited in the next or any downstream tasks unless explicitly authorized by a later governance task:
- Emitting `ScoreIR`.
- Creating recognised clef objects.
- Inferring pitch, rhythm, key signature, time signature, notes, rests, voices, or any other musical semantics.
- Deciding that a staff is musically parsed.
- Fusing vector and raster evidence.
- Running or introducing OCR.
- Treating `"treble_clef_candidate"` or the diagnostics summary as a confirmed treble clef or semantic recognition.
- Mutating product models, candidate data, or the extracted summary.

### Evidence and privacy rules
- `"unknown"` must remain a first-class, consumer-visible result.
- Missing, malformed, unexpected, or ambiguous summary inputs must stay safe and non-semantic.
- Existing private fixtures remain intentionally authorised and tracked. Do not relitigate them.
- Do not add new private files, logs, generated PDFs, screenshots, or local artifacts to the repository.

### Known limitations
This summary tool strictly operates on the raw outputs of conservative spatial heuristics. It does not guarantee the existence of semantic clefs, nor does it form a complete recognition model. It is a diagnostic reporting tool intended to surface corpus-wide metadata.

## Candidate Next Tasks
- `Task 59 — Define raster diagnostics summary reporting/export boundary`
- `Task 60 — Implement read-only raster diagnostics summary reporting`

## Recommended Next Task
The explicitly recommended next task is:
**Task 59 — Define raster diagnostics summary reporting/export boundary**

Task 60 is not authorised until Task 59 is merged.

## Stop Conditions
Any implementation task that attempts to consume this diagnostic summary to build a semantic recogniser, emit `ScoreIR`, or prematurely fuse vector/raster evidence must be blocked. Product work must not proceed until the reporting/export boundary is properly defined.
