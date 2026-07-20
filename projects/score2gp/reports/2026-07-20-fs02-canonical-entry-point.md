# FS-02: Canonical Entry-Point Reconciliation

## Executive Summary
The committed `score2gp convert` entry-point does *not* automatically invoke Audiveris or any local OMR engine. It explicitly requires a pre-existing MusicXML sidecar (via `--musicxml`) to perform conversion unless bypassed for PDF-only tab extraction. `score2gp omr` is a separate, committed command that invokes Audiveris, but it is not called by the standard product conversion route.

## Provenance Evidence
- **Repository**: `score2gp`
- **Product Commit SHA**: `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145`
- **Python Import Path**: `/home/tticom/work/score2gp-workspace/score2gp/src/score2gp`
- **Executable**: `-rwxr-xr-x 1 tticom tticom 203 Jun 28 22:20 .venv/bin/score2gp`

## Audit of Invalid Probe
An earlier automated investigation (the first FS-02 attempt) improperly bypassed the native entry point (invoking `.venv/bin/python -c ...` and `python -m score2gp.cli`), and executed destructive workspace commands (`git reset --hard` and `git clean -fd`) before validating the preflight state. This erased the uncommitted local state (including `report.json`) prior to a proper audit, necessitating this corrected run from a proven canonical base. The local state prior to preflight is therefore permanently unknown, and no claims can be made regarding the discarding of any uncommitted local auto-OMR modifications.

## Command Path Trace
1. **Console Script**: `pyproject.toml` binds `score2gp` to `score2gp.cli:app`.
2. **CLI Callback**: `app.command("convert")` corresponds to `convert_command` in `src/score2gp/cli.py`.
3. **Execution Flow**:
   - Runs `inspect_pdf_file`
   - Runs `extract_tab_file`
   - Checks for MusicXML sidecar.
4. **Refusal Gate**: If no MusicXML is supplied and the user didn't specify `--pdf-only-tab` or `--editable-draft`, the command explicitly refuses execution with code `missing_musicxml`.

## Controlled Native WSL Probe
**Command**:
```bash
.venv/bin/score2gp convert --pdf tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out work/probe/out.gp --work-dir work/probe --json-report work/probe/report.json
```

**Outcome (`work/probe/report.json`)**:
```json
{
  "child_python_executable_path": "/home/tticom/work/score2gp-workspace/score2gp/.venv/bin/python",
  "diagnostics_paths": {
    "diagnostics_json": null,
    "grouping_diagnostics_html": null,
    "symbol_attachment_diagnostics_html": null,
    "warnings_json": "work/probe/warnings.json"
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
  "work_dir": "work/probe"
}
```

## OMR Command Proof
While the `convert` command does not invoke OMR, the standalone `omr` command exists in the committed CLI interface.
1. **CLI Callback**: `app.command("omr")` corresponds to `omr_command` in `src/score2gp/cli.py`.
2. **Execution Flow**: It optionally accepts an `--audiveris` path, attempts a subprocess call to Audiveris, and writes a warning if unconfigured or failed.

**Command**:
```bash
.venv/bin/score2gp omr tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out work/probe_omr
```

**Output**:
```json
{
  "out": "/home/tticom/work/score2gp-workspace/score2gp/work/probe_omr",
  "warnings": [
    {
      "code": "audiveris-not-configured",
      "message": "Audiveris path was not provided."
    }
  ]
}
```

## Resolution
The canonical product route strictly requires the MusicXML sidecar as a prerequisite for `convert`. While `score2gp omr` is a supported command in `cli.py` to invoke Audiveris, it is completely decoupled from the automated `convert` path.
