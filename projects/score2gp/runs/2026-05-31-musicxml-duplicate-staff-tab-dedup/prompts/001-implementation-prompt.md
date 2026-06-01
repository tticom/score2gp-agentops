# Antigravity Task: MusicXML Duplicate Staff/TAB Voice Deduplication v0.1

## Pre-Flight Merge Check

Before writing code or creating a new branch, verify that the research branch has been reviewed and merged into `main`.

Run:

```bash
gh pr list --state open
gh pr view <MUSICXML_POLYPHONY_DIAGNOSTICS_PR_NUMBER> --web=false
gh pr checks <MUSICXML_POLYPHONY_DIAGNOSTICS_PR_NUMBER>
git switch main
git pull --ff-only origin main
```

Proceed only if the MusicXML polyphony diagnostics PR is merged and local `main` is synced.

If it is still open, failing checks, or unmerged, stop immediately and report the status. Do not implement anything.

## Branch

Create:

```bash
git switch -c feature/musicxml-duplicate-staff-tab-dedup-v0.1
```

## Context

The large-spaced TAB staff detection blocker has been fixed.

The next blocker has been classified by the research branch:

```text
musicxml_scoreir_polyphony_gate_refused
```

The private melodic soloing score appears to contain duplicate representations of the same guitar line:

* standard notation staff parsed as Voice 1
* TAB staff parsed as Voice 5

The current pipeline treats these as independent overlapping voices on the same instrument. That produces cross-voice timing overlap diagnostics and triggers the MusicXML polyphony gate.

The diagnostic branch classifies this as:

```text
over_conservative_duplicate_staff_tab_voice
```

This branch should implement a narrow, evidence-backed deduplication strategy for suspected duplicate standard-notation/TAB voices.

## Goal

Detect and reconcile duplicate standard-notation and TAB MusicXML voices representing the same guitar line, so that the converter can build a unified guitar voice without relying on `allow_remediation=True` to bypass the polyphony gate.

The desired outcome is:

* standard notation provides rhythm/duration/onset authority
* TAB provides string/fret/playability evidence where available
* duplicate voices are merged only when evidence is clear and 100% stable across all active measures
* both standard and TAB voice notes are preserved in the ScoreIR aligned note's provenance trail

## Success Criteria

This branch is successful when:

1. Public synthetic duplicate staff/TAB fixtures pass.
2. Genuine independent polyphony remains refused.
3. Same-voice chord stacks are not misclassified as duplicate voices.
4. The private melodic soloing score no longer needs `allow_remediation=True` solely for duplicate staff/TAB overlap.
5. Layout checks are not bypassed as the success path.
6. Matched fret candidate count improves beyond zero, or a later first failing stage is clearly reported.
7. No private artifacts are committed.
8. The full test suite passes.

## Validation Commands

Run:

```bash
python -m pytest tests/test_musicxml.py
python -m pytest tests/test_musicxml_polyphony_diagnostics_edge_cases.py
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

## Expected Final Report

Return:

```text
Branch:
Files changed:
Duplicate detection strategy:
Deduplication strategy:
Public tests added:
Validation results:
Private-safe smoke metrics:
First failing stage after this branch:
Private-safety audit:
Remaining limitations:
Recommended next branch:
Merge recommendation:
```

## Merge Rule

Do not recommend merge if:

* deduplication is based only on voice number without musical evidence
* independent polyphony is accidentally allowed
* `allow_remediation=True` is still required for the duplicate case
* layout checks are bypassed to claim success
* private artifacts are committed
* tests only check diagnostics and not actual unified output

This branch should move the project from “diagnosed duplicate staff/TAB blocker” to “safe duplicate staff/TAB unification for a narrow synthetic and private-safe case.”
