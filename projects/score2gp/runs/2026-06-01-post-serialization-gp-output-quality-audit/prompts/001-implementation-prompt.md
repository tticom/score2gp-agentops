# Antigravity Task: Post-Serialization GP Output Quality Audit v0.1

## Pre-Flight Merge Check

Before writing code or creating a new branch, verify that both recent PRs are merged and local workspaces are synced.

Run in `score2gp`:

```bash
gh pr view 154 --web=false
git switch main
git pull --ff-only origin main
python -m pytest
```

Run in `score2gp-agentops`:

```bash
gh pr view 17 --web=false
git switch main
git pull --ff-only origin main
```

Proceed only if:

* `score2gp` PR #154 is merged.
* `score2gp-agentops` PR #17 is merged.
* Local `main` is clean and synced in both repos.
* Public tests pass.

If any of these are false, stop and report the exact state. Do not create a branch.

## Branch

Create in `score2gp`:

```bash
git switch -c research/post-serialization-gp-output-quality-audit-v0.1
```

This is a research/diagnostic branch first. Do not start by implementing a new feature.

## Context

The project has now passed a major milestone:

* Large-spaced TAB staff detection is implemented.
* MusicXML polyphony diagnostics are implemented.
* Strict duplicate standard-notation/TAB voice deduplication is implemented.
* Private lesson scores reportedly serialize Guitar Pro packages under default `allow_remediation=False`.

This is real progress, but it is not the same as semantic correctness.

A valid `.gp` package can still be wrong if:

* the staff is non-empty but missing many notes
* bars are shifted
* durations are wrong
* duplicate notes remain
* notes are assigned to wrong strings/frets
* slurs/hammer-ons/pull-offs/slides/bends are lost
* GPIF contains structurally valid but musically incomplete tracks
* warnings reveal a new first blocker

This task must classify the next true blocker after successful serialization.

## Goal

Create a private-safe post-serialization quality audit that compares the pipeline stages for each private score and reports whether generated Guitar Pro packages are musically plausible enough to move toward technique serialization, or whether there is still a more basic alignment/timing/note-coverage defect.

The output should answer:

```text
Now that GP packages are generated, what is the next real correctness blocker?
```

## Non-Goals

Do not implement full support for:

* hammer-ons
* pull-offs
* slides
* bends
* bend releases
* GPIF technique curves
* manual fixture transcription
* broad rhythm reconstruction
* visual screenshot comparison
* private artifact promotion into git

Do not claim success based only on file existence.

Do not commit private PDFs, GP files, ScoreIR files, rendered images, extracted JSON, or `work/` artifacts.

## Required Investigation

Run the full private smoke flow and inspect generated private-safe summaries.

For each private input score, report only counts, statuses, warning codes, and artifact paths.

Required private-safe metrics per input:

* input label
* pass/fail status
* first failing stage, if any
* inferred system count
* detected bar count
* MusicXML measure count
* ScoreIR bar count
* ScoreIR event count
* ScoreIR note count
* GPIF measure count
* GPIF beat count
* GPIF note count
* playable fret candidate count
* matched fret candidate count
* unmatched fret candidate count
* non-playable technique/text candidate count
* warning code counts
* whether duplicate staff/TAB deduplication was applied
* whether large-spaced TAB detection was applied
* whether GP package was produced
* whether GP package contains non-empty note content
* artifact paths only

Do not include note sequences, fret sequences, score text, coordinates, screenshots, or copied commercial content.

## Required Classification

For each private score, classify the current state as one of:

```text
gp_output_quality_pass_basic
gp_output_empty_or_near_empty
gp_output_note_coverage_low
gp_output_bar_alignment_suspect
gp_output_duration_alignment_suspect
gp_output_fret_matching_suspect
gp_output_duplicate_notes_suspect
gp_output_technique_loss_expected
gp_output_technique_loss_blocking
gp_output_unknown_quality
```

Definitions:

### `gp_output_quality_pass_basic`

Use only when:

* GP package exists
* GPIF contains non-zero notes
* ScoreIR contains non-zero notes
* bar counts are plausible
* matched fret candidate count is plausible
* no critical warning category remains
* no obvious empty-staff or shifted-bar symptom remains

This does not mean final musical correctness.

### `gp_output_technique_loss_expected`

Use when:

