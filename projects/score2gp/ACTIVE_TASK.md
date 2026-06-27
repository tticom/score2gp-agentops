# Active Task

**Task**: Architect diagnostic task: use the merged read-only StaffPositionDiagnostics capability on committed safe fixtures to determine whether geometric staff-position evidence is sufficient to support the next recognition step, insufficient without additional diagnostics, or not viable. No semantic pitch, clef, rhythm, whole-note recognition, ScoreIR semantic, or GP export implementation is authorised.
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops` / `tticom/score2gp`

## 1. Baseline
- Product PR #330 merged read-only `StaffPositionDiagnostics`.
- Product PR #330 merge commit: `dc511e6f663c08c180e1beae473c5b0d31f31bc4`.
- The merged capability exposes geometric staff-relative vertical positions (`staff_step_index`, `nearest_staff_line_index`, etc.) for notations bounding boxes, with strict safety checks (e.g. exactly 5 lines required, off-grid `OFF_GRID_TOLERANCE` constraints, notehead uncertainty).
- The merged capability is explicitly non-semantic.

## 2. Active Blocker
The previous blocker (absence of a generic, read-only staff-position capability) is closed.
The new blocker is that the project has not yet used this merged diagnostic capability to produce decision-useful evidence about whether these geometric positions are sufficient, insufficient, or too ambiguous to authorise the next concrete note-recognition step.

## 3. Authorised Scope
The Architect is authorised to:
- evaluate the merged `StaffPositionDiagnostics` output on safe committed fixtures;
- write experimental diagnostic scripts or tests to aggregate the evidence;
- map out the exact limitations of the geometric positions;
- determine the next viable recognition step.

The Architect must not:
- implement semantic pitch recognition;
- implement G-clef inference;
- implement rhythm inference;
- implement whole-note recognition;
- change ScoreIR semantics;
- change GP export;
- use private fixtures.

## 4. Required Outcomes
The next task must force one of these outcomes:
- **Outcome A**: `StaffPositionDiagnostics` produces decision-useful geometric evidence sufficient to authorise a narrowly scoped next diagnostic/product step.
- **Outcome B**: `StaffPositionDiagnostics` is useful but insufficient alone; another read-only diagnostic or architecture step is required.
- **Outcome C**: `StaffPositionDiagnostics` does not provide decision-useful evidence for the intended recognition path; stop or pivot before more implementation.

No semantic implementation is authorised until this Architect research explicitly justifies it and a subsequent Reviewer gate authorises it.
