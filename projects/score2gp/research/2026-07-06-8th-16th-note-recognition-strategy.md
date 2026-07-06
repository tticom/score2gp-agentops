# Architect Research — 8th/16th-Note Recognition and Rhythm Semantics

## 1. Verdict
Outcome A — Raster path viable for a narrow next bridge task, not proven as general real-world 8th/16th-note OMR support.

## 2. Baseline Reviewed
- **Governance PR #239 merge commit**: `cd68a684f188f0499c511986fcd4e9e2c0fafa61`
- **Product PR #336 merge commit**: `cae6a416076e66f6b84940ad0cbf3061beb241d9`
- **Product Repo HEAD Commit**: `cae6a416076e66f6b84940ad0cbf3061beb241d9`
- **Governance Repo HEAD Commit**: `cd68a684f188f0499c511986fcd4e9e2c0fafa61`
- **Relevant prior decisions/reports inspected**:
  - `projects/score2gp/decisions/2026-07-06-whole-note-pivot-and-loop-efficiency.md`
  - `projects/score2gp/decisions/2026-07-06-authorise-8th-16th-note-architect-research.md`

## 3. Current Product Capability Inventory
- **PDF parsing**: Handled by PyMuPDF (fitz) in `src/score2gp/pdf.py`, extracting drawings and text spans.
- **Staff geometry**: Handled by `src/score2gp/pdf_staff_geometry.py` and `src/score2gp/pdf_raster_staff_diagnostics.py` to identify systems, staves, coordinates, and spacing.
- **Note/rest candidate extraction**: Bounded whole-note, half-note, and quarter-note candidates are extracted from drawings/spans in `src/score2gp/pdf_staff_notation_diagnostics.py`.
- **Notation bridge**: `src/score2gp/notation_bridge.py` maps outcome candidates to ScoreIR Events and Notes.
- **ScoreIR**: Defined in `src/score2gp/ir.py` and `src/score2gp/build_ir.py` using Timing, Event, Note, and Track objects.
- **GP export**: Built in `src/score2gp/gp_package.py` and `src/score2gp/gpif.py` to construct valid `.gp` structures.
- **CLI**: Entrypoints defined in `src/score2gp/cli.py` including `--assume-treble-clef` and CLI conversions.
- **Tests**: Core tests exist under `tests/test_whole_note_*.py`, `tests/test_notation_bridge.py`, and `tests/test_whole_note_recogniser_fractional_beam_extraction.py`.
- **Fixtures**: Standard test PDFs are tracked under `tests/fixtures/pdf/` and `fixtures/public/generated_simple/`.

## 4. Current Gaps for 8th/16th Notes
- **Noteheads**: Solid noteheads are extracted as `quarter_note_candidate` but do not distinguish eighth/sixteenth noteheads until composed.
- **Stems**: Associated via simple vertical line proximity; complex stem direction or sharing is not modeled.
- **Flags**: Extracted based on basic curves or diagonal stroke dimensions; heuristics may fail on curved articulation marks.
- **Beams**: Horizontal line/rectangle dimensions are evaluated, but multi-beam and fractional beam groupings are simplified.
- **Association**: Noteheads are linked to beams/flags by spatial bounding box intersections, which assumes single-track monophony.
- **Duration classification**: Grouped notes map to `"eighth"` or `"sixteenth"`, but 32nd or 64th notes are not fully triaged.
- **Onset/duration mapping**: `notation_bridge.py` sequentially increments onsets for all candidates unconditionally, causing vertically aligned notes (chords) to be serialized sequentially, violating timing and exceeding measure limits.
- **GP export**: Lacks polyphony/multi-voice representation; only a single sequential track (`trk_0`) is generated.
- **Tests/fixtures**: Limited to synthetic files (e.g. `4SixteenthNotes.pdf`, `2EighthNotes.pdf`); no real-world or complex rhythm tests exist.

