# 0004 - Review FS-06 Notation OMR Modularisation

## Objective

Independently review product PR #381 at exact head `df60957a`. Confirm that
FS-06C through FS-06E are behaviour-preserving extractions and that
`whole_note_recogniser.py` remains a stable compatibility import surface.

## Start

1. Work only in canonical Ubuntu WSL paths under
   `/home/tticom/work/score2gp-workspace`.
2. Confirm GitHub CLI identifies `tticom-automation` and the product repository
   Git identity is `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Reviewer skill, and this
   prompt.
4. Fetch both repositories. Do not modify or repair unrelated dirty worktrees.
5. Check out product PR #381 without rewriting its branch.
6. Verify `git rev-parse HEAD` is exactly `df60957a`. Stop if it differs.

## Review Scope

- `src/score2gp/notation_omr/clef.py`
- `src/score2gp/notation_omr/pitch.py`
- `src/score2gp/notation_omr/notehead.py`
- `src/score2gp/notation_omr/duration.py`
- `src/score2gp/notation_omr/timeline.py`
- `src/score2gp/notation_omr/pipeline.py`
- `src/score2gp/whole_note_recogniser.py`

Review for:

- changed signatures, return shapes, exception behavior, ordering, or imports;
- circular dependencies or incorrect relative imports;
- legacy symbols no longer exported through `whole_note_recogniser.py`;
- source functions duplicated instead of moved;
- behavior changes hidden inside the refactor;
- missing direct or existing regression coverage.

## Required Verification

Run:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

Also verify representative compatibility identities:

```bash
.venv/bin/python -c 'from score2gp import whole_note_recogniser as legacy; from score2gp.notation_omr import clef, pitch, notehead, duration, timeline, pipeline; assert legacy.extract_treble_clef_candidate_evidence is clef.extract_treble_clef_candidate_evidence; assert legacy.map_clef_resolved_staff_pitch is pitch.map_clef_resolved_staff_pitch; assert legacy.shape_whole_note_candidate_evidence is notehead.shape_whole_note_candidate_evidence; assert legacy.compose_filled_duration_candidates is duration.compose_filled_duration_candidates; assert legacy.build_staff_timeline_preview is timeline.build_staff_timeline_preview; assert legacy.run_recognition_on_file is pipeline.run_recognition_on_file'
```

## Publication

Publish an independent GitHub review on PR #381:

- request changes for any correctness, compatibility, or scope defect;
- otherwise approve it and state the exact reviewed head and verification;
- do not modify the product branch;
- do not merge the PR;
- do not start another task.
