# FS-03E: Sidecar-to-ScoreIR Event-Loss Trace (Revised Canonical Rerun)

**Authorised Role**: Architect, Tier B evidence-only
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`
**Date**: 2026-07-22
**AgentOps Local Head**: `4a0dd9c3bde0c1332d2d58dce89d7ad46d78ea89` (branch `agy/fs03e-event-loss-trace`)
**Product Local Head**: `df6e5c8178794f0ea7f98d69e069a1be3593f176` (branch `agy/fs03e-event-loss-trace-product`)
**Worktree-Local Python Interpreter**: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv/bin/python`
**Canonical CLI Executable**: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv/bin/score2gp`

---

## 1. Executive Summary & Context

Governance task **FS-03E** is an Architect, Tier B evidence-only trace investigation. Its goal is to locate the first observable boundary at which MusicXML or TAB evidence yields zero ScoreIR events during explicit sidecar conversion.

### Revision & Canonical Setup
In accordance with governance requirements:
1. A worktree-local ignored `.venv` was established inside the product worktree (`/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/.venv`).
2. The exact checked-out product revision (`df6e5c8178794f0ea7f98d69e069a1be3593f176`) was installed into it via `pip install -e .`.
3. All reruns of `omr` and `convert` were executed strictly via `.venv/bin/score2gp` (without invoking `python -m score2gp.cli`).
4. All inspection commands were executed as one-shot commands without creating persistent analysis scripts.

### Key Observed Finding
1. **First Observable Boundary**: The first observable MusicXML note-bearing boundary is **already zero** (`<note>` element count = 0 inside the generated `.mxl` archive).
2. **No Observed Internal Audiveris Transition**: Because Audiveris 5.7.0 execution occurs within an external black box process, no non-zero-to-zero transition inside Audiveris was directly observed.
3. **Causal Uncertainty**: The cause of zero notes in the Audiveris MusicXML output remains **unproven**. It may be attributable to Audiveris OMR recognition capabilities, the specific visual layout of paired standard-notation + TAB systems, or unsupported engine/input runtime conditions.
4. **Scope of Propagation**: Downstream `score2gp` modules (`parse_musicxml`, `PdfStaffTabTimingAligner`, `build_ir_with_diagnostics`) propagate the zero-input sidecar as directly observed (0 parsed `MusicXmlNote` objects -> 0 aligned events -> `event_count: 0`). No claim is made that `score2gp` is "operating as designed" beyond this directly observed zero-input propagation.

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

## 3. Boundary Count Matrix (Canonical Rerun)

All counts below were produced by rerunning the canonical CLI executable `.venv/bin/score2gp` in new ignored per-candidate directories (`work/fs03e_canonical_rerun/cand1` and `work/fs03e_canonical_rerun/cand2`).

| Boundary / Stage | Metric / Observable Field | Fixture 1: `generated_paired_notation_tab_system.pdf` | Fixture 2: `generated_paired_notation_tab_system_double_barline.pdf` | Transition Status |
|---|---|---|---|---|
| **PDF Input** | File SHA-256 | `31669e6c264ed6e48423c0901f853e7fa93564fd0aa60cdc4189c53a8796dcad` | `307df45e57bad8b9539cca846265ddfb972a2aaae7264b7197dec1d880c954e2` | Input Available |
| **TabRaw Extraction** | Playable fret candidates | 4 playable candidates | 4 playable candidates | Non-Zero Evidence |
| **TabRaw Assignment** | System 1 / Staff 1 / Bars 1-2 | 4 assigned candidates | 4 assigned candidates | Non-Zero Evidence |
| **TabRaw Safety Gate** | `safe_grouping` | `true` (`pdf_grouping_complete`) | `true` (`pdf_grouping_complete`) | Gate Passed |
| **Audiveris OMR CLI** | `.venv/bin/score2gp omr` | `execution_status: success`, `validation_status: success` | `execution_status: success`, `validation_status: success` | Manifest Success |
| **Audiveris MXL Sidecar** | MXL Sidecar SHA-256 | `a6698f6ec6667f9990a02ae4306892dd1f42066666c941f066dd73bca1634ec7` | `6993925d7050972479a4f3c478355056d5453ffc57f0048213f22c161f7b8cff` | File Created |
| **MusicXML XML Root** | Root Element Tag | `<score-partwise>` (count = 1) | `<score-partwise>` (count = 1) | Root Present |
| **MusicXML Part List** | `<part>` element count | 2 (`P1: Voice`, `P2: Voice`) | 2 (`P1: Voice`, `P2: Voice`) | Structure Present |
| **MusicXML Measures** | Total `<measure>` count | 2 (1 measure in P1, 1 measure in P2) | 2 (1 measure in P1, 1 measure in P2) | Structure Present |
| **MusicXML Note Tags** | `<note>` element count | **0** | **0** | **FIRST OBSERVABLE BOUNDARY IS ZERO** |
| **MusicXML Pitched Notes** | `<note>/<pitch>` count | **0** | **0** | Zero |
| **MusicXML Rests** | `<note>/<rest>` count | **0** | **0** | Zero |
| **`parse_musicxml`** | `MusicXmlNote` objects | **0** | **0** | Zero |
| **`PdfStaffTabTimingAligner`** | `aligned_pairs` count | **0** | **0** | Zero |
| **ScoreIR Model** | `bar_count` / `event_count` | 1 bar / **0 events** | 1 bar / **0 events** | Zero Events |
| **ScoreIR Model** | `matched_candidate_count` | **0** | **0** | Zero |
| **ScoreIR Model** | `unmatched_tabraw_candidate_count` | 3 | 2 | Unmatched Candidates |
| **Conversion Report** | `exit_code`, `status`, `stage` | `0`, `success`, `gp-write` | `0`, `success`, `gp-write` | Output Written (`converted.gp`) |

---

## 4. Source-Path Map: Facts vs Code-Derived Inference

The canonical `.venv/bin/score2gp convert` route processes the inputs through six distinct pipeline boundaries:

```
[PDF Vector Input]
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[TabRaw Extraction]              [.venv/bin/score2gp omr]
 (4 playable candidates)          (Invokes Audiveris 5.7.0)
       │                                         │
       │                                         ▼
       │                                [MusicXML MXL Sidecar]
       │                                 (0 <note> elements) ◄── FIRST OBSERVABLE BOUNDARY IS ZERO
       │                                         │
       │                                         ▼
       │                                [parse_musicxml]
       │                                 (0 MusicXmlNote objects)
       │                                         │
       └───────────────────┬─────────────────────┘
                           ▼
             [PdfStaffTabTimingAligner]
              (0 staff timing events)
                           │
                           ▼
                  [ScoreIR Generation]
                   (event_count: 0)
                           │
                           ▼
                  [GP Package Writer]
                   (converted.gp written)
