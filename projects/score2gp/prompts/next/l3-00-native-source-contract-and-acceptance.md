# L3-00 — Lesson 3 native source contract and red acceptance

Status: PROPOSED; not executable until promoted in ORCHESTRATION_STATE.json.
Repository: `tticom/score2gp`. Suggested branch: `feat/l3-00-native-acceptance`.
Role: Developer after bounded Architect/source-contract verification.

## Requirement and authority

Implement the acceptance boundary for
[L3-NATIVE](../../plans/2026-09-05-lesson3-native-working-slice.md).
Audiveris replacement by native Score2GP recognition is settled. The immediate
product goal is the complete original Lesson 3 PDF converted faithfully to GP,
not merely a successful crop or infrastructure task. This task supplies a red
real-source acceptance test and a precise first implementation contract.

Promotion requires disposition of active REC-04 / PR #459 and fresh product,
AgentOps and skills revisions. The current REC-05 proposal is not implicitly
executed alongside this task. This file does not itself alter live authority.

## Context, progress baseline and active blocker

At product `16cba3a41dc831cf0b44a3b44a205e8c095a3cb6`, original Lesson 3
PDF-only conversion refuses at layout gating with exit 4,
`pdf_only_tab_grouping_unsafe` and
`pdf_bar_box_construction_not_enough_for_build_ir`; no output GP exists.
The source is four pages with notation/TAB, sustained/dotted rhythms, rests,
multi-digit frets, section labels and rolled chords. Candidate reference
aggregates are in the requirement and remain subject to PDF adjudication.

Existing REC-01 tests primarily establish infrastructure behavior; they do not
provide this complete source-adjudicated, independently parsed acceptance path.
Repeating the refusal or counting extracted candidates is insufficient progress.

## Goal and scope

Produce a trustworthy private source manifest and a repeatable red end-to-end
native acceptance result, with the earliest source-located divergence on the
first complete system and the exact next topology/token implementation seam.
Validate the oracle independently before using its failures to direct changes.

Proposed allowed product paths, to be frozen in the promoted assignment:

- `scripts/native_slice_acceptance.py` — new acceptance coordinator.
- `scripts/native_slice_reference.py` — independent GP reference expansion and
  comparison; must not import product GP parser/writer or generation internals.
- `tests/test_native_slice_acceptance.py` — infrastructure/negative controls.
- `tests/test_lesson3_native_acceptance.py` — real-source acceptance integration.

No recognition, IR, writer, CLI, dependency, governance, or fixture-repository
mutation is authorized by this product task. The adjudicated manifest is a
local ignored artifact beside private acceptance evidence, not a committed
transcription. If the independent reader requires a dependency, freeze that
choice and its bounded packaging scope before implementation rather than
silently changing pyproject.toml. Standard-library GPIF traversal is the first
bounded option; its supported fields must be explicit and fail closed.

## Preflight and bounded Architect work

1. Run the identity/workspace/skills gates; pin clean revisions, source hashes,
   executable/import paths and current PR state. Read the complete L3-NATIVE
   requirement, project privacy policy and author evidence contract.
2. Inspect every original source page. Record source features and select the
   first complete system including its sustained ending in the private manifest.
   Do not substitute a newly engraved/generated PDF.
3. Traverse the reference graph by occurrence, not definition count. Validate
   IDs/links and ordered measure/voice/beat/note expansion independently of
   product code. Verify the PDF/reference arrangement before declaring truth.
4. Record exact rational durations/onsets, rests, chord ownership, string/fret,
   pitch, source-supported track/tempo/key/meter/text/barline/technique facts,
   and absent/defaultable properties. Preserve disagreements explicitly.
5. Inspect vector/text observations in the first system and map the earliest
   missing/incorrect topology relationship to a source region. Identify one
   candidate production seam and a falsifiable detector/resolution hypothesis.

The Architect selects A/B/C for any uncertain recognition experiment under the
project contract. The default planning hypothesis is vector/text-led, not
raster-first. Independent adversarial architecture verification must establish
the smallest next implementation task; do not claim full recognizer viability
from primitive availability alone.

## Implementation and privacy boundary

Use requirement-driven tests. The acceptance coordinator takes the source PDF,
private oracle location and a fresh output directory but launches generation
with only the PDF, production code and declared options. Use an isolated
filesystem/container or equivalent enforced read boundary: a subprocess with
the same unrestricted reference access is insufficient. Inject a sentinel
reference path to prove generation cannot read it. Preserve the immutable
original source; a renamed byte-identical staged PDF is permitted for isolation.

