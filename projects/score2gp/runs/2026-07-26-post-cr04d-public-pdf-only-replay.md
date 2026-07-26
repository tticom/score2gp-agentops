# Post-CR-04D Public PDF-Only Conversion Replay

## Executive Summary

Following the merge of refactoring sequence CR-04D (D1 through D5), a fresh runtime-provenance replay of the committed PDF-only conversion path was executed on the deterministic generated score-like public fixture (`tests/fixtures/pdf/generated_scorelike_tab.pdf`) without a MusicXML sidecar. Both strict and diagnostic channels executed cleanly with exit status 0, producing valid, inspectable `ScoreIR` v0.1 and Guitar Pro (`.gp`) binary packages.

---

## Pinned Environment & Repository State

* **Product Repository SHA**: `d70d559152c5aa357a7d2eb38e65b09f288bb08f`
* **AgentOps Repository SHA**: `96592ba2385d10f0b0ad2ef841dbcbaf0da2731d`
* **Skills Lock SHA**: `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`
* **CLI Executable Path**: `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/score2gp`
* **Python Module Location**: `src/score2gp/__init__.py`
* **Input Fixture**: `tests/fixtures/pdf/generated_scorelike_tab.pdf`
* **Input SHA-256**: `b3106b083de608db600f63822c0a31f614fd96523ac27ffb5b2c80cd41d8d564`
* **Pre-Replay Preflight Gate**: `.venv/bin/python scripts/agent_verify.py` — **Overall status: PASS**

---

## Channel 1: Strict Execution

### Command & Parameters
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

### Channel Results
* **Exit Code**: `0`
* **Summary Status**: `"success"`
* **Refusals / Errors**: None
* **Artifacts Created**:
  * `TabRaw`: `work/20260726_post_cr04d_replay/strict/intermediate/tab/tabraw.json` (exists)
  * `ScoreIR`: `work/20260726_post_cr04d_replay/strict/intermediate/score.ir.json` (exists)
  * `Guitar Pro`: `work/20260726_post_cr04d_replay/strict/generated_scorelike_tab.gp` (exists)
* **ScoreIR Structure**:
  * Total Bars: `4`
  * Total Events: `13` (9 note-events, 4 remainder rest-events)
  * Total Notes: `11`
  * Bar 1: 3 events (3 notes, 1 remainder rest)
  * Bar 2: 4 events (3 notes, 1 remainder rest)
  * Bar 3: 3 events (2 notes, 1 remainder rest)
  * Bar 4: 3 events (3 notes, 1 remainder rest)
* **Validation**:
  * `validate-ir`: `"valid": true`, 0 errors
  * GP Package Inspection: `is_zip == True`, `xml_well_formed == True`, `bar_count == 4`, `note_count == 11`

---

## Channel 2: Diagnostic / Remediation Execution

### Command & Parameters
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

### Channel Results
* **Exit Code**: `0`
* **Summary Status**: `"success"`
* **Refusals / Errors**: None
* **Artifact Coherence**: Identical to Strict execution (the generated public scorelike PDF has clean six-line tab system geometry that passes strict layout gating without triggering remediation).

---

## Warnings Audit

Both channels emitted 13 warning items across 9 distinct warning codes:

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
2. **Technique Text Attachment**: Text tokens near staff lines (e.g. `'ring'`) are recorded as evidence but not mapped to ScoreIR note techniques.
3. **Controlled Fixture vs Real Score**: This replay confirms architectural stability and pipeline integrity on a clean, generated PDF. It does not constitute a claim of real-world OMR accuracy on arbitrary commercial PDF scores.

---

## Recommended Follow-up Candidate (Unauthorised)

* **Candidate**: Standard-notation staff assembly extraction (e.g., potential `CR-05`), modularizing standard-notation staff line and clef processing out of `build_ir.py`.
* **Status**: Unauthorised candidate only. `ACTIVE_TASK.md` and `NEXT.md` remain unchanged.
