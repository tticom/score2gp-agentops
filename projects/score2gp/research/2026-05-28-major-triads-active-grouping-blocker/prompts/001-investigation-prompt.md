You are an expert Python engineer and diagnostic investigator working on ScoreToGP.

This is a research/localisation task first, not an implementation task.

# Repositories

Product repo:

https://github.com/tticom/score2gp

Agent governance repo:

https://github.com/tticom/score2gp-agentops

# Current State

The following PRs must already be merged before this task proceeds:

- score2gp PR #145: paired notation/TAB staff grid fixture and guards
- score2gp-agentops PR #8: paired notation/TAB staff grid run record
- score2gp PR #147: paired TAB row fragment normalization
- score2gp-agentops PR #10: paired staff row normalization run record

If any of these PRs is not merged, stop and report. Do not proceed.

Known result from PR #147 / PR #10:

The row-fragmentation fixture and guardrail work passed public tests, but it did not move Major Triads Lesson 3 private metrics.

Lesson 3 baseline vs after remained identical:

- page count: 4
- total candidates: 591
- playable fret candidates: 548
- candidates with system: 431
- candidates with bar: 399
- candidates with string: 430
- grouping status: partial
- inferred system count: 22
- inferred bar box count: 49
- partial x-span systems: 0
- first blocker: pdf_grouping_confidence_below_threshold
- ScoreIR written: no
- GP written: no
- semantic round-trip attempted: no

Therefore, do not continue coding against the row-fragmentation hypothesis. It is now a guardrail, not the active blocker.

# Goal

Identify the active remaining grouping blocker for Major Triads Lesson 3 after PR #147.

Produce a precise, private-safe failure matrix that explains why strict build-ir still refuses.

The output must identify the next smallest implementable fix, backed by public fixture requirements.

Do not implement the fix in this task unless the evidence is trivial and the public fixture is added first. Prefer research/reporting only.

# Branches

In score2gp, create from clean main:

research/major-triads-active-grouping-blocker-v0.1

In score2gp-agentops, create from clean main:

research/major-triads-active-grouping-blocker-v0.1

Use v0.2 if either branch already exists.

# Mandatory Prompt Chain Record

Before completing the task, create this directory in score2gp-agentops:

projects/score2gp/research/2026-05-28-major-triads-active-grouping-blocker/
  RUN.md
  prompt-manifest.json
  prompts/
    001-investigation-prompt.md

Store this entire prompt exactly in:

projects/score2gp/research/2026-05-28-major-triads-active-grouping-blocker/prompts/001-investigation-prompt.md

Record it in:

projects/score2gp/research/2026-05-28-major-triads-active-grouping-blocker/prompt-manifest.json

The task is incomplete without this prompt-chain record.

# Required Reading

From score2gp-agentops:

- projects/score2gp/README.md
- projects/score2gp/REVIEW_RULES.md
- projects/score2gp/ACCEPTANCE_TARGETS.md
- projects/score2gp/BENCHMARK_LADDER.md
- projects/score2gp/MAJOR_TRIADS_BENCHMARK.md
- projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/RUN.md
- projects/score2gp/runs/2026-05-28-paired-staff-tab-grid-detection/RUN.md
- projects/score2gp/runs/2026-05-28-paired-staff-row-normalization/RUN.md
- projects/score2gp/templates/RESEARCH_REPORT_TEMPLATE.md
- projects/score2gp/templates/PROMPT_CHAIN_README.md

From score2gp:

- AGENTS.md
- HANDOFF.md
- docs/architecture.md
- docs/limitations.md
- src/score2gp/pdf.py
- tests/test_pdf.py
- tests/test_pdf_parsing.py
- all public paired notation/TAB fixtures
- all code handling:
  - grouping status
  - candidate system assignment
  - candidate bar assignment
  - candidate string assignment
  - fret optical bounds confidence
  - grouping confidence
  - compact staff ambiguity
  - edge-boundary fallback

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
Do not commit private PDFs, GP files, MXL/MusicXML files, diagnostics, overlays, reports, logs, generated GP files, or anything under work/.
Do not claim conversion success.

# Investigation Inputs

Run a fresh Lesson 3 diagnostic into a new work directory:

work/major_triads_active_grouping_blocker_<timestamp>/lesson_3/

Do not delete old outputs.

Use the normal current extraction/diagnostic command for Lesson 3.

Do not print private fret sequences or private musical text.

Use only private-safe counts, statuses, warning codes, page/system indices, and geometry summaries.

# Required Analysis

## Q1: Which strict gate is actually failing?

Report:

- grouping status
- grouping confidence status
- first blocker code
- all build-ir-blocking warning codes
- whether the first blocker is system, bar, string, fret optical bounds, or aggregate confidence

Do not accept “missing_pdf_grouping” as sufficient. Decompose it.

## Q2: Candidate assignment breakdown

Produce a private-safe breakdown of all candidates and all playable fret candidates:

For all candidates:
- total
- with system
- with bar
- with string
- with all three
- missing system
- missing bar
- missing string

For playable fret candidates only:
- total
- with system
- with bar
- with string
- with all three
- missing system
- missing bar
- missing string

Group by page and system where available.

## Q3: Warning taxonomy by count

Produce a warning-code frequency table from warnings/tabraw diagnostics.

Group warning codes into categories:

- system detection
- bar detection / edge boundary
- string assignment
- fret optical bounds
- grouping confidence
- candidate outside bar/system
- non-playable text filtering
- other

For each category, identify whether it is build-ir-blocking or diagnostic-only.

## Q4: First high-impact failure cluster

Find the smallest cluster that explains the largest number of unassigned playable candidates.

Examples:

- one page/system has many playable candidates missing string
- one page/system has candidates with system/string but no bar
- one page/system has candidates with bar/string but no system
- many candidates are actually non-tab text misclassified as playable
- fret optical bounds rejects tall but valid digits
- compact staff string ambiguity prevents string assignment

Report:

- page index
- system index if available
- candidate count affected
- missing dimension
- dominant warning codes
- whether the visual overlay suggests real TAB content or non-tab text, if available

Do not include private fret sequences.

## Q5: Are the remaining blockers caused by notation/TAB geometry, string snapping, fret optical bounds, or bar boxing?

Label each hypothesis:

- supported
- unverified
- contradicted

Hypotheses to evaluate:

1. paired-staff row fragmentation remains the active blocker
2. string assignment confidence/compact-staff ambiguity is now the active blocker
3. fret optical bounds confidence is the active blocker
4. bar boxes are still incomplete despite row normalization
5. non-tab text is still being counted as playable
6. grouping confidence threshold is aggregating several smaller non-fatal warnings
7. diagnostic counters are inconsistent across stages

## Q6: What public fixture reproduces the active blocker?

Design one public fixture for the active blocker.

Examples:

- compact staff string ambiguity fixture
- tall fret bbox optical bounds fixture
- candidate outside bar edge fixture
- barline double/short boundary fixture
- non-tab numeric text filtering fixture

The fixture must include:
- expected success case
- expected safe-refusal case
- production-path test assertions

Do not implement unless tiny and clearly supported.

## Q7: What is the next PR-sized implementation?

Define one and only one next implementation slice.

It must include:

- branch name
- goal
- non-goals
- public fixture required
- private Lesson 3 metric expected to move
- guardrail test
- acceptance criteria
- verification commands
