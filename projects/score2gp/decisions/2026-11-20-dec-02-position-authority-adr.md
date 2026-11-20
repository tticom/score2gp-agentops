# ADR-009: Observed TAB positions are authoritative; inference only for notation-only notes, always labelled

- **Status**: **Proposed (2026-11-20)**. Awaits maintainer acceptance. The author does not mark it Accepted or Approved.
- **Authority item**: DEC-02. **Requirement**: `REQ-0001:U04`.
- **Maintainer position (2026-09-25)**: "Position is the TAB's super power."
- **Reconciles**: ADR-006 (this repository, approved 2026-08-13) and product ADR-0004 (`doc/architecture/decisions/0004-retention-of-biomechanical-position-optimization.md` in `tticom/score2gp`, accepted 2026-08-15).

## 1. Current-state facts

Source: `tticom/score2gp` `main` at `42acd81af90ec4e756e6dd7fc1f16ad39b86cfa8` (2026-11-16), read-only. Reproduce with `git -C <score2gp> show 42acd81:<path>`. Line numbers refer to that revision. No private musical content is cited.

### 1.1 The two records
- ADR-006 forbids inferring hand positions; notes lacking explicit fretboard ownership are dropped or raise a clear error.
- Product ADR-0004 retains `BiomechanicalPositionOptimizer`, on the premise that "the fusion of TAB numbers into the timeline is not yet implemented" and that every note therefore arrives as notation without TAB.

### 1.2 Where observed TAB string and fret enter the pipeline
- `src/score2gp/tabraw.py:68` `TabCandidate.to_provenance()` turns an extracted TAB candidate (`string`, `parsed_fret`, `source_stage`, page, system, bar, bbox, `raw_token_id`) into a `Provenance` record.
- PDF-only TAB path, `src/score2gp/build_ir.py`: candidates missing string, bar, system or x are refused (line 1866); notes are built with `provenance=[candidate.to_provenance()]` (line 2008, also 3000 and 3012). No position is invented.
- MusicXML plus TAB path, `build_ir.py:2657` `_aligned_note`: string and fret come from the TabRaw candidate; the TAB provenance is appended to the note (lines 2714-2739). On a pitch mismatch the TAB-derived pitch is kept and a `musicxml-tab-pitch-mismatch` warning is raised (around lines 2700-2711).

### 1.3 Is TAB fusion into the timeline implemented?
Yes, in the `build_ir.py` paths of 1.2: TAB candidates are aligned to MusicXML notes by bar and x order (`alignment_strategy`, line 2715) and become `Note` records. ADR-0004's premise ("not yet implemented") no longer holds for those paths. It does still hold for the `notation_omr` path (1.4): nothing under `src/score2gp/notation_omr/` sets `parsed_fret`, `string` or `string_index` on a recognition outcome (a grep of `parsed_fret|string_index|fret_number` there finds only `position_optimizer.py`).

### 1.4 Does `BiomechanicalPositionOptimizer` exist, and where is it called?
- It exists: `src/score2gp/notation_omr/position_optimizer.py:71`. Cost weights are in its constructor (lines 74-86); inference is at lines 135-175 and picks a position by fret jump and string stretch from the previous position, or by distance from fret 3 for the first note.
- Single production call site: `src/score2gp/notation_omr/pipeline.py:312-313` (`optimizer.optimize_sequence(outcomes)`), emitted as `fretboard_position_ownership` (line 324) in the diagnostic result of `run_recognition_on_file`, which the `cli.py` recognition commands consume (lines 372, 390, 766, 814, 1576).
- Observed-versus-inferred branch: `position_optimizer.py:121-134` returns an `observed_tab` record when the event carries a fret and string; otherwise lines 135-175 return an `inferred_position` record. Because the extractor (1.3) never supplies a fret and string, every record from this call is `inferred_position`.

### 1.5 How provenance (observed versus inferred) is recorded
- Recorded at the optimizer: `FretTokenOwnership.modality` is `observed_tab` or `inferred_position`, with `is_observed`, `is_inferred` and `cost` (`position_optimizer.py:40-68`). It is serialised into the diagnostic JSON.
- Lost at the compiler: `src/score2gp/scoreir_compiler.py:204-214` builds `Note(string, fret, pitch)` from the owner and drops `modality` and `cost`; the `Note` gets no provenance there. `Note` has a `provenance` list (`src/score2gp/ir.py:500`) but `SourceStage` (`ir.py:17-24`) has no value meaning "position inferred from pitch". `SourceStage.INFERRED` exists and is used only for implied rests (`pdf_tab_event_factory.py:172`).
- Defaulted to observed: when ownership arrives as a dict without `modality`, `scoreir_compiler.py:74` defaults it to `observed_tab`.
- Reachability: `ScoreIRCompiler` and `GPIFBuilder` are referenced under `src/` only by each other (`gpif_builder.py:7`); the consumers of `fretboard_position_ownership` that I found are tests (`tests/test_scoreir_gpif_compiler_refactor.py:129-171`). I found no CLI command that compiles inferred positions into a written file. This is a lead for the maintainer, not a proof of absence.
- The `build_ir.py` MusicXML path never infers: a note with no TAB candidate is skipped with warnings `tab-candidate-missing` and `scoreir-event-skipped` (around lines 2605-2640), which is ADR-006 behaviour.

