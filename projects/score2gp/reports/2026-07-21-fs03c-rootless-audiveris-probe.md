# FS-03C: Rootless Audiveris Runtime Probe

## 1. Scope

- **Task and exact outcome:** FS-03C evidence-only runtime probe testing Audiveris 5.7.0 as a standalone OMR route and conversion handoff in Ubuntu 24.04 WSL.
- **Baseline:** Product base SHA `df6e5c8178794f0ea7f98d69e069a1be3593f176`, AgentOps base SHA `e3b6185fdac8f4efeb41bd73ed8c8d228063f104`.
  - Executable: `/home/tticom/work/score2gp-workspace/score2gp-fs03c/work/audiveris_probe/extracted/opt/audiveris/bin/Audiveris`
  - Import path: `/home/tticom/work/score2gp-workspace/score2gp-fs03c/src/score2gp`
  - Input class: PDF `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`
  - Sidecar provenance: Supplied via `score2gp omr` standalone generation using extracted Audiveris 5.7.0 x86_64 deb (SHA-256 `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`).
- **Changed files:**
  - `projects/score2gp/reports/2026-07-21-fs03c-rootless-audiveris-probe.md`
  - `projects/score2gp/ACTIVE_TASK.md`
- **Non-goals:** Product source changes, pipeline timing repairs, and automatic OMR conversion integration are strictly excluded.

## 2. Claim Ledger

| Claim | Evidence inspected or command | Exact revision and input | Observed result | Limit or remaining unknown |
|---|---|---|---|---|
| Environment WSL identity | `uname -s`, `uname -m`, `/etc/os-release` | Local WSL | `Linux x86_64 Ubuntu 24.04` | Tested local WSL env only |
| Audiveris asset integrity | `wget` and `sha256sum -c` | `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` | Hash verified `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426` | N/A |
| Audiveris runtime available | `dpkg-deb -x` and standalone `.venv/bin/score2gp omr` execution | Product `df6e5c81...` with `generated_standard_staff_whole_note.pdf` | OMR ran successfully, manifest reports `execution_status: success`, `validation_status: success` | Sidecar generation does not prove musical correctness |
| MusicXML handoff accepted by convert | `score2gp convert --pdf ... --musicxml ...` | Product `df6e5c81...` | `status: refused`, `refusal_code: missing_pdf_grouping` with exit code 2 | Route is classified as `unavailable` because convert refuses the grouped PDF/MusicXML |

**Classification:** The OMR standalone route is available locally but the resulting `convert` handoff is **unavailable** (refused due to `missing_pdf_grouping`).

## 3. Pre-submit Challenge

1. **What is the strongest way this could appear successful while failing the product outcome?** The OMR process succeeds and writes a valid MXL file, creating the illusion that conversion is complete.
2. **Which command, source inspection, generated artifact, or regression test rules that out?** Running the explicit `convert --musicxml` handoff proves that the pipeline refuses the generated output with `missing_pdf_grouping`.
3. **Which failure modes remain untested, and do they limit the claim?** We did not test any other PDF or manually attempt to fix the grouping risk. The claim correctly stops at classifying the route as unavailable.
4. **Is any assertion based only on fixture-specific coordinates, bar numbers, filenames, titles, reference GP data, aggregate counts, or file creation?** No. The failure is a documented refusal code directly from the product runtime.
5. **Does the evidence come from the exact remote head intended for review?** Yes, local branch head matches report.

## 4. Validation And Handoff

Validation commands run:
- `wsl -d Ubuntu-24.04 gh auth status` (exit code 1)
- `sha256sum -c` for downloaded DEB (verified)
- `score2gp omr` standalone (success)
- `score2gp convert` handoff (refused: exit 2, missing_pdf_grouping)

No product files were changed. Artifacts remain isolated in ignored `work/` directory.

PR state: LOCAL_HANDOFF_READY — awaiting independent review
Unresolved risks: Convert pipeline refuses the generated Audiveris MusicXML output with missing_pdf_grouping.
