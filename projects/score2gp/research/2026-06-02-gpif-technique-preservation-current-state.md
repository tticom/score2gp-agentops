# Research Report: GPIF Technique Preservation Current State (v0.1)

- **Repository**: `score2gp-agentops` and `score2gp`
- **Branch**: `research/gpif-technique-preservation-current-state-v0.1` (score2gp) and `agent/gpif-technique-preservation-current-state-v0.1` (score2gp-agentops)
- **Operative Prompt**: `projects/score2gp/research/2026-06-02-gpif-technique-preservation-current-state/prompts/001-research-prompt.md`

---

## 1. Purpose

This research report inspects the current `score2gp` pipeline to identify where guitar-technique evidence (hammer-on, pull-off, slide, bend, vibrato, palm mute, dead note, etc.) exists in the pipeline and determine the smallest safe next implementation slice for technique preservation.

---

## 2. Current Verified State

Both recent PRs are merged:
- Product PR `tticom/score2gp#157` (melodic soloing barline/layout refinement).
- Governance PR `tticom/score2gp-agentops#20` (run record for melodic soloing refinement).

The local `main` branches of both repositories have been fast-forwarded to the merged states. All 442 public tests pass cleanly.

---

## 3. Investigation & Verification Commands Run

All commands were executed within the `score2gp` WSL environment:
1. `git status` (confirmed clean state on research branch)
2. `git branch --show-current` (confirmed `research/gpif-technique-preservation-current-state-v0.1`)
3. `git log --oneline --decorate --max-count=10` (verified merge history of PR #157)
4. `wsl env PYTHONPATH=. .venv/bin/pytest` (confirmed all 442 public tests pass in 14.07s)
5. `wsl env PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py` (executed quality audit successfully)
6. `git ls-files fixtures/private work` (verified private-safety invariant: outputs exactly `fixtures/private/.gitkeep`)
7. `rg -n` symbol searches for techniques across the codebase.

---

## 4. Public Test Results

```text
============================= 442 passed in 14.07s =============================
```

---

## 5. Private Audit Result Summary (Private-Safe)

The quality audit was executed successfully on the 9 private scores:

| Score Label | Status | Quality Category | Playable Frets | Matched Frets | Tech Count |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `private_input_1` | fail | `gp_output_empty_or_near_empty` | 0 | 0 | 106 |
| `private_input_2` | fail | `gp_output_empty_or_near_empty` | 0 | 0 | 25 |
| `private_input_custom` | fail | `gp_output_empty_or_near_empty` | 0 | 0 | 3 |
| `private_input_custom_lesson_3` | pass | `gp_output_technique_loss_expected` | 451 | 451 | 4 |
| `private_input_custom_lesson_4` | pass | `gp_output_technique_loss_expected` | 546 | 546 | 31 |
| `private_input_custom_lesson_5` | pass | `gp_output_technique_loss_expected` | 295 | 295 | 21 |
| `private_input_custom_lesson_6` | pass | `gp_output_technique_loss_expected` | 115 | 115 | 13 |
| `private_input_custom_lesson_7` | pass | `gp_output_technique_loss_expected` | 624 | 624 | 13 |
| `private_input_custom_melodic_soloing` | pass | `gp_output_fret_matching_suspect` | 16 | 16 | 51 |

---

## 6. Search Terms Used

```bash
rg -n "hammer|pull|slide|bend|vibrato|trill|tap|harmonic|mute|palm|dead|ghost|grace|slur|tie|technique|articulation|ornament|gliss|legato|let ring|let-ring|staccato|accent" src tests scripts
```

---

## 7. Files Inspected

- `src/score2gp/ir.py` (ScoreIR technique models)
- `src/score2gp/gpif.py` (GPIF XML serialization)
- `src/score2gp/pdf.py` (PDF text block splitting and classification)
- `src/score2gp/musicxml.py` (MusicXML notation parsing)
- `src/score2gp/tabraw.py` (TabCandidate schema and classification tokens)
- `src/score2gp/build_ir.py` (Heuristic technique-text candidate note-mapping)
- `src/score2gp/gp_package.py` (ScoreIR recovery from GPIF XML files)
- `tests/test_gp_writer.py` (GPIF writer technique serialization assertions)
- `tests/test_symbol_attachment.py` (Heuristic attachment test assertions)

---

## 8. Technique Evidence Table

| Technique | Evidence found? | Earliest pipeline location | Durable model field? | Serialized to GPIF? | Evidence path/symbol | Notes |
| :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| **hammer-on** | yes | raw PDF text candidates | yes | yes | `HammerOnTechnique` | Heuristic note attachment matches only in bars with exactly 2 notes. Lost during GPIF deserialization recovery in `gp_package.py`. |
| **pull-off** | yes | raw PDF text candidates | yes | yes | `PullOffTechnique` | Heuristic note attachment matches only in bars with exactly 2 notes. Lost during GPIF deserialization recovery in `gp_package.py`. |
| **slide** | yes | raw PDF text candidates | yes | yes | `SlideTechnique` | Heuristic note attachment matches only in bars with exactly 1 note. Deserialized back to generic `Technique(kind="slide")`. |
| **bend** | yes | raw PDF text candidates | yes | yes | `BendTechnique` | Heuristic note attachment matches only in bars with exactly 1 note. Deserialized back with points in `gp_package.py`. |
| **vibrato** | yes | raw PDF text candidates | yes | yes | `VibratoTechnique` | Heuristic note attachment matches only in bars with exactly 1 note. Deserialized back to generic `Technique(kind="vibrato")`. |
| **trill** | partial | ScoreIR model | yes | yes | `TrillTechnique` | Not detected in PDF or MusicXML. Serialized to GPIF but not parsed back. |
| **tap** | partial | ScoreIR model | yes | yes | `TappingTechnique` | Not detected in PDF or MusicXML. Serialized to GPIF but not parsed back. |
| **harmonic** | no | nowhere durable yet | no | no | None | Completely absent from PDF, MusicXML, ScoreIR, and GPIF. |
| **palm mute** | yes | raw PDF text candidates | yes | yes | `PalmMuteTechnique` | Extracted from PDF as candidate text, but skipped in `build_ir.py` (causes `unsupported_technique_text` warning). Not parsed from MusicXML or GPIF. |
| **dead note / ghost note** | yes | raw PDF text candidates | yes | yes | `Note.is_dead` | Extracted as `"x"`/`"X"` from PDF but filtered out as non-playable candidate. Serialized to GPIF. Recovered from GPIF. |
| **grace note** | yes | MusicXML | yes | yes | `GraceTechnique` | Skipped in `build_ir.py` with warning `musicxml-grace-skipped`. Serialized to GPIF. Not parsed from PDF or GPIF. |
| **tie** | yes | MusicXML | yes | yes | `TieTechnique` | Parsed from MusicXML. Serialized to GPIF and recovered back to ScoreIR. Not parsed from PDF. |
| **slur / legato** | yes | MusicXML | yes | yes | `SlurTechnique` | Parsed from MusicXML. Serialized to GPIF. Not parsed from PDF or GPIF. |
| **staccato / accent** | yes | ScoreIR model | yes | yes | `Note.articulations` | Not parsed from PDF/MusicXML. Serialized to GPIF. Recovered from GPIF. |
| **let ring** | yes | raw PDF text candidates | yes | yes | `LetRingTechnique` | Extracted from PDF as candidate text, but skipped in `build_ir.py` (causes `unsupported_technique_text` warning). Not parsed from MusicXML or GPIF. |
| **glissando** | yes | ScoreIR model | yes | yes | `SlideTechnique.glissando` | Only exists in ScoreIR and serialized to GPIF. |
| **tremolo bar** | yes | ScoreIR model | yes | yes | `TremoloBarTechnique` | Only exists in ScoreIR and serialized to GPIF. |
| **tremolo picking** | yes | ScoreIR model | yes | yes | `TremoloPickingTechnique` | Only exists in ScoreIR and serialized to GPIF. |
| **slap** | yes | ScoreIR model | yes | yes | `SlapTechnique` | Only exists in ScoreIR and serialized to GPIF. |
| **pop** | yes | ScoreIR model | yes | yes | `PopTechnique` | Only exists in ScoreIR and serialized to GPIF. |
| **rasgueado** | yes | ScoreIR model | yes | yes | `RasgueadoTechnique` | Only exists in ScoreIR and serialized to GPIF. |

---

## 9. Pipeline Map

```text
PDF drawings (No evidence)
  -> PDF text candidates (h, p, sl, vib, pm, pm., let ring, x/X extracted as text)
  -> PDF candidates / TabRaw (Mixed tokens split, kind="technique-text" or "candidate-text")
  -> TAB/fret candidates / build_ir (Heuristic attach of h/p/sl/vib/bend under 1-note/2-note limits. Rest skipped/warned)
  -> ScoreIR (Preserved under Note.techniques or Note.is_dead)
  -> GPIF writer (Serialized to HO, PO, Slide, Bend, LetRing, PalmMute, DeadNote, Vibrato, etc.)
  -> Quality Audit (Counts non_playable_technique_text_candidate_count, warns on loss)
```

---

## 10. Findings

1. **PDF Text Extraction is Effective**: PYMuPDF text extraction successfully extracts technique characters like `H`, `P`, `sl.`, `vib`, `pm.`, `let ring`, `x`, `X`.
2. **TabRaw Classification is Active**: Mixed words are correctly split (e.g., `12h14` is split into `12` fret and `h` technique text). Techniques are preserved under the `"technique-text"` candidate kind in TabRaw with their spatial metadata.
3. **Core Pipeline Heuristic is Restrictive**:
   - `build_ir.py` uses a naive count heuristic: it only attaches hammer-on/pull-off if there are **exactly two notes** in the bar, and slide/bend/vibrato if there is **exactly one note** in the bar. In complex melodic soloing bars (which contain many notes), these techniques fail to attach and issue `ambiguous_technique_attachment` warnings.
4. **GPIF Relational Parser is Incomplete**:
   - While `gpif.py` fully serializes hammer-ons (`HO`) and pull-offs (`PO`) to the relational GPIF format, the parser `gp_package.py` **entirely lacks** recovery logic for them. They are ignored when loading generated `.gp` files back to ScoreIR.
5. **Palm Mute, Let Ring, Articulations, and Dead Notes are Skipped**:
   - These techniques exist in ScoreIR models and GPIF serialization, but are not mapped or assigned in `build_ir.py` or are filtered out during layout grouping (e.g. dead note `"x"`).

---

## 11. Recommended Next Branch

We recommend creating the following branch:

**Branch name**: `feature/gpif-hammer-pull-slide-minimal-v0.1`

### Why this is the next smallest useful step:
Hammer-on, pull-off, and slide evidence is already successfully extracted from PDFs as text candidates and exists in ScoreIR and GPIF serialization. However, we cannot claim end-to-end preservation because of two gaps:
1. **GPIF Parser Gap**: `gp_package.py` does not deserialize `<HO>` and `<PO>` back to ScoreIR.
2. **Proximity Attachment Gap**: `build_ir.py` attaches techniques purely based on note counts in a bar rather than visual `x` proximity, failing in bars with multiple notes.

Fixing these two gaps is the smallest safe step to unlock end-to-end technique preservation.

### Likely files:
- `src/score2gp/gp_package.py` (Add `<HO>` and `<PO>` relational extraction under `_extract_score_ir_from_relational_gpif_root`).
- `src/score2gp/build_ir.py` (Refine `_attach_symbols_and_techniques` to use visual `x` coordinate proximity to assign technique text to notes, rather than bar note count limits).

### Non-goals:
- Do not extract visual curves/slurs from PDF vector drawings.
- Do not change ScoreIR models or schemas.
- Do not implement complex bends or vibrato curve extraction.

### Acceptance criteria:
1. `gp_package.py` successfully recovers `HammerOnTechnique` and `PullOffTechnique` from relational GPIF XML.
2. `build_ir.py` uses proximity `x` alignment to attach technique candidates to notes in bars containing more than 2 notes.
3. All 442 public tests pass cleanly.
4. Private audit reports stable statuses and no regressions on Lessons 3–7.

### Validation commands:
```bash
python -m pytest
python scripts/private_gp_quality_audit.py
git diff --check
git status --short
```

### Stop conditions:
- Regressions in Lessons 3–7 or melodic soloing empty output.
- XML validation errors or parse errors in generated `.gp` packages.

---

## 12. Stop Conditions Encountered

None.

---

## 13. Private-Safety Audit Result

```bash
git ls-files fixtures/private work
```
Output:
```text
fixtures/private/.gitkeep
```
No private files, generated GP files, audit telemetry, logs, or overlays have been tracked or staged.
