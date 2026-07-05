# Active Task

**Task**: Architect Research — Real-fixture E2E validation of `notation-whole-note-export`
**Authorised Role**: Architect
**Repository**: `tticom/score2gp-agentops`

## 1. Baseline
- Bounded whole-note font-glyph extraction is complete and verified only for the approved BWV 772 / Mutopia LilyPond fixture path.
- The `notation_bridge` can convert whole-note candidates to ScoreIR.
- A CLI command named `notation-whole-note-export` exists.
- Current verification is mock-patched unit testing, not real PDF E2E export validation.
- The next public synthetic fixture boundary is `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`.

## 2. Active Blocker
- The `notation-whole-note-export` CLI lacks a real-fixture E2E validation proving that it can run on `generated_standard_staff_whole_note.pdf` and produce a structurally correct `.gp` package without mocks.

## 3. Goal
- Perform Architect research to determine whether `notation-whole-note-export` can run end-to-end on `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf` and produce a structurally correct `.gp` package.

## 4. Non-goals
- Do not implement fixes.
- Do not modify product code or tests.
- Do not create a product PR.
- Do not broaden beyond `generated_standard_staff_whole_note.pdf`.
- Do not validate arbitrary PDF whole-note recognition.
- Do not validate broad LilyPond support.
- Do not validate raster/OMR whole-note support.
- Do not use BWV 772, Mutopia PDFs, private PDFs, downloaded PDFs, unpinned URLs, or unapproved local fixtures for this task.
- Do not commit generated `.gp` files or score-derived outputs.

## 5. Fixture Boundary
- `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`

## 6. Required Output
Architect must choose exactly one outcome:
- **Outcome A**: Real-fixture E2E export path is viable. The CLI runs on the fixture and produces a structurally correct `.gp` package for the intended whole-note evidence.
- **Outcome B**: CLI/export path is partially viable but blocked by specific implementation gaps in the GP writer, notation bridge, CLI, layout safety gates, duration mapping, pitch association, measure construction, or package structure.
- **Outcome C**: No viable E2E export path exists yet from this CLI/fixture combination; Developer implementation is not authorised until blockers are resolved by a new requirement.

## 7. Stop Conditions
- Fixture is missing or not safe/public synthetic.
- CLI is missing or command syntax cannot be discovered safely.
- Global layout safety gates block PDF-only export.
- Missing time-signature support blocks valid GP construction.
- Generated `.gp` cannot be inspected with available tooling.
- Any unsafe artifact would need to be committed.
- Product repo becomes dirty with unintended changes.
