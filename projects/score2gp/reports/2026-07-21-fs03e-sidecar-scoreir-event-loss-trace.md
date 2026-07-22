# FS-03E: Sidecar-to-ScoreIR Event-Loss Trace

**Authorised Role**: Architect, Tier B evidence-only  
**Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`  
**Date**: 2026-07-21  
**AgentOps Local Head**: `62be8e6fe279b894d7d73ee845de516ce1996dbd` (branch `agy/fs03e-event-loss-trace`)  
**Product Local Head**: `df6e5c8178794f0ea7f98d69e069a1be3593f176` (branch `agy/fs03e-event-loss-trace-product`)

---

## 1. Executive Summary & Context

Governance task **FS-03E** is an Architect, Tier B evidence-only trace investigation. Its goal is to locate the earliest exact boundary at which non-zero Audiveris/MusicXML or TAB evidence becomes zero ScoreIR events during explicit sidecar conversion.

### Core Finding
The earliest non-zero-to-zero event loss transition occurs **inside the external Audiveris OMR sidecar generation step** (`Audiveris 5.7.0` engine invoked via `score2gp omr`). For both target paired notation+TAB vector PDF fixtures:
1. `extract-tab` extracts **4 non-zero playable TAB fret candidates** with safe PDF grouping (`safe_grouping: true`).
2. `Audiveris 5.7.0` generates a structurally valid `.mxl` container (`execution_status: success`, `validation_status: success`), creating `<score-partwise>` with 2 `<part>` elements (`P1` and `P2`) and 1 `<measure>` per part.
3. However, Audiveris recognizes **0 pitched notes and 0 rests** from the standard notation staff in both fixtures. The resulting `.mxl` XML measures contain `<divisions>0</divisions>` and **zero `<note>` tags**.
4. When `score2gp convert --musicxml` receives this sidecar, `parse_musicxml` instantiates 0 `MusicXmlNote` objects. Consequently, `PdfStaffTabTimingAligner` receives 0 staff timing events, produces 0 aligned pairs, and yields `event_count: 0` in `ScoreIR`.

The loss occurs upstream of `score2gp` in the Audiveris 5.7.0 recognition engine output file. Downstream `score2gp` code processes the 0-note sidecar deterministically without error or refusal.

---

## 2. Environment Verification & Asset Identity

### Safety Boundary Verification
1. `gh auth status` executed once in WSL: **failed with exit code 1 (unauthenticated)**. No remote Git or GitHub API operations were performed.
2. Fresh local `agy/` worktrees created from `origin/main`:
   - AgentOps: `/home/tticom/work/score2gp-workspace/score2gp-agentops-agy-fs03e-trace` (HEAD: `62be8e6fe279b894d7d73ee845de516ce1996dbd`)
   - Product: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace` (HEAD: `df6e5c8178794f0ea7f98d69e069a1be3593f176`)
3. Both worktrees confirmed clean prior to execution.
4. Audiveris 5.7.0 Ubuntu 24.04 package downloaded into ignored product directory `work/fs03e_trace/`:
   - Asset: `Audiveris-5.7.0-ubuntu24.04-x86_64.deb`
   - Verified SHA-256: `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`
   - Executable path: `/home/tticom/work/score2gp-workspace/score2gp-agy-fs03e-trace/work/fs03e_trace/extracted/opt/audiveris/bin/Audiveris`

---

## 3. Boundary Count Matrix

