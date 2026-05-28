# Prompt Record

## Prompt Metadata

- Prompt ID: 001
- Source: human
- Target agent: antigravity
- Date/time: 2026-05-28T09:41:57+01:00
- Supersedes: None
- Status: executed

## Explicit Prompt Text

```text
You are an expert Python engineer working on ScoreToGP.

This is a product implementation task, but it must stay tightly bounded by the accepted research. Do not turn this into a broad layout rewrite or a conversion-success claim.

# Repositories

Product repo:

https://github.com/tticom/score2gp

Agent governance repo:

https://github.com/tticom/score2gp-agentops

# Current State

Both repos are back on `main` as the only active branch.

The following governance/research work is merged:

* `score2gp-agentops` PR #6: prompt-chain records are mandatory for ScoreToGP agent runs.
* `score2gp` PR #144: product repo points agent runs to `score2gp-agentops` for durable records and prompt-chain recording.
* `score2gp-agentops` PR #7: paired notation+TAB staff research is merged and accepted as the research basis.

# Accepted Research Basis

Read this file first from `score2gp-agentops`:

`projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/RUN.md`

Accepted finding:

The Major Triads Lesson 3 layout failure is strongly linked to the lack of an explicit paired notation+TAB layout model.

More precisely:

* The detector fragments TAB rows into partial pseudo-systems.
* Collinear horizontal TAB segments are not merged early enough.
* Notation/TAB stems pollute vertical barline-candidate telemetry.
* Five-line notation staves are not proven to be promoted as TAB systems.
* A hard “5 lines = notation / 6 lines = TAB” rule is unsafe because damaged TAB rows may be detected as five lines.
* Public fixture coverage is required before production parsing changes can be trusted.

This task must implement the first public-fixture-backed step in that direction.

# Required Pre-Flight

In `score2gp`:

```bash
git switch main
git pull --ff-only origin main
git status --short
git status --branch
git log --oneline --decorate -8
gh pr status
```

In `score2gp-agentops`:

```bash
git switch main
git pull --ff-only origin main
git status --short
git status --branch
git log --oneline --decorate -8
gh pr status
```

Stop immediately if either repo is dirty before you start.

# Branches

In `score2gp`, create:

```bash
bugfix/paired-staff-tab-grid-detection-v0.1
```

In `score2gp-agentops`, create:

```bash
runs/paired-staff-tab-grid-detection-v0.1
```

If either branch already exists, use `v0.2`.

# Mandatory Prompt Chain Record

Before completing the task, create this directory in `score2gp-agentops`:

```text
projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/
  RUN.md
  prompt-manifest.json
  prompts/
    001-implementation-prompt.md
