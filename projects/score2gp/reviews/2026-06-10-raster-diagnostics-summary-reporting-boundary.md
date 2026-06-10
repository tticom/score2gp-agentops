# Raster Diagnostics Summary Reporting Boundary

## Verified Prerequisites
- Governance PR #111 is merged, establishing the requirement to define this reporting/export boundary before product implementation.

## Purpose
This note defines the consumer contract for exporting or reporting the raster diagnostics summary. It establishes how a downstream product task may expose the summary data without committing artifacts, leaking private fixtures, or implying semantic recognition.

## Allowed Reporting Mechanisms
A later implementation task is authorised to report the summary data using **only** the following mechanisms:
- Standard output (stdout) or standard error (stderr) logging during script execution.
- Appending to a locally generated, git-ignored diagnostic JSON report (e.g., in an `output/`, `scratch/`, or `.tmp/` directory).
- Returning the summary dictionary from a CLI entrypoint or smoke script.

## Disallowed Reporting Mechanisms
The implementation **must not**:
- Commit generated JSON reports, logs, or other artifacts to the repository.
- Emit `ScoreIR` or include the summary data inside `ScoreIR` payloads.
- Leak paths or content of private fixtures into committed files or public test output.
- Generate and commit rendered PDFs, PNGs, or GP files.
- Persist the summary data into any tracked product model or database beyond the ephemeral script execution.

## Allowed Interpretations in Reports
- The report may display the raw `kind`, `status`, `page_index`, `staff_count`, `label_counts`, and `staffs` lists.
- The report may format these counts for human readability (e.g., "Found 5 treble_clef_candidate and 2 unknown").

## Disallowed Interpretations in Reports
- The report **must not** label the candidates as confirmed notation (e.g., "Found 5 treble clefs").
- The report **must not** infer or display pitch, rhythm, key signature, or time signature based on the candidates.
- The report **must not** attempt to fuse this raster data with vector data.
- The report **must not** attempt to run OCR to supplement the summary.

## Stop Conditions
Any implementation task that attempts to use the summary for semantic inference, emit ScoreIR, or violate the artifact and privacy rules must be blocked.

## Candidate Next Tasks
- `Task 60 — Implement read-only raster diagnostics summary reporting`

## Recommended Next Task
The explicitly recommended next task is:
**Task 60 — Implement read-only raster diagnostics summary reporting**
