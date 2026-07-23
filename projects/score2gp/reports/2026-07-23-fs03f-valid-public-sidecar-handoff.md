# FS-03F Valid Public MusicXML Sidecar Handoff Verification

## Executive Summary & Claim Ledger
FS-03F verifies the supported explicit MusicXML sidecar conversion route in score2gp using the committed public fixture pair:
- PDF: tests/fixtures/pdf/generated_tiny_tab.pdf
- MusicXML: tests/fixtures/musicxml/generated_tiny_tab.musicxml

The verification confirms that when provided a valid, non-empty public MusicXML timing source alongside its paired PDF:
1. score2gp convert completes successfully through the gp-write stage with status success and refusal code null.
2. The conversion pipeline writes a GP output artifact (converted.gp) to disk (output_written: true). This task does not independently establish Guitar Pro compatibility or musical equivalence.
3. Non-zero events are produced in both convert_report.json (event_count: 8) and score.ir.json (8 events across 2 bars).
4. All 6 playable TAB fret candidates from the PDF page text are successfully matched to MusicXML pitch events.
5. No product source code, tests, schemas, fixtures, or sidecars were modified, and no instrumentation or repair logic was added.

---

## Execution Environment & Repository Revisions
- Product Base SHA: df6e5c8178794f0ea7f98d69e069a1be3593f176 (clean, from origin/main)
- AgentOps Base SHA: 670d9a13988b501775eaa43cb70bb95bccabc8da (from origin/main)
- Environment: Canonical WSL (Ubuntu 24.04 LTS x86_64, Python 3.12.3)
- Canonical CLI Executable: /home/tticom/work/score2gp-workspace/score2gp-fs03f-worktree/.venv/bin/score2gp
- Python Import Path: /home/tticom/work/score2gp-workspace/score2gp-fs03f-worktree/src/score2gp
- Child Python Executable: /home/tticom/work/score2gp-workspace/score2gp-fs03f-worktree/.venv/bin/python3

---

## Input & Output SHA-256 Hashes
| Asset | File Path | SHA-256 Hash |
|---|---|---|
| PDF Input | tests/fixtures/pdf/generated_tiny_tab.pdf | 7917b8cae7e3da9c7888a28204743e882b6d4fe4a703225e33c90b8d85274fed |
| MusicXML Input | tests/fixtures/musicxml/generated_tiny_tab.musicxml | c7a2d4c58c1000ebe7ed8dfb1ae37a5a8277d6558971b21a83f26b8c579651b6 |
| Generated GP Output | work/fs03f/converted.gp | Run-specific; see output-hash qualification below. |

### Output-Hash Qualification
The PDF and MusicXML input hashes above are stable input identities. The GP writer emits run-specific package metadata: independent successful runs at the same product revision produced distinct SHA-256 values (748fd7eb5d4b2d2749b0372a8f3997e75da4f98d0d4543712cc3f975b4384534 and 4d580ea4f188e8ef3e11ed59c76436a765f0bfd8dd31bde3c5ccffa0c521c1d8). Therefore an output hash identifies an individual run artifact only; it is not evidence of reproducibility, compatibility, or musical equivalence.

---

## Pre-Conversion MusicXML Inspection
Inspected structure of tests/fixtures/musicxml/generated_tiny_tab.musicxml prior to conversion:
- Root Tag: score-partwise
- Part Count: 1 (id='P1')
- Measure Count: 2
- Note Count: 8
- Pitched Note Count: 6
- Rest Count: 2

---

## Execution Command

Executed worktree-local .venv conversion pipeline without invoking OMR:

    .venv/bin/score2gp convert \
      --pdf tests/fixtures/pdf/generated_tiny_tab.pdf \
      --musicxml tests/fixtures/musicxml/generated_tiny_tab.musicxml \
      --out work/fs03f/converted.gp \
      --work-dir work/fs03f/convert_work \
      --json-report work/fs03f/convert_report.json

---

## Conversion Metrics & Field Inspection

### convert_report.json Top-Level Fields
- status: success
- stage: gp-write
- refusal_code: null
- output_written: true
- output_path: work/fs03f/converted.gp
- summary_counts:
  - bar_count: 2
  - event_count: 8
  - matched_candidate_count: 6
  - unmatched_musicxml_event_count: 0
  - unmatched_tabraw_candidate_count: 0
  - warning_count: 6

