# Post-Documentation Milestone Verification v0.1

This report presents the final verification outcomes of the `score2gp` release-hardening documentation milestone and defines the recommended next milestones.

## Verdict
`documentation milestone verification passed; release contract is active; CLI UX hardening recommended as next milestone`

---

## Merged PRs verified
* **Product (`score2gp`)**: Merged PR #171 (`docs: add release contract and sidecar workflow`) into `main`.
  * Commit SHA: `88e13b28859ff7b5fa38cc3c10886b6a22cc3c7d`
* **Agentops (`score2gp-agentops`)**: Merged PR #40 (`research: release hardening and sidecar workflow v0.1`) and PR #41 (`run: release hardening documentation milestone`).
  * Commit SHA: `d528f44cf6ee8dfad9d71c4c1a7d653ccfe6dc9c`

---

## Current release contract status
The release contract is **active and enforced**. The five new documentation files establish the quality, privacy, and support gates for version v0.1.
* **Supported Inputs**: Digital vector PDFs with standard six-line tab staves and vertical barlines + matching MusicXML sidecar.
* **Refusal Rules**: Untimed inputs, scanned/raster PDFs, ASCII tabs without alignment, and overlapping polyphony are rejected cleanly by the preflight gates.
* **Privacy Controls**: Private score assets and work outputs are completely gitignored.

---

## Validation results
* **Public Tests**: `PYTHONPATH=. .venv/bin/python3 -m pytest` -> **467 / 467 passed**
* **Private Smoke Test**: `PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py` -> **Completed successfully** against 12 private score booklets.
* **GP Quality Audit**: `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py` -> **Completed successfully**; stable note-matching metrics verified:
  * `private_input_1`: 153 / 153 matched
  * `private_input_custom_lesson_3`: 459 / 459 matched
  * `private_input_custom_lesson_4`: 546 / 546 matched
  * `private_input_custom_lesson_5`: 295 / 295 matched
  * `private_input_custom_lesson_6`: 235 / 235 matched
  * `private_input_custom_lesson_7`: 624 / 624 matched
  * `private_input_custom_melodic_soloing`: 82 / 82 matched

---

## Private-safety result
Running `git ls-files fixtures/private work` outputs exactly:
```text
fixtures/private/.gitkeep
```
The private-safety invariant is fully intact.

---

## Documentation consistency check
All five required documentation files exist and are verified as accurate in relation to the current codebase:
* **[docs/release-contract.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/release-contract.md)**: Accurately maps the support scope, milestone metrics, and refusal codes.
* **[docs/input-requirements.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/input-requirements.md)**: Specifies the geometry rules for drawn staves and the timing preflight checks for MusicXML.
* **[docs/sidecar-workflow.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/sidecar-workflow.md)**: Documents naming, pairing, and troubleshooting directions.
* **[TESTING.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/TESTING.md)**: Standardizes verification commands and PR description requirements.
* **[PRIVACY.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/PRIVACY.md)**: Specifies rules for local-only folders and redacted summaries.

---

## Remaining known limitations
* **No OCR/Raster Support**: Scan sheets and image-based PDFs remain unsupported.
* **No Sidecarless ASCII Conversion**: Cannot automatically convert ASCII sheet text without a pre-constructed alignment mapping.
* **Unsupported Polyphony**: Complex overlapping track structures are rejected by preflight.

---

## Candidate next milestones

1. **Option A: Sidecar Acquisition Workflow v0.2**
   * *Description*: Develop automated or guided tooling to ease matching/generating MusicXML files from digital notation sheets, enabling developers to import more real-world scores into the pipeline.
2. **Option B: Release Packaging and CLI UX Hardening**
   * *Description*: Consolidate the multi-stage pipeline commands into a robust, unified `convert` CLI interface. Enhance error reporting, handle missing external binaries (e.g. Audiveris) gracefully, and build a demonstrable workflow for the current release scope.
3. **Option C: ASCII Alignment Sidecar Architecture**
   * *Description*: Develop standard schemas and automation to map ASCII column positions to notation onsets, prioritizing compatibility for `private_input_2` (e.g. CAGED shapes).

---

## Recommended next milestone
**Option B: Release Packaging and CLI UX Hardening**

### Why
Now that the core conversion gates, grace note support, and validation logic are fully stable for the current release class, the project should focus on making this milestone usable and demonstrable. 

Consolidating the disjointed CLI stages (inspecting, OMR, extracting, building IR, writing GP, validating) into a hardened, user-friendly `convert` command with explicit user-facing troubleshooting tips and diagnostic output will provide a solid, clean, and reliable interface before attempting to scale inputs or support complex ASCII shapes.

---

## Stop conditions
* Product `main` is modified or dirty.
* Tests fail to pass.
* Private-safety check leaks files.

---

## Next prompt
```markdown
Title: CLI UX Hardening and Unified Pipeline v0.1

Goal:
Implement a hardened, unified CLI 'convert' pipeline that groups the individual extraction and alignment stages, handles missing dependencies gracefully, and provides clear user-facing guidance.
```