| Boundary / Stage | Metric / Observable Field | Fixture 1: `generated_paired_notation_tab_system.pdf` | Fixture 2: `generated_paired_notation_tab_system_double_barline.pdf` | Transition Status |
|---|---|---|---|---|
| **PDF Input** | File SHA-256 | `31669e6c264ed6e48423c0901f853e7fa93564fd0aa60cdc4189c53a8796dcad` | `307df45e57bad8b9539cca846265ddfb972a2aaae7264b7197dec1d880c954e2` | Input Available (Non-Zero) |
| **TabRaw Extraction** | Extracted Fret Candidates | 4 playable candidates | 4 playable candidates | Non-Zero Evidence |
| **TabRaw Assignment** | System 1 / Staff 1 / Bars 1-2 | 4 assigned candidates | 4 assigned candidates | Non-Zero Evidence |
| **TabRaw Safety Gate** | `safe_grouping` | `true` (`pdf_grouping_complete`) | `true` (`pdf_grouping_complete`) | Gate Passed |
| **Audiveris OMR CLI** | Execution Manifest | `execution_status: success`, `validation_status: success` | `execution_status: success`, `validation_status: success` | Manifest Success |
| **Audiveris MXL Sidecar** | Sidecar SHA-256 | `1774cd5cf28bc160c0c7eb0575e467efa131e35b5b4967306b25446a13237e2e` | `f87bdf0eda77fa55ebec30e377365620913fd1d3ce0d4fe227cd7c3e6ab2fa65` | File Created |
| **MusicXML XML Root** | Root Element Tag | `<score-partwise>` (count = 1) | `<score-partwise>` (count = 1) | Root Present |
| **MusicXML Part List** | `<part>` element count | 2 (`P1: Voice`, `P2: Voice`) | 2 (`P1: Voice`, `P2: Voice`) | Structure Present |
| **MusicXML Measures** | Total `<measure>` count | 2 (1 measure in P1, 1 measure in P2) | 2 (1 measure in P1, 1 measure in P2) | Structure Present |
| **MusicXML Note Tags** | `<note>` element count | **0** | **0** | **NON-ZERO TO ZERO TRANSITION** |
| **MusicXML Pitched Notes** | `<note>/<pitch>` count | **0** | **0** | Zero |
| **MusicXML Rests** | `<note>/<rest>` count | **0** | **0** | Zero |
| **`parse_musicxml`** | `MusicXmlNote` objects | **0** | **0** | Zero |
| **`PdfStaffTabTimingAligner`** | `aligned_pairs` count | **0** | **0** | Zero |
| **ScoreIR Model** | `bar_count` | 1 | 1 | 1 Bar |
| **ScoreIR Model** | `event_count` | **0** | **0** | Zero |
| **ScoreIR Model** | `matched_candidate_count` | **0** | **0** | Zero |
| **ScoreIR Model** | `unmatched_tabraw_candidate_count` | 3 | 2 | Unmatched Candidates |
| **Conversion Report** | `exit_code`, `status`, `stage` | `0`, `success`, `gp-write` | `0`, `success`, `gp-write` | Output Written (`converted.gp`) |

---

## 4. Source-Path Map: Facts vs Code-Derived Inference

The committed conversion data flow spans six distinct pipeline boundaries from PDF input to `.gp` output package creation.

