# CR-03D Architect Report: Local tuplet-group evidence and meter resolution

## Active Blocker
The product emits incorrect rhythmic topologies in Lesson-7:
- An opening chord is emitted as an eighth but should be a quarter.
- The following 12 notes are emitted as ordinary eighths but are 3:2 sixteenth-note groups.
- A dotted eighth rest is invented although the source has no rest.
- Pitches are substantially correct while rhythmic topology is wrong.
- Double/final barlines, source line breaks, and phrase headings are missing.

## Scope Separation
This report explicitly separates the CR-03D tuplet and duration resolution logic from other work:
1. **CR-03D (This task)**: Focuses strictly on distinguishing duration variants (ordinary sixteenths, 3:2 sixteenth tuplets, dotted values, genuine rests) and building a fail-closed measure/voice duration ledger.
2. **CR-04A**: False-rest capacity gates and voice balancing are deferred to CR-04A.
3. **CR-05**: Layout parsing (double/final barlines, source line breaks) and title text identification are deferred to CR-05.

## Verified Repository State
- The product extracts `pdf_staff_geometry` and basic note candidates.
- The CR-03C revert restored the integrity of `whole_note_recogniser.py` and diagnostic outputs.
- `src/score2gp/musicxml.py` structures tuplet ratios and duration limits.
- Rhythmic timing mapping currently assumes standard ratios without robust fail-closed association for ambiguous markings (e.g. `3`).

## Research Question
How can the source-to-output chain generically map PDF geometry (specifically the digit `3` and duration dots) to true rhythmic candidate evidence and group them accurately in the timeline, safely distinguishing between tuplets, dotted notes, and ordinary divisions without inventing non-existent rests?

## References Reviewed
- `src/score2gp/musicxml.py`: Validates duration and `MusicXmlTuplet` capacity logic.
- `src/score2gp/build_ir.py`: Timeline event grouping and diagnostics structure.

## Claim-by-Claim Evidence Table

| Claim | Reference | Evidence Type |
|---|---|---|
| Ambiguous text `3` can be a tuplet, fret number, or text | Domain knowledge | Direct |
| 3:2 Tuplets require exactly three sequential rhythmic events in standard notation | Domain knowledge | Direct |
| A tuplet requires local geometric association between the tuplet mark and the note group | Domain knowledge | Direct |
| Emitted events must be provably tracked in a duration ledger to detect invented rests | `src/score2gp/musicxml.py` capacity logic | Direct |

## Options Considered

1. **Global/Heuristic Thresholds**: Count the number of notes in a measure and guess the tuplet ratio.
2. **Strict Local Geometric Association**: Require a standard tuplet lane and an exact X-axis tolerance for the tuplet mark to associate with exactly three contiguous rhythmic events. Build a duration ledger to verify the measure.

## Rejected Options and Reasons
- **Global/Heuristic Thresholds**: Rejected. This was attempted in prototype/CR-03A and caused scope drift and brittle behavior. It invents tuplets and false rests.
- **Fixture-Specific Hardcoding**: Forbids fixture-specific bar numbers, title text, coordinates, or count thresholds. This violates the generalizability requirement of the parser.

## Selected Outcome
**Outcome A — Raster path is viable.** 
The pipeline will be extended to build a measure/voice duration ledger and apply strict local geometric association for tuplet identification.

## Proposed Developer Task (CR-03D Implementation)

### 1. Evidence and Diagnostics
Extend diagnostics to distinguish:
- Ordinary sixteenths
- 3:2 sixteenth tuplets
- Dotted values
- Genuine rests

### 2. Measure/Voice Duration Ledger
Require a duration ledger that proves the math for every emitted event and rest. It must strictly account for the measure's time signature capacity and reject (fail-closed) if the ledger does not balance.

### 3. Public Synthetic Adversarial Tests
Create synthetic extraction fixtures to prove the fail-closed logic. The adversarial tests must contain:
- True 3:2 tuplet `3` marks.
- Adversarial TAB fret `3` digits.
- Measure label `3` headers.
- Unrelated text containing `3` (e.g., metadata `[3:50]`).

### 4. Corpus Probes
Add at least two diverse corpus probes (e.g. Lesson-7 segments) proving the tuplet recognition and duration ledger logic in a real-world context, strictly comparing generated output against source evidence.

## Exact Future Product File Allowlist
The subsequent Developer phase is strictly limited to modifying:
- `src/score2gp/whole_note_recogniser.py`
- `tests/test_tuplet_association.py` (or equivalently named new synthetic tests)

## Measurable Success Criterion
- Public synthetic tests pass, successfully rejecting adversarial `3`s and associating genuine tuplets.
- Corpus probes correctly map durations without inventing false rests.
- Ledger math balances perfectly or fails-closed explicitly.

## Known Risks
- X-axis tolerance for tuplet lane association may be overly strict for poor-quality scans, requiring careful bounding box intersection math.
- The duration ledger may trigger fail-closed behavior on legitimately incomplete measures (e.g., anacrusis/pickup measures) unless explicitly handled.

## What was not verified
- Support for complex nested tuplets or ratios other than 3:2 sixteenth and eighth tuplets.
