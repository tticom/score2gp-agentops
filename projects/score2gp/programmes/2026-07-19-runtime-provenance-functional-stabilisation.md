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

Completed 2026-07-20: product PR #378 was externally merged as `e72cd7c8de5277d3d3ba91234c0eea4fbd63e145` (PR head `a8ba0e75d57f558d07acfaa0e5292f753025b533`). The native corpus baseline truthfully observed `missing_musicxml` rather than successful conversion.

### FS-02: Canonical Entry-Point Reconciliation

Use FS-01 evidence to answer one question: which committed function path is
actually run by the supported command? If a local auto-OMR path exists but is
not committed, it is an uncontrolled runtime and must be cleanly committed and
reviewed or discarded. Do not describe an external OMR engine, a deterministic
generator, or a diagnostic bridge as the product route without direct function
and revision evidence.

Correction 2026-07-20: a prior FS-02 completion record is invalid. Its probe
used a module invocation rather than the supported console command, and its
agent used `git reset --hard` and `git clean -fd` before the local preflight
state could be recorded. That run cannot establish whether a pre-clean local
route existed or was discarded. FS-02 remains active and must be repeated in
the WSL-controlled environment.

Recovery 2026-07-20: following the unauthorized-merge incident, the WSL
GitHub and local Git identities were independently verified as
`tticom-automation`, and active `Main_Protect` rulesets on both repositories
were verified to require approving review, dismiss stale approvals, and deny
that automation identity a bypass. FS-02 may resume only after the governance
record of this verification is externally merged. PR #332 is stale and is not
evidence of FS-02 completion.

Completion 2026-07-20: the corrected canonical evidence was independently
reviewed and preserved on `main` through governance PR #337. At product SHA
`e72cd7c8de5277d3d3ba91234c0eea4fbd63e145`, the supported `convert` route
requires an explicit MusicXML sidecar and does not call the standalone OMR
command. FS-02 is DONE. The human maintainer selected the write-access with
ruleset-containment operating model recorded in the second merge-attempt
incident report.

### FS-03 And FS-04: Stabilise The Real Path

Run the selected corpus, identify the first shared source/output divergence,
and repair one behaviour class per PR. Required evidence follows the event
through source evidence, MusicXML, ScoreIR, GPIF, and rendered output where
applicable. A reviewer must be able to trace a ghost rest by stable event or
source identifier before accepting a rest-related claim.

FS-03A is an Architect-first prerequisite: define the supported, provenance
recorded MusicXML timing-source route before implementing this phase. It must
not assume that the standalone OMR command is integrated with `convert`.

Completed 2026-07-21: governance PR #339 was externally merged as
`5ba1514430d83ecda1b137fad402c9bb239fb36e`. It established that the explicit
MusicXML sidecar is the only supported timing-source route at the examined
product revision, and that the standalone `omr` route remains unproven until
it has an artifact contract.

### FS-03B: OMR Artifact Contract

Create the smallest public-testable contract around the existing standalone
`omr` command: deterministic XML/MXL discovery, zero/multiple candidate
refusals, XML/MXL validation, PDF/artifact hashes, a machine-readable manifest,
and an explicit `convert --musicxml` handoff path. It must not call `convert`,
make `convert` call `omr`, require Audiveris in public CI, or alter recognition,
timing semantics, ScoreIR, GPIF, layout, or embellishment behaviour. The
product PR must obey `PR_EVIDENCE_CONTRACT.md`.

Completed 2026-07-21: product PR #379 was externally merged as
`df6e5c8178794f0ea7f98d69e069a1be3593f176` from reviewed head
`60b0fa1622292f42032aa98f0b3d99e7b5240d29`. It adds deterministic standalone
OMR artifact discovery, validation, and manifest generation. It does not prove
that Audiveris is installed or that its output can be handed to `convert`.

### FS-03C: Rootless Audiveris Runtime Probe

Use the official pinned Audiveris 5.7.0 Ubuntu 24.04 x86_64 package in an
ignored, user-local WSL probe directory. Verify the published SHA-256 before
extracting it without root privileges, run one public-fixture `omr` invocation,
then explicitly pass any validated sidecar to `convert --musicxml`. Record the
exact observed status and first failure. This task establishes environment
evidence only: it must not add product behaviour, hide a failed handoff, or
claim recognition or visual correctness.

Completed 2026-07-21: governance PR #345 was externally merged as
`418a2bf2897aff05212e0935535957cc85cef450`. At product SHA
`df6e5c8178794f0ea7f98d69e069a1be3593f176`, rootless Audiveris produced one
structurally validated MXL artifact for the authorised standard-staff fixture.
The explicit handoff then refused at `tabraw-import` because that fixture has
no safe TAB grouping. The result proves artifact availability for that runtime,
but leaves a compatible-PDF handoff and musical correctness unproven.

### FS-03D: Compatible Public Sidecar-Handoff Matrix

Run the committed rootless OMR and explicit sidecar handoff against the public
paired notation-and-TAB fixtures, first the standard system and then its
double-barline counterpart. For each fixture, separately record PDF grouping
eligibility, OMR artifact status, explicit convert stage/result, timing status,
and first remaining warning. Do not modify product behaviour or infer musical
correctness from output creation. This task determines whether the missing
grouping in FS-03C was solely a fixture mismatch and names the first shared
product divergence only when the exact route demonstrates one.

Completed 2026-07-21: governance PR #347 was externally merged as
`cbc9e983d85750fd69d43bfadadd1642bd2fad8f`. Rootless Audiveris produced
validated sidecars and explicit conversion reached `gp-write` for both public
paired notation-and-TAB fixtures. The converted results had zero events and
zero matched candidates, leaving extracted TAB candidates unused. This is an
observed handoff, not a supported functional route.

### FS-03E: Sidecar-to-ScoreIR Event-Loss Trace

Use the exact FS-03D public fixtures and product revision to determine the
first data-loss, filtering, or unsupported transformation between the
Audiveris sidecar and the empty ScoreIR result. This is Architect-led,
evidence-only work: reproduce the explicit sidecar route, capture counts at
each observable boundary, map the committed parser-to-ScoreIR source path, and
name the first observed non-zero-to-zero transition. If existing diagnostics
cannot expose it, record that observability limit instead of adding
instrumentation or guessing a cause. No product repair or refactor may begin
until this trace is independently reviewed.

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