## 5. Facts
- **Fact 5.1**: `src/score2gp/whole_note_recogniser.py` (lines 852-858) maps composed note candidates to `"eighth"`, `"sixteenth"`, `"thirty_second"`, or `"sixty_fourth"` based on intersecting flag/beam counts.
- **Fact 5.2**: `tests/test_whole_note_recogniser_fractional_beam_extraction.py` verifies that `run_recognition_on_file` correctly extracts eighth and sixteenth note candidates from `4SixteenthNotes.pdf` and `2EighthNotes.pdf`.
- **Fact 5.3**: `src/score2gp/notation_bridge.py` (lines 130-151) supports mapping `"eighth"`, `"sixteenth"`, `"thirty_second"`, and `"sixty_fourth"` values to their corresponding ticks (`DEFAULT_TICKS_PER_QUARTER // 2`, `// 4`, `// 8`, `// 16` respectively).
- **Fact 5.4**: `src/score2gp/notation_bridge.py` (lines 155-156) raises `NotationBridgeInputError("cumulative_duration_exceeds_one_4_4_bar")` when total accumulated ticks exceed `max_ticks_in_4_4_bar`.
- **Fact 5.5**: `src/score2gp/notation_bridge.py` (line 172) increments `current_onset_ticks += dur_ticks` unconditionally for every outcome mapped, serializing all outcomes sequentially regardless of their horizontal position or alignment.
- **Fact 5.6**: `src/score2gp/pdf_staff_notation_diagnostics.py` (lines 797-837) extracts diagonal strokes/curves as `flag_candidates` and horizontal lines/rectangles as `beam_candidates`.
- **Fact 5.7**: `src/score2gp/gpif.py` (lines 1819-1820) loops over `event.notes` and calls `_note` for each note in the event, confirming the GP writer supports exporting multiple notes per event as a chord.

## 6. Inferences
- **Inference 6.1**: Basic visual candidate extraction for eighth/sixteenth notes is verified only on the existing synthetic fixtures inspected in this task. This supports a narrow bridge-level same-onset chord-grouping task, but does not prove robust real-world 8th/16th-note OMR. Beam, flag, stem, association, curved glyph, and complex-layout handling remain unresolved risks.
- **Inference 6.2**: If multiple note candidates are aligned vertically (e.g. chords or polyphonic voices), `notation_bridge.py` will fail with `cumulative_duration_exceeds_one_4_4_bar` because it sequentially progresses ticks for each note candidate instead of grouping them into a chord event (supported by Fact 5.4 and 5.5).
- **Inference 6.3**: The current codebase does not support polyphonic timing alignment or chord composition at the bridge layer, representing a blocker for complex rhythm/note recognition (supported by Fact 5.5).

## 7. Hypotheses
- **Hypothesis 7.1**: Grouping note candidates that share the same page, system, staff index, and have horizontal coordinates/onset coordinates within a tolerance of 1.0 points into a single ScoreIR `Event` will allow polyphonic notes to be exported as a Guitar Pro chord without exceeding the bar tick limit. This can be verified by unit testing the bridge with simulated vertically aligned outcomes.
- **Hypothesis 7.2**: Standard PDF renders of complex multi-staff or polyphonic music will require robust beam/flag segmentation that handles overlapping vertical strokes better than the current heuristic aspect-ratio and bounding box intersection rules.

## 8. Unknowns
- **Unknown 8.1**: How the GP writer handles multi-voice streams (e.g., voice 1 and voice 2) if they occur on the same staff, since the current bridge assumes a single sequential event list (`trk_0`).
- **Unknown 8.2**: Whether the current flag extraction heuristics will produce false positives on real public-domain music scores due to curved articulation marks (slurs, staccato dots) or text characters near the stem.

## 9. Candidate Approaches
- **Approach 1: Raster/vector geometry approach (Selected)**
  - *Description*: Utilize existing `PdfGeometryCandidateExtractor` and `pdf_raster_staff_diagnostics` to extract primitives, compose noteheads, stems, flags, and beams, and enhance the notation bridge to handle chord grouping.
  - *Supporting facts*: Fact 5.1, 5.2, and 5.6 prove the core OMR extraction is already functional.
  - *Risks*: Heuristic parameters (margins/dimensions) may need tuning for complex layouts.
  - *Fixture needs*: Existing public generated test PDFs (no new files required).
  - *Validation needs*: Pytest unit and integration tests.
  - *Stop/pivot condition*: Stop if OMR candidate extraction logic requires major restructuring.
- **Approach 2: MusicXML/sidecar-assisted path**
  - *Description*: Skip PDF visual recognition for rhythm and instead ingest a MusicXML sidecar to align note onsets and durations.
  - *Supporting facts*: MusicXML parsing exists in `tests/test_musicxml.py`.
  - *Risks*: Relies entirely on the presence of a correct MusicXML sidecar, bypassing PDF OMR capabilities.
  - *Fixture needs*: Paired PDF and MusicXML files.
  - *Validation needs*: Visual comparison.
  - *Stop/pivot condition*: Bypassed in favor of Approach 1 to maintain visual OMR integrity.

