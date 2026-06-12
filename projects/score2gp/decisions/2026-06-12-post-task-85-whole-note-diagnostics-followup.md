# Post-Task 85: Record Whole-Note Diagnostics and Authorise Integration Follow-up

## 1. Product Task 85 Completion

Product Task 85 is fully complete via PR #249 in `tticom/score2gp`.

The implementation delivered read-only whole-note candidate diagnostics, establishing positive whole-note coverage, negative noise coverage, and half-note negative coverage. The work successfully proved the extraction of `whole_note_candidate` properties exclusively through geometric constraints without emitting ScoreIR or GP structures.

## 2. Whole-Note versus Half-Note Diagnostic Boundary

The task formalized a substantive distinction between whole notes and half notes:
* **Whole note**: A hollow oval without an attached or closely adjacent vertical stem.
* **Half note**: A hollow oval with an attached or closely adjacent vertical stem.

This distinction is now a required diagnostic boundary. Any whole-note candidate diagnostics must explicitly detect and exclude hollow ovals with nearby or attached stems to avoid inflated candidate counts.

## 3. Codex Review Process Correction

During Task 85, a Codex review comment accurately identified the stem-exclusion flaw before merge. Codex comments are vital review evidence. From this point forward:
* Reviewers must explicitly inspect and disposition all Codex comments and review threads.
* Every review must include a "Codex comment disposition" section.
* The disposition must list each comment, state whether it is accepted as a blocker, accepted as non-blocking, already fixed, or rejected, alongside a brief reason.
* Plausible correctness bugs identified by Codex must be paired with regression tests unless a clear reason exists to ignore them.

## 4. Product Task 87 Authorisation

With standalone whole-note diagnostics operating successfully, the next visible product step is to integrate these capabilities.

Product Task 87 is hereby authorised.

### Task 87 Mandate:
* Integrate whole-note candidate diagnostics into an existing diagnostics structure, command, or report surface.
* Ensure a normal diagnostic run can show whole-note candidate counts and/or locations.
* Preserve the standalone script if useful, but avoid making it the only visible route.
* Maintain the half-note exclusion logic.
* Include comprehensive regression testing for:
  - Positive whole-note candidate detection.
  - Negative noise/non-note case.
  - Half-note hollow-oval-with-stem case.
  - No ScoreIR or GP output.
  - No pitch or rhythm inference beyond diagnostic labels.

### Strict Non-Goals:
* Do not emit ScoreIR or GP files.
* Do not claim full semantic note recognition.
* Do not infer pitch or duration beyond the `whole_note_candidate` label.
* Do not infer voices, measures, key signatures, time signatures, rests, or full notation.
* Do not use OCR.
* Do not require private fixtures or commit generated raw JSON, PDFs, or scratch artifacts.
* Do not regress existing treble-clef/raster diagnostics behaviour.
* Do not modify governance records during product implementation.
