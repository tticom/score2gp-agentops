# Antigravity Task: Palm Mute / Let Ring Minimal Support v0.1

## Role

You are the Developer.

Implement minimal support for palm mute and let ring PDF technique text candidates. These markings are already extracted as PDF text candidates but currently treated as unsupported or skipped in `build_ir.py`.

This is a narrow implementation branch. Do not implement long-range/span semantics. Do not infer continuation lines. Do not parse vector markings.

## Dependency

Proceed only after these PRs are merged into `main`:

* `feature/gpif-hammer-pull-slide-minimal-v0.1`
* `feature/pdf-technique-x-proximity-assignment-v0.1`

Start from clean, current main:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/pdf-palm-mute-let-ring-minimal-v0.1
```

If the branch already exists, inspect it before reuse:

```bash
git status
git branch --show-current
git log --oneline --decorate --max-count=10
git diff --stat
```

## Current verified state

The previous technique proximity branch added visual x-proximity assignment for slide, hammer-on, and pull-off text candidates.

The relevant baseline after Prompt 2 should be:

```text
Full public tests: 444 passed
Lessons 3–7: stable at gp_output_technique_loss_expected
Melodic soloing: stable at gp_output_fret_matching_suspect
Private-safety invariant: git ls-files fixtures/private work -> fixtures/private/.gitkeep
```

Research finding:

* Palm mute and let ring are extracted from PDF text candidates.
* They are currently skipped/unsupported in `build_ir.py`.
* ScoreIR models for `PalmMuteTechnique` and `LetRingTechnique` appear to exist.
* GPIF writer support is believed to exist, but verify before depending on it.

## Goal

Map existing palm mute and let ring technique text candidates into the existing ScoreIR note technique model using the same conservative x-proximity alignment used for slide.

For this branch:

```text
palm mute = note-level technique only
let ring = note-level technique only
```

Do not infer spans, ranges, or continuation duration.

## Non-goals

Do not implement long-range palm mute or let ring spans.
Do not infer technique duration from lines, dashes, repeated text, or visual extenders.
Do not parse PDF vector drawings.
Do not change PDF extraction.
Do not redesign ScoreIR.
Do not implement unrelated techniques.
Do not change hammer-on, pull-off, or slide behaviour except where needed to share a helper safely.
Do not modify private fixtures.
Do not commit generated outputs or anything under `work/`.

## Required pre-flight checks

Run from `score2gp`:

```bash
git status
git branch --show-current
git log --oneline --decorate --max-count=10
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
```

Expected private-safety output:

```text
fixtures/private/.gitkeep
```

Stop if clean main fails public tests, private audit cannot run, or the private-safety invariant is violated.

## Investigation guidance

Inspect:

```text
src/score2gp/build_ir.py
src/score2gp/ir.py
src/score2gp/gpif.py
src/score2gp/gp_package.py
tests/test_symbol_attachment.py
tests/test_gp_writer.py
tests/test_build_ir.py
```

Search:

```bash
rg -n "palm|mute|let ring|let-ring|let_ring|PalmMute|LetRing|unsupported_technique_text|technique-text|_classify_technique|_attach_symbols_and_techniques" src tests
```

Confirm before editing:

1. Exact constructor signatures for `PalmMuteTechnique` and `LetRingTechnique`.
2. Whether they need explicit `kind` values.
3. Whether `gpif.py` serializes them.
4. Whether `gp_package.py` parses them back.
5. Whether existing tests already cover writer/parser behaviour.

Do not guess constructor parameters.

## Implementation guidance

### 1. Extend `_classify_technique`

Add conservative mappings for palm mute:

```text
"palm-mute"
"p.m."
"p.m"
"pm"
"palm mute"
```

Map these to:

```text
"palm-mute"
```

Add conservative mappings for let ring:

```text
"let-ring"
"l.r."
"l.r"
"lr"
"let ring"
```

Map these to:

```text
"let-ring"
```

Respect whatever normalization `_classify_technique` already uses. Do not create overly broad matching that could misclassify ordinary text.

### 2. Extend note-level x-proximity attachment

Extend the single-note x-proximity technique logic currently used for slide so it also handles:

```text
palm-mute
let-ring
```

Expected behaviour:

* If `candidate.x` is present and notes have visual x coordinates:

  * choose the closest note by visual x distance;
  * if the nearest and second-nearest notes differ by less than `TECHNIQUE_ATTACHMENT_AMBIGUITY_EPSILON`, do not attach;
  * emit `ambiguous_technique_attachment`.
* If `candidate.x` is missing or no note x coordinates are available:

  * preserve fallback exact-count behaviour;
  * attach only when there is exactly one note in the bar;
  * otherwise emit the existing ambiguity warning.
* Do not infer target spans.
* Do not attach to multiple notes.
* Do not attach across bars.

### 3. Instantiate the correct ScoreIR technique

Use the existing ScoreIR model:

```text
PalmMuteTechnique
LetRingTechnique
```

Verify whether the constructors require `kind="palm-mute"` / `kind="let-ring"` or have defaults.

Do not create generic `Technique(kind="palm-mute")` unless the model design already does that elsewhere.

### 4. Preserve existing slide / hammer / pull behaviour

Existing Prompt 2 tests must continue to pass.

Do not change the ambiguity threshold unless tests prove it is required.

## Required public tests

Add tests in `tests/test_symbol_attachment.py`.

Create `test_proximity_palm_mute_let_ring_attachment` or equivalent, covering:

1. `pm` candidate attaches to the closest note using visual x-proximity.
2. `p.m.` or `palm mute` is classified and attaches.
3. `lr` candidate attaches to the closest note using visual x-proximity.
4. `l.r.` or `let ring` is classified and attaches.
5. Ambiguous nearest note distance emits `ambiguous_technique_attachment` and does not attach.
6. Fallback succeeds when visual coordinates are unavailable and there is exactly one note in the bar.
7. Fallback warns and does not attach when visual coordinates are unavailable and there are multiple notes in the bar.
8. Existing slide / hammer / pull proximity tests still pass.

Add or extend GPIF tests where practical:

1. ScoreIR containing `PalmMuteTechnique` writes to GPIF without warnings.
2. ScoreIR containing `LetRingTechnique` writes to GPIF without warnings.
3. If GPIF parser already supports these techniques, assert round-trip recovery.
4. If parser does not support them, document that as a known limitation and do not broaden scope unless the parser change is tiny and safe.

## Validation commands

Run targeted tests:

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_symbol_attachment.py -k "palm or mute or let or ring or technique"
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_symbol_attachment.py
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_gp_writer.py -k "palm or mute or let or ring" || true
```

