# Decision: Authorise Product Task 156 (Staff-Position Inference)

## Context
Product Task 154 has been completed in the `tticom/score2gp` product repository.
Product PR #278 (`feat(recognition): expose staff geometry in read-only report`) was merged successfully.

* Final head SHA: `2be455b4d302b1c08c24168d4c05e88299ba0c48`
* Merge commit: `a1b7385271c6bb3f82b22c1a7f4ed174e2efc2b0`

**What Product Task 154 accomplished:**
* Exposed `staff_geometry` as a top-level array in the read-only recognition report payload.
* Preserved existing `read_only_recognition_outcomes`.
* Included `page_index`, `system_index`, `staff_index`, `bbox`, and `line_y_coords` in the staff geometry.
* Note candidates can now be successfully joined to staff geometry by `page_index`, `system_index`, and `staff_index`.
* Omitted `staff_space` because it was not available without changing extraction heuristics.
* Pitch inference was not implemented.
* Added necessary test coverage and preserved whole-note recognition compatibility.

**Remaining Limitations:**
* Pitch inference is still not authorised.
* Clef recognition, ledger-line handling, accidental handling, rhythm, ScoreIR, MusicXML, and Guitar Pro output remain out of scope.
* `staff_space` remains unavailable at the report boundary.

## Decision
Record Product Task 154 as complete and authorise Product Task 156.

Product Task 156 is authorised as a narrow read-only staff-position inference task. 
**Explicit constraint:** Product Task 156 must NOT infer pitch names.
