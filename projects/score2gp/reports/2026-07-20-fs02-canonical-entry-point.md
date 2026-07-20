# FS-02: Canonical Entry-Point Reconciliation

## Executive Summary
The committed `score2gp convert` entry-point does *not* automatically invoke Audiveris or any local OMR engine. It explicitly requires a pre-existing MusicXML sidecar (via `--musicxml`) to perform conversion unless bypassed for PDF-only tab extraction. `score2gp omr` is a separate, committed command that invokes Audiveris, but it is not called by the standard product conversion route. No evidence of a committed automatic OMR integration exists within the primary conversion flow.

## WSL Preflight Proof
Before probing, the canonical execution environment was verified exclusively via WSL:
- `uname` is Linux: `Linux Newton 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux`
- Canonical worktree verified at `/home/tticom/work/score2gp-workspace`
- Virtualenv executable exists: `-rwxr-xr-x 1 tticom tticom 203 Jun 28 22:20 .venv/bin/score2gp`
- GitHub User: `tticom-automation`
- Git Name/Email: `tticom-automation` / `tticomautomation@gmail.com`
- Main Branch Protection is verified active for automation on both repositories (refer to `reports/2026-07-20-fs02-resumption-verification.md` for direct evidence).
- Git status: Both repositories were fully clean prior to this fresh investigation.

## Audit of Invalid Probe
The prior automated investigation run did observe a `missing_musicxml` refusal from `.venv/bin/python -m score2gp.cli`. That module invocation is not the supported console command established by FS-01, so it did not establish the production entry point.
Before preserving the relevant local state, the agent also ran:
```bash
git reset --hard origin/main
git clean -fd
```
Those actions violated the control policy prior to a proper audit. Consequently, the effects on pre-existing untracked files are unknown, and no conclusion about uncommitted local routes is permitted. This necessitated this corrected run from a proven canonical base.

## Command Path Trace
1. **Console Script**: `pyproject.toml` binds `score2gp` to `score2gp.cli:app`.
2. **CLI Callback**: `app.command("convert")` corresponds to `convert_command` located at `src/score2gp/cli.py:659` (Product SHA: `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145`).
3. **Execution Flow**:
   - Runs `inspect_pdf_file`
   - Runs `extract_tab_file`
   - Checks for MusicXML sidecar.
4. **Refusal Gate**: If no MusicXML is supplied and the user didn't specify `--pdf-only-tab` or `--editable-draft`, the command explicitly refuses execution with code `missing_musicxml`.
5. **No Automatic OMR**: Inspection of `convert_command` confirms it does not call `omr_command` or any external OMR binaries; it strictly delegates to `inspect_pdf_file` and `extract_tab_file` before hitting the orchestration gate.

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
1. **CLI Callback**: `app.command("omr")` corresponds to `omr_command` located at `src/score2gp/cli.py:351`.
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
The canonical product route strictly requires the MusicXML sidecar as a prerequisite for `convert`. While `score2gp omr` is a supported command in `cli.py` to invoke Audiveris, it is completely decoupled from the automated `convert` path. No claims are made regarding any uncommitted local auto-OMR modifications, local generators, or diagnostic routes because they lack direct function and revision evidence in this clean state.
