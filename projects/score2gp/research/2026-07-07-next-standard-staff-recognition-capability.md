# Architect Research — Next Standard-Staff Recognition Capability

## Verdict
Outcome B

## Verified Baseline
- Product PR #337: squash-merged at `eae13541de67899ff9563a09f48ed747171dea6b`
- Governance PR #242: squash-merged at `373b6836b2121b82ad815753bcf78bc90e942137`
- Governance PR #243: squash-merged at `e43afed7ac541c8b1710693b5e0bce6a46bce9d4`
- Current product main SHA: `eae13541de67899ff9563a09f48ed747171dea6b`
- Current governance main SHA: `e43afed7ac541c8b1710693b5e0bce6a46bce9d4`

## Files Inspected
- `src/score2gp/notation_bridge.py`
- `tests/test_notation_bridge.py`
- `src/score2gp/whole_note_recogniser.py`
- `src/score2gp/pdf_staff_notation_diagnostics.py`
- `tests/test_whole_note_recogniser_fractional_beam_extraction.py`
- `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`

## Commands Run
- `PYTHONPATH=. .venv/bin/pytest tests/test_notation_bridge.py tests/test_whole_note_recogniser_fractional_beam_extraction.py`
- `PYTHONPATH=. .venv/bin/pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py`

## Facts
- **Fact 1**: `src/score2gp/notation_bridge.py` sorts outcomes by `(page, sys, staff, x_pos, candidate_id)`.
- **Fact 2**: `src/score2gp/notation_bridge.py` sequentially accumulates duration ticks using `current_onset_ticks += dur_ticks` unconditionally for all outcomes, regardless of whether they lie on different staves (`staff_index`).
- **Fact 3**: `notation_bridge.py` raises `NotationBridgeInputError("cumulative_duration_exceeds_one_4_4_bar")` if `current_onset_ticks + dur_ticks` exceeds 960 (4 * 240) ticks.
- **Fact 4**: The `ScoreIR` structure defined in `src/score2gp/ir.py` natively supports multiple `Track` objects.
- **Fact 5**: Synthetic multi-staff PDF fixture `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf` is already committed to the product repository.

## Inferences
- **Inference 1**: If a PDF contains multiple staves on a system (such as a piano score or a standard notation and tab pair), `notation_bridge.py` will serialize the note candidates from the second staff sequentially *after* the note candidates of the first staff.
- **Inference 2**: Because of sequential serialization, any multi-staff input will likely fail with a `cumulative_duration_exceeds_one_4_4_bar` error or generate incorrect timing in a single track (`trk_0`).
- **Inference 3**: Fixing multi-staff alignment is a logical timing/bridge mapping problem rather than a visual OMR extraction problem. It can be solved entirely in `notation_bridge.py` using existing candidate metadata (page, system, staff_index).

## Hypotheses
- **Hypothesis 1**: Tracking `current_onset_ticks` independently for each `staff_index` and mapping each unique `staff_index` to its own `Track` in `ScoreIR` will allow parallel multi-staff notation to be exported as separate tracks in a Guitar Pro file. This will prevent tick overflow errors and align parallel events correctly.
- **Hypothesis 2**: Visual OMR candidate extraction heuristics (stems, flags, beams) on complex layouts are highly sensitive to layout geometry and will require extensive visual tuning. Implementing logical bridge timing is a lower-risk and higher-value next step than visual parameter tuning.

## Unknowns
- **Unknown 1**: Whether the GP writer (`gp_package.py` and `gpif.py`) will require adjustments to export multiple parallel standard notation tracks cleanly, since standard staff multi-track export has not yet been end-to-end integration tested.

## Candidate 1 — Raster/OMR Stem, Flag, and Beam Association
- **Evidence**: `whole_note_recogniser.py` associates flags and beams using basic bounding box intersections and hardcoded threshold checks (such as checking if a flag is to the right of the stem).
- **Viability**: Low. While the current heuristics are sufficient for synthetic fixtures, hardening them for complex layouts is highly speculative. More importantly, even if visual candidate extraction is improved, the bridge remains blocked from processing multi-staff files.
- **Required tests/fixtures**: Synthetic fixtures like `2EighthNotes.pdf` are already present, but complex layouts would require new visual fixtures.
- **Risks**: High risk of regression on existing fixtures and infinite heuristic parameter tuning.
- **Stop/pivot triggers**: Stop if visual parameters require separate tuning for different fixtures.
- **Decision**: Rejected as the immediate next step.

