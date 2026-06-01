# Antigravity Task: Bar Alignment Quality Gate v0.1

## Pre-Flight Merge Check

Before writing code or creating a new branch, verify that both recent PRs have been merged and local workspaces are synced.

Run in `score2gp`:

```bash
gh pr view 155 --web=false
git switch main
git pull --ff-only origin main
python -m pytest
```

Run in `score2gp-agentops`:

```bash
gh pr view 18 --web=false
git switch main
git pull --ff-only origin main
```

Proceed only if:

* `score2gp` PR #155 is merged.
* `score2gp-agentops` PR #18 is merged.
* Local `main` is clean and synced in both repositories.
* Public tests pass.

If any condition fails, stop and report the exact state. Do not create a branch.

## Branch

Create in `score2gp`:

```bash
git switch -c feature/bar-alignment-quality-gate-v0.1
```

## Context

The post-serialization GP output quality audit is now strict enough to compare actual serialized GPIF output against ScoreIR.

The latest audit produced two important findings:

1. Lessons 3–7 now classify as:

```text
gp_output_bar_alignment_suspect
```

Reason:

```text
GPIF measure count differs from ScoreIR bar count by exactly 4 bars.
```

This appears to be related to cover-page/booklet/movement setup bars added by the booklet compiler, but that must be verified from code and artifacts. Do not assume the +4 bars are correct.

2. The melodic soloing score still classifies as:

```text
gp_output_empty_or_near_empty
```

Reason:

```text
59 playable fret candidates remain unmatched, resulting in 0 notes.
```

That melodic soloing blocker is out of scope for this branch unless investigation proves it is caused by the same bar alignment issue.

## Goal

Build a safe bar-alignment quality gate that distinguishes:

* expected GPIF template/booklet prelude bars,
* expected movement/cover-page setup bars,
* real bar loss,
* real bar duplication,
* shifted bar alignment,
* and unknown mismatch cases.

The goal is not to force GPIF and ScoreIR counts to match blindly.

The correct behaviour is:

```text
Expected structural/template bars should be recognised and reported.
Unexpected musical bar mismatches should remain defects.
```

## Non-Goals

Do not implement guitar technique serialization.

Do not implement hammer-ons, pull-offs, slides, bends, or bend releases.

Do not “fix” the +4 bar mismatch by deleting GPIF bars unless code evidence proves they are wrong.

Do not weaken the quality audit so that any fixed offset is automatically accepted.

Do not hide genuine bar loss or duplication.

Do not make melodic soloing pass by bypassing matching, barline construction, or onset mapping.

Do not commit private artifacts, private PDFs, generated GP files, rendered images, ScoreIR JSON, extracted tab JSON, or anything under `work/`.

## Required Investigation

### 1. Locate where the +4 bars are introduced

Inspect the code path that builds the final `.gp` / GPIF package for custom Lessons 3–7.

Find:

* where GPIF measures are created,
* whether booklet/template/cover-page bars are intentionally inserted,
* whether movement setup bars are expected,
* whether the +4 bars appear before musical content, after musical content, or interleaved,
* whether the added bars have metadata, empty beats, rests, titles, repeat markers, section labels, or movement markers,
* whether they are consistent across all affected private lesson scores.

Do not report private note sequences or copied score content.

Private-safe reporting may include:

* counts,
* offsets,
* warning codes,
* stage names,
* artifact paths,
* and whether mismatch appears as prefix/suffix/interleaved.

### 2. Define bar alignment semantics

Create a precise distinction between:

```text
scoreir_bar_count
gpif_measure_count
musical_gpif_measure_count
template_gpif_measure_count
expected_prelude_measure_count
unexpected_measure_delta
```

The audit should not compare raw `gpif_measure_count` to `scoreir_bar_count` when GPIF intentionally includes non-musical template/prelude measures.

Instead, it should compare:

```text
musical_gpif_measure_count == scoreir_bar_count
```

when the template/prelude bars are verified.

### 3. Add explicit metadata or detection

Prefer explicit metadata over magic offsets.

Good options:

* detect known template/prelude GPIF measures by structural markers,
* add metadata from the booklet compiler identifying expected prelude/template measures,
* record `template_gpif_measure_count`,
* record `musical_gpif_measure_start_index`,
* record `musical_gpif_measure_count`,
* record `expected_template_measure_count`.

Avoid:

```text
if delta == 4: pass
```

unless that rule is backed by explicit template metadata and public tests.

### 4. Update the quality audit classification

Update `scripts/private_gp_quality_audit.py`.

The classification should become:

```text
gp_output_quality_pass_basic
```

only when:

* GPIF exists,
* GPIF contains non-zero notes,
* ScoreIR contains non-zero notes,
* serialized GPIF note coverage is acceptable,
* and musical GPIF measure count aligns with ScoreIR bar count after known template/prelude bars are accounted for.

Add or preserve these categories:

```text
gp_output_bar_alignment_suspect
gp_output_expected_template_bars_accounted
gp_output_template_bar_metadata_missing
gp_output_template_bar_count_mismatch
gp_output_empty_or_near_empty
gp_output_note_coverage_low
gp_output_technique_loss_expected
```

If you do not want to add new public category names, at least add machine-readable fields that explain the alignment:

```json
{
  "raw_gpif_measure_count": 28,
  "scoreir_bar_count": 24,
  "template_gpif_measure_count": 4,
  "musical_gpif_measure_count": 24,
  "bar_alignment_status": "expected_template_bars_accounted"
}
```

