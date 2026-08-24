# Formal Review Record — OMR-to-MusicXML Sidecar Generator Implementation

- **Target Repository**: `tticom/score2gp`
- **Target PR**: #404
- **Head SHA**: `a27a125539dc5f8576da4a136e0e8060820c32f1`
- **Branch**: `agy/musicxml-sidecar-generator`
- **Reviewer Role**: Sceptical Reviewer (Hard-Review Protocol)
- **Verdict**: **`APPROVED`**

---

## 1. Summary of Changes

PR #404 implements OMR-to-MusicXML generation from timeline preview structures:
1. **OMR-to-MusicXML Generator Engine** ([`src/score2gp/notation_omr/musicxml_generator.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/notation_omr/musicxml_generator.py)):
   - Compiles OMR recognition outcomes into valid MusicXML 4.0 `<score-partwise>` strings using `build_staff_timeline_preview`.
   - Generates polyphonic voices with `<backup>` elements when `voice=2` events exist.
   - Generates chord structures with `<chord/>` elements for co-located notes.
   - Maps pitch names (e.g. `F#5`, `Bb4`) to MusicXML `<step>`, `<alter>`, and `<octave>` elements.
   - Resolves key signature fifths (`<fifths>`) from semantic candidates (e.g., `D Major` -> `<fifths>2</fifths>`).
2. **CLI Route**: Added `generate-sidecar` command in [`src/score2gp/cli.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/src/score2gp/cli.py) to output valid `.musicxml` sidecar files directly from input PDFs.
3. **Design Knowledge Base**: Added architectural design document [`docs/design/omr-musicxml-sidecar-generation.md`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/docs/design/omr-musicxml-sidecar-generation.md).
4. **Unit Test Suite**: Added [`tests/test_musicxml_generator.py`](file:///home/tticom-codex/work/score2gp-workspace/score2gp/tests/test_musicxml_generator.py) covering monophonic scores, polyphonic voice backups, chord tags, and round-trip parsing through `score2gp.musicxml.parse_musicxml`.

---

## 2. Adversarial Probes & Evidence Ledger

| Claim | Production Code Path | Executed Probe / Counterexample | Observed Output & Oracle | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Key Signature Fifths Resolution** | `musicxml_generator.py#L86-L90` | `semantic_candidates` with `key_name="D Major"`. | Generated MusicXML includes `<fifths>2</fifths>`. | **VERIFIED** |
| **Empty Outcomes Safety** | `musicxml_generator.py#L73-L74` | `generate_musicxml_from_omr([])` | Returns `""` cleanly without throwing exceptions. | **VERIFIED** |
| **Accidental Pitch Parsing** | `musicxml_generator.py#L43-L62` | `parse_resolved_pitch("F#5")` & `("Bb4")`. | Returns `('F', 1, 5)` and `('B', -1, 4)`. | **VERIFIED** |
| **Roundtrip Parsing Verification** | `test_musicxml_generator.py#L49-L79` | Generated 4/4 measure written to disk and parsed back with `parse_musicxml`. | 4 notes parsed cleanly, 0 timing/overlap errors. | **VERIFIED** |

---

## 3. Disconfirmation & Sabotage Verification

- **Sabotage Test**: Deliberately corrupted `parse_resolved_pitch` to return `None` for accidental pitches. `test_musicxml_generator_roundtrip` immediately failed with missing notes.
- **Verification Commands Executed**:
  - `.venv/bin/python -m pytest tests/test_musicxml_generator.py tests/test_cr06_key_signature_semantics.py` (8 passed)
  - `.venv/bin/python scripts/agent_verify.py` (1078 passed, 1 skipped)

---

## 4. Verdict & Next Step

- **Verdict**: **`APPROVED`**
- **Suggested Next Step**: Human maintainer may merge PR #404 in `tticom/score2gp`.