## Candidate 2 — Multi-Staff / Limited Multi-Voice Bridge Timing
- **Evidence**: `notation_bridge.py` has access to `page_index`, `system_index`, and `staff_index` / `system_staff_index` metadata on outcomes, but currently serializes all outcomes sequentially on `trk_0`.
- **Viability**: High. This is a pure logical mapping task that directly unblocks multi-staff files (such as grand staff or multi-instrument scores).
- **Required tests/fixtures**: Can be fully tested using mock outcomes representing multiple staves in `tests/test_notation_bridge.py`.
- **Risks**: Low risk since it is logical and does not touch OMR image processing or staff detection algorithms.
- **Stop/pivot triggers**: Stop if it requires modifying visual feature extraction or staff geometry models.
- **Decision**: Selected.

## Candidate 3 — Smaller Bridge/Export-Side Capability
- **Evidence**: Quarter rests are already mapped.
- **Viability**: Low. No other smaller logical capabilities are blocked that do not require either visual extraction changes (Candidate 1) or timing strategy changes (Candidate 2).
- **Required tests/fixtures**: N/A
- **Risks**: N/A
- **Stop/pivot triggers**: N/A
- **Decision**: Rejected.

## Selected Outcome
- **Outcome**: Outcome B (Raster/OMR path not currently viable, but another bounded approach is viable).
- **Reason**: The OMR extraction heuristics are not robust enough for general complex scores, but we can make significant progress by enabling multi-staff track separation and parallel timing in the bridge using existing candidate metadata.
- **Why rejected candidates were not selected**: Candidate 1 (OMR robustness) was rejected because it does not unblock multi-staff/multi-track support and has high visual tuning risk. Candidate 3 was rejected because no smaller high-value logic-only task exists.

## Recommended Next Task
- **Role**: Developer
- **Task title**: Implement multi-staff track separation and parallel timing in `notation_bridge.py`
- **Baseline**: Product PR #337 merged.
- **Scope**:
  - Map each unique `staff_index` in outcomes to a separate `Track` in `ScoreIR` (e.g. `trk_0` for `staff_index=0`, `trk_1` for `staff_index=1`).
  - Track `current_onset_ticks` independently for each staff/track, allowing parallel progression of time.
  - Align parallel events using their horizontal coordinates (`x_pos`) or independent onset tracking per track.
- **Non-goals**:
  - True same-staff polyphony (multiple independent voices on a single staff).
  - Modifying any OMR candidate extraction or staff geometry logic.
  - Committing new PDF/GP fixtures to git.
- **Files likely in scope**: `src/score2gp/notation_bridge.py`, `tests/test_notation_bridge.py`.
- **Tests / evidence required**: Unit tests in `tests/test_notation_bridge.py` verifying multi-staff outcomes produce multiple tracks with correct parallel onsets and durations.
- **Acceptance criteria**:
  - Outcomes with different `staff_index` values are mapped to separate tracks.
  - Timing for each track is tracked independently.
  - Multi-staff inputs do not raise `cumulative_duration_exceeds_one_4_4_bar` for valid parallel structures.
- **Failure criteria**:
  - Outcomes from different staves are serialized sequentially.
  - Timing across tracks is incorrect.
- **Stop/pivot triggers**: Stop if the task requires changing OMR candidate extraction code or if the GP writer fails to export multi-track standard staff notation.
- **Required next review**: Reviewer implementation conformance review.

## Developer Authorisation
- **Developer authorised now**: No
- **Conditions required before Developer work**: The Supervisor must merge this research report PR, update the governance plan, and explicitly copy the approved task description into `ACTIVE_TASK.md` under a new governance PR.

## Artifact Hygiene
- **Private/generated artifacts**: None
- **Product repo modified**: No
- **Governance repo modified**: Yes (created research report)
