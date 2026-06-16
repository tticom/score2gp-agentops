# ACTIVE TASK: Product Task 172
**Repository:** `tticom/score2gp`
**Title:** Add conservative logical clef candidate extraction from existing left-margin primitives
**Goal:** Create a conservative, deterministic, diagnostic-only logical clef candidate extractor/classifier that operates over existing `LeftMarginPrimitiveCandidate` evidence and emits safe clef candidate evidence that future tasks can bridge into clef-resolved pitch mapping.

## Pre-flight Checks
Run and report the results of:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
gh pr view 179 --repo tticom/score2gp-agentops --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
gh pr view 290 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
```
You MUST verify Governance PR #179 and Product PR #290 are merged before changing code. Verify the working tree is clean.

## Investigation Guidance
Inspect the current product repository before changing code. Do not hard-code file assumptions. Likely areas include:
* left-margin primitive extraction
* `LeftMarginPrimitiveCandidate` model or dataclass definitions
* raster clef diagnostics
* note candidate recognition/reporting
* Task 170 coverage analysis
* tests around left-margin primitives, clef diagnostics, note candidate recognition, and pitch coverage

## Scope and Instructions
* Work in `tticom/score2gp`.
* Locate `LeftMarginPrimitiveCandidate` production and consumption.
* Locate current raster clef evidence production in `pdf_raster_staff_diagnostics.py`.
* Locate current clef evidence boundaries used by note candidate or pitch coverage reporting.
* Add a small, conservative logical clef candidate extraction/classification boundary over existing left-margin primitive evidence.
* The extractor/classifier may classify only when evidence is deterministic and strong enough.
* Weak, malformed, absent, or ambiguous evidence must produce `unknown` or no candidate, not a guessed treble clef.
* Emit diagnostic/candidate evidence only.
* Add tests for positive deterministic cases, missing evidence, malformed evidence, weak evidence, and ambiguous evidence.
* Preserve existing raster clef diagnostics.
* Preserve existing `assumed_treble_pitch`.
* Preserve existing `clef_resolved_staff_pitch` semantics.
* Preserve diagnostic/reporting boundary.
* Avoid any new private fixtures.
* Favour a small pure function or module that accepts existing left-margin primitive evidence, validates shape/type defensively, returns structured diagnostic result or `unknown`/empty for weak/missing evidence, and does not alter pitch mapping.

## Non-Goals (DO NOT IMPLEMENT)
* Do not bridge logical clef candidates into `clef_resolved_staff_pitch` yet.
* Do not declare `clef_resolved_staff_pitch` canonical.
* Do not implement playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Do not implement broad visual clef recognition.
* Do not guess treble clef globally.
* Do not use `assume_treble_clef` as visual clef evidence.
* Do not infer clef from pitch outcomes, note positions, staff position, or ledger-line placement.
* Do not commit private fixtures, private diagnostics, screenshots, logs, scratch JSON, PDFs, images, GP files, credentials, generated dumps, or sensitive material.

## Validation Requirements
Run and report the exact commands and results for:
* focused unit tests for the new logical clef candidate extractor/classifier;
* relevant existing tests for left-margin primitive extraction, if present;
* relevant raster clef diagnostics tests, if shared types or boundaries are touched;
* relevant note-candidate reporting or coverage tests, if diagnostic output is surfaced there;
* `git diff --check`
* `git diff --stat`
* `git status --short`
* `git status --ignored`
* `git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true`

## Acceptance Criteria
1. Governance PR #179 is verified merged before implementation.
2. Product PR #290 is verified merged before implementation.
3. Existing left-margin primitive evidence is located and described.
4. A conservative logical clef candidate extractor/classifier is added.
5. The extractor/classifier is deterministic and defensive.
6. Missing, weak, malformed, or ambiguous evidence does not produce a guessed clef.
7. Existing raster clef diagnostics are preserved.
8. `assumed_treble_pitch` is preserved and not treated as visual clef evidence.
9. `clef_resolved_staff_pitch` semantics are preserved.
10. No direct bridge into pitch mapping is introduced.
11. Focused regression tests pass.
12. No private or unsafe artifacts are committed.
13. A product PR is opened with complete evidence.

## Stop Conditions (Halt and Report if encountered)
* Governance PR #179 is not merged.
* Product PR #290 is not merged.
* The working tree is dirty before changes and the dirt is unrelated.
* `LeftMarginPrimitiveCandidate` or equivalent left-margin primitive evidence cannot be located.
* The only feasible implementation requires broad visual clef recognition.
* The only feasible implementation requires global treble guessing.
* The only feasible implementation requires using `assume_treble_clef` as visual evidence.
* The only feasible implementation requires inferring clef from pitch outcomes, note positions, staff position, or ledger-line placement.
* The implementation would require private fixtures or unsafe artifacts.
* The implementation would require playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Tests fail in a way the agent cannot explain or isolate.
* Requirements conflict with verified repository state.

## Commit and PR Requirements
* Work on a short-lived feature branch.
* Commit only intentional product changes.
* Open a product PR against `main`.
* Include in the PR body:
  * Task summary.
  * Governance PR #179 prerequisite verification.
  * Product PR #290 prerequisite verification.
  * Implementation summary.
  * Exact files changed.
  * Logical clef evidence boundary summary.
  * Tests run and results.
  * Safety and privacy/artifact hygiene result.
  * Behavioural confirmations.
  * Known limitations.
  * Suggested next action.
* Do not merge the product PR.

## Reporting Format
You must report back with:
* Branch name.
* Product PR link.
* Full head SHA.
* Exact files changed.
* Governance PR #179 verification result.
* Product PR #290 verification result.
* Located left-margin primitive evidence summary.
* Logical clef candidate extraction/classification summary.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Behavioural confirmations. 
* Known limitations. 
* Suggested next action. 
