# Melodic Soloing Fragmented TAB Staff-Line Grouping v0.1

## Goal
Implement a conservative fragmented horizontal staff-line merging strategy in `src/score2gp/pdf.py` so TAB staff lines broken by fret digits can still form a coherent six-line TAB system, specifically targeting the missing middle system in `private_input_custom_melodic_soloing`.

## Guidelines
- Define constant: `FRAGMENTED_STAFF_LINE_NEIGHBOR_MAX_GAP = 360.0`.
- Preserve existing close-gap merging for gaps <= `max_gap_x` (120.0).
- Add wide-gap merging for gaps > 120.0 and <= 360.0 only when at least two continuous neighboring staff lines span the gap.
- Exclude the current left/right fragments from neighbor count.
- Implement four unit tests (positive wide-gap, negative single-neighbor wide-gap, negative far-neighbor wide-gap, and close-gap regression).
- Ensure no private/generated files are committed.
