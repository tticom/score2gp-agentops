# Post-CLI Release-Readiness Audit v0.1

This report presents the validation outcomes of the post-CLI release-readiness audit and outlines the current stability posture and recommended next milestones.

## Verdict
`CLI UX and unified convert pipeline verified; documentation and code aligned; product is ready for release scoping`

---

## Merged PRs verified
- **Product (`score2gp`)**:
  - Merged PR #172 (`feat: CLI UX Hardening and Unified Convert Pipeline v0.1`).
    - Merge Commit: `df3b328540af2bff2ff9e39e433fe44d2211b582`
  - Merged PR #173 (`docs: update convert examples to match hardened CLI options`).
    - Merge Commit: `c13541c4df2e212fa4e8bf9515efb31fe8793b89`
- **Agentops (`score2gp-agentops`)**:
  - Merged PR #43 (`research: CLI UX hardening and unified pipeline architecture v0.1`).
    - Merge Commit: `517fcf5ac68529bab8a17be696aebef1394c62cb`
  - Merged PR #44 (`record: CLI UX hardening and unified pipeline run v0.1`).
    - Merge Commit: `32cc3dce9cd61e3ad84128f73105fb55cb476686`

---

## CLI Hardening & Options Contract Alignment
The CLI `convert` command has been fully verified to comply with the unified contract rules:
- **Options Signature**: Explicitly supports `--pdf`, `--musicxml`, `--template`, `--out`, `--work-dir`, `--json-report`, and `--strict` / `--no-strict`.
- **Pipeline Preservation**: Sequentially groups and preserves stages: PDF coordinate inspection and extraction -> MusicXML preflight gating -> ScoreIR building -> GP package serialization and validation.
- **Refusal Exit-Code Mapping**:
  - `0`: Success.
  - `1`: General CLI parameter or missing input path/dependency.
  - `2`: PDF layout grouping refusal.
  - `3`: MusicXML timing/polyphony preflight refusal.
  - `4`: ASCII/MusicXML alignment compatibility refusal.
  - `5`: GP writing/validation failure.
- **Priority Exit Code Gating**: Correctly prioritizes ASCII categories so that `pdf_input_class_ascii_tab_requires_alignment` propagates exit code `4` (not `2`).
- **File Safety**: Atomic writes verify target output under a temporary file before moving it to `--out`. Pre-existing user output files are preserved on failure.
- **Strictness Exit Gating**: If no GP output is produced, the command always returns a non-zero exit code, even when `--no-strict` is specified.
- **JSON Summary Report**: Attempts to write a private-safe JSON report containing: `status`, `stage`, `exit_code`, `error_type`, `refusal_code`, `recommended_action`, `output_path`, `output_written`, `work_dir`, `diagnostics_paths`, `strict`, and counts.

---

## Documentation Consistency Audit
We conducted a comprehensive audit of all documentation files to ensure absolute alignment:
- **[docs/release-contract.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/release-contract.md)**: Accurately reflects current supported scopes, refusal rules, and milestones.
- **[docs/input-requirements.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/input-requirements.md)**: Matches current digital vector PDF and MusicXML preflight requirements.
- **[docs/sidecar-workflow.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/sidecar-workflow.md)**: Directs users on how to align PDFs with MusicXML.
- **[docs/intermediate-contracts.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/intermediate-contracts.md)**: Corrected to use the hardened `--pdf` and `--work-dir` signature.
- **[docs/workflow.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/workflow.md)**: Corrected to use the hardened `--pdf` and `--work-dir` signature.
- **[TESTING.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/TESTING.md)** and **[PRIVACY.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/PRIVACY.md)**: Verified as fully aligned with verification pipelines and private-safety practices.

---

## Validation Results
- **Public Tests**: `PYTHONPATH=. .venv/bin/pytest` -> **478 / 478 passed**
- **Private Smoke Test**: `PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py` -> **Completed successfully** against 12 private score booklets.
- **GP Quality Audit**: `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py` -> **Completed successfully**; stable note-matching metrics verified:
  - `private_input_1`: 153 / 153 matched
  - `private_input_custom_lesson_3`: 459 / 459 matched
  - `private_input_custom_lesson_4`: 546 / 546 matched
  - `private_input_custom_lesson_5`: 295 / 295 matched
  - `private_input_custom_lesson_6`: 235 / 235 matched
  - `private_input_custom_lesson_7`: 624 / 624 matched
  - `private_input_custom_melodic_soloing`: 82 / 82 matched

---

## Private-Safety Result
Running `git ls-files fixtures/private work` outputs exactly:
```text
fixtures/private/.gitkeep
```
No private PDF, MusicXML, GP, or generated audit details have leaked into the repository. The private-safety invariant is fully intact.

---

## Candidate next milestones

1. **Option A: Sidecar Acquisition Workflow v0.2**
   - *Description*: Build tools or automated helper scripts to easily generate/match MusicXML files from digital notation sheets.
2. **Option B: ASCII Alignment Sidecar Architecture**
   - *Description*: Develop a schema and automated calibrator to resolve layout and timing alignment for ASCII tabs without a full MusicXML sidecar, targeting inputs like `private_input_2` (e.g. CAGED shapes).
3. **Option C: OCR Integration and Scanned PDF Preflight**
   - *Description*: Research integrating Audiveris or custom OCR engines to extract text, coordinates, and lines from scanned/raster images.

---

## Recommended next milestone
**Option B: ASCII Alignment Sidecar Architecture**

### Why
Now that the born-digital vector PDF pipeline and CLI contract are hardened, the next major hurdle is addressing ASCII/character-based sheet tabs (like `private_input_2`), which currently fail gating checks (`pdf_input_class_ascii_tab_requires_alignment`). Designing a lightweight alignment sidecar schema will unlock these inputs without compromising the strict timing/voice structures of the core compiler.

---

## Stop conditions
- Product `main` is modified or dirty.
- Tests fail to pass.
- Private-safety check leaks files.