```
[PDF Vector Input] 
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[TabRaw Extraction]                     [Audiveris 5.7.0 OMR]
 (4 playable candidates)                 (Generates .mxl sidecar)
       │                                         │
       │                                         ▼
       │                                [MusicXML XML Sidecar]
       │                                 (0 <note> elements) ◄── FIRST-LOSS BOUNDARY
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

#### Boundary 2: Audiveris OMR Sidecar Generation
- **Module**: `src/score2gp/cli.py` (`omr_command`)
- **Executable**: `Audiveris 5.7.0` binary (`bin/Audiveris`)
- **Observed Fact**: Audiveris executes without crash (`exit_code: 0`). It parses the PDF and produces an `.mxl` archive.
- **Observed Fact**: Direct XML inspection (`ElementTree` parse of `generated_paired_notation_tab_system.mxl` and `generated_paired_notation_tab_system_double_barline.mxl`) proves:
  - Root tag: `<score-partwise>`
  - Part count: 2 (`P1` Voice, `P2` Voice)
  - Measures: `<measure number="1">` under `P1`, `<measure number="1">` under `P2`
  - Attributes: `<divisions>0</divisions>`, `<staff-details print-object="yes"/>`
  - **Note count**: `len(root.findall(".//note")) == 0`
  - **Pitched note count**: `len(root.findall(".//note/pitch")) == 0`
  - **Rest count**: `len(root.findall(".//note/rest")) == 0`

#### Boundary 3: MusicXML Sidecar Parsing
- **Module**: `src/score2gp/musicxml.py`
- **Functions**: `parse_musicxml(source_path)`
- **Data Types**: `MusicXmlImport`, `MusicXmlPart`, `MusicXmlMeasure`, `MusicXmlNote`
- **Count-bearing Fields**: `measure.notes`
- **Code-Derived Inference**: `parse_musicxml` iterates through `<part>` and `<measure>` elements in the XML. Because `<note>` elements are absent in the XML, `measure.notes` is populated as `[]` (empty list).

#### Boundary 4: Staff/TAB Timing Alignment
- **Module**: `src/score2gp/pdf_staff_tab_timing_aligner.py`
- **Functions**: `PdfStaffTabTimingAligner.align(staff_events, tab_groups_by_bar)`
- **Data Types**: `PdfStaffTimingEvent`, `CandidateXGroupDiagnostics`, `PdfStaffTabAlignmentResult`
- **Count-bearing Fields**: `result.aligned_pairs`, `result.unmatched_staff_events`, `result.unmatched_tab_groups`
- **Code-Derived Inference**: `staff_events` is constructed from `MusicXmlNote` objects. Since there are 0 `MusicXmlNote` objects, `staff_events` is empty (`len = 0`). `align(...)` finds no staff events for bar `(1, 1, 1, 1)` and places the bar into `bars_using_fallback_timing`, leaving `aligned_pairs` empty (`len = 0`).

#### Boundary 5: ScoreIR Construction
- **Module**: `src/score2gp/build_ir.py`
- **Functions**: `build_ir_with_diagnostics(...)`
- **Data Types**: `ScoreIR`, `BarIR`, `EventIR`
- **Count-bearing Fields**: `score.bars`, `bar.events`, `diagnostics.matched_candidate_count`, `diagnostics.unmatched_tabraw_candidate_count`
- **Observed Fact**: `ScoreIR` contains 1 `BarIR` with `events: []`. `event_count` is 0. `matched_candidate_count` is 0. Unmatched TabRaw candidates remain unconsumed (3 for Candidate 1, 2 for Candidate 2).

#### Boundary 6: Output Packaging & Reporting
- **Module**: `src/score2gp/cli.py` (`_write_convert_report`, `write_gp`)
- **Observed Fact**: `write_gp` creates `converted.gp` with default single-bar empty score structure. `_write_convert_report` records `exit_code: 0`, `status: "success"`, `stage: "gp-write"`, `output_written: true`.

---

## 5. Earliest First-Loss Finding & Observability Limit

### Earliest Loss Boundary
The earliest observed non-zero-to-zero transition occurs **INSIDE THE AUDIVERIS OMR ENGINE STEP** prior to any `score2gp` Python code execution.

- **Pre-boundary State**: PDF input contains non-zero standard staff notation + TAB staff; TabRaw extracts **4 playable fret candidates**.
- **Post-boundary State**: The `.mxl` file written by Audiveris 5.7.0 contains **0 `<note>` elements** (0 pitched notes, 0 rests).

### Observability Limit
Within `score2gp` codebase observability, the input sidecar file itself arrives at `parse_musicxml` with **0 note tags at byte/XML level**. 

`score2gp` does not drop, filter, or refuse the notes. The internal Audiveris 5.7.0 recognition pipeline fails to detect noteheads or stems in synthetic paired notation+TAB vector PDFs, producing an empty measure envelope.

---

## 6. Claim Ledger

| Claim | Evidence Inspected / Command | Input & Revision | Observed Result | Boundary / Limitation |
|---|---|---|---|---|
| **WSL Execution Gate** | `uname -s`, `uname -m`, `pwd -P` | Local WSL Ubuntu 24.04 | `Linux x86_64`, `/home/tticom/work/...` | WSL environment proved |
| **gh Auth Safety** | `gh auth status` | Local WSL | Exit code 1 (unauthenticated) | No remote API/Git operations run |
| **Audiveris Asset Integrity** | `sha256sum -c` | `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` | Verified `b7d26b9a9013...` | Official release asset |
| **Fixture 1 TabRaw Extraction** | `extract-tab` | `generated_paired_notation_tab_system.pdf` | 4 playable candidates, `safe_grouping: true` | Non-zero TAB evidence |
| **Fixture 1 OMR Execution** | `score2gp omr` | `generated_paired_notation_tab_system.pdf` | Manifest `success`, written `.mxl` | Sidecar archive created |
| **Fixture 1 MXL Structure** | Python `zipfile` + `ElementTree` | Candidate 1 `.mxl` sidecar | 1 `<score-partwise>`, 2 `<part>`, 2 `<measure>`, **0 `<note>`** | **Earliest 0-event transition** |
| **Fixture 1 Conversion Handoff** | `score2gp convert --musicxml` | Candidate 1 PDF + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `event_count: 0`, `unmatched_tabraw: 3` | Observed handoff complete |
| **Fixture 2 TabRaw Extraction** | `extract-tab` | `generated_paired_notation_tab_system_double_barline.pdf` | 4 playable candidates, `safe_grouping: true` | Non-Zero TAB evidence |
| **Fixture 2 OMR Execution** | `score2gp omr` | `generated_paired_notation_tab_system_double_barline.pdf` | Manifest `success`, written `.mxl` | Sidecar archive created |
| **Fixture 2 MXL Structure** | Python `zipfile` + `ElementTree` | Candidate 2 `.mxl` sidecar | 1 `<score-partwise>`, 2 `<part>`, 2 `<measure>`, **0 `<note>`** | **Earliest 0-event transition** |
| **Fixture 2 Conversion Handoff** | `score2gp convert --musicxml` | Candidate 2 PDF + Audiveris `.mxl` | Exit `0`, stage `gp-write`, `event_count: 0`, `unmatched_tabraw: 2` | Observed handoff complete |

---

## 7. Pre-Submit Challenge

1. **What is the strongest way this could appear successful while failing the product outcome?**  
   `score2gp convert --musicxml` exits with status `0`, stage `gp-write`, and creates `converted.gp`, creating the illusion of a fully successful end-to-end conversion.
2. **Which command, source inspection, generated artifact, or regression test rules that out?**  
   Direct XML inspection of the Audiveris `.mxl` sidecar confirms `len(root.findall(".//note")) == 0`, and `convert_report.json` records `event_count: 0` and `matched_candidate_count: 0`.
3. **Which failure modes remain untested, and do they limit the claim?**  
   Whether Audiveris 5.7.0 would recognize standard notation notes on PDFs without TAB staves, or with different DPI/rendering parameters, remains unproven. This trace is bounded to the two specified synthetic paired notation+TAB vector PDF fixtures.
4. **Is any assertion based only on fixture-specific coordinates, bar numbers, filenames, titles, reference GP data, aggregate counts, or file creation?**  
   No. Findings rely on exact XML element trees, CLI exit codes, manifest fields, JSON conversion reports, and line-by-line source path tracing.
5. **Does the evidence come from the exact remote head intended for review?**  
   Under the local-preparation model, evidence comes from exact local heads (`df6e5c8178794f0ea7f98d69e069a1be3593f176` product, `62be8e6fe279b894d7d73ee845de516ce1996dbd` AgentOps).

---

## 8. Bounded Recommended Next Task

### Next Task Recommendation: FS-03F
**Task Name**: FS-03F: Synthetic / Opt-In Timing Sidecar Handoff Verification  
**Objective**: Establish a public-testable handoff path using a valid synthetic MusicXML sidecar (containing non-zero pitched notes matching standard staff notation) to verify that `score2gp convert --musicxml` correctly aligns MusicXML timing events with TabRaw candidates and produces `event_count > 0` and `matched_candidate_count > 0`.  
**Boundaries**: Architect evidence-only or minimal integration. No modification of OMR engines.

---

## 9. Local Handoff Verification

- AgentOps Branch: `agy/fs03e-event-loss-trace`
- AgentOps HEAD: `62be8e6fe279b894d7d73ee845de516ce1996dbd`
- Product Branch: `agy/fs03e-event-loss-trace-product`
- Product HEAD: `df6e5c8178794f0ea7f98d69e069a1be3593f176`
- Changed Files in AgentOps:
  - `projects/score2gp/reports/2026-07-21-fs03e-sidecar-scoreir-event-loss-trace.md` [NEW]
  - `projects/score2gp/ACTIVE_TASK.md` [MODIFIED]
- Status: `LOCAL_HANDOFF_READY`
