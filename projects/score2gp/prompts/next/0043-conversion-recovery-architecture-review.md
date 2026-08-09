# 0043 — Conversion Recovery Evidence Adjudication and Architecture Review

Status: READY_FOR_GOVERNANCE_PROMOTION; not executable until ACTIVE_TASK.md
names this exact prompt.

## Role

Act as Architect and Researcher. Do not implement product behaviour. Use the
project Architect skill, conversion-recovery-director skill, research skill,
codebase-design skill, domain-modeling skill, and identity-safe governed loop.

## Context

The master diagnosis concludes that Score2GP can either refuse real inputs or
write musically corrupt output while a large synthetic test suite remains
green. Several source reports conflict, and six related PRs are still open.
Product main is not identical to any proposed workaround branch.

Pinned planning evidence:

- product main at 4a4f5c339e09987b9f41641397f1db7e8ab1be5d;
- product PR 418 head 6f8e438a600a3b33b1b017de462ba906e4861a9d;
- product PR 419 head 28c8a5965cb7a19a88ad76a38c86406dedb4655c;
- product PR 420 head 70a2d05077374640cf496503506226ac71b5ce38;
- AgentOps report PR 511 head b99fc3b218eff4311236283ca4d6079edfad5a64;
- AgentOps report PR 512 head f9d81b31c4419c039cda4db7efaff4aaf187d8eb;
- AgentOps report PR 513 head 648d750489faf849e30d78d391d3d5d275db7649;
- master aggregation head 14cccf577c9479200c58fbb79ee6145edb243f62.
- investigation disposition and archive index:
  projects/score2gp/reports/2026-08-09-investigation-pr-and-branch-disposition.md.

Re-query all SHAs at execution. A moved head invalidates the pin and must be
recorded before analysis continues.

Superseded investigation branches may be absent by execution time. Resolve
their exact trees through the archive tags named in the disposition report.

## Goal

Produce a full, evidence-backed recovery architecture and migration decision
that:

1. adjudicates every material contradiction and proposed workaround;
2. traces the current conversion call graph and ownership of musical truth;
3. defines deep target modules and typed interfaces;
4. identifies what works and must be preserved;
5. identifies what must be wrapped, replaced, removed, or researched;
6. defines a real-source-only testing architecture using
   score2gp-private-fixtures without reference leakage;
7. selects bounded downstream research and implementation slices with explicit
   dependencies, acceptance, counterexamples, and stop or pivot criteria.

## Required repositories and outputs

Read only:

- tticom/score2gp-agentops source reports and governance;
- tticom/score2gp source, tests, open PRs, and history;
- tticom/score2gp-private-fixtures approved private inputs and references.

Durable architecture belongs in a single product PR on branch
agy/conversion-recovery-architecture. Allowed product files:

- docs/design/2026-08-09-conversion-recovery-architecture.md
- docs/design/2026-08-09-real-source-testing-architecture.md
- docs/design/2026-08-09-conversion-module-migration-map.md

No source, test, fixture, dependency, workflow, schema, or generated artifact
may be changed. AgentOps status/prompt changes require a separate governance
promotion and are not part of the product architecture PR.

## Preflight

1. Prove Linux user, home, GitHub login, Git identity, canonical WSL roots, and
   locked skills revision.
2. Fetch without switching or mutating report branches.
3. Require clean task worktrees. Use a dedicated product worktree at the exact
   authorized base.
4. Record exact heads and changed paths for all source branches and PRs.
5. Record private fixture hashes and paths only in ignored local evidence.
6. Prove the reference GP is inaccessible to the generation process used in
   any replay.

## Evidence adjudication

For each report claim, label it verified repository fact, reproduced corpus
fact, inference, hypothesis, contradicted, or unknown. At minimum resolve:

- whether Lesson 5 and 6 contain embedded text, vector paths, raster evidence,
  or a mixture, page by page;
- correct measure, event, tempo, metre, triplet, voice, and fingering facts;
- first divergence on product main and each product PR;
- whether threshold changes recover true physical barlines or admit stems and
  cross-system candidates;
- page-continuous indexing behavior;
- multi-digit fret versus adjacent fingering and event-token segmentation;
- whether any duration scaling, capacity partition, truncation, deduplication,
  rest insertion, or missing-TAB synthesis changes musical truth;
- which report counts are events, note occurrences, chord members, or OMR
  candidates and therefore not directly comparable.

Create a hunk-level disposition for product PRs 418–420: preserve, replace,
reject, or unproven, with a reproducing command and real-source observation.
Recommend close, supersede, split, or retain-for-research. Do not merge.

## Current architecture review

Trace concrete functions and data transformations from:

- CLI and runtime provenance;
- PDF text, drawing, and raster acquisition;
- staff/system/barline detection and measure identity;
- notation OMR and sidecar generation;
- TAB candidate extraction and duration evidence;
- timeline, tuplets, voices, rests, and measure capacity;
- build_ir alignment and fallbacks;
- ScoreIR validation;
- GPIF serialization;
- semantic comparison and diagnostics.

