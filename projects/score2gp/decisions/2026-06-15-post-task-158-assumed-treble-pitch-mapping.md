# Post-Task 158: Record Discovery and Authorise Assumed-Treble Pitch Mapping

## Context
Product Task 158 is complete.

Product Task 158 was discovery-only and produced no product implementation PR.
Discovery revealed that generic pitch inference is unsafe because the read-only recognition/reporting boundary does not expose explicit clef evidence, ledger-line evidence, accidental evidence, or key signature evidence.

## Decisions Recorded
* Generic pitch inference remains explicitly unauthorised.
* Clef evidence is not available in the read-only report boundary.
* Exporter-only `G2` clef output (in `gpif.py`) is not valid recognition evidence.
* Ledger lines, accidentals, and key signatures are not semantically represented.
* Octave/sounding pitch policy is unresolved (e.g., standard Treble vs. Treble 8vb).
* An explicit opt-in assumed-treble mode is authorised *only* as a narrow read-only boundary for generated public fixtures.

## Next Step
Product Task 160 is authorised.

**Product Task 160 must be disabled by default and must not implement generic pitch inference.**
It is restricted to adding an explicit assumed-treble read-only pitch mapping specifically for natural notes within the standard five-line staff.
