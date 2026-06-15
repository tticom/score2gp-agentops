# Post-Task 160: Record Assumed-Treble Pitch Mapping and Authorise Ledger-Line Discovery

## Context
Product Task 160 is complete and merged in PR #280 (`67ae5a3c75ba1791b7abd3c68a0f97e7f84e6245`).

Product Task 160 successfully introduced an explicit opt-in `--assume-treble-clef` pitch mapping for read-only note candidates. The mode relies strictly on existing `staff_position_index` without inferring any clef, accidentals, or geometric placement. Positions are bounded to `0..8` (the 5 lines and 4 spaces), meaning it only handles natural notes on the five-line staff.

To support pitch inference for notes outside the staff, we must eventually map ledger lines. However, our discovery in Task 158 indicated that ledger-line primitives are currently omitted from the semantic candidate boundary.

## Decisions Recorded
* Assumed-treble mapping is strictly bounded to the `0..8` staff positions.
* Missing or out-of-bounds `staff_position_index` fails safely.
* Ledger lines remain unmapped and unexposed at the semantic recognition boundary.
* A discovery and design task is required to define a `ledger_line_candidate` output boundary before proceeding with extended pitch mapping.

## Next Step
Product Task 161 is authorised.

**Product Task 161 is discovery and design only.**
It must explore `pdf_raster_staff_diagnostics.py`, determine how ledger-line primitives exist in current unboxed diagnostics, and propose a semantic boundary. It must not implement extraction or update pitch mapping logic.
