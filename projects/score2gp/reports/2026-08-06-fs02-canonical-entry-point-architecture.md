# FS-02 Architecture Report: Canonical Conversion Entry Point and Call-Chain Reconciliation

**Date**: 2026-08-06  
**Task**: FS-02: Reconcile Uncontrolled Runtime and Canonical Conversion Entry Point  
**Repository**: `tticom/score2gp` / `tticom/score2gp-agentops`  
**Authorised Identity**: `tticom-automation`  
**Role**: Architect  

---

## 1. Context & Objective

Following the completion and merge of task `FS-01` (*Runtime Provenance Baseline and Corpus Stabilisation Harness*, PR #409, commit `2101d8cf65ed6fad3d3984657703d131a165b97b`), task `FS-02` executes the Architect phase to verify and trace the canonical conversion route in `score2gp`. 

The objective of this architecture phase is to:
1. Formally trace `score2gp convert` and `score2gp omr` in `src/score2gp/cli.py`.
2. Confirm whether `score2gp convert` or `score2gp omr` constitutes the canonical conversion entry point.
3. Define the exact source-to-output call chain for `.gp` file generation.
4. Establish evidence bounds and non-negotiable constraints for downstream functional gates (`FS-03` corpus execution and `FS-04` defect remediation).

---

## 2. CLI Entry Point Verification & Reconciliation

Direct codebase inspection of `src/score2gp/cli.py` yields the exact definitions of the two sub-commands:

### 2.1 `score2gp convert` (Canonical Conversion Entry Point)
- **Function**: `convert_command` (`src/score2gp/cli.py` L801–L821)
- **Role**: Primary, canonical source-to-output conversion command.
- **Inputs**: `--pdf` (input born-digital PDF), optional `--musicxml` (`-m`) sidecar, `--out` (`-o` target `.gp` package path), `--work-dir`, `--json-report`, `--strict/--no-strict`, `--pages`, `--pdf-only-tab`, `--editable-draft`, `--tempo-bpm`, `--ref-gp`, `--sidecar-manifest`.
- **Outputs**: Target `.gp` Guitar Pro 7 package and consolidated JSON execution summary (`convert-report.json`).
- **Verdict**: `score2gp convert` is the **only** committed entry point capable of performing full PDF/MusicXML processing, ScoreIR construction, and `.gp` package generation.

### 2.2 `score2gp omr` (Optional Upstream Sidecar Generator)
- **Function**: `omr_command` (`src/score2gp/cli.py` L376–L398)
- **Role**: Optional external OMR helper for Audiveris batch execution.
- **Inputs**: `input_pdf`, `--out`, optional `--audiveris` path.
- **Outputs**: Intermediate XML/MXL artifact files and `omr_manifest.json` containing a `next_handoff` pointer (e.g. `score2gp convert --pdf <pdf> --musicxml <artifact>`).
- **Verdict**: `score2gp omr` does **not** generate `.gp` files or form a direct conversion pipeline. It is strictly an upstream sidecar producer whose output feeds into `score2gp convert`.

---

## 3. Source-to-Output Call Chain

The committed end-to-end call chain for `score2gp convert` is defined as:

1. **Invocation & CLI Routing**: `score2gp.cli:convert_command`
   - Validates option flags, argument dependencies (`--tempo-bpm`, `--work-dir`), and resolves MusicXML sidecar metadata (`_get_mxl_info`).
2. **Extraction & Alignment**:
   - PDF born-digital vector Tab/Notation extraction.
   - Alignment with optional MusicXML sidecar (`--musicxml`).
3. **ScoreIR Construction & Optimization**:
   - `score2gp.build_ir`: Constructs internal `ScoreIR` representation.
   - Applies Left-hand finger position and fret-snapping optimization (`optimize_fret_snapping`).
4. **Package Serialization**:
   - Serializes `ScoreIR` into the target Guitar Pro `.gp` package format at `--out`.
5. **Provenance Logging & Diagnostics**:
   - Invokes `_write_convert_report` to generate structured `convert-report.json`.
   - Records product SHA, runtime environment, exit code, refusal codes, and strict-mode status.

---

## 4. Evidence Bounds & Non-Negotiable Constraints for FS-03 / FS-04

Downstream tasks `FS-03` (Corpus Divergence Capture) and `FS-04` (Shared Defect Remediation) must strictly operate within the following bounds:

1. **Committed Route Only**: All conversion runs must execute exclusively via `score2gp convert`. No uncommitted conversion routes or custom scripts may bypass this CLI entry point.
2. **Runtime Provenance Enforcement**: Every corpus run must capture and retain a complete `provenance_record.json` as established in `FS-01` (product SHA, clean status, executable path, command, input classification, sidecar hash, exit code).
3. **Diagnostic Integrity**: `--ref-gp` must remain diagnostic-only; reference GP packages must never influence note generation, thresholds, or branch execution logic.
4. **No Special-Casing**: Production conversion code paths must not contain hardcoded filenames, bar numbers, fixed coordinates, score titles, or reference-GP literal values.
5. **Private Artifact Isolation**: Private score PDFs, reference GP files, and detailed execution logs must remain in ignored local working directories and must not be committed to Git.

---

## 5. Architectural Approval & Governance Next Steps

With this architecture phase complete:
- The canonical entry point `score2gp convert` is verified and reconciled.
- The call chain and evidence bounds are established for `FS-03`/`FS-04`.
- Governance PR branch `gov/promote-fs02-reconcile-entry-point` will be published on `tticom/score2gp-agentops` for independent Codex review and promotion.