### score.ir.json Inspection
- Top-Level Bar Count: 2
- Total ScoreIR Events: 8 across 2 bars:
  - Bar 1: 4 events
    - Event 1 (mx-m1-e1): Pitch 64 (E4), string 1, fret 0 (quarter note)
    - Event 2 (mx-m1-e2): Pitch 60 (C4), string 2, fret 1 (quarter note)
    - Event 3 (mx-m1-e3): Pitch 76 (E5), string 1, fret 12 (quarter note)
    - Event 4 (mx-m1-e4): Rest (quarter note)
  - Bar 2: 4 events
    - Event 1 (mx-m2-e1): Pitch 57 (A3), string 3, fret 2 (quarter note)
    - Event 2 (mx-m2-e2): Pitch 67 (G4), string 1, fret 3 (quarter note)
    - Event 3 (mx-m2-e3): Pitch 62 (D4), string 2, fret 3 (quarter note)
    - Event 4 (mx-m2-e4): Rest (quarter note)

### TabRaw Candidate Inspection (tab_raw.json)
Total text candidates extracted from PDF: 8
- Matched Fret Candidates (6):
  - Candidate 0 (fret 0 on string 1) -> Matched to Bar 1 Event 1 (Pitch 64)
  - Candidate 12 (fret 12 on string 1) -> Matched to Bar 1 Event 3 (Pitch 76)
  - Candidate 3 (fret 3 on string 1) -> Matched to Bar 2 Event 2 (Pitch 67)
  - Candidate 1 (fret 1 on string 2) -> Matched to Bar 1 Event 2 (Pitch 60)
  - Candidate 3 (fret 3 on string 2) -> Matched to Bar 2 Event 3 (Pitch 62)
  - Candidate 2 (fret 2 on string 3) -> Matched to Bar 2 Event 1 (Pitch 57)
- Unmatched Non-Fret Candidates (2):
  - Candidate E (kind: chord-symbol, non-playable chord text)
  - Candidate vib (kind: technique-text, non-playable technique text)

### Warnings & Diagnostics
Full warning log in convert_work/warnings.json (10 items logged across pipeline stages):
1. tab-extraction-incomplete: Tab extraction records text candidates with heuristic staff/string/bar estimates.
2. pdf_bar_boxes_constructed: Bar boxes constructed for system 1.
3. pdf_layout_details: Detected tab systems layout details.
4. pdf_grouping_complete: PDF layout grouping complete.
5. tabraw-technique-text-not-aligned: Candidate vib preserved but not aligned by build-ir phase.
6. ambiguous_technique_attachment: Technique vib requires exactly one note target in bar 2.

---

## Acceptance Matrix
| Requirement | Criteria | Observed Value | Verdict |
|---|---|---|---|
| Pipeline Status | Must equal success | success | PASS |
| Pipeline Stage | Must reach gp-write | gp-write | PASS |
| Refusal Code | Must be null | null | PASS |
| Output Written | Must be true | true | PASS |
| Event Count | Must be > 0 | 8 (in report and ScoreIR) | PASS |
| Matched TAB Candidates | Must be > 0 | 6 | PASS |
| Unmatched Candidates | Recorded transparently | 0 playable unmatched; 2 non-playable text tokens (E, vib) recorded | PASS |
| Zero Product Mutation | Product tree remains clean | Clean (0 modified files in product repo) | PASS |

---

## Pre-Submit Challenge
1. Did product code change? No. Product tree is clean.
2. Were fixtures, schemas, or tests edited? No.
3. Were worktrees pristine? Created fresh from origin/main.
4. Were unauthorized git or gh actions taken? No. gh auth status failed as required, no gh invoked thereafter, no push/PR/merge performed.

---

## Local Branch & Head Details
- AgentOps Local Branch: agy/fs03f-valid-public-sidecar-handoff
- Product Local Branch: agy/fs03f-valid-public-sidecar-handoff-product
- Product Head SHA: df6e5c8178794f0ea7f98d69e069a1be3593f176
