# CLI UX Hardening and Unified Convert Pipeline v0.1

Harden the `score2gp convert` command and establish a unified conversion pipeline in the product repository.

Requirements:
1. Support explicit options: `--pdf`, `--musicxml`, `--template`, `--out`, `--work-dir`, `--json-report`, and `--strict` / `--no-strict`.
2. Preserve pipeline ordering: PDF inspection/extraction, MusicXML preflight/gating, ScoreIR build, GP package write/validation.
3. Map exit codes based on category of BuildIrInputRiskError:
   - 0: Success
   - 1: Missing input/path/dependency failure
   - 2: PDF layout/grouping refusal
   - 3: MusicXML timing/polyphony refusal
   - 4: ASCII/MusicXML alignment compatibility refusal
   - 5: GP writing/validation failure
4. Patch exit-code priority so `pdf_input_class_ascii_tab_requires_alignment` maps to exit code 4, not 2.
5. Write GP output to a temporary file under `--work-dir`, validate it, and move to `--out` only on success. Protect pre-existing output files on failure.
6. Ensure `--no-strict` still exits non-zero if no valid GP package is produced.
7. Write private-safe JSON report containing: status, stage, exit_code, error_type, refusal_code, recommended_action, output_path, output_written, work_dir, diagnostics_paths, strict, and summary counts.
