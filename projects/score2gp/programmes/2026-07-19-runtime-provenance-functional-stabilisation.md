# Runtime-Provenance and Functional-Stabilisation Programme

## Purpose

Make the committed `score2gp convert` route demonstrably usable before any
module rename or package split. The programme treats an output screenshot, a
green unit suite, and a file written by an uncommitted executable as different
things. Only a reproducible source-to-output record is evidence.

## Definition Of A Liveable Baseline

The selected Lesson corpus has a local, repeatable conversion record that:

1. identifies the exact product SHA and runtime import path;
2. produces a GP file for each supported selected input from the committed
   command path, rather than silently using uncommitted code;
3. records its timing source and any MusicXML sidecar hash;
4. has no unresolved `musicxml_timing_risk` or other timing refusal for an
   input claimed as supported;
5. traces every emitted rest to explicit source evidence or explicitly refuses
   instead of inventing a rest; and
6. records any deferred double bars, line breaks, headings, keys, or
   embellishments as deferred rather than claiming they are implemented.

The first implementation target is Lessons 3 through 7. Fixture observations
may be acceptance evidence, but no production algorithm may branch on a
fixture filename, bar number, fixed coordinate, title, or reference GP data.

## Ordered Work

### FS-01R: Remediate Invalid FS-01 Merge

Product PR #376 was merged without a valid independent review and does not
satisfy FS-01: its provenance claims are not supported by its implementation.
It must not be treated as FS-01 completion or as a base for FS-02.

Create one normal product revert PR for the #376 merge commit. The revert PR
must identify that merge commit, contain no unrelated change, run the relevant
public tests, and be reviewed independently. Agy may open and revise this PR,
but it must leave it `READY_FOR_EXTERNAL_MERGE`; it must never merge it. Only
after the revert lands may a fresh FS-01 implementation begin from `main`.

Completed 2026-07-19: product PR #377 was independently reviewed as an exact
inverse of the #376 merge relative to its first parent, then externally merged
as `e869940d0f12493aa0cb833c4b3ae9ace7e55cfb`. FS-01 starts from that clean
baseline; none of #376's provenance claims are accepted.

### FS-01: Runtime Provenance Baseline And Corpus Harness

Extend the existing private smoke tooling or add a small adjacent runner. For
every input, write an ignored JSON record containing:

- product SHA and `git status --short` classification;
- resolved CLI executable and Python import path;
- exact command and input class;
- supplied or generated MusicXML path, SHA-256, and generation provenance;
- output/report paths, exit status, output-written flag, stage, and refusal
  codes; and
- sanitized counts for bars, events, source rests, emitted rests, and timing
  issues when available.

The public repository may test record schema and runner behaviour using
synthetic/public inputs. Private corpus records remain under an ignored work
directory. FS-01 changes no conversion semantics.

### FS-02: Canonical Entry-Point Reconciliation

Use FS-01 evidence to answer one question: which committed function path is
actually run by the supported command? If a local auto-OMR path exists but is
not committed, it is an uncontrolled runtime and must be cleanly committed and
reviewed or discarded. Do not describe an external OMR engine, a deterministic
generator, or a diagnostic bridge as the product route without direct function
and revision evidence.

### FS-03 And FS-04: Stabilise The Real Path

Run the selected corpus, identify the first shared source/output divergence,
and repair one behaviour class per PR. Required evidence follows the event
through source evidence, MusicXML, ScoreIR, GPIF, and rendered output where
applicable. A reviewer must be able to trace a ghost rest by stable event or
source identifier before accepting a rest-related claim.

### FS-05: Baseline Decision

The Project Director records whether the baseline is liveable. Layout and
embellishment capabilities may be deferred only with a precise list of what is
missing and why their absence does not invalidate the supported conversion
claim.

### FS-06 And FS-07: Refactor Only After Stability

The refactor starts as an architecture task. Its intended package is
`score2gp.notation_omr`, with cohesive modules such as `models`,
`staff_geometry`, `duration_evidence`, `rest_evidence`, `pitch`, `timeline`,
and `diagnostics`. `whole_note_recogniser.py` remains a compatibility shim
during behaviour-preserving migration. No rename-only change is accepted until
the FS corpus record is stable.

## Review And Merge Rules

This programme opts into the Unattended Consecutive Loop Protocol. Developer
and Reviewer contexts must be distinct. Reviewers begin
from fresh state and look first for unsupported causal claims, hidden runtime
differences, fixture-specific logic, and claimed behaviour that the evidence
does not demonstrate.

Agy may never merge. After its reviewer accepts an exact head, it records an
external-merge handoff containing the generated provenance summary, validation,
and risks. Published PR commits are never amended or force-pushed.

## Stop And Pivot

If the first divergence cannot be traced after two focused attempts, record a
small research pivot that names the missing observation. Continue with any
other eligible stabilisation capability. Stop only when no credible task or
pivot remains inside this programme.
