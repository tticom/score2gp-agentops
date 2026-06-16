# ACTIVE TASK: Product Task 171

**Repository:** `tticom/score2gp`
**Goal:** Bridge logical clef candidate evidence into clef-resolved pitch mapping for generated public fixtures.

## Pre-flight Checks
Run and report the results of:
```bash
git status --short
git branch --show-current
git fetch --all --prune
git log --oneline --decorate --graph --max-count=20
gh pr view 290 --repo tticom/score2gp --json state,mergedAt,mergeCommit,headRefOid,baseRefName,isDraft,title,url,changedFiles
```
You MUST verify Product PR #290 is merged before changing code.

## Investigation Requirements
Inspect the current product repository state before implementing. Do not assume exact file locations without checking. Likely areas include:
* clef candidate diagnostics or recogniser output
* staff diagnostics models
* note candidate recognition/reporting code
* `clef_resolved_staff_pitch` production/consumption boundary
* Task 170 coverage analysis script and tests
* tests around note candidate recognition, whole-note recognition, and pitch mapping

## Scope and Instructions
* Verify where logical clef candidate evidence is produced.
* Verify where `clef_resolved_staff_pitch` obtains clef evidence.
* Use existing logical clef candidate evidence already produced by the pipeline, if present.
* Bridge safe, deterministic logical clef candidate evidence into the clef evidence boundary used by `clef_resolved_staff_pitch`.
* Target the missing-clef blocker identified by Product Task 170.
* Preserve strict clef evidence policy.
* Preserve existing `assumed_treble_pitch`.
* Preserve existing `clef_resolved_staff_pitch` semantics.
* Preserve the diagnostic-only/reporting boundary.
* Add or update tests proving missing-clef coverage improves on authorised generated public fixtures or synthetic data.
* Re-run focused regression tests.

## Non-Goals (DO NOT IMPLEMENT)
* Do not declare `clef_resolved_staff_pitch` canonical.
* Do not implement playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Do not implement broad new visual clef recognition unless governance explicitly authorises it later.
* Do not guess treble clef globally.
* Do not use `assume_treble_clef` as visual clef evidence.
* Do not infer clef from pitch outcomes, note positions, or ledger-line placement.
* Do not commit private fixtures, private diagnostics, screenshots, logs, scratch JSON, PDFs, images, GP files, credentials, or generated dumps.

## Validation Requirements
Run and report the exact commands and results for:
* Focused tests for the changed implementation files
* Focused tests for Task 170 coverage analysis, if the script/report boundary is touched or used as validation
* Relevant note-candidate / clef-resolved pitch regression tests
* `git diff --check`
* `git status --short`
* Privacy/artifact checks

## Acceptance Criteria
1. Product PR #290 is verified merged before implementation.
2. Existing logical clef candidate evidence is located and described, or the agent stops and reports that it is not present.
3. The bridge uses deterministic clef evidence only.
4. The strict clef evidence policy is preserved.
5. `assumed_treble_pitch` remains preserved and is not treated as visual clef evidence.
6. `clef_resolved_staff_pitch` semantics remain preserved.
7. Missing-clef coverage improves on authorised generated public fixtures or a justified synthetic fixture/test proves the bridge.
8. No canonical pitch adoption or playable output is introduced.
9. Focused regression tests pass.
10. No private or unsafe artifacts are committed.
11. A product PR is opened with complete evidence.

## Stop Conditions (Halt and Report if encountered)
* Product PR #290 is not merged.
* The working tree is dirty before changes and the dirt is unrelated.
* Existing logical clef candidate evidence cannot be located.
* The only available route requires guessing treble clef globally.
* The only available route uses `assume_treble_clef` as visual clef evidence.
* The only available route infers clef from pitch outcomes, note positions, or ledger-line placement.
* The task would require broad new visual clef recognition.
* The task would require private fixtures or unsafe artifacts.
* The task would require implementing playable output, ScoreIR, MusicXML, GP output, rhythm, accidentals, key signatures, rests, or OCR.
* Tests fail in a way the agent cannot explain or isolate.
* Requirements conflict with the verified repository state.

## Commit and PR Requirements
* Work on a short-lived feature branch.
* Commit only intentional product changes.
* Open a product PR against `main`.
* Include in the PR body:
  * Task summary.
  * Product PR #290 prerequisite verification.
  * Implementation summary.
  * Exact files changed.
  * Tests run and results.
  * Coverage improvement evidence.
  * Safety and privacy/artifact hygiene result.
  * Behavioural confirmations.
  * Known limitations.
* Do NOT merge the product PR.
