# FS-03E: Sidecar-to-ScoreIR Event-Loss Trace (Revised Canonical Handoff)

**Authorised Role**: Architect, Tier B evidence-only
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`
**Date**: 2026-07-22
**Agy Local Evidence Commits**: `4a0dd9c3bde0c1332d2d58dce89d7ad46d78ea89`, `23c7e6bd2ea2ae34227e63f20920041831aeccb4`, and `5ed1a08b9af7e7151d87e8547f12fa79e30ea1bb` on branch `agy/fs03e-event-loss-trace`
**Product Local Head**: `df6e5c8178794f0ea7f98d69e069a1be3593f176` (branch `agy/fs03e-event-loss-trace-product`)
**Worktree-Local Python Interpreter**: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv/bin/python`
**Canonical CLI Executable**: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv/bin/score2gp`

---

## 1. Executive Summary & Context

Governance task **FS-03E** is an Architect, Tier B evidence-only trace investigation. Its goal is to locate the first observable boundary at which MusicXML or TAB evidence yields zero ScoreIR events during explicit sidecar conversion.

### Scope and Canonical Setup
1. A worktree-local ignored `.venv` was established inside the product worktree (`/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv`).
2. The exact checked-out product revision (`df6e5c8178794f0ea7f98d69e069a1be3593f176`) was installed into it via `pip install -e .`.
3. All reruns of `omr` and `convert` were executed strictly via `.venv/bin/score2gp` (without invoking `python -m score2gp.cli`).
4. All inspection commands were executed as one-shot inline commands without creating persistent analysis scripts.

### Key Observed Finding
1. **First Observable Boundary**: The first observable MusicXML note-bearing boundary is **already zero** (`<note>` element count = 0 inside the generated `.mxl` archive).
2. **No Observed Internal Audiveris Transition**: Because Audiveris 5.7.0 execution occurs within an external black box process, no non-zero-to-zero transition inside Audiveris was directly observed.
3. **Causal Uncertainty**: The cause of zero notes in the Audiveris MusicXML output remains **unproven**. It may be attributable to Audiveris OMR recognition capabilities, the specific visual layout of paired standard-notation + TAB systems, or unsupported engine/input runtime conditions.
4. **Direct Zero-Input Propagation**: Downstream `score2gp` modules (`parse_musicxml`, `build_ir_with_diagnostics_from_imports`, `_measure_events`) propagate the zero-input sidecar as directly observed (0 parsed `MusicXmlNote` objects -> 0 note groups -> `event_count: 0`). Beyond this directly observed zero-input propagation, no broader claim is made regarding component design or performance.

---

## 2. Environment Verification & Asset Identity

### Safety Boundary Verification
1. `gh auth status` executed in WSL: **failed with exit code 1 (unauthenticated)**. No remote Git or GitHub API operations were performed.
2. Existing local `agy/` worktrees preserved:
   - AgentOps: `/home/tticom/work/score2gp-workspace/score2gp-agentops-agy-fs03e-trace`
   - Product: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace`