* notes are present
* basic alignment is plausible
* guitar techniques are visibly detected or expected
* technique serialization is not yet implemented
* loss of technique detail is now the next known limitation

### `gp_output_note_coverage_low`

Use when:

* GP package exists
* but note count is much lower than playable fret candidates or expected MusicXML events
* unmatched candidates remain high

### `gp_output_bar_alignment_suspect`

Use when:

* bars exist
* but measure/bar mapping warnings suggest shifted or skipped bars

### `gp_output_fret_matching_suspect`

Use when:

* MusicXML notes exist
* TAB candidates exist
* but matched fret candidates are unexpectedly low

## Public-Safe Instrumentation

If existing summaries do not expose enough information, add narrow public-safe summary instrumentation.

Preferred script updates:

* `scripts/private_e2e_smoke.py`
* `scripts/private_diagnostic_smoke.py`
* or a new script such as `scripts/private_gp_quality_audit.py`

If adding a new script, it must:

* write reports only under `work/`
* be safe to run locally
* never write private content into git
* report only counts/statuses/warning codes/artifact paths
* avoid printing private note/fret sequences

Recommended output path:

```text
work/private_gp_quality_audit_v0_1/summary.json
```

## Public Tests

If code is added, include public synthetic tests for the summary logic.

Suggested tests:

### Test 1: Non-empty ScoreIR/GPIF Is Classified as Basic Pass

Synthetic public fixture with:

* non-empty ScoreIR
* non-empty GPIF note count
* matched candidate count above zero

Expected:

```text
gp_output_quality_pass_basic
```

### Test 2: Empty GPIF Is Classified as Empty/Near-Empty

Synthetic public fixture with:

* GP package or GPIF structure present
* zero notes

Expected:

```text
gp_output_empty_or_near_empty
```

### Test 3: Low Matched Candidate Count Is Classified

Synthetic summary with:

* many playable candidates
* low matched candidates

Expected:

```text
gp_output_fret_matching_suspect
```

### Test 4: Technique Markers Without Serialization Are Classified Separately

Synthetic summary with:

* notes present
* technique/text candidates present
* no critical alignment failures

Expected:

```text
gp_output_technique_loss_expected
```

Do not add tests that depend on private files.

## Private Smoke

Run:

```bash
python scripts/private_e2e_smoke.py
```

If the new audit script exists, run:

```bash
python scripts/private_gp_quality_audit.py
```

Report only:

* summary path
* per-input status category
* key counts
* warning code counts
* next blocker classification

Do not report private content.

## Validation Commands

Run:

```bash
python -m pytest
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
python scripts/private_e2e_smoke.py
git diff --check
git ls-files fixtures/private work
```

Expected private-safety invariant:

```text
fixtures/private/.gitkeep
```

If new public tests are added, run them explicitly as well.

## Deliverables

Produce a private-safe research report containing:

* branch name
* files changed
* whether new instrumentation was added
* private-safe per-score quality categories
* current first blocker per score
* whether all generated GP packages are non-empty
* whether note coverage appears plausible
* whether bar alignment appears plausible
* whether guitar technique loss is now the next blocker
* validation results
* private-safety audit result
* recommended next branch

## Acceptance Criteria

This task is complete when:

1. Every private input has a post-serialization quality category.
2. Generated GP packages are checked for non-empty musical content, not just file existence.
3. The report identifies the next true blocker after serialization.
4. Any new instrumentation is private-safe and covered by public tests where appropriate.
5. The full public test suite passes.
6. No private artifacts are committed.
7. The next branch is narrowly scoped and justified by evidence.

## Merge Rule

PR this branch only if it adds durable value, such as:

* a reusable private-safe quality audit script,
* public tests for quality classification,
* or a clear diagnostic report that identifies the next blocker.

Do not PR if the branch only adds generic handoff text.

## Likely Next Branches

Choose the next implementation branch only after the audit.

Possible outcomes:

```text
feature/guitar-technique-preservation-v0.1
feature/gpif-hammer-pull-slide-minimal-v0.1
feature/gpif-bend-release-research-v0.1
feature/fret-matching-coverage-improvement-v0.1
feature/bar-alignment-quality-gate-v0.1
research/gp-output-semantic-diff-v0.1
```

Do not choose one until the audit proves the next blocker.
