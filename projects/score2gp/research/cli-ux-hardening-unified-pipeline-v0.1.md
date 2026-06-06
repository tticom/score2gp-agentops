# CLI UX Hardening and Unified Pipeline Architecture v0.1

This document investigates the current CLI entry points and designs a hardened, unified `convert` command that respects the release contract, propagates exit codes, and provides clear user-facing refusal guidance.

## Verdict
`unified convert command architecture defined; exit code propagation and strict preflight gating designed`

---

## Current CLI surface

The `score2gp` command-line entry point is defined in [pyproject.toml](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/pyproject.toml#L24-L25) as `score2gp = "score2gp.cli:app"`.

The current CLI commands registered in [src/score2gp/cli.py](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/cli.py) are:
1. **GP Package Inspection**: `inspect-gp`, `validate`, `compare`.
2. **ScoreIR Validation**: `validate-ir`, `compare-ir`, `export-schema`.
3. **Execution Packages**: `write-gp`, `validate-roundtrip`, `batch`, `diagnose`.
4. **Pipeline Stage Diagnostics**: `inspect-pdf`, `extract-tab`, `omr`, `build-ir`, `align-ascii-musicxml`, `convert`.

---

## Current pipeline stages

To convert a PDF to a Guitar Pro package, the following pipeline stages are chained sequentially:

1. **inspect-pdf**: Renders pages and extracts text coordinates.
2. **extract-tab**: Groups six staff lines, barlines, and Snug-Fits fret candidate characters into `tabraw.json`.
3. **align-ascii-musicxml** *(optional)*: For ASCII inputs, aligns character column layout with MusicXML onsets.
4. **build-ir**: Performs MusicXML timing preflight checks, aligns candidates, and builds `score.ir.json` plus `diagnostics.json`.
5. **write-gp**: Serializes the `ScoreIR` JSON to a Guitar Pro 7 package using template profiles.

### Existing convert command gaps
Although a `convert` command exists in `src/score2gp/cli.py`, it has several limitations:
1. **Exit Code Suppression**: When `build-ir` raises a `BuildIrInputRiskError` (e.g. due to layout or timing risks), `convert` catches the error, writes diagnostics, but returns `None` (exiting with code `0` instead of a non-zero error code).
2. **No Custom JSON Summary**: There is no `--json-report` flag to write a clean consolidated execution summary to a user-specified path outside the workspace directories.
3. **No Strict Control**: There is no `--strict` / `--no-strict` switch to enable or disable immediate termination on timing/grouping warning risks.
4. **Inconsistent Arguments**: The arguments use `--workdir` instead of the standard `--work-dir`.

---

## Recommended convert command contract

The unified `convert` command should feature the following signature:

```bash
score2gp convert \
  --pdf <input_pdf> \
  --musicxml <input_musicxml> \
  --out <output_gp> \
  --work-dir <work_directory> \
  --json-report <json_report_path> \
  --strict
```

### Options contract
* `--pdf <path>`: Path to the born-digital vector PDF.
* `--musicxml <path>` / `-m`: Optional path to the matching MusicXML/MXL sidecar.
* `--out <path>` / `-o`: Output path for the serialized Guitar Pro (`.gp`) file.
* `--work-dir <path>`: Directory where intermediate artifacts (ScoreIR, TabRaw, diagnostic HTML/JSON) are saved.
* `--json-report <path>`: Path to write a private-safe consolidated JSON execution summary.
* `--strict`: Boolean flag (defaults to `True`) to enforce strict non-zero exit codes on timing or grouping preflight refusals.

---

## Supported success path

When all preflight timing and layout checks succeed:
1. The PDF candidate coordinates are extracted and grouped.
2. The MusicXML timing preflight succeeds.
3. `ScoreIR` and `diagnostics.json` are written to `--work-dir`.
4. A valid Guitar Pro package is written to `--out`.
5. A consolidated execution summary is written to `--json-report`.
6. Command exits with status code `0`.

---

## Unsupported/refusal behaviour

When preflight validation fails or inputs are unsupported:
1. The conversion halts immediately at the failing stage.
2. No Guitar Pro file is written to `--out` (preventing corrupt or misleading outputs).
3. The diagnostics JSON and HTML reports are written to `--work-dir`.
4. A clean error message (containing the refusal code and recommended action) is outputted to stderr.
5. The execution summary is written to `--json-report`.
6. Command exits with a specific non-zero exit code based on the refusal category.

---

## Exit-code proposal

We propose a stable set of exit codes for the conversion CLI:
* **`0`**: Success.
* **`1`**: General CLI parameter or environment error (e.g. input PDF not found).
* **`2`**: PDF layout grouping refusal (e.g. scanned PDF, missing barlines, or incomplete systems).
* **`3`**: MusicXML timing or polyphony validation refusal.
* **`4`**: ASCII/MusicXML alignment compatibility refusal.
* **`5`**: GP package serialization/validation failure.

---

## Architecture recommendation

### Smallest Next Product Implementation Task

Harden the CLI `convert` command to support standard report paths and propagate preflight refusal exit codes under strict validation.

* **Branch Name**: `feature/cli-ux-hardening-unified-pipeline-v0.1`
* **Affected Files/Modules**:
  * [src/score2gp/cli.py](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/src/score2gp/cli.py)
* **Goal**: Update `convert` command parameters to support `--work-dir`, `--json-report`, and `--strict`, and ensure that timing/grouping refusals propagate correct non-zero exit codes.
* **Non-goals**:
  * Do not change OCR or OMR capabilities.
  * Do not modify underlying alignment or preflight checking logic.
  * Do not write mock GP packages on failure.
* **Implementation Approach**:
  1. **Modify CLI Parameters**:
     * Add `work_dir` (as an option with alias `workdir`).
     * Add `json_report` (optional Path).
     * Add `strict` (bool, default `True`).
  2. **Check Arguments**: Validate that `--pdf` and `--out` exist and are provided (exit code `1` if missing).
  3. **Map Refusal Exit Codes**:
     * Catch `BuildIrInputRiskError` inside `convert_command`.
     * Write diagnostics payload to `work-dir`.
     * If `strict` is enabled, map the exception category to the correct exit code:
       * PDF layout/grouping codes -> exit code `2`.
       * MusicXML timing/polyphony codes -> exit code `3`.
       * ASCII alignment status codes -> exit code `4`.
     * Raise `typer.Exit(code)`.
  4. **Consolidated Summary**: Compilation of a private-safe JSON summary written to the path specified by `--json-report`.
* **Tests required**:
  * Verify help options for `convert` are documented.
  * Verify missing input paths raise exit code `1`.
  * Verify PDF grouping failures return exit code `2`.
  * Verify MusicXML timing preflight failures return exit code `3`.
  * Verify correct execution (exit code `0`) on a public synthetic PDF fixture.
* **Validation commands**:
  ```bash
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
  PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
  git ls-files fixtures/private work
  git diff --check
  ```
* **Acceptance Criteria**:
  * All public tests pass.
  * Private-safety invariant check outputs exactly `fixtures/private/.gitkeep`.
  * Command exits with correct codes on supported and unsupported inputs.
* **Stop conditions**:
  * Any public test fails.
  * Untracked generated outputs are checked into Git.
* **Reporting format**:
  ```text
  Verdict:
  Branch:
  Commit hash:
  Files changed:
  Documentation summary:
  Commands run:
  Test results:
  Private-safety result:
  Known limitations:
  Next recommended task:
  ```

---

## Privacy/artifact constraints
* The CLI execution summary and reports must remain private-safe (anonymized labels, no song titles/metadata, and no raw candidate dumps).
* Output packages and work folders must remain inside the gitignored `work/` directory.

## Stop conditions
* Product `main` is dirty or has uncommitted modifications.
* Public tests fail before starting research.
* The safety invariant fails.

## Known limitations
* Conversion requires matching MusicXML files (no automated duration extraction from PDF lines).
* CLI does not automatically run external Audiveris binaries unless paths are explicitly configured.