3. Audiveris 5.7.0 Ubuntu 24.04 package verified in product directory `work/fs03e_trace/`:
   - Asset: `Audiveris-5.7.0-ubuntu24.04-x86_64.deb`
   - Verified SHA-256: `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`
   - Executable path: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/work/fs03e_trace/extracted/opt/audiveris/bin/Audiveris`

---

## 3. Boundary Count Matrix (Canonical Conversion Route)

All counts below reflect the canonical CLI route `.venv/bin/score2gp` executed in ignored directories (`work/fs03e_canonical_rerun/cand1` and `work/fs03e_canonical_rerun/cand2`), inspecting `convert_work/tab/tab_raw.json` and `.mxl` sidecars directly.

| Boundary / Stage | Metric / Observable Field | Fixture 1: `generated_paired_notation_tab_system.pdf` | Fixture 2: `generated_paired_notation_tab_system_double_barline.pdf` | Observed Status |
|---|---|---|---|---|
| **PDF Input** | File SHA-256 | `31669e6c264ed6e48423c0901f853e7fa93564fd0aa60cdc4189c53a8796dcad` | `307df45e57bad8b9539cca846265ddfb972a2aaae7264b7197dec1d880c954e2` | Input Available |
| **Conversion TabRaw** | Extracted playable fret candidates (`tab_raw.json`) | 3 playable candidates | 2 playable candidates | Non-Zero Evidence |
| **TabRaw Candidate Safety** | Candidate-level `raw.safe_grouping` | `false` (all 3 candidates) | `false` (both 2 candidates) | `safe_grouping: false` |
| **Conversion Grouping Gate** | Grouping gate refusal status | Reached gate without layout refusal (`pdf_grouping_complete` info warning) | Reached gate without layout refusal (`pdf_grouping_complete` info warning) | Gate Reached |
| **Audiveris OMR CLI** | `.venv/bin/score2gp omr` | `execution_status: success`, `validation_status: success` | `execution_status: success`, `validation_status: success` | Manifest Success |
| **Audiveris MXL Sidecar** | MXL Sidecar SHA-256 | `a6698f6ec6667f9990a02ae4306892dd1f42066666c941f066dd73bca1634ec7` | `6993925d7050972479a4f3c478355056d5453ffc57f0048213f22c161f7b8cff` | File Created |
| **MusicXML XML Root** | Root Element Tag | `<score-partwise>` (count = 1) | `<score-partwise>` (count = 1) | Root Present |
| **MusicXML Part List** | `<part>` element count | 2 (`P1: Voice`, `P2: Voice`) | 2 (`P1: Voice`, `P2: Voice`) | Structure Present |
| **MusicXML Measures** | Total `<measure>` count | 2 (1 measure in P1, 1 measure in P2) | 2 (1 measure in P1, 1 measure in P2) | Structure Present |
| **MusicXML Note Tags** | `<note>` element count | **0** | **0** | **FIRST OBSERVABLE BOUNDARY IS ZERO** |
| **MusicXML Pitched Notes** | `<note>/<pitch>` count | **0** | **0** | Zero |
| **MusicXML Rests** | `<note>/<rest>` count | **0** | **0** | Zero |
| **`parse_musicxml`** | `MusicXmlNote` objects | **0** | **0** | Zero |
| **Part Selection** | Selected part / Warning | Selected `P1`, emitted `musicxml-extra-parts-ignored` for `P2` | Selected `P1`, emitted `musicxml-extra-parts-ignored` for `P2` | Part `P1` Selected |
| **`_measure_events`** | Event groups constructed | **0** | **0** | Zero |
| **ScoreIR Model** | `bar_count` / `event_count` | 1 bar / **0 events** | 1 bar / **0 events** | Zero Events |
| **ScoreIR Diagnostics** | `matched_candidate_count` | **0** | **0** | Zero |
| **`CandidatePools`** | `unmatched_tabraw_candidate_count` | 3 candidates retained unconsumed | 2 candidates retained unconsumed | Unconsumed Candidates |
| **Conversion Report** | `exit_code`, `status`, `stage` | `0`, `success`, `gp-write` | `0`, `success`, `gp-write` | Output Written (`converted.gp`) |

### Clarification on TabRaw Counts & Safety Flags
- **Candidate Counts**: Conversion `tab_raw.json` contains 3 candidates for Fixture 1 and 2 candidates for Fixture 2. Prior standalone `extract-tab` runs produced 4 candidates. The report records the exact canonical conversion `TabRaw` counts (3 and 2) and does not establish why prior standalone extraction counts differed.
- **Safety Gate vs Candidate Flag**: Conversion reached the grouping gate without layout refusal (`pdf_layout_warnings` empty, `pdf_grouping_complete` info recorded). However, this does not make candidate-level `raw.safe_grouping` true (`raw.safe_grouping` is `false` for all candidates in both fixtures).

---

## 4. Canonical Source-Path Map: Observed Data Flow

At product SHA `df6e5c8178794f0ea7f98d69e069a1be3593f176`, the canonical `.venv/bin/score2gp convert` route follows this exact inspected code path:

```
[PDF Vector Input + Audiveris .mxl Sidecar]
                     │
                     ▼
              [cli.convert]
                     │
                     ▼
  [build_ir_with_diagnostics_from_files]
                     │
                     ├──────────────────────────────────────────┐
                     ▼                                          ▼
             [parse_musicxml]                       [CandidatePools.from_tabraw]
     (Parses .mxl into MusicXmlImport)              (Loads 3 / 2 TabRaw candidates)
                     │                                          │
                     ▼                                          │
   [build_ir_with_diagnostics_from_imports]                     │
     - Selects musicxml.parts[0] (P1)                           │
     - Emits musicxml-extra-parts-ignored for P2                │
     - With 0 <note> tags, measure.notes is []                  │
                     │                                          │
                     ├──────────────────────────────────────────┘
                     ▼
             [_measure_events]
    (Receives 0 notes -> constructs 0 events)
                     │
                     ▼
           [ScoreIR Construction]
    (event_count: 0, 3 / 2 unmatched candidates)
                     │
                     ▼
     [write_gp / _write_convert_report]
  (Writes converted.gp, report: exit 0, gp-write)
