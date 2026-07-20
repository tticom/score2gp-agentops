# FS-02: Canonical Entry-Point Reconciliation

## Executive Summary
The committed `score2gp convert` entry-point does *not* automatically invoke Audiveris or any local OMR engine. It explicitly requires a pre-existing MusicXML sidecar (via `--musicxml`) to perform conversion unless bypassed for PDF-only tab extraction. The uncontrolled local auto-OMR paths are not part of the committed pipeline. Therefore, the product claims regarding automatic OMR from PDF directly to GP cannot be supported by the current committed codebase.

## Provenance Evidence
- **Repository**: `score2gp`
- **Product Commit SHA**: `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145`
- **Python Import Path**: `/home/tticom/work/score2gp-workspace/score2gp/src/score2gp`
- **Executable**: `/home/tticom/work/score2gp-workspace/score2gp/.venv/bin/python`

## Command Path Trace
1. **Console Script**: `pyproject.toml` binds `score2gp` to `score2gp.cli:app`.
2. **CLI Callback**: `app.command("convert")` corresponds to `convert_command` in `src/score2gp/cli.py`.
3. **Execution Flow**:
   - Runs `inspect_pdf_file`
   - Runs `extract_tab_file`
   - Checks for MusicXML sidecar.
4. **Refusal Gate**: If no MusicXML is supplied and the user didn't specify `--pdf-only-tab` or `--editable-draft`, the command explicitly refuses execution with code `missing_musicxml`.

## Controlled Native Probe
**Command**:
```bash
.venv/bin/python -m score2gp.cli convert --pdf tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out out.gp --work-dir work --json-report report.json
```

**Outcome**:
```json
{
  "child_python_executable_path": "/home/tticom/work/score2gp-workspace/score2gp/.venv/bin/python",
  "diagnostics_paths": {
    "diagnostics_json": null,
    "grouping_diagnostics_html": null,
    "symbol_attachment_diagnostics_html": null,
    "warnings_json": "work/warnings.json"
  },
  "error_type": "ValueError",
  "exit_code": 1,
  "musicxml_sidecar_info": {
    "provenance": "absent"
  },
  "output_path": null,
  "output_written": false,
  "python_import_path": "/home/tticom/work/score2gp-workspace/score2gp/src/score2gp",
  "recommended_action": "Provide a matching MusicXML sidecar before attempting build-ir.",
  "refusal_code": "missing_musicxml",
  "stage": "orchestration-gate",
  "status": "refused",
  "strict": true,
  "summary_counts": {},
  "work_dir": "work"
}
```

## Resolution
The uncontrolled local route that previously bypassed this gate or silently generated MusicXML via local OMR is discarded, as it was never committed into the verifiable `score2gp` package. The real product route requires the MusicXML sidecar as a prerequisite for `convert`.

FS-02 is complete. This finding safely unblocks FS-03/FS-04 where we can trace actual divergence once sidecars are explicitly provided (or handled appropriately by the harness).