Then run full validation:

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest
PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py
git status --ignored
git ls-files fixtures/private work
find . -path "./.git" -prune -o -type f -size +10M -print
```

Expected tracked private files output:

```text
fixtures/private/.gitkeep
```

## Acceptance criteria

This branch is complete only when:

1. Palm mute text candidates classify correctly.
2. Let ring text candidates classify correctly.
3. Palm mute attaches to the closest unambiguous note using visual x-proximity.
4. Let ring attaches to the closest unambiguous note using visual x-proximity.
5. Ambiguous palm mute / let ring candidates warn and do not attach incorrectly.
6. Exact-count fallback is preserved when x coordinates are unavailable.
7. Existing slide / hammer-on / pull-off tests still pass.
8. GPIF writer support for palm mute / let ring is covered by public tests, or documented if not currently possible.
9. Full public tests pass.
10. Private audit shows no regression in Lessons 3–7 or melodic soloing.
11. No private/generated artifacts are tracked.

## Stop conditions

Stop and report instead of continuing if:

* `PalmMuteTechnique` or `LetRingTechnique` cannot be represented in ScoreIR without model changes.
* Correct implementation requires span/range semantics.
* Correct implementation requires vector line/dash detection.
* You cannot classify the text forms safely without broad false positives.
* Existing slide / hammer-on / pull-off proximity behaviour regresses.
* Full public tests fail for unrelated reasons.
* Private audit regresses Lessons 3–7 or melodic soloing.
* Any private PDF, XML, GP package, audit JSON, overlay, log, or `work/` artifact becomes tracked or staged.

## Required product PR body

When opening the product PR, include:

```text
Summary:
- Adds minimal palm mute and let ring classification from existing PDF technique text candidates.
- Reuses conservative visual x-proximity note attachment.
- Preserves exact-count fallback when coordinates are unavailable.
- Does not infer long-range/span semantics.

Validation:
- <targeted symbol tests>
- <GPIF writer tests, if added>
- <full pytest result>
- <private audit summary, private-safe only>
- git ls-files fixtures/private work -> fixtures/private/.gitkeep

Known limitations:
- Palm mute and let ring are note-level only in this branch.
- Long-range spans, continuation lines, repeated text, and vector markings are not inferred.
- GPIF parse recovery is only included if already supported or implemented trivially.
```

## Governance record

Create a run record in `score2gp-agentops` under:

```text
projects/score2gp/runs/2026-06-02-pdf-palm-mute-let-ring-minimal-v0.1/
```

Include:

```text
RUN.md
prompt-manifest.json
prompts/001-implementation-prompt.md
```

The governance record must include:

* exact product branch name;
* exact agentops branch name;
* files changed;
* commands run;
* public test results;
* private audit summary, private-safe only;
* private-safety invariant result;
* known limitations.

## Feedback gate

After opening the product and governance PRs, stop.

Do not proceed to slur recovery until both PRs are reviewed and merged.
