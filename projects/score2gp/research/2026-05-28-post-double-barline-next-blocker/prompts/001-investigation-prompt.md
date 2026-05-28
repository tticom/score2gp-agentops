You are an expert Python engineer and diagnostic investigator working on ScoreToGP.

This is a post-merge benchmark and next-blocker localisation task.

# Repositories

Product repo:
https://github.com/tticom/score2gp

Agentops repo:
https://github.com/tticom/score2gp-agentops

# Current State

Both of these PRs are merged:

- score2gp PR #149: final double-barline logical boundary clustering
- score2gp-agentops PR #13: double-barline resolution run record

The double-barline work reportedly improved Major Triads Lesson 3 bar-assigned fret candidates by 32, but strict grouping still remained partial. ScoreIR and GP were not written.

Do not assume the system can now convert a lesson PDF to GP.

Your task is to run a fresh benchmark from current `main` and identify the next active blocker.

# Branches

In score2gp, create from clean `main`:

research/post-double-barline-next-blocker-v0.1

In score2gp-agentops, create from clean `main`:

research/post-double-barline-next-blocker-v0.1

Use `v0.2` if either branch exists.

# Pre-flight

In score2gp:

git switch main
git pull --ff-only origin main
git status --short
git status --branch
git log --oneline --decorate -8
gh pr status

In score2gp-agentops:

git switch main
git pull --ff-only origin main
git status --short
git status --branch
git log --oneline --decorate -8
gh pr status

Stop if either repo is dirty.

# Mandatory Prompt Chain Record

Before completing the task, create this directory in score2gp-agentops:

projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/
  RUN.md
  prompt-manifest.json
  prompts/
    001-investigation-prompt.md

Store this entire prompt exactly in:

projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/prompts/001-investigation-prompt.md

Record it in:

projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/prompt-manifest.json

The task is incomplete without this prompt-chain record.

# Required Reading

From score2gp-agentops, read:

- projects/score2gp/README.md
- projects/score2gp/REVIEW_RULES.md
- projects/score2gp/ACCEPTANCE_TARGETS.md
- projects/score2gp/BENCHMARK_LADDER.md
- projects/score2gp/MAJOR_TRIADS_BENCHMARK.md
- the merged paired-staff research report
- the merged paired-staff grid detection run record
- the merged paired-staff row normalization run record
- the merged active grouping blocker / double-barline run record
- templates for research/run/prompt records

From score2gp, read:

- AGENTS.md
- HANDOFF.md
- docs/architecture.md
- docs/limitations.md
- src/score2gp/pdf.py
- tests/test_pdf.py
- tests/test_pdf_parsing.py
- public paired-staff and double-barline fixtures

# Goal

Run a clean post-merge benchmark of Major Triads Lesson 3 from current main.

Answer:

1. Does strict Gate A now pass?
2. Is ScoreIR written?
3. Is GP written?
4. If not, what is the next active blocker by candidate impact?
5. What is the next smallest public-fixture-backed implementation slice?

# Non-Goals

Do not implement a fix in this task.

Do not modify timing rules.

Do not implement native GP oracle parsing.

Do not use GP/MusicXML pitch, tuning, or oracle data to drive PDF geometry.

Do not loosen grouping, string, fret, timing, or build-ir gates.

Do not skip candidates or warnings.

Do not commit private PDFs, GP files, MXL/MusicXML files, diagnostics, overlays, logs, generated GP files, or anything under work/.

Do not claim conversion success unless strict ScoreIR and GP are written and semantic comparison passes.

# Benchmark Inputs

Use the private Major Triads Lesson 3 files available locally.

Run into a fresh output directory:

work/post_double_barline_next_blocker_<timestamp>/lesson_3/

Do not delete old work directories.

Do not print private fret sequences or private musical text.

Use private-safe basenames only.

# Required Analysis

## Q1: Gate status

Report:

- strict extraction/grouping status
- grouping_safe true/false
- ScoreIR written yes/no
- GP written yes/no
- semantic round-trip attempted yes/no
- primary blocker code
- all build-ir-blocking warning codes

