# Feature: Public multi-note and rest fixture inventory and export proof

## Repository
tticom/score2gp

## Goal
The project has successfully implemented and verified single-note GP export paths for all single-note durations (whole through 64th). Additional public fixtures (e.g., `HalfNotes.pdf`, `WholeNoteRest.pdf`) exist but remain unverified. This task must first inventory the remaining simple fixtures, then prove exact capability through the production path, or stop with a precise unsupported-feature report.

## Progress Baseline
* PR #310 completed developer implementation for filled single-note durations (quarter through 64th).
* All single-note duration paths are verified against public fixtures in `fixtures/public/generated_simple/simple/`.

## Incremental Progress Check
* The next task must produce new decision-useful evidence by producing a verified fixture inventory for the remaining fixtures in `fixtures/public/generated_simple/simple/`.
* It must not assume all durations or rests are supported without CLI/GP inspection evidence.
* Progress is proven by either identifying the exact supported set with proof, or producing a verified stop/pivot decision if multi-note or rest classification is speculative or hygiene fails.
* Duplicate/no-progress result: claiming support without proof, or failing to report the fixture inventory table.

## Authorised Workflow
The task must explicitly follow this loop:
Requirement → Architect diagnosis/research → Reviewer architecture verification → Developer implementation only if authorised → Reviewer implementation conformance review → PR readiness review.

The initial task is strictly inspect/proof-only. No implementation is authorised yet. If any unsupported feature is found, return to supervisor/Architect.

## Baseline Verification
The next product task must inspect `tticom/score2gp` from a clean branch and produce a fixture inventory before implementing anything.

The product task must run and report commands equivalent to:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
find fixtures/public -type f | sort
git ls-files fixtures/public | sort
git ls-files fixtures/private work/private || true
git status --ignored --short
```

The product task must build a fixture inventory table with columns:
* expected feature (e.g. multi-note, rest);
* expected GP note value/count;
* fixture path;
* tracked/public status;
* whether current recognition produces valid candidates;
* whether current export path supports it;
* acceptance status;
* blocker if unsupported.

Expected feature set to verify if fixtures exist:
* multiple half notes (`HalfNotes.pdf`);
* single whole rest (`WholeNoteRest.pdf`);
* standard staff vs tab staff properties.

## Evidence and Export Proof
The product task must prove explicit GP export capability using authorised public generated fixtures. For each supported feature it must report:
* exact fixture path;
* exact CLI command;
* generated artifact inspection result;
* note count;
* bar count;
* time signature;
* proof no private fixture path is required;
* proof generated artifacts were not committed.

## Constraints and Preservation
The product task must preserve:
* existing single-note command behaviours (whole through 64th);
* default `convert` behaviour;
* repository artifact hygiene.

The product task must not:
* add broad automatic score conversion;
* change default conversion behaviour;
* add tab-only support;
* add chord support;
* train or introduce a model;
* use OCR;
* rely on private fixtures for acceptance.

## Decision Rule
* Inspect/proof only. No implementation authorised. If any unsupported feature is found, return to supervisor/Architect.
* If multi-note or rest recognition is missing or speculative, stop and request an Architect task to decide the approach.
* If the new fixtures are not tracked/public, stop and report the fixture hygiene blocker.
