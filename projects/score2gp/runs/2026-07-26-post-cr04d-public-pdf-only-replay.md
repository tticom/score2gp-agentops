# Post-CR-04D Public PDF-Only Conversion Replay

## Executive Summary

Following the merge of refactoring sequence CR-04D (D1 through D5), a fresh runtime-provenance replay of the committed PDF-only conversion path was executed on the deterministic generated score-like public fixture (`tests/fixtures/pdf/generated_scorelike_tab.pdf`) without a MusicXML sidecar. Both strict and diagnostic channels executed cleanly with exit status 0, demonstrating structural CLI execution and pipeline artifact production of valid, inspectable `ScoreIR` v0.1 and Guitar Pro (`.gp`) binary packages.

---

## Pinned Environment & Repository State

* **Product Repository SHA**: `d70d559152c5aa357a7d2eb38e65b09f288bb08f`
* **AgentOps Repository SHA**: `96592ba2385d10f0b0ad2ef841dbcbaf0da2731d`
* **Skills Lock SHA**: `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`
* **CLI Executable Path**: `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/score2gp`
* **Resolved Python Module Location**: `/home/tticom-automation/work/score2gp-workspace/score2gp/src/score2gp/__init__.py`
* **Input Fixture**: `tests/fixtures/pdf/generated_scorelike_tab.pdf`
* **Input SHA-256**: `b3106b083de608db600f63822c0a31f614fd96523ac27ffb5b2c80cd41d8d564`
* **Pre-Replay Preflight Gate**: `.venv/bin/python scripts/agent_verify.py` — **Overall status: PASS**

---

## Author-Reported Evidence vs. Author Post-Run Validation

* **Author-Reported Evidence**: CLI invocation command lines, flag parameters, and stdout execution logs.
* **Author Post-Run Validation**:
  * `validate-ir` CLI output (`"valid": true`, 0 errors)
  * `inspect_gp()` package inspection (`is_zip: True`, `xml_well_formed: True`, `bar_count: 4`, `note_count: 11`)
  * `ScoreIR.from_json_file()` object model counts (4 bars, 13 events, 11 notes)
  * Direct file byte SHA-256 hashes and zip member hash comparisons

---

## Channel Execution Results

### Channel 1: Strict Execution (`--strict`)

* **Command**:
  ```bash
  .venv/bin/python -m score2gp.cli convert \
    --pdf tests/fixtures/pdf/generated_scorelike_tab.pdf \
    --out work/20260726_post_cr04d_replay/strict/generated_scorelike_tab.gp \
    --work-dir work/20260726_post_cr04d_replay/strict/intermediate \
    --json-report work/20260726_post_cr04d_replay/strict/summary.json \
    --pdf-only-tab \
    --editable-draft \
    --strict
  ```
* **Exit Code**: `0`
* **Summary Status**: `"success"`
* **First Warning Details**:
  * **Code**: `"tab-extraction-incomplete"`
  * **Message**: `"This phase records born-digital text candidates with heuristic staff/string/bar estimates where page geometry allows it; full optical tab alignment is pending."`
  * **Category / Stage / Severity / Details**: `absent/not emitted` in `warnings.json` payload structure.
* **Artifact Existence & Metrics**:
  * `TabRaw`: `work/20260726_post_cr04d_replay/strict/intermediate/tab/tab_raw.json` (exists)
  * `ScoreIR`: `work/20260726_post_cr04d_replay/strict/intermediate/score.ir.json` (exists, SHA-256: `b3c23f4974850524258e0de5c82438ce6652c1dc63ce02bb8f821b312029eb59`)
    * Bar count: `4`
    * Events total: `13` (9 note-events, 4 remainder rest-events)
    * Total Notes: `11` (Bar 1: 3 notes + 1 rest, Bar 2: 3 notes + 1 rest, Bar 3: 2 notes + 1 rest, Bar 4: 3 notes + 1 rest)
  * `Guitar Pro`: `work/20260726_post_cr04d_replay/strict/generated_scorelike_tab.gp` (exists, SHA-256: `a70a233573fc079bcaeaa45cea363ab177d4c971dc08ff1e584ecf3ab78ade21`)
    * `is_zip == True`, `xml_well_formed == True`, `bar_count == 4`, `note_count == 11`
* **Validation Results**: `validate-ir` returned `"valid": true`, 0 errors.
* **Strongest False-Success Mode**: Successful GP package creation and clean ScoreIR schema validation might falsely imply musical or rhythmic accuracy, whereas rhythm is actually assigned via equal spatial offset heuristics (480 ticks per onset).
* **First Mismatch / Remaining Unknown**: Equal spatial offset duration assignment (notes assigned fixed eighth-note onsets without visual beam/flag duration recovery).
* **Coherence with Unmeasured Round-Trip Result**: Produces valid `ScoreIR` v0.1 and valid `.gp` package structure; however, semantic round-trip re-ingestion (`GP -> IR` or `IR -> GP` round-trip losslessness) remains unmeasured in this replay.

---

### Channel 2: Diagnostic Execution (`--no-strict --allow-remediation`)

* **Command**:
  ```bash
  .venv/bin/python -m score2gp.cli convert \
    --pdf tests/fixtures/pdf/generated_scorelike_tab.pdf \
    --out work/20260726_post_cr04d_replay/diagnostic/generated_scorelike_tab.gp \
    --work-dir work/20260726_post_cr04d_replay/diagnostic/intermediate \
    --json-report work/20260726_post_cr04d_replay/diagnostic/summary.json \
    --pdf-only-tab \
    --editable-draft \
    --no-strict \
    --allow-remediation
  ```
