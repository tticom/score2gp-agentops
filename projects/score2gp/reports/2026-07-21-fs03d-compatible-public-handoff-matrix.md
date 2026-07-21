# FS-03D: Compatible Public Sidecar-Handoff Matrix

## 1. Scope

- **Task and exact outcome:** FS-03D evidence-only probe evaluating Audiveris 5.7.0 rootless OMR sidecar generation and explicit `convert --musicxml` handoff across compatible public fixtures with safe PDF grouping.
- **Baseline:** Product base SHA `df6e5c8178794f0ea7f98d69e069a1be3593f176`, AgentOps base SHA `b16cf9135048cf76efae1eecae8943df49520e50`.
  - Executable: `/home/tticom/work/score2gp-workspace/score2gp-fs03d-worktree/.venv/bin/score2gp`
  - OMR Dependency: `/home/tticom/work/score2gp-workspace/score2gp-fs03d-worktree/work/fs03d_probe/extracted/opt/audiveris/bin/Audiveris` (extracted Audiveris 5.7.0 Ubuntu 24.04 x86_64 deb, SHA-256 `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`)
  - Import path: `/home/tticom/work/score2gp-workspace/score2gp-fs03d-worktree/src/score2gp`
- **Changed files:**
  - `projects/score2gp/reports/2026-07-21-fs03d-compatible-public-handoff-matrix.md`
  - `projects/score2gp/ACTIVE_TASK.md`
- **Non-goals:** Product source changes, pipeline timing repairs, automatic OMR invocation from `convert`, and musical correctness assertions are strictly excluded.

## 2. Per-Candidate Probe Matrix

| Candidate PDF | PDF SHA-256 | TabRaw Grouping Status | Playable / Assigned Candidates | OMR Execution & Sidecar SHA-256 | Convert Exit & Stage | Output Written | Classifications |
|---|---|---|---|---|---|---|---|
| `generated_paired_notation_tab_system.pdf` | `31669e6c...` | `pdf_grouping_complete` (grouped, safe=true) | 4 playable / 4 assigned (1 system, 1 staff, 2 bar boxes, 6 strings) | `success`, Sidecar `60513163...` | Exit `0`, stage `gp-write`, refusal `null` | `true` (`converted.gp`) | `compatible_pdf`, `artifact_available`, `handoff_observed`, `handoff_supported` |
| `generated_paired_notation_tab_system_double_barline.pdf` | `307df45e...` | `pdf_grouping_complete` (grouped, safe=true) | 4 playable / 4 assigned (1 system, 1 staff, 2 bar boxes, 6 strings) | `success`, Sidecar `bb1b8c9d...` | Exit `0`, stage `gp-write`, refusal `null` | `true` (`converted.gp`) | `compatible_pdf`, `artifact_available`, `handoff_observed`, `handoff_supported` |

### Detailed Candidate Results

#### Candidate 1: `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`
1. **`extract-tab`**:
   - PDF SHA-256: `31669e6c264ed6e48423c0901f853e7fa93564fd0aa60cdc4189c53a8796dcad`
   - 4 playable fret candidates extracted (all 4 assigned system 1, staff 1, string lines 1-6, bars 1-2).
   - Layout: 1 system, 1 staff, 2 bar boxes, 6 string lines.
   - Status: `pdf_grouping_complete` (safe grouping = `true`). No unsafe grouping warning codes.
2. **`score2gp omr`**:
   - Manifest: `execution_status: success`, `discovery_status: success`, `validation_status: success`, `refusal_code: null`.
   - Sidecar MXL SHA-256: `60513163944c74dc2b99c67776d619df33195ff935834c8fde8859dada815afe`
3. **`score2gp convert --musicxml`**:
   - Command: `.venv/bin/score2gp convert --pdf tests/fixtures/pdf/generated_paired_notation_tab_system.pdf --musicxml <sidecar.mxl> --out work/cand1/converted.gp --json-report work/cand1/convert_report.json --work-dir work/cand1/convert_work`
   - Result: Exit `0`, status `success`, stage `gp-write`, refusal_code `null`.
   - `output_written`: `true` (`work/cand1/converted.gp`).
   - Timing issues: `0`.
   - First remaining warning: `tab-candidate-unused` (or `info_pdf_barline_too_short`).

#### Candidate 2: `tests/fixtures/pdf/generated_paired_notation_tab_system_double_barline.pdf`
1. **`extract-tab`**:
   - PDF SHA-256: `307df45e57bad8b9539cca846265ddfb972a2aaae7264b7197dec1d880c954e2`
   - 4 playable fret candidates extracted (all 4 assigned system 1, staff 1, string lines 1-6, bars 1-2).
   - Layout: 1 system, 1 staff, 2 bar boxes, 6 string lines.
   - Status: `pdf_grouping_complete` (safe grouping = `true`). No unsafe grouping warning codes.