### 1.6 Net
The two ADRs are each half true on `main`. The `build_ir` pipeline follows ADR-006 (observed TAB only, drop with warning). The `notation_omr` pipeline follows ADR-0004 (infers, because it extracts no TAB). The synthetic `(string=1, fret=0)` fallback that ADR-0004 promised to remove is absent from `scoreir_compiler.py`; an unowned note raises "Unowned note" (around lines 216-226).

## 2. Decision (proposed)

1. **Observed TAB position is authoritative.** Where a note has an observed TAB string and fret, that position is the output. Inference never overrides or "improves" an observed position; a conflict with notation pitch is a warning and the TAB position wins (the existing mismatch rule).
2. **Inference is permitted only for notation-only notes**, meaning notes with no observed TAB candidate at all. This replaces ADR-006's blanket ban and ADR-0004's "until fusion lands" condition with one rule that does not depend on implementation state.
3. **Every inferred position carries provenance and is never presented as observed.** The label must survive into ScoreIR and every written output or report, and must be machine-readable (a note-level provenance record, not only a diagnostic key). The default for an unlabelled position is "unknown", never "observed".
4. **Inference is a position choice, not a musical claim.** The cost model may choose among positions that sound the written pitch; it must not change pitch, rhythm or note count. If no position yields the pitch, the note is dropped with a located warning or the conversion fails clearly, as in ADR-006.
5. **No synthetic fallback positions**, such as `(string=1, fret=0)`.

## 3. Reason

- The maintainer's position treats TAB as the only source of fretboard truth; a player reading the output relies on it.
- ADR-006's reason holds: stylistic variation means an inferred position can be musically wrong, and silent substitution corrupts output.
- ADR-0004's reason also holds: a Guitar Pro note needs a string and fret, and notation-only input exists. A total ban would reject or drop every notation-only note.
- Labelling reconciles them: inference is allowed where nothing observed exists, and nothing inferred can be mistaken for evidence.

## 4. Consequences

- The `notation_omr` optimizer can stay, but only for notation-only notes and only with a surviving label.
- ScoreIR needs a way to mark a note's position as inferred (finding F-1). That is a product change for governance to task; this record does not make it.
- A written file may mix observed and inferred positions only if the output or report says which. This is an acceptance-test target for a follow-up.
- Tests must show both: an observed position is never altered, and an inferred position is labelled all the way to output.
- The rule does not decide whether inferred positions are written by default or only behind an opt-in. See Q-1.

## 5. Supersession proposal (applies only once this ADR is accepted)

This record does not edit ADR-006 or the product repository. Migrating the product ADRs is DEC-03.

- **ADR-006** (`projects/score2gp/ARCHITECTURE_DECISIONS.md`): mark **Amended by ADR-009**. Keep the title and Decision text for history and add the status line "Amended by ADR-009 (date): the ban on inference is narrowed to notes that have observed TAB; the rule against synthetic positions and silent failure is retained". The retained parts are decision points 4 and 5 above.
- **Product ADR-0004**: mark **Superseded by ADR-009** (the reconciling record lives in the governance repository; the product copy should link to it). Its premise that TAB fusion is not implemented is stale for the `build_ir` paths. What survives is the retention of the optimizer for notation-only notes, now conditional on labelling; the removal of the synthetic fallback is confirmed. Product text migration is DEC-03.

## 6. Findings: divergences between code and the proposed rule (none fixed here)

- **F-1 (important)**: `src/score2gp/scoreir_compiler.py:204-214` drops `modality` and `cost`, so an inferred position becomes an unlabelled `Note`. `ir.py:17-24` and `ir.py:43-54` have no stage or field meaning "inferred position". Breaks decision point 3.
- **F-2**: `src/score2gp/scoreir_compiler.py:74` defaults a missing `modality` to `observed_tab`, so an unlabelled position is presented as observed. Breaks point 3's default.
- **F-3**: `position_optimizer.py:118-119` decides "observed" only from the keys `parsed_fret`/`fret_number` and `string_index`/`string`. Key-name drift in an upstream outcome would silently turn observed TAB into inference. Needs a test.
- **F-4**: `position_optimizer.py:135-175` appends nothing, with no warning or record, for an event whose pitch cannot be parsed or has no position within frets 0-24 (hard-coded). The compiler later raises "Unowned note", but the optimizer drops silently and the loss is not located.
- **F-5**: Product ADR-0004's premise (no TAB fusion) is false on `main` for `build_ir.py` and still true for `notation_omr`. The product ADR text is stale (migration is DEC-03).
- **F-6**: `pipeline.py:312-313` runs the optimizer whether or not TAB evidence exists elsewhere in the same PDF. Nothing ties `notation_omr` outcomes to the `build_ir` TAB candidates for the same note, so a note with observed TAB could still receive an inferred position in the diagnostic output.

## 7. Questions for the maintainer

- **Q-1**: should inferred positions be written to the output by default, or only behind an explicit opt-in, with the label always present?
- **Q-2**: if a score has TAB for some notes and none for others, is per-note inference acceptable, or must the whole score be refused?
- **Q-3**: are frets 0-24 and standard tuning an acceptable inference boundary, or must tuning come from observed evidence?
- **Q-4**: must the label be visible in the Guitar Pro file itself (for example a text annotation), or only in a sidecar report?