The command being assessed is the target CLI in L3-NATIVE, including precise
timing and strict mode. Baseline commands may reproduce today's layout refusal
separately. A conversion refusal yields `NOT_CONVERTED` and overall nonzero
acceptance; downstream semantic/application checks are `NOT_EVALUATED`.
Never substitute a successful mocked output into the real-source result.

The intentionally red product acceptance is expected while recognition is
being built. A harness regression may assert its exact classified failure,
but reports must distinguish `HARNESS_VERIFIED` from `L3_NATIVE_NOT_ACHIEVED`.
Do not turn the red acceptance into a skipped/xfail success or a waived product
qualification gate. Keep it a separately reported acceptance command until
the production path earns green.

## Acceptance and validation

- Source hash/feature/region contract exists privately, is source-adjudicated,
  and matches the requirement; unresolved facts are explicit blockers.
- Correctly expands reused GP records and detects duplicate/dangling IDs.
- Oracle detects mutations to every represented musical field, including
  rest/chord/dot/arpeggio and section structure; identical semantics pass.
- Oracle expectations never come from the generated artifact or copied
  production parser/writer logic; generated/reference aliases are rejected.
- Wrong/missing corpus, source or oracle, stale output and reference access by
  generation cannot result in acceptance or an unexplained test skip.
- Original PDF reaches the actual CLI in a fresh isolated run and produces an
  exact, nonzero baseline acceptance receipt; no fake successful score.
- First-system source overlay/relationship evidence identifies a new exact
  divergence and a bounded next seam, beyond the already-known refusal code.
- No private musical contents, coordinates, images, generated files or raw logs
  are committed. Public results contain hashes, counts, statuses and code paths.

Commands to register in the promoted assignment (new paths are not present yet):

```bash
python3 -m pytest tests/test_native_slice_acceptance.py tests/test_lesson3_native_acceptance.py
python3 scripts/native_slice_acceptance.py --help
python3 scripts/artifact_audit.py
git diff --check
```

The coordinator's required invocation contract is:

```bash
python3 scripts/native_slice_acceptance.py \
  --pdf <original-lesson3-pdf> --oracle <adjudicated-private-manifest> \
  --out-dir <new-private-output-directory>
```

Run that command separately and record its nonzero baseline result. Also run
the repository-required full suite and static checks for the changed seam.
The reviewer must execute real-source cases in the private environment and
cannot treat an unavailable fixture as acceptance.

## Stop/pivot, review and handoff

Stop the affected step on unresolved source/reference equivalence, a manifest
derived from product output, unenforced reference isolation, an untrustworthy
reader, privacy failure, or a required edit outside the promoted scope. Continue
independent source-region work where possible. Missing application access does
not block this harness task, but it remains a final milestone prerequisite.

One cycle must produce the manifest, red acceptance and new first divergence.
A second cycle requires a different explicit hypothesis; repeating counts or
the baseline warning is duplicate/no-progress. Do not reopen third-party
recognizer selection or start a general framework replacement.

Publish one exact-head product PR using the author evidence contract, with
source hashes, private-safe comparisons, focused/full validation results and
the distinction between harness completion and unfinished L3-NATIVE.
An independent reviewer must explicitly use `devils-advocate-review`, start
from cannot-verify, attack false success and contamination, and publish an
Adversarial Review Evidence Ledger plus exact-head verdict and summary. Fix
findings within this task; any scope change returns to the bounded assignment.
Human merge precedes next-task promotion. Do not self-review or self-merge.

## Incremental Progress Check

- New evidence: adjudicated occurrence-level oracle and first-system causal
  divergence, with a demonstrated red native acceptance command.
- Must not repeat: the existing full-PDF layout-refusal report or aggregate
  note counts without source relationships.
- Progress proof: a known-bad semantic output is rejected, the baseline failure
  is classified through the actual CLI, and exactly one next changed seam is
  supported by source-region evidence.
- Duplicate/no-progress result: only the same warning, renamed tests, copied
  report, or unsupported declaration that vector recognition will work.
- Next decision enabled: authorize the smallest topology/token seam needed
  to bring the first complete system through the native vertical path.
