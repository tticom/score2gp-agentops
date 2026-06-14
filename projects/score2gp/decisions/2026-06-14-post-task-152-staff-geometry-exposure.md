# 2026-06-14: Post-Task 152 — Staff Geometry Exposure

## Context
Product Task 152 has been completed. It was a discovery-only task and produced no product implementation PR.

The discovery concluded that semantic pitch inference is not yet safe to implement because the project lacks explicit clef recognition, ledger-line handling, accidental handling, and sufficient semantic fixture evidence. Specifically:
- Semantic pitch inference remains blocked.
- Clefs are not geometrically detected; treble clef is currently implicit only.
- Ledger lines are not represented.
- Accidentals are not represented.

However, a smaller, safer prerequisite was discovered:
- Staff-line y coordinates (`NotationStaffGeometry.line_y_coords`) and staff spacing (`staff_space`) exist internally but are not exposed at the read-only recognition report boundary.
- Note candidates already possess `page_index`, `system_index`, and `staff_index` join keys, but downstream read-only consumers currently cannot join note candidates back to staff-line y positions because the geometry block is discarded.

## Decision
Exposing staff geometry is the smallest safe prerequisite before any staff-position mapping can occur.

Therefore, we authorise **Product Task 154 — Expose staff geometry in read-only recognition report payload**.

**Constraints**: Product Task 154 must NOT implement pitch inference or staff-position inference. It is strictly limited to exposing the internal staff geometry alongside the existing candidate reports.