* **Exit Code**: `0`
* **Summary Status**: `"success"`
* **First Warning Details**:
  * **Code**: `"tab-extraction-incomplete"`
  * **Message**: `"This phase records born-digital text candidates with heuristic staff/string/bar estimates where page geometry allows it; full optical tab alignment is pending."`
  * **Category / Stage / Severity / Details**: `absent/not emitted` in `warnings.json` payload structure.
* **Artifact Existence & Metrics**:
  * `TabRaw`: `work/20260726_post_cr04d_replay/diagnostic/intermediate/tab/tab_raw.json` (exists)
  * `ScoreIR`: `work/20260726_post_cr04d_replay/diagnostic/intermediate/score.ir.json` (exists, SHA-256: `f45c392e28f90a4568852bf932aa10bd7c407e883945bd84fb9b16c3d16d7824`, 4 bars, 13 events, 11 notes)
  * `Guitar Pro`: `work/20260726_post_cr04d_replay/diagnostic/generated_scorelike_tab.gp` (exists, SHA-256: `55c725f9df533b00d9762c7a45db17283bee55deb366cc6b48967318ee67269e`, `is_zip == True`, `xml_well_formed == True`, 4 bars, 11 notes)
* **Channel Comparison & Package Member Audit**:
  * *Zip Member Byte-Identity*: All 6 inner archive members inside the `.gp` package are **100% byte-identical** between Strict and Diagnostic channels:
    * `Content/score.gpif`: `660dfdfb11846f0bc6a38ee50af57152056df1747b4176b7b6d73ac44797ed2d` (identical)
    * `Content/Preferences.json`: `73eb7fb1d4be03347c66e3183dab98958d1b7529d8fb25101ba4e6e1a92a949c` (identical)
    * `Content/LayoutConfiguration`: `4c153ee66abbf5ef721ede069c3009815e1f28cc43553a0744dca96027f3ead1` (identical)
    * `Content/BinaryStylesheet`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (identical)
    * `Content/PartConfiguration`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (identical)
    * `VERSION`: `64342505aa59f739d87352bbe5ae4f97f3c4e7348bb6372a7f9ec6859d11f99e` (identical)
  * *Outer Archive & ScoreIR Hashes*: The outer `.gp` zip hashes (`a70a23...` vs `55c725...`) differ solely due to creation timestamps recorded in zip local file headers during compression. `score.ir.json` SHA-256 hashes (`b3c23f...` vs `f45c39...`) differ because `score.ir.json` embeds execution timestamps (`conversion_info.created_at`) and absolute/relative output provenance paths.
* **Validation Results**: `validate-ir` returned `"valid": true`, 0 errors.
* **Strongest False-Success Mode**: Clean execution under diagnostic mode does not validate layout remediation mechanisms, as the public score-like fixture passes strict checks cleanly without exercising remediation routines.
* **First Mismatch / Remaining Unknown**: Remediation logic remains unexercised by clean public fixtures.
* **Coherence with Unmeasured Round-Trip Result**: Zip content byte-identity proves identical GPIF generation across strict and diagnostic runs; however, round-trip semantic fidelity remains unmeasured.

---

### Channel 3: Semantic Round-Trip Channel

* **Status**: `not run/unmeasured` (Semantic round-trip conversion channel was not executed as part of this replay).

---

## Warnings Audit

Both channels emitted 13 warning items across 9 distinct warning codes (each warning object containing only `code` and `message` fields):

1. `pdf_editable_draft`: Inferred draft tempo applied (120 BPM).
2. `pdf_grouping_complete`: System/staff/bar boxes inferred for born-digital tab systems.
3. `pdf_bar_boxes_constructed`: Global bar indices mapped from system staff bounds.
4. `pdf_layout_details`: Informational bounding geometry details.
5. `pdf_only_tab_inferred_timing`: Equal spatial offset rhythm timing applied.
6. `tab-extraction-incomplete`: Some non-playable text unaligned.
7. `tabraw-technique-text-not-aligned`: Non-playable technique text preserved without string assignment.
8. `unsupported_technique_text`: Technique text `'ring'` is unsupported in v0.1 vocabulary.
9. `ambiguous_technique_attachment`: Non-playable candidate text attached via proximity heuristics.

---

## Observed Limitations & Residual Unknowns

1. **Rhythm Inference Heuristic**: Spatial x-position spacing maps notes to equal eighth-note onsets (480 ticks) + remainder rest decomposition. Full visual duration beam detection remains unhandled in PDF-only mode.
2. **Technique Text Attachment**: Text tokens near staff lines (e.g., `'ring'`) are recorded as evidence but not mapped to ScoreIR note techniques.
3. **Controlled Fixture vs. Real Score**: This replay demonstrates structural CLI execution on a clean generated PDF. It does not constitute a claim of real-world OMR accuracy on arbitrary commercial PDF scores.

---

## Recommended Follow-up Candidate (Unauthorised)

* **Candidate**: Smallest evidence task addressing observed PDF-tab limitations: PDF-only tab duration/beam extraction or technique text alignment evidence on multi-bar PDF tab fixtures.
* **Justification**: Directly addresses the primary limitations observed in this replay (equal spatial duration assignment and unaligned technique text).
* **Status**: Unauthorised candidate only. `ACTIVE_TASK.md` and `NEXT.md` remain unchanged.
