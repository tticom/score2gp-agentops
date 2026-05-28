# Prompt Record

## Prompt Metadata

- Prompt ID: 001
- Source: human
- Target agent: antigravity
- Date/time: 2026-05-28T11:57:21+01:00
- Supersedes: None
- Status: executed

## Explicit Prompt Text

```text
You are an expert Python engineer working on ScoreToGP.

This is the next product implementation task after the paired notation/TAB fixture-and-guardrail PR.

# Repositories

Product repo:

https://github.com/tticom/score2gp

Agent governance repo:

https://github.com/tticom/score2gp-agentops

# Current State

The workspace may now be reorganised locally under:

C:\Users\niall\src\Python\score2gp-workspace
score2gp
score2gp-agentops
score2gp.code-workspace

Use the actual local paths if they differ. Do not assume the old sibling layout if the workspace has been moved.

The following PRs must already be merged before this task proceeds:

* score2gp PR #145: Add paired notation/TAB staff grid detection fixture and guards
* score2gp-agentops PR #8: Record paired notation/TAB staff grid detection run

If either PR is not merged, stop and report. Do not proceed.

# Goal

Move from public fixture guardrails to the first real layout improvement against Major Triads Lesson 3.

Specifically:

Use the paired notation/TAB grid primitives from PR #145 to reduce real PDF system fragmentation and partial horizontal-span pseudo-systems.

This task is still layout-only.

It must not attempt GP generation as the acceptance target.

# Accepted Technical Basis

The accepted research and PR #145 establish:

* Major Triads Lesson 3 has real detected TAB/fret content.
* The converter is blocked because grouping remains unsafe.
* The current detector fragments TAB rows into partial pseudo-systems.
* Collinear TAB segments need to be merged before system/bar grouping becomes stable.
* Standard notation geometry and TAB rhythm stems must not pollute TAB barline detection.
* A hard “5 lines = notation / 6 lines = TAB” rule is unsafe.
* The new public paired notation/TAB fixture and guardrail helpers exist and must remain covered by tests.

# Pre-flight

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

Stop if either repo is dirty.

# Branches

In `score2gp`, create:

```bash
bugfix/paired-staff-row-normalization-v0.1
```

In `score2gp-agentops`, create:

```bash
runs/paired-staff-row-normalization-v0.1
```

Use `v0.2` if either branch already exists.

# Mandatory Prompt Chain Record

Before completing the task, create this directory in `score2gp-agentops`:

```text
projects/score2gp/runs/2026-05-28-paired-staff-row-normalization/
  RUN.md
  prompt-manifest.json
  prompts/
    001-implementation-prompt.md
```

Store this entire prompt exactly in:

```text
projects/score2gp/runs/2026-05-28-paired-staff-row-normalization/prompts/001-implementation-prompt.md
```

Record it in:

```text
projects/score2gp/runs/2026-05-28-paired-staff-row-normalization/prompt-manifest.json
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
* `projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/RUN.md`
* `projects/score2gp/templates/RUN_RECORD_TEMPLATE.md`
* `projects/score2gp/templates/PROMPT_CHAIN_README.md`

From `score2gp`, read:

* `AGENTS.md`
* `HANDOFF.md`
* `docs/architecture.md`
* `docs/limitations.md`
* `src/score2gp/pdf.py`
* `tests/test_pdf.py`
* `tests/test_pdf_parsing.py`
* the public paired notation/TAB fixtures added in PR #145
* all tests related to:

  * tab line grouping
  * system detection
  * barline detection
  * string assignment
  * edge-boundary fallback
  * PDF grouping diagnostics

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

# Phase 1: Establish a coherent full Lesson 3 baseline

Run a fresh private-safe Lesson 3 diagnostic smoke in a new work directory:

```text
work/paired_staff_row_normalization_<timestamp>/lesson_3_baseline/
```

Do not delete old outputs.

The baseline must report:

* exact input basename
* page count
* total candidates
* playable fret candidates
* candidates with system
* candidates with bar
* candidates with string
* grouping status
* inferred system count
* inferred bar box count
* count of partial x-span systems if available
* first page/system blocker
* ScoreIR written yes/no
* GP written yes/no
* semantic round-trip attempted yes/no

If the page count or metrics are inconsistent with prior reports, stop and explain the inconsistency before implementing code.

Do not print private fret sequences or private musical text.

# Phase 2: Add public row-fragmentation fixture

Add a public fixture that specifically reproduces the real supported failure mode:

```text
fixtures/public/generated_paired_tab_row_fragmentation.json
```

If helpful, also generate a corresponding PDF under:

