# 0006 - CR-03D Local Triplet Association

## Objective

Implement the previously approved deterministic association of a printed
tuplet `3` with exactly one local sequence of three eighth-note events. Reject
TAB fret digits, measure labels, metadata text, and ambiguous geometry. This is
a bounded diagnostic association task, not a claim of end-to-end corpus repair.

## Start

1. Work only in canonical Ubuntu WSL paths under
   `/home/tticom/work/score2gp-workspace`.
2. Confirm GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Developer skill, this prompt,
   and:
   - `reports/2026-07-18-cr-03a-architect-report.md`
   - `reviews/2026-07-18-cr-03a-architect-review.md`
   - `tasks/2026-07-17-visual-output-correctness-backlog.md`
4. Fetch product `origin/main`; require exact base
   `dacb0e53e47a366c557d2bba78851b77145874fb`.
5. Require a clean product worktree and create
   `agy/cr03d-local-triplet-association` from that revision.
6. Do not copy code from the reverted CR-03A prototype or recovery branches.

## Product Boundary

Allowed product files:

- `[NEW] src/score2gp/notation_omr/tuplet.py`
- `[MODIFY] src/score2gp/notation_omr/pipeline.py`
- `[MODIFY] src/score2gp/notation_omr/timeline.py`
- `[MODIFY if needed] src/score2gp/notation_omr/__init__.py`
- `[NEW] tests/test_notation_omr_tuplet.py`
- `[MODIFY if strictly needed]` one existing public PDF fixture generator and
  its directly corresponding public test.

Do not modify:

- `src/score2gp/whole_note_recogniser.py`;
- CLI contracts, ScoreIR, MusicXML importer, GP writer, schemas, private
  fixtures, or unrelated diagnostics;
- generated schema files or repository governance files.

If existing committed diagnostics cannot expose a candidate tuplet marker with
page/system/staff/span and bounding-box evidence, stop and report that precise
observability gap. Do not broaden the file list or invent marker evidence.

## Required Model and Association Rule

Implement typed immutable or validation-backed representations for:

- `TupletMarkerEvidence`: marker ID, literal `3`, page/system/staff ownership,
  span ID, bounding box, source, and geometry facts;
- `TupletAssociation`: marker ID, exactly three ordered candidate IDs, ratio
  `3:2`, span ID, geometry facts, and status `associated` or `ambiguous`.

A marker may associate only when:

1. it lies in the above-standard-staff lane from the top staff line to two
   staff spaces above it;
2. marker and events share page, system, staff, and explicit span ownership;
3. its x-center lies strictly between the first and third notehead centers;
4. the group contains exactly three sequential eighth-note events with no
   intervening rest or different duration;
5. exactly one candidate group satisfies all constraints.

Zero matching groups means no association. Multiple matching groups or
competing markers mean `ambiguous`; surface that status in pipeline/timeline
diagnostics and do not scale or guess.

No global count threshold, “11 eighth notes” fallback, filename rule, fixed
measure index, or fixture coordinate is permitted.

## Public Regression Contract

Tests must include:

- one genuine above-staff tuplet `3` associated to exactly three eighth notes;
- a TAB fret `3` or `13`;
- a measure label `3`;
- metadata containing `[3:50]`;
- a marker positioned ambiguously between competing three-event groups;
- ordinary unmarked eighth-note groups in 6/8 and 12/8;
- malformed ownership, missing span, and invalid geometry.

Prove:

- only the genuine marker produces `associated`;
- adversarial digits produce no association;
- ambiguity is explicit and fail-closed;
- unmarked compound-meter eighth notes remain unscaled;
- association status is not discarded before timeline diagnostics.

## Verification

Run:

```bash
.venv/bin/python -m pytest -q tests/test_notation_omr_tuplet.py
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

## Publication

Commit only the allowed product files, push the `agy/` branch, and open one
draft product PR. The PR body must state the exact head SHA, rule implemented,
adversarial cases, tests, limits, and first remaining mismatch. Do not merge,
enable auto-merge, or begin CR-04A.