2. **`score2gp omr`**:
   - Manifest: `execution_status: success`, `discovery_status: success`, `validation_status: success`, `refusal_code: null`.
   - Sidecar MXL SHA-256: `bb1b8c9dcb5b9a55d9c52d46ab7e9cd283de3db05950ec8543bf22747d67f05f`
3. **`score2gp convert --musicxml`**:
   - Command: `.venv/bin/score2gp convert --pdf tests/fixtures/pdf/generated_paired_notation_tab_system_double_barline.pdf --musicxml <sidecar.mxl> --out work/cand2/converted.gp --json-report work/cand2/convert_report.json --work-dir work/cand2/convert_work`
   - Result: Exit `0`, status `success`, stage `gp-write`, refusal_code `null`.
   - `output_written`: `true` (`work/cand2/converted.gp`).
   - Timing issues: `0`.
   - First remaining warning: `tab-candidate-unused` (or `info_pdf_barline_too_short`).

## 3. Claim Ledger

| Claim | Evidence inspected or command | Exact revision and input | Observed result | Limit or remaining unknown |
|---|---|---|---|---|
| Environment WSL identity | `uname -s`, `uname -m`, `/etc/os-release` | Local WSL | `Linux x86_64 Ubuntu 24.04` | Tested local WSL env only |
| Audiveris asset integrity | `sha256sum -c` | `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` | Verified `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426` | N/A |
| Candidate 1 PDF compatibility | `extract-tab` | `generated_paired_notation_tab_system.pdf` | `pdf_grouping_complete`, 4 playable candidates assigned, safe=true | `compatible_pdf` |
| Candidate 1 OMR artifact | `score2gp omr` | `generated_paired_notation_tab_system.pdf` | Manifest `success`, wrote `.mxl` | `artifact_available` |
| Candidate 1 convert handoff | `score2gp convert --musicxml` | `generated_paired_notation_tab_system.pdf` + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `output_written: true` | `handoff_supported` |
| Candidate 2 PDF compatibility | `extract-tab` | `generated_paired_notation_tab_system_double_barline.pdf` | `pdf_grouping_complete`, 4 playable candidates assigned, safe=true | `compatible_pdf` |
| Candidate 2 OMR artifact | `score2gp omr` | `generated_paired_notation_tab_system_double_barline.pdf` | Manifest `success`, wrote `.mxl` | `artifact_available` |
| Candidate 2 convert handoff | `score2gp convert --musicxml` | `generated_paired_notation_tab_system_double_barline.pdf` + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `output_written: true` | `handoff_supported` |

## 4. Pre-submit Challenge

1. **What is the strongest way this could appear successful while failing the product outcome?** An `.mxl` sidecar and `.gp` output file are written, creating the appearance of conversion without proving musical correctness.
2. **Which command, source inspection, generated artifact, or regression test rules that out?** We verify that `handoff_supported` is assigned strictly because exit code is 0, refusal code is null, and output_written is true. Provenance notes state this is command-run handoff provenance, not proof of musical equivalence.
3. **Which failure modes remain untested, and do they limit the claim?** Complex multi-page or polyphonic scores (such as `Lesson-5.pdf`) produce timing risks; musical accuracy of Audiveris glyph recognition on complex scores remains unproven.
4. **Is any assertion based only on fixture-specific coordinates, bar numbers, filenames, titles, reference GP data, aggregate counts, or file creation?** No. Assertions rely on exact CLI exit codes, manifest statuses, JSON report fields, and diagnostic flags.
5. **Does the evidence come from the exact remote head intended for review?** Under the local-preparation model, no remote branch exists by design. Evidence comes from the exact local handoff head on branch `agy/fs03d-public-handoff-matrix`.

## 5. Validation And Handoff

Validation commands run:
- `wsl -d Ubuntu-24.04 gh auth status` (exit code 1, unauthenticated safety proof)
- `sha256sum -c` for Audiveris DEB asset (verified)
- Candidate 1 `extract-tab`, `omr`, `convert --musicxml` (all exit 0, output written)
- Candidate 2 `extract-tab`, `omr`, `convert --musicxml` (all exit 0, output written)

No product files were changed. All probe artifacts remain isolated in ignored `work/` directory.

Local handoff state: LOCAL_HANDOFF_READY — awaiting Codex review
No remote branch or PR exists by design.