```

### Boundary-by-Boundary Inspection

#### Boundary 1: TabRaw Extraction & Geometry Grouping
- **Module**: `src/score2gp/pdf_geometry_candidate_extraction.py` and `src/score2gp/tabraw.py`
- **Functions**: `extract_tab_candidates_from_pdf(...)`
- **Data Types**: `TabRaw`, `TabCandidate`
- **Observed Fact**: For Candidate 1 and Candidate 2, exactly 4 fret candidates are extracted from the TAB staff lines. All 4 candidates pass safe grouping (`safe_grouping: true`).

#### Boundary 2: Audiveris OMR Sidecar Generation via Canonical CLI
- **Module**: `src/score2gp/cli.py` (`omr_command`)
- **Executable**: `.venv/bin/score2gp omr` -> Audiveris 5.7.0 binary (`bin/Audiveris`)
- **Observed Fact**: `.venv/bin/score2gp omr` completes successfully (`execution_status: success`, `validation_status: success`). It produces a valid `.mxl` zip archive containing `META-INF/container.xml` and an XML score file.
- **Observed Fact**: One-shot XML inspection of `generated_paired_notation_tab_system.mxl` and `generated_paired_notation_tab_system_double_barline.mxl` proves:
  - Root tag: `<score-partwise>`
  - Part count: 2 (`P1` Voice, `P2` Voice)
  - Measures: `<measure number="1">` under `P1`, `<measure number="1">` under `P2`
  - Attributes: `<divisions>0</divisions>`, `<staff-details print-object="yes"/>`
  - **Note tag count**: 0 (`<note>` elements)
  - **Pitched note count**: 0 (`<pitch>` elements)
  - **Rest tag count**: 0 (`<rest>` elements)

#### Boundary 3: MusicXML Sidecar Parsing
- **Module**: `src/score2gp/musicxml.py`
- **Functions**: `parse_musicxml(source_path)`
- **Data Types**: `MusicXmlImport`, `MusicXmlPart`, `MusicXmlMeasure`, `MusicXmlNote`
- **Count-bearing Fields**: `measure.notes`
- **Code-Derived Inference**: `parse_musicxml` parses the XML score. Because `<note>` tags are absent in the XML, `measure.notes` is populated as an empty list (`[]`), instantiating 0 `MusicXmlNote` objects.

#### Boundary 4: Staff/TAB Timing Alignment
- **Module**: `src/score2gp/pdf_staff_tab_timing_aligner.py`
- **Functions**: `PdfStaffTabTimingAligner.align(staff_events, tab_groups_by_bar)`
- **Data Types**: `PdfStaffTimingEvent`, `CandidateXGroupDiagnostics`, `PdfStaffTabAlignmentResult`
- **Count-bearing Fields**: `result.aligned_pairs`, `result.unmatched_staff_events`, `result.unmatched_tab_groups`
- **Code-Derived Inference**: `staff_events` is constructed from `MusicXmlNote` objects. Since there are 0 `MusicXmlNote` objects, `staff_events` is empty (`len = 0`). `align(...)` finds no staff events for bar `(1, 1, 1, 1)` and assigns fallback timing, leaving `aligned_pairs` empty (`len = 0`).

#### Boundary 5: ScoreIR Construction
- **Module**: `src/score2gp/build_ir.py`
- **Functions**: `build_ir_with_diagnostics(...)`
- **Data Types**: `ScoreIR`, `BarIR`, `EventIR`
- **Count-bearing Fields**: `score.bars`, `bar.events`, `diagnostics.matched_candidate_count`, `diagnostics.unmatched_tabraw_candidate_count`
- **Observed Fact**: `ScoreIR` contains 1 `BarIR` with `events: []`. `event_count` is 0. `matched_candidate_count` is 0. Unmatched TabRaw candidates remain unconsumed (3 for Candidate 1, 2 for Candidate 2).

#### Boundary 6: Output Packaging & Reporting
- **Module**: `src/score2gp/cli.py` (`_write_convert_report`, `write_gp`)
- **Observed Fact**: `.venv/bin/score2gp convert` writes `converted.gp` and `convert_report.json`. The report records `exit_code: 0`, `status: "success"`, `stage: "gp-write"`, `output_written: true`.

---

## 5. First Observable Boundary & Causal Uncertainty

### First Observable Boundary
The first observable MusicXML note-bearing boundary is **already zero**.

- When the `.mxl` sidecar archive emitted by `.venv/bin/score2gp omr` is inspected at byte/XML level, `<note>` element count is **0**.

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
| **Fixture 1 TabRaw Extraction** | `extract-tab` | `generated_paired_notation_tab_system.pdf` | 4 playable candidates, `safe_grouping: true` | Non-zero TAB evidence |
| **Fixture 1 Canonical OMR** | `.venv/bin/score2gp omr` | `generated_paired_notation_tab_system.pdf` | Manifest `success`, written `.mxl` | Sidecar archive created |
| **Fixture 1 MXL Structure** | One-shot XML inspection | Candidate 1 `.mxl` sidecar | 1 `<score-partwise>`, 2 `<part>`, 2 `<measure>`, **0 `<note>`** | **First observable boundary is zero** |
| **Fixture 1 Canonical Convert** | `.venv/bin/score2gp convert` | Candidate 1 PDF + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `event_count: 0`, `unmatched_tabraw: 3` | Observed handoff complete |
| **Fixture 2 TabRaw Extraction** | `extract-tab` | `generated_paired_notation_tab_system_double_barline.pdf` | 4 playable candidates, `safe_grouping: true` | Non-zero TAB evidence |
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
   Under the local-preparation model, evidence comes from exact local heads (`df6e5c8178794f0ea7f98d69e069a1be3593f176` product, `4a0dd9c3bde0c1332d2d58dce89d7ad46d78ea89` AgentOps).

---

## 8. Bounded Recommended Next Task

### Next Task Recommendation: FS-03F
**Task Name**: FS-03F: Synthetic / Opt-In Timing Sidecar Handoff Verification
**Objective**: Establish a public-testable handoff path using a valid synthetic MusicXML sidecar (containing non-zero pitched notes matching standard staff notation) to verify that `.venv/bin/score2gp convert --musicxml` correctly aligns MusicXML timing events with TabRaw candidates and produces `event_count > 0` and `matched_candidate_count > 0`.
**Boundaries**: Architect evidence-only or minimal integration. No modification of OMR engines.

---

## 9. Local Handoff Verification

- AgentOps Branch: `agy/fs03e-event-loss-trace`
- AgentOps Local Head: `4a0dd9c3bde0c1332d2d58dce89d7ad46d78ea89`
- Product Branch: `agy/fs03e-event-loss-trace-product`
- Product HEAD: `df6e5c8178794f0ea7f98d69e069a1be3593f176`
- Changed Files in AgentOps:
  - `projects/score2gp/reports/2026-07-21-fs03e-sidecar-scoreir-event-loss-trace.md` [MODIFIED]
  - `projects/score2gp/ACTIVE_TASK.md` [UNCHANGED at `LOCAL_HANDOFF_READY`]
- Status: `LOCAL_HANDOFF_READY`
