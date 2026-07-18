# CR-03D Architect Report: Local tuplet-group evidence and meter resolution (Rework)

## Active Blocker
The product emits incorrect rhythmic topologies in Lesson-7:
- An opening chord is emitted as an eighth but should be a quarter.
- The following 12 notes are emitted as ordinary eighths but are 3:2 sixteenth-note groups.
- A dotted eighth rest is invented although the source has no rest.
- Pitches are substantially correct while rhythmic topology is wrong.
- Double/final barlines, source line breaks, and phrase headings are missing.

## Scope Separation
This report separates the initial candidate classification from downstream time signature balancing and document layout logic:
1. **CR-03D (This task)**: Strict classification of local rhythmic candidate evidence (distinguishing genuine 3:2 tuplet marks, true duration dots, and genuine rest symbols from adversarial text), and building the crucial hand-off into the ScoreIR timeline.
2. **CR-04A**: The false-rest rejection and measure/voice duration ledger proving every emitted event balances the time signature.
3. **CR-05**: Layout parsing (double/final barlines, source line breaks) and title text identification.

## Verified Repository State
- The product extracts basic geometry in `pdf_geometry.py`.
- The CR-03C revert restored the codebase to revision `64579b3ce86fdb7af44c885567a61797bb649158` where the OMR-derived timeline explicitly captures baseline tests before we augment it with PDF tuplet diagnostics. This is proven by 923 passing tests on `main`.
- Rhythmic timing mapping currently assumes standard ratios without robust fail-closed association for ambiguous markings like `3` or dots.

## Exact Current Source-to-Output Chain
The current code exposes a disconnect between read-only diagnostics and the actual production timeline:
1. **Isolated Diagnostic Layer**: `src/score2gp/whole_note_recogniser.py` and `src/score2gp/notation_bridge.py`. These modules are exclusively used by read-only `cli.py` diagnostic commands. They currently do not flow into the main IR pipeline.
2. **OMR Event Generation**: The real pipeline relies on an external OMR engine (e.g., Audiveris) to extract and recognize standard notation, which is exported as an intermediate MusicXML file.
3. **MusicXML Parsing & Rest Origin**: `src/score2gp/musicxml.py` parses the OMR-generated MusicXML. False "ghost" rests originate strictly from the external OMR engine, which fabricates `<rest/>` elements in an attempt to mathematically balance measure timing when it fails to recognize tuplets. `musicxml.py` merely parses these and reports overlap diagnostics.
4. **IR Building & Emission**: `src/score2gp/build_ir.py` ingests the MusicXML structures and builds the `ScoreIR`, passing it unaltered into the final format via `gpif.py`.

## Research Question
How can we bridge the isolated read-only PDF diagnostics (`whole_note_recogniser.py`) into the actual `build_ir.py` pipeline, specifically injecting precise tuplet and duration dot evidence to override or reconcile the flawed timing and fabricated ghost rests produced by the external OMR engine?

## References Reviewed
- `src/score2gp/whole_note_recogniser.py`: Shape and text bounding box logic (Currently Diagnostic-only).
- `src/score2gp/build_ir.py`: Timeline builder from MusicXML structure.
- `src/score2gp/musicxml.py`: Ingestion of OMR-generated nodes (including fabricated ghost rests).

## Claim-by-Claim Evidence Table

| Claim | Reference | Evidence Type |
|---|---|---|
| Ambiguous text `3` can be a tuplet, fret number, or text | Domain knowledge | Direct |
| 3:2 Tuplets require exactly three sequential rhythmic events | Domain knowledge | Direct |
| Ghost rests are invented by external OMR, not by our pipeline | Codebase (`musicxml.py`) | Direct |
| Diagnostic evidence currently has no hand-off to the IR | Codebase (`build_ir.py`) | Direct |

## Options Considered

1. **Global/Heuristic Thresholds**: Guess tuplet and dot presence based on measure note count.
2. **Strict Local Geometric Association (End-to-End)**: Implement tuplet and dot identification in the diagnostic layer, pass that data through `build_ir.py`, and map it correctly in `musicxml.py`.

## Rejected Options and Reasons
- **Global/Heuristic Thresholds**: Rejected. This was attempted in prototype/CR-03A and caused scope drift. It invents tuplets and false rests.
- **Fixture-Specific Hardcoding**: Forbids fixture-specific bar numbers, title text, coordinates, or count thresholds. This violates generalizability.

## Selected Outcome
**Outcome B — Raster path is not viable but another approach is.**
The pure raster path is currently unproven for this task. Instead, the approach is strict bounding-box geometric candidate association mapping (from PDF vector geometry) that explicitly builds a hand-off from `whole_note_recogniser.py` into the core pipeline.

## Proposed Developer Task (CR-03D Implementation)

### 1. Evidence and Diagnostics
Extend candidate extraction to distinguish local rhythmic indicators safely:
- Ordinary sixteenths
- 3:2 sixteenth tuplets (by pairing `3` text bounds closely with note clusters)
- Dotted values (by isolating genuine duration dot bounds)
- Genuine rests (vs empty space)

### 2. Pipeline Hand-off Architecture
Design and implement the data hand-off bridging the read-only tuplet/dot diagnostics from `whole_note_recogniser.py` into the core pipeline (e.g., intercepting `build_ir.py` or modifying the ScoreIR builder directly) to explicitly override or reconcile the flawed OMR timing.

### 3. Public Synthetic Adversarial Tests
Create synthetic extraction fixtures to prove the fail-closed logic. The adversarial tests must contain:
- True 3:2 tuplet `3` marks.
- Adversarial TAB fret `3` digits.
- Measure label `3` headers.
- Unrelated text containing `3` (e.g., metadata `[3:50]`).

### 4. Corpus Probes
Two diverse corpus probes must be specified for validation:
- **Probe 1**: Input class: Dense 3:2 sixteenth-note sections. Command: `python -m pytest tests/test_corpus_dense_tuplet_probe.py`. Evidence Fields: `diagnostic_rhythm_candidates`. Pass/Fail rule: Must exactly associate all genuine 3:2 sixteenth-note tuplets in the target corpus without false positives, and never assign tuplets to unrelated rhythmic groups. No private artifacts are written to disk.
- **Probe 2**: Input class: Tablature text elements. Command: `python -m pytest tests/test_corpus_lesson_5_probe.py`. Evidence Fields: `diagnostic_fret_candidates`. Pass/Fail rule: Tablature fret `3` marks must never be extracted or grouped as a rhythmic tuplet candidate. No private artifacts are written to disk.

## Exact Future Product File Allowlist
To accomplish the end-to-end chain required for these acceptance criteria, the file allowlist is expanded to every required code owner:
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/notation_bridge.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/musicxml.py`
- New synthetic and corpus public tests (e.g., `tests/test_tuplet_association.py`, `tests/test_corpus_dense_tuplet_probe.py`, `tests/test_corpus_lesson_5_probe.py`)

## Measurable Success Criterion
- Public synthetic tests pass, successfully rejecting adversarial `3`s and associating genuine tuplets.
- The 2 corpus probes yield exact tuplet evidence in their outputs without regression on the existing 923 tests.
- A functional hand-off bridge is implemented integrating diagnostic evidence into `build_ir.py`.

## Known Risks
- X-axis tolerance for tuplet lane association may be overly strict, requiring careful bounding box intersection math.
- Differentiating a duration dot from an articulation dot may require additional rules.
- Resolving timeline conflicts between OMR MusicXML elements and PDF geometry candidates could require robust merging logic.

## What was not verified
- Support for complex nested tuplets or ratios other than 3:2.