```

Store this entire prompt exactly in:

```text
projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/prompts/001-implementation-prompt.md
```

Record it in:

```text
projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/prompt-manifest.json
```

The task is incomplete without this prompt-chain record.

# Required Reading

From `score2gp-agentops`, read:

* `projects/score2gp/README.md`
* `projects/score2gp/REVIEW_RULES.md`
* `projects/score2gp/ACCEPTANCE_TARGETS.md`
* `projects/score2gp/BENCHMARK_LADDER.md`
* `projects/score2gp/MAJOR_TRIADS_BENCHMARK.md`
* `projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/RUN.md`
* `projects/score2gp/templates/RUN_RECORD_TEMPLATE.md`
* `projects/score2gp/templates/PROMPT_CHAIN_README.md`
* `projects/score2gp/templates/PROMPT_MANIFEST_TEMPLATE.json`
* `projects/score2gp/templates/PROMPT_RECORD_TEMPLATE.md`

From `score2gp`, read:

* `AGENTS.md`
* `HANDOFF.md`
* `docs/architecture.md`
* `docs/limitations.md`
* `src/score2gp/pdf.py`
* `tests/test_pdf_parsing.py`
* any tests related to:

  * tab line grouping,
  * system detection,
  * barline detection,
  * string assignment,
  * edge-boundary fallback,
  * PDF grouping diagnostics.

If `score2gp-agentops` is unavailable, stop and ask the maintainer. Do not recreate governance rules locally.

# Goal

Implement the smallest safe public-fixture-backed improvement for paired notation+TAB layout detection.

This is not a full converter fix.

The implementation target is:

1. Add a public synthetic paired notation+TAB geometry fixture.
2. Add or refactor production-callable helpers for collinear horizontal TAB segment merging.
3. Add spacing-aware TAB-vs-notation staff classification.
4. Add vertical candidate filtering against the authoritative TAB grid.
5. Preserve strict refusal for ambiguous or damaged cases.

# Non-Goals

Do not implement native GP oracle parsing.

Do not modify timing rules.

Do not modify build-ir timing preflight.

Do not use MusicXML, GP, pitch, tuning, or oracle data to drive PDF geometry.

Do not infer strings/frets from pitch.

Do not loosen global grouping, string, fret, timing, or build-ir gates.

Do not skip candidates, bars, systems, warnings, or pages to make metrics look better.

Do not implement OCR.

Do not implement scanned-PDF support.

Do not implement ML layout recognition.

Do not implement MusicXML timing repair.

Do not implement GPIF expansion.

Do not commit private PDFs, GP files, MXL/MusicXML files, diagnostics, overlays, reports, logs, generated GP files, or anything under `work/`.

Do not claim conversion success.

# Implementation Phases

## Phase 1: Public synthetic fixture

Create a public synthetic fixture in `score2gp`, preferably JSON-based unless the current tests already have a better public fixture mechanism:

```text
fixtures/public/generated_paired_notation_tab_system.json
```

It should model one paired Guitar Pro score row:

* one standard 5-line notation staff above;
* one six-line TAB staff below;
* true shared barlines spanning notation+TAB;
* notation-only stems inside the notation staff;
* TAB rhythm stems inside the TAB area;
* fret digit candidates on TAB string lines;
* at least one fragmented horizontal TAB line split into left/right collinear segments.

Also add a damaged/incomplete TAB variant, either in the same fixture or in a second fixture:

```text
fixtures/public/generated_paired_notation_tab_system_ambiguous.json
```

This variant must model a damaged TAB staff where one line is missing or too fragmented, proving the code does not blindly classify every five-line group as notation.

## Phase 2: Collinear horizontal segment merging

In the PDF layout code, add or refactor a small internal helper to merge horizontal line segments that:

* have nearly the same y coordinate;
* are collinear;
* have compatible thickness/height where that data exists;
* have small horizontal gaps or known interruptions caused by glyphs;
* belong to the same likely staff row.

This helper must be testable from synthetic geometry without private PDFs.

Do not merge unrelated systems across large x/y gaps.

Do not merge notation and TAB staves into one line group.

## Phase 3: Spacing-aware TAB-vs-notation classifier

Add a production-callable classifier that distinguishes staff candidates by geometry:

* likely TAB staff: six-line pattern or incomplete six-line pattern with TAB-like spacing and fret-digit intersections;
* likely notation staff: five-line pattern with wider spacing, paired above a TAB staff, and no fret-digit intersections;
* ambiguous: refuse safely.

Do not implement a hard rule that “5 lines means notation.”

The classifier must allow damaged/incomplete TAB candidates to remain candidates if spacing, neighbouring line groups, and surrounding context support TAB.

Use the private research spacing values as evidence only, not as hard global constants. The public fixture may use representative spacing, but production code should express tolerance logic defensibly.

## Phase 4: Vertical candidate filtering against authoritative TAB grid

Update barline-candidate filtering so vertical line candidates are assessed against the authoritative TAB grid.

True measure barlines may span notation+TAB or intersect the TAB grid.

Notation-only stems must not be accepted as TAB barlines.

TAB rhythm stems must not be accepted as measure boundaries merely because they are vertical.

The implementation must preserve existing warning/refusal behaviour for ambiguous cases.

## Phase 5: Public tests

Add tests that prove:

1. The paired notation+TAB fixture produces exactly one authoritative TAB staff row.
2. The five-line notation staff is not counted as a TAB system.
3. Fragmented TAB horizontal segments are merged into the authoritative six-line TAB grid.
4. Notation-only stems are not accepted as TAB barlines.
5. TAB rhythm stems are not accepted as measure boundaries.
6. True shared barlines are accepted.
7. Damaged/incomplete TAB staff is not thrown away merely because only five lines are detected.
8. Ambiguous damaged cases still refuse safely.

Tests must exercise production code paths or helpers that production code calls. Do not test duplicated logic.

# Implementation Boundaries

Prefer a small module or a clearly isolated section in `src/score2gp/pdf.py` if that matches the current architecture.

Suggested concepts, if useful:

* `HorizontalSegment`
* `StaffLineGroup`
* `StaffClass`
* `TabStaffCandidate`
* `PairedStaffCandidate`
* `merge_collinear_horizontal_segments`
* `classify_staff_line_group`
* `filter_tab_barline_candidates`

Use existing project style and typing.

Avoid broad rewrites.

Keep the first PR reviewable.

# Optional Private Lesson 3 Smoke

After public tests pass, optionally run the Major Triads Lesson 3 extraction locally in a fresh work directory.

Do not delete old work directories.

Use a path like:

```text
work/paired_staff_tab_grid_detection_<timestamp>/lesson_3/
```

Report only private-safe metrics:

* total candidates;
* playable fret candidates;
* candidates with system;
* candidates with bar;
* candidates with string;
* grouping status;
* number of inferred systems;
* number of inferred TAB staves if available;
* number of systems with partial x-span if available;
* first page/system blocker;
* ScoreIR written yes/no;
* GP written yes/no;
* semantic round-trip attempted yes/no.

Do not print private fret sequences.

Do not print private musical text.

Do not commit `work/`.

Expected outcome:

This first PR does not need to generate GP.

It should either:

* improve the paired-staff/system-detection metrics, or
* add public tests and diagnostics proving the next safe change.

Do not claim conversion success unless semantic round-trip passes, which is not expected in this task.

# Acceptance Criteria

The PR is acceptable only if all of these are true:

1. A public synthetic paired notation+TAB fixture exists.
2. Public tests prove TAB staff classification and guardrails.
3. Collinear TAB segment merging is covered by tests.
4. Notation/TAB stems are not accepted as barlines in the fixture.
5. Damaged/incomplete TAB cases refuse or remain candidates safely.
6. No global gates are loosened.
7. No private artifacts are committed.
8. The prompt chain and run record are written to `score2gp-agentops`.
9. Product PR body clearly states no conversion success is claimed.

# Required Verification

In `score2gp`, run:

```bash
python -m pytest
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check
git diff -- schemas
git ls-files fixtures/private work
git status --short
git status --branch
```

Private-safety invariant:

```bash
git ls-files fixtures/private work
```

must output only:

```text
fixtures/private/.gitkeep
```

In `score2gp-agentops`, run:

```bash
git diff --check
git status --short
git status --branch
```

# Required Agentops RUN.md

Write:

```text
projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/RUN.md
```

It must include:

* product repo branch;
* agentops branch;
* prompt chain links;
* files changed;
* tests added;
* public fixture names;
* private-safe Lesson 3 smoke metrics if run;
* strict conversion status;
* generated file existence;
* semantic round-trip status;
* private-safety audit;
* verification command results;
* next required evidence.

# PRs

Open a draft PR in `score2gp`.

Title:

```text
Add paired notation/TAB staff grid detection fixture and guards
```

Open a draft PR in `score2gp-agentops` if the run record is committed separately.

Title:

```text
Record paired notation/TAB staff grid detection run
```

PR bodies must state:

* public-fixture-backed layout work only;
* no timing/oracle change;
* no conversion success claimed;
* no private files or work outputs committed;
* prompt chain recorded;
* next task depends on review outcome.

# Final Response

Report:

* product branch and PR URL;
* agentops branch and PR URL;
* commit hashes;
* files changed;
* public tests added;
* exact verification results;
* private-safety audit result;
* whether Lesson 3 smoke was run;
* private-safe Lesson 3 metrics if run;
* whether ScoreIR/GP/semantic round-trip were attempted;
* next recommended evidence.

Do not mark the task complete until both repos are clean, pushed, and the required draft PRs are open.
```