## Q2: Candidate assignment metrics

For all candidates and playable fret candidates, report:

- total
- with system
- with bar
- with string
- with all three
- missing system
- missing bar
- missing string

Group by page/system where available.

## Q3: Delta from pre-double-barline baseline

Compare current main against the known pre-fix baseline:

- bar-assigned fret candidates: 391 before, 423 after according to PR #13
- strict grouping remained partial

If current metrics differ from PR #13, explain whether this is expected or an artifact inconsistency.

## Q4: Remaining warning taxonomy

Produce a warning-code frequency table grouped into:

- system detection
- bar detection / edge boundary
- string assignment
- compact staff ambiguity
- fret optical bounds
- grouping confidence
- candidate outside bar/system
- non-playable filtering
- other

Mark which are build-ir-blocking.

## Q5: Next high-impact blocker

Identify the smallest remaining failure cluster with the largest candidate impact.

Report:

- page index
- system index if available
- candidate count affected
- missing dimension
- dominant warning codes
- whether the visual overlay suggests real TAB content or non-tab text, if available

Do not include private fret sequences.

## Q6: Hypothesis review

Label each as supported / unverified / contradicted:

1. double-barline ambiguity remains the active blocker
2. string assignment confidence / compact-staff ambiguity is now the active blocker
3. fret optical bounds confidence is now the active blocker
4. bar boxes remain incomplete in other systems
5. candidate text outside bar boxes is now the active blocker
6. non-tab text is being counted as playable
7. aggregate grouping confidence is blocking despite most dimensions being assigned
8. diagnostic counters are inconsistent across stages

## Q7: Next public fixture

Design exactly one public fixture for the next active blocker.

It must include:

- expected success case
- expected safe refusal case
- production-path assertions
- expected private-safe metric movement on Lesson 3

Do not implement it in this task unless tiny and explicitly justified.

# Required Output

Write the durable report in score2gp-agentops:

projects/score2gp/research/2026-05-28-post-double-barline-next-blocker/RUN.md

Use this structure:

# Post Double-Barline Next Blocker Research

## Summary Verdict

State whether the current active blocker is:

- system detection
- bar detection
- string assignment
- compact staff ambiguity
- fret optical bounds
- aggregate grouping confidence
- mixed / uncertain

## Prompt Chain

## Repositories and Branches

## Commands Run

## Input Availability

## Artifact Coherence

## Gate Status

## Candidate Assignment Breakdown

## Delta From Double-Barline Baseline

## Warning Taxonomy

## First High-Impact Failure Cluster

## Supported Hypotheses

## Unverified Hypotheses

## Contradicted Hypotheses

## Recommended Public Fixture

## Recommended Next Implementation Slice

## Non-Goals and Invariants

## Verification Results

## Private-Safety Audit

## Next Required Evidence

# Product Repo Output

Prefer no product code changes.

Only update product files if a tiny diagnostic helper is needed to expose already-existing private-safe counts.

Do not update product HANDOFF.md with long-form state.

# Verification

In score2gp:

python -m pytest
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check
git diff -- schemas
git ls-files fixtures/private work
git status --short
git status --branch

Private-safety invariant:

git ls-files fixtures/private work

must output only:

fixtures/private/.gitkeep

In score2gp-agentops:

git diff --check
git status --short
git status --branch

# PRs

Open a draft PR in score2gp-agentops.

Title:

Record post double-barline next blocker research

Only open a product PR if product files changed.

Product PR title, if needed:

Expose post double-barline blocker diagnostics

PR bodies must state:

- research/reporting only
- no conversion success claimed
- no private files or work outputs committed
- prompt chain recorded
- next implementation depends on review outcome

# Final Response

Report:

- product branch, if changed
- agentops branch and PR URL
- commit hashes
- files changed
- commands run
- private-safe gate summary
- private-safe blocker summary
- verification results
- private-safety audit result
- next recommended implementation slice

Do not mark the task complete until both repos are clean, pushed, and the required draft PRs are open.