For every stage record inputs, outputs, invariants, hidden state, fallback,
failure modes, duplicated ownership, callers, tests, and evidence loss.

## Target architecture design

Design the architecture twice:

1. topology-first internal reconstruction with optional sidecar adapters;
2. sidecar-first transcription with Score2GP topology and TAB correction.

Compare depth, interface size, locality, determinism, real-source testability,
failure transparency, migration cost, rollback, licensing, privacy, and
ability to preserve 4/4 triplets and observed TAB.

Select one outcome:

- Outcome A: a target route is viable and implementation can be sliced;
- Outcome B: a different route is viable but named research must precede it;
- Outcome C: no implementation route is justified and only named unblockers
  are authorized.

Define typed interfaces and explicit absence, ambiguity, conflict, observed,
derived, and inferred states for:

- source evidence;
- document topology and global measure identity;
- notation and TAB recognition adapters;
- paired-staff evidence fusion;
- musical timeline;
- observed and inferred fretboard assignment;
- ScoreIR and GPIF compilation;
- read-only semantic oracle.

## Sidecar research

Reconcile and update the 2026-08-03 alternatives work. Evaluate at least:

- current Audiveris batch output;
- corrected Audiveris OMR before MusicXML export;
- credible local OMR alternatives;
- credible assisted or commercial routes under privacy and license gates;
- direct typed Score2GP timing evidence;
- a hybrid sidecar using Score2GP topology, metre, tuplets, and voices.

Lesson 6 is a mandatory discriminator: the route must encode its source 4/4
triplets with balanced measures. File creation, 12/8 substitution, silent
repair, or parseability is failure. Produce an A, B, or C decision and smallest
next probe. Do not add a production dependency.

Lesson 6 is held-out acceptance evidence only. Reject any design that inspects
its filename, hash, page, coordinates, expected counts, or reference identity,
or that introduces constants or branches calibrated only to this fixture. The
same generic route must be evaluated on a second structurally distinct score.

## Real-source testing architecture

Design a three-repository contract:

- private-fixtures owns PDFs, references, confidential oracles, and manifests;
- product owns generic runners, parsers, comparators, and result schemas;
- AgentOps owns acceptance policy, task authority, and sanitized receipts.

The generation subprocess must not receive or discover the reference GP path.
The oracle runs afterward in a separate process. Define how local and CI
credentials access the private repository, how absence fails clearly, and how
no private data enters public artifacts.

Inventory current tests by claim and data source. Plan replacement of every
synthetic behavioural conversion test with a real-source acceptance or
provenance-linked extracted case. Pure format tests may remain only when they
make no recognition or musical-fidelity claim. Refusal tests remain safety
tests and require paired productive success evidence.

Require the replacement harness to fail against known-bad implementations:
300pt snapping, duration scaling, open-string synthesis, capacity
fragmentation, page index reset, and proximity digit concatenation.

## Required deliverables

The three architecture documents must jointly include:

1. executive decision and supported product outcome;
2. claim-by-claim adjudication table with exact revisions;
3. open PR disposition;
4. current call graph and failure propagation;
5. domain glossary;
6. two target designs and trade-off comparison;
7. selected outcome and module interfaces;
8. preserve, wrap, replace, and delete matrix;
9. sidecar technology decision or bounded probes;
10. real-source test and private CI architecture;
11. legacy synthetic-test migration inventory method;
12. dependency graph mapping CRP-00 through CRP-15;
13. implementation-ready prompt specification for the first unblocked task,
    recorded in the product migration map for a separate AgentOps governance
    promotion;
14. skeleton refinements for dependent tasks;
15. risks, rollback, stop conditions, and unverified facts.

## Acceptance

- Every non-obvious claim has exact repository or primary-source support.
- Every material report contradiction is resolved or explicitly blocks a task.
- The architecture preserves verified working behavior and does not layer new
  logic over destructive fallbacks.
- Each implementation task touches one seam and has a real-source failing
  oracle that is red on a known-bad revision.
- Lesson 5 and Lesson 6 are mandatory; a second distinct score is required for
  every claimed generic repair.
- The migration map contains an implementation-ready first-prompt
  specification. The Architect does not publish or activate that AgentOps
  prompt from the product PR; dependent AgentOps prompts remain skeletons.
- The plan ends in useful GP output, not merely cleaner refusal.
- Product verification and artifact audit pass with docs-only changes.

## Stop conditions

Stop and return Outcome C if private evidence cannot be inspected, reference
isolation cannot be proved, report conflicts cannot be reproduced, no sidecar
route can preserve Lesson 6 timing, a task requires fixture-specific logic, or
the proposed architecture cannot be migrated one seam at a time.

## Handback

Report branch, exact base and head, files changed, evidence commands, private
artifact audit, selected outcome, first prompt specification awaiting separate
governance promotion, rejected alternatives, open unknowns, and the first
remaining product mismatch.