### 5. Keep real mismatches strict

The following must still classify as `gp_output_bar_alignment_suspect`:

* GPIF has fewer musical measures than ScoreIR.
* GPIF has extra musical measures not marked as template/prelude.
* extra measures are interleaved with musical bars.
* template bar count does not match compiler metadata.
* template/prelude bars contain unexpected note content.
* alignment offset varies across the score.
* no metadata/detection explains the mismatch.

## Public Tests

Add public tests under:

```text
tests/test_gp_quality_audit.py
```

or a new file:

```text
tests/test_bar_alignment_quality_gate.py
```

Required tests:

### Test 1: Expected template prelude bars are accounted for

Synthetic summary:

```json
{
  "scoreir_bar_count": 24,
  "gpif_measure_count": 28,
  "template_gpif_measure_count": 4,
  "musical_gpif_measure_count": 24,
  "gpif_note_count": 100,
  "scoreir_note_count": 100
}
```

Expected:

```text
not gp_output_bar_alignment_suspect
bar_alignment_status == expected_template_bars_accounted
```

### Test 2: Raw +4 mismatch without template evidence remains suspect

Synthetic summary:

```json
{
  "scoreir_bar_count": 24,
  "gpif_measure_count": 28,
  "template_gpif_measure_count": 0,
  "musical_gpif_measure_count": 28
}
```

Expected:

```text
gp_output_bar_alignment_suspect
```

### Test 3: Template bars with note content remain suspect

If template/prelude measures contain playable notes unexpectedly, classify as suspect.

Expected:

```text
gp_output_bar_alignment_suspect
```

### Test 4: Fewer GPIF musical bars than ScoreIR remains suspect

Synthetic summary:

```json
{
  "scoreir_bar_count": 24,
  "gpif_measure_count": 23,
  "musical_gpif_measure_count": 23
}
```

Expected:

```text
gp_output_bar_alignment_suspect
```

### Test 5: Technique loss is only reached after bar alignment passes

Synthetic summary:

* bar alignment accounted for,
* note coverage is high,
* technique candidates exist,
* unsupported technique serialization remains.

Expected:

```text
gp_output_technique_loss_expected
```

### Test 6: Low serialized note coverage still beats template success

Synthetic summary:

* template bars accounted for,
* GPIF note count is far lower than ScoreIR note count.

Expected:

```text
gp_output_note_coverage_low
```

## Private Smoke / Audit

Run:

```bash
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py
```

Report only private-safe metrics:

* input label,
* ScoreIR bar count,
* raw GPIF measure count,
* template/prelude GPIF measure count,
* musical GPIF measure count,
* bar alignment status,
* GPIF note count,
* ScoreIR note count,
* playable fret candidate count,
* matched fret candidate count,
* warning code counts,
* quality classification,
* artifact paths only.

Do not report:

* private note sequences,
* fret sequences,
* coordinates,
* score text,
* screenshots,
* rendered pages,
* copied commercial content.

## Expected Outcome

For Lessons 3–7, one of two outcomes is acceptable:

### Outcome A: Template bars are verified

If the +4 bars are proven to be intentional template/prelude/booklet bars:

* classify them as expected template bars,
* report musical GPIF measure count separately,
* Lessons 3–7 should no longer be `gp_output_bar_alignment_suspect` solely because of the +4 raw measure delta,
* if note coverage is high and technique markers remain, they may classify as:

```text
gp_output_technique_loss_expected
```

### Outcome B: Template bars are not verified

If the +4 bars cannot be proven intentional:

* preserve `gp_output_bar_alignment_suspect`,
* report why the mismatch remains unsafe,
* recommend a narrower follow-up branch.

For melodic soloing:

* do not force a pass.
* It may remain `gp_output_empty_or_near_empty`.
* If this branch reveals that its emptiness is caused by bar alignment/musical measure indexing, report that as evidence for the next branch.
* Otherwise leave melodic soloing as the next separate blocker.

## Validation Commands

Run:

```bash
python -m pytest tests/test_gp_quality_audit.py
python -m pytest
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
python scripts/private_e2e_smoke.py
python scripts/private_gp_quality_audit.py
git diff --check
git ls-files fixtures/private work
```

Expected private-safety invariant:

```text
fixtures/private/.gitkeep
```

## Deliverables

Final report must include:

```text
Branch:
Files changed:
Where +4 GPIF bars are introduced:
Whether +4 bars are intentional:
How template/prelude bars are identified:
Public tests added:
Validation results:
Private audit summary:
Per-score quality classifications:
Melodic soloing status:
Private-safety audit:
Recommended next branch:
Merge recommendation:
```

## Acceptance Criteria

This branch is complete when:

1. The audit distinguishes raw GPIF measure count from musical GPIF measure count.
2. Expected template/prelude bars are only accepted with explicit evidence.
3. Unexplained bar mismatches remain suspect.
4. Lessons 3–7 are reclassified only if the +4 bars are verified as intentional.
5. Low serialized note coverage still fails even when template bars are accounted for.
6. Melodic soloing is not falsely passed.
7. Public tests cover both positive and negative bar-alignment cases.
8. Full public test suite passes.
9. Private smoke/audit runs without leaking private artifacts.
10. No private files or `work/` artifacts are committed.

## Governance

After the product PR is reviewed and merged, create a matching `score2gp-agentops` governance PR recording:

* original implementation prompt,
* prompt manifest,
* private-safe run summary,
* strict classifications,
* next recommended branch.

Do not merge the governance PR before the product PR.