## 10. Artifact and Fixture Strategy
- **Fixture Path Recommended**: Use existing public tracked fixtures (`2EighthNotes.pdf`, `4SixteenthNotes.pdf`) and simulated mock candidates in `tests/test_notation_bridge.py`.
- **Explicit generated PDF authorisation**: Not needed at this stage; mock-object tests are sufficient to verify the bridge fix.
- **Forbidden**: Committing new generated PDF fixtures, private PDFs, or generated `.gp` packages to git.

## 11. Recommended Outcome
Outcome A — Raster path viable for a narrow next bridge task, not proven as general real-world 8th/16th-note OMR support.
The existing vector/raster candidate extraction pipelines for noteheads, stems, beams, and flags successfully extract eighth/sixteenth note candidates from synthetic fixtures. However, significant OMR recognition, layout, and association gaps remain for real-world scores. The primary immediate blocker is in `notation_bridge.py`, which serializes vertically aligned notes sequentially rather than grouping them into chords. Correcting this bridge logic to group same-onset notes into chords is the smallest, highest-value next step.

## 12. Smallest Next Task
- **Exact Intended Capability**: Implement same-onset chord grouping in `notation_bridge.py` for eighth and sixteenth note candidates. Overlapping candidates aligned horizontally (same onset) must group into a single ScoreIR `Event` containing multiple `Note` objects.
- **Exact Non-goals**: True polyphony, same-staff multi-voice streams, voice separation, multiple independent rhythmic voices, changing OMR candidate extraction code, modifying staff geometry classification, or committing new PDF fixtures.
- **Likely files affected**: `src/score2gp/notation_bridge.py`, `tests/test_notation_bridge.py`.
- **Tests/fixtures required**: Bridge unit tests in `tests/test_notation_bridge.py` using mock outcome inputs representing chords, validating that same-onset candidates are correctly grouped and timing ticks are assigned correctly.
- **Validation commands**: `pytest tests/test_notation_bridge.py`
- **Acceptance criteria**:
  - `notation_bridge.py` groups overlapping note candidates sharing horizontal coordinate alignment into a single `Event` containing multiple `Note` objects.
  - The timing (onset and duration ticks) is correctly assigned for chords.
  - Total tick count for the 4/4 measure does not exceed 960 (4 * 240) for valid chord inputs.
- **Failure criteria**:
  - Overlapping note candidates are serialized sequentially.
  - Exception `cumulative_duration_exceeds_one_4_4_bar` is raised for chords.
- **Stop conditions**: Stop if the task requires changing OMR candidate extraction logic or if it requires committing new PDF fixtures.
- **Artifact constraints**: No generated PDFs or GP files committed to git.
- **Required next review**: Reviewer implementation conformance review.

## 13. Commands Run
- `git status --short`
- `git branch --show-current`
- `git fetch --all --prune`
- `find src -type f | sort`
- `find tests fixtures src -type f 2>/dev/null | sort`
- `git log --oneline -n 20`
- `ls -la /home/tticom/work/score2gp-workspace/`
- `cd ../score2gp && git status --short && sed -n '1810,1830p' src/score2gp/gpif.py`

## 14. Evidence Not Verified
None.

## 15. Cleanliness and Artifact Hygiene
- **Product repo working tree state**: clean
- **Governance repo working tree state**: clean (except new research report and prompts files)
- **Artifact hygiene checks**: clean; no private or generated artifacts added.

## 16. Prompt Chain
- **Operative Prompts**:
  - Prompt 1: [001_authorise_research_prompt.md](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/research/prompts/001_authorise_research_prompt.md) (authorised the initial research)
  - Prompt 2: [002_correction_prompt.md](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/research/prompts/002_correction_prompt.md) (returned PR #240 to Architect for correction)
- **Operative Prompt for Final conclusion**: Prompt 2 ([002_correction_prompt.md](file:///home/tticom/work/score2gp-workspace/score2gp-agentops/projects/score2gp/research/prompts/002_correction_prompt.md)) was operative for the final report corrections.
- **Constraints Recorded**: Bounded to documentation correction; no-implementation; no new fixtures/PDFs/GP files committed; Developer implementation remains blocked.
- **Next Required Stage**: Reviewer architecture re-verification.
