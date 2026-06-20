# Feature: Public single-note duration fixture inventory and export proof

## Repository
tticom/score2gp

## Goal
The project has explicit single whole-note and single half-note GP export paths, and PR #308 created a safer public generated fixture baseline. The user has added more single-note duration PDFs, but the repository state and production capability for those durations are not verified. This task must first inventory the fixtures, then prove exact capability per duration through the production path, or stop with a precise unsupported-duration report.

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

The product task must build a duration fixture inventory table with columns:
* expected duration;
* expected GP note value;
* fixture path;
* tracked/public status;
* whether current recognition produces a valid single candidate;
* whether current export path supports it;
* acceptance status;
* blocker if unsupported.

Expected duration set to verify if fixtures exist:
* whole note;
* half note;
* quarter/q4 note;
* eighth note;
* sixteenth note;
* thirty-second note;
* sixty-fourth note.

## Evidence and Export Proof
The product task must prove explicit single-note notation GP export using authorised public generated fixtures. For each supported duration it must report:
* exact fixture path;
* exact CLI command;
* generated artifact inspection result;
* note count;
* bar count;
* time signature;
* track name;
* pitch/string/fret evidence where available;
* GP note value evidence;
* proof no private fixture path is required;
* proof generated artifacts were not committed.

## Constraints and Preservation
The product task must preserve:
* existing whole-note command behaviour;
* existing half-note command behaviour;
* default `convert` behaviour;
* repository artifact hygiene.

The product task must not:
* add broad automatic score conversion;
* change default conversion behaviour;
* add tab-only support;
* add rest support;
* add multi-note sequencing;
* add chord support;
* train or introduce a model;
* use OCR;
* rely on private fixtures for acceptance.

## Decision Rule
* If all single-note duration fixtures are tracked and the current production evidence can support all durations with bounded changes, implement and test the full single-note duration set.
* If only whole/half can be supported through current evidence, prove those using public fixtures and report unsupported durations precisely.
* If filled-note duration recognition is missing or speculative, stop and request an Architect task to decide the duration-classification approach.
* If the new fixtures are not tracked/public, stop and report the fixture hygiene blocker.