```

### Component Inspection Details

1. **`cli.convert`**: Entry point for conversion CLI command in `src/score2gp/cli.py`.
2. **`cli.convert` preparation and `build_ir_with_diagnostics_from_files`**: `cli.convert` first writes the PDF extraction to `tab_raw.json` through `extract_tab_file`. `build_ir_with_diagnostics_from_files`, in `src/score2gp/build_ir.py`, then loads that `TabRaw` from its path and calls `parse_musicxml` on the sidecar path.
3. **`parse_musicxml`**: Located in `src/score2gp/musicxml.py`. Iterates through XML `<part>` and `<measure>` nodes. Because `<note>` tags are absent in the Audiveris `.mxl` file, `measure.notes` is returned as an empty list (`[]`), instantiating 0 `MusicXmlNote` objects.
4. **`build_ir_with_diagnostics_from_imports`**: Located in `src/score2gp/build_ir.py`. Selects `musicxml.parts[0]` (`P1`). Since Audiveris produced 2 parts (`P1` and `P2`), it logs `MusicXmlWarning` code `musicxml-extra-parts-ignored` for `P2`.
5. **`CandidatePools.from_tabraw`**: Located in `src/score2gp/build_ir.py`. Loads TabRaw candidates (3 for Candidate 1, 2 for Candidate 2) into candidate pools.
6. **`_measure_events`**: Located in `src/score2gp/build_ir.py`. Iterates over `measure.notes`. Because `measure.notes` is empty, `_measure_events` creates 0 measure events (`event_count: 0`).
7. **ScoreIR & Diagnostics Output**: `ScoreIR` is constructed with 1 `BarIR` and 0 events. `CandidatePools` retains all TabRaw candidates as unconsumed (`unmatched_tabraw_candidate_count`: 3 for Cand 1, 2 for Cand 2).
8. **Output Packaging**: `write_gp` writes `converted.gp`, and `_write_convert_report` writes `convert_report.json` with `exit_code: 0`, `status: "success"`, `stage: "gp-write"`, `output_written: true`.

*Note on Unexecuted Code*: `PdfStaffTabTimingAligner` (in `src/score2gp/pdf_staff_tab_timing_aligner.py`) exists in the repository for alternative/legacy alignment experiments, but is **not invoked** by the canonical `convert` route at product SHA `df6e5c8178794f0ea7f98d69e069a1be3593f176`.

---

## 5. First Observable Boundary & Causal Uncertainty

### First Observable Boundary
The first observable MusicXML note-bearing boundary is **already zero**.

- Direct inspection of the `.mxl` sidecar archive emitted by `.venv/bin/score2gp omr` confirms `<note>` element count is **0**.

### No Observed Internal Audiveris Transition
- Audiveris 5.7.0 runs as an external black box process.
- No non-zero-to-zero transition inside Audiveris was directly observed.

### Causal Uncertainty
The cause of zero notes in the Audiveris-generated MusicXML remains **unproven**. Potential contributing factors include:
1. Audiveris OMR recognition limitations on synthetic vector scores;
2. The specific visual layout/shape of paired standard-notation + TAB systems;
3. Unsupported OMR engine parameters, DPI settings, or missing input conditions.

---

## 6. Claim Ledger

| Claim | Evidence Inspected / Command | Input & Revision | Observed Result | Boundary / Limitation |
|---|---|---|---|---|
| **Venv & Canonical CLI Setup** | `.venv/bin/pip install -e .` | Product revision `df6e5c81...` | `.venv/bin/score2gp` executable built & verified | Local worktree venv only |
| **gh Auth Safety** | `gh auth status` | Local WSL | Exit code 1 (unauthenticated) | No remote API/Git operations run |
| **Audiveris Asset Integrity** | `sha256sum -c` | `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` | Verified `b7d26b9a9013...` | Official release asset |
| **Fixture 1 Conversion TabRaw** | `convert_work/tab/tab_raw.json` | Candidate 1 `convert_work` | 3 playable candidates, `raw.safe_grouping: false` | Canonical TabRaw evidence |
| **Fixture 1 Canonical OMR** | `.venv/bin/score2gp omr` | `generated_paired_notation_tab_system.pdf` | Manifest `success`, written `.mxl` | Sidecar archive created |
| **Fixture 1 MXL Structure** | One-shot XML inspection | Candidate 1 `.mxl` sidecar | 1 `<score-partwise>`, 2 `<part>`, 2 `<measure>`, **0 `<note>`** | **First observable boundary is zero** |
| **Fixture 1 Canonical Convert** | `.venv/bin/score2gp convert` | Candidate 1 PDF + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `event_count: 0`, `unmatched_tabraw: 3` | Observed handoff complete |
| **Fixture 2 Conversion TabRaw** | `convert_work/tab/tab_raw.json` | Candidate 2 `convert_work` | 2 playable candidates, `raw.safe_grouping: false` | Canonical TabRaw evidence |
| **Fixture 2 Canonical OMR** | `.venv/bin/score2gp omr` | `generated_paired_notation_tab_system_double_barline.pdf` | Manifest `success`, written `.mxl` | Sidecar archive created |
| **Fixture 2 MXL Structure** | One-shot XML inspection | Candidate 2 `.mxl` sidecar | 1 `<score-partwise>`, 2 `<part>`, 2 `<measure>`, **0 `<note>`** | **First observable boundary is zero** |
| **Fixture 2 Canonical Convert** | `.venv/bin/score2gp convert` | Candidate 2 PDF + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `event_count: 0`, `unmatched_tabraw: 2` | Observed handoff complete |

---

## 7. Pre-Submit Challenge

1. **What is the strongest way this could appear successful while failing the product outcome?**
   `.venv/bin/score2gp convert` exits with status `0`, stage `gp-write`, and creates `converted.gp`, creating the illusion of a fully successful end-to-end conversion.
2. **Which command, source inspection, generated artifact, or regression test rules that out?**
   One-shot XML inspection of the Audiveris `.mxl` sidecar confirms `<note>` count is 0, and `convert_report.json` records `event_count: 0` and `matched_candidate_count: 0`.
3. **Which failure modes remain untested, and do they limit the claim?**
   Whether Audiveris 5.7.0 would recognize standard notation notes on PDFs without TAB staves, or under different resolution/rendering parameters, remains unproven. This trace is strictly bounded to the two specified synthetic paired notation+TAB vector PDF fixtures.
4. **Is any assertion based only on fixture-specific coordinates, bar numbers, filenames, titles, reference GP data, aggregate counts, or file creation?**
   No. Findings rely on exact XML element trees, CLI exit codes, manifest fields, JSON conversion reports, and line-by-line source path tracing.
5. **Does the evidence come from the exact remote head intended for review?**
   Under the local-preparation model, evidence comes from local heads (`df6e5c8178794f0ea7f98d69e069a1be3593f176` product, local AgentOps branch `agy/fs03e-event-loss-trace`).

---

## 8. Bounded Recommended Next Task

### Next Task Recommendation: FS-03F
**Task Name**: FS-03F: Synthetic / Opt-In Timing Sidecar Handoff Verification
**Objective**: Establish a public-testable handoff path using a valid synthetic MusicXML sidecar (containing non-zero pitched notes matching standard staff notation) to verify that `.venv/bin/score2gp convert --musicxml` correctly aligns MusicXML timing events with TabRaw candidates and produces `event_count > 0` and `matched_candidate_count > 0`.
**Boundaries**: Architect evidence-only or minimal integration. No modification of OMR engines.

---

## 9. Local Handoff Verification

- AgentOps Branch: `agy/fs03e-event-loss-trace`
- AgentOps Local Evidence Commits: `4a0dd9c3bde0c1332d2d58dce89d7ad46d78ea89`, `23c7e6bd2ea2ae34227e63f20920041831aeccb4`, and `5ed1a08b9af7e7151d87e8547f12fa79e30ea1bb`
- Product Branch: `agy/fs03e-event-loss-trace-product`
- Product HEAD: `df6e5c8178794f0ea7f98d69e069a1be3593f176`
- Changed Files in AgentOps:
  - `projects/score2gp/reports/2026-07-21-fs03e-sidecar-scoreir-event-loss-trace.md` [MODIFIED]
  - `projects/score2gp/ACTIVE_TASK.md` [UNCHANGED at `LOCAL_HANDOFF_READY`]
- Status: `LOCAL_HANDOFF_READY`
