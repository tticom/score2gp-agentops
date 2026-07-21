# FS-03C: Rootless Audiveris Runtime Probe

## 1. Scope

- **Task and exact outcome:** FS-03C evidence-only runtime probe testing Audiveris 5.7.0 as a standalone OMR route and conversion handoff in Ubuntu 24.04 WSL.
- **Baseline:** Product base SHA `df6e5c8178794f0ea7f98d69e069a1be3593f176`, AgentOps base SHA `e3b6185fdac8f4efeb41bd73ed8c8d228063f104`.
  - Executable: `/home/tticom/work/score2gp-workspace/score2gp-fs03c/.venv/bin/score2gp` (committed CLI executable)
  - OMR Dependency: `/home/tticom/work/score2gp-workspace/score2gp-fs03c/work/audiveris_probe/extracted/opt/audiveris/bin/Audiveris` (extracted Audiveris 5.7.0 launcher)
  - Import path: `/home/tticom/work/score2gp-workspace/score2gp-fs03c/src/score2gp`
  - Input class: PDF `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`
  - Sidecar provenance: Supplied via `score2gp omr` standalone generation using extracted Audiveris 5.7.0 x86_64 deb (SHA-256 `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`).
- **Changed files:**
  - `projects/score2gp/reports/2026-07-21-fs03c-rootless-audiveris-probe.md`
- **Non-goals:** Product source changes, pipeline timing repairs, and automatic OMR conversion integration are strictly excluded.

## 2. Claim Ledger

| Claim | Evidence inspected or command | Exact revision and input | Observed result | Limit or remaining unknown |
|---|---|---|---|---|
| Environment WSL identity | `uname -s`, `uname -m`, `/etc/os-release` | Local WSL | `Linux x86_64 Ubuntu 24.04` | Tested local WSL env only |
| Audiveris asset integrity | `wget` and `sha256sum -c` | `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` | Hash verified `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426` | N/A |
| Standalone OMR route | `.venv/bin/score2gp omr` execution with `--audiveris` launcher | Product `df6e5c81...` with `generated_standard_staff_whole_note.pdf` | OMR ran successfully, manifest reports `execution_status: success`, `validation_status: success`, wrote `.mxl` sidecar | Standalone `score2gp omr` artifact generation is **available** for this exact public fixture and runtime |
| Audiveris musical correctness | Manifest inspection | Wrote MXL artifact `generated_standard_staff_whole_note.mxl` | Wrote valid MXL file artifact | Musical correctness of generated MXL remains **unproven** |
| Explicit `convert --musicxml` handoff | `.venv/bin/score2gp convert --pdf ... --musicxml ...` | Product `df6e5c81...` with generated MXL sidecar | `status: refused`, `refusal_code: missing_pdf_grouping` with exit code 2 at stage `tabraw-import` | Explicit `convert --musicxml` handoff is **unproven** for PDFs with safe TAB grouping |

**Detailed Analysis of Handoff Refusal:**
The `missing_pdf_grouping` refusal arose at stage `tabraw-import` during PDF vector extraction. Diagnostics showed zero playable candidates, zero detected TAB systems/string lines/bar boxes in `generated_standard_staff_whole_note.pdf`. Because the refusal occurred during PDF grouping prior to timing alignment, the pipeline refusal cannot be attributed to the generated Audiveris MXL file.

## 3. Pre-submit Challenge

1. **What is the strongest way this could appear successful while failing the product outcome?** The OMR process succeeds and writes a valid MXL file, creating the illusion that conversion is complete.
2. **Which command, source inspection, generated artifact, or regression test rules that out?** Running the explicit `convert --musicxml` handoff proves that the pipeline refuses the input at `tabraw-import` due to `missing_pdf_grouping`.
3. **Which failure modes remain untested, and do they limit the claim?** Conversion using a PDF with safe TAB grouping remains untested; the handoff route is unproven for safe TAB PDFs.
4. **Is any assertion based only on fixture-specific coordinates, bar numbers, filenames, titles, reference GP data, aggregate counts, or file creation?** No. Findings are based on exact manifest execution statuses, JSON report exit codes, and refusal diagnostics.
5. **Does the evidence come from the exact remote head intended for review?** Under the local-preparation model, no remote branch exists by design. Evidence comes from the exact local handoff head on branch `agy/fs03c-rootless-audiveris-rerun`.

## 4. Validation And Handoff

Validation commands run:
- `wsl -d Ubuntu-24.04 gh auth status` (exit code 1, unauthenticated safety proof)
- `sha256sum -c` for downloaded DEB (verified `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`)
- `.venv/bin/score2gp omr tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out work/omr_out --audiveris work/audiveris_probe/extracted/opt/audiveris/bin/Audiveris` (success, exit 0)
- `.venv/bin/score2gp convert --pdf tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --musicxml work/omr_out/run_563c71320fd842998d932e85ae66337c/generated_standard_staff_whole_note.mxl --out work/omr_out/converted.gp --json-report work/omr_out/convert_report.json --work-dir work/convert_work` (refused: exit 2, stage `tabraw-import`, refusal_code `missing_pdf_grouping`)

No product files were changed. All probe artifacts remain isolated in ignored `work/` directory.

Local handoff state: LOCAL_HANDOFF_READY — awaiting Codex review
No remote branch or PR exists by design.
Unresolved risks: Convert pipeline refuses the test PDF at tabraw-import with missing_pdf_grouping; handoff accuracy on safe TAB PDFs remains unproven.