```text
tests/fixtures/pdf/generated_paired_tab_row_fragmentation.pdf
```

The fixture must model:

* one paired notation+TAB row
* the TAB staff line segments split into left/right horizontal fragments
* matching fragments across all or most TAB strings
* notation staff above
* true shared barlines
* notation-only stems
* TAB rhythm stems
* fret candidates on the TAB grid

Expected behaviour:

* the fragments are normalised into one authoritative TAB row
* the notation staff is not counted as TAB
* true shared barlines remain accepted
* notation/TAB stems remain rejected as measure boundaries
* fret candidates assign to the merged TAB row

Add a negative fixture or test case:

* two genuinely separate systems or columns with similar y coordinates must not be merged into one row.

# Phase 3: Implement paired-staff row normalisation

Extend the current layout code carefully so that, before system construction, TAB line fragments can be normalised into complete row candidates.

The implementation must:

1. Build row-level candidates from collinear horizontal TAB line fragments.
2. Use spacing-aware classification from PR #145.
3. Preserve damaged/incomplete TAB candidates safely.
4. Avoid merging notation and TAB staves.
5. Avoid merging genuinely separate systems/columns.
6. Retain explicit refusal when the evidence is ambiguous.

This should be a small, reviewable extension of the PR #145 helpers, not a broad rewrite of `pdf.py`.

# Phase 4: Add tests

Add public tests proving:

1. Fragmented TAB row pieces merge into one authoritative TAB row.
2. Fret candidates on the merged row receive stable system/string/bar assignment.
3. Notation staff is not counted as TAB.
4. Notation-only stems are rejected as barlines.
5. TAB rhythm stems are rejected as measure boundaries.
6. Two separate same-y systems/columns do not merge.
7. Ambiguous row geometry refuses safely.

Tests must exercise production code paths or helpers called by production code.

# Phase 5: Private Lesson 3 smoke after implementation

After public tests pass, run a second fresh Lesson 3 diagnostic smoke:

```text
work/paired_staff_row_normalization_<timestamp>/lesson_3_after/
```

Report private-safe metrics only.

Compare baseline vs after:

* page count
* total candidates
* playable fret candidates
* candidates with system
* candidates with bar
* candidates with string
* grouping status
* inferred system count
* inferred bar box count
* partial x-span system count if available
* first page/system blocker
* ScoreIR written yes/no
* GP written yes/no
* semantic round-trip attempted yes/no

Expected outcome:

The PR does not need to produce GP.

The desired metric movement is:

* fewer fragmented/partial x-span pseudo-systems;
* more candidates safely assigned to systems/bars/strings;
* clearer first blocker if strict conversion still fails.

Do not claim conversion success unless semantic round-trip passes, which is not expected in this task.

# Acceptance Criteria

This PR is acceptable only if:

1. A public row-fragmentation fixture or equivalent public test exists.
2. Tests prove fragmented TAB row normalisation.
3. Tests prove separate systems/columns do not merge incorrectly.
4. Tests prove notation/TAB stems are not accepted as barlines.
5. No global gates are loosened.
6. No private artifacts or work outputs are committed.
7. Baseline and after private Lesson 3 metrics are recorded privately and reported only as private-safe counts/statuses.
8. Agentops run record and prompt chain are written.

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
projects/score2gp/runs/2026-05-28-paired-staff-row-normalization/RUN.md
```

It must include:

* product repo branch
* agentops branch
* prompt chain links
* files changed
* tests added
* public fixture names
* exact baseline command
* exact after command
* private-safe baseline metrics
* private-safe after metrics
* strict conversion status
* generated file existence
* semantic round-trip status
* private-safety audit
* verification command results
* next required evidence

Use relative links in the run record. Do not use `file:///c:/...` links.

# PRs

Open a draft PR in `score2gp`.

Title:

```text
Normalize paired TAB row fragments before system grouping
```

Open a draft PR in `score2gp-agentops` for the run record.

Title:

```text
Record paired staff row normalization run
```

PR bodies must state:

* public-fixture-backed layout work only
* no timing/oracle change
* no conversion success claimed
* no private files or work outputs committed
* prompt chain recorded
* baseline vs after Lesson 3 private-safe metrics included in agentops
* next task depends on review outcome

# Final Response

Report:

* product branch and PR URL
* agentops branch and PR URL
* commit hashes
* files changed
* public tests added
* exact verification results
* private-safety audit result
* baseline vs after private-safe Lesson 3 metrics
* whether ScoreIR/GP/semantic round-trip were attempted
* next recommended evidence

Do not mark the task complete until both repos are clean, pushed, and the required draft PRs are open.
```
