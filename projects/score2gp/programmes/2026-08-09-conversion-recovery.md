# Score2GP Conversion Recovery Programme

Status: PROPOSED — governance planning only
Date: 2026-08-09
Evidence: projects/score2gp/reports/2026-08-09-master-conversion-failure-diagnosis.md
Branch: agy/master-conversion-failure-diagnosis

## Outcome

Restore Score2GP as a useful deterministic conversion system. A successful
run must produce a musically faithful Guitar Pro document from an approved
real-world PDF. A clean refusal remains a safety property, but refusal alone
is never a product-success or programme-completion result.

The first acceptance scores are Lesson 5 and Lesson 6. Lesson 6 must preserve
its source metre and triplet timing; a sidecar that reinterprets 4/4 triplets
as 12/8 or emits underfull or overlapping voices is not adequate merely
because it is parseable.

## Authority and execution

This document and its backlog are informative until a governance PR promotes
one task to ACTIVE_TASK.md. The programme uses Tier A:

1. evidence adjudication and architecture;
2. independent architecture review;
3. one bounded implementation task and one product PR;
4. exact-head adversarial review using real-fixture evidence;
5. human merge;
6. fresh corpus replay before the next promotion.

No product implementation may begin from this document alone.

## Evidence hierarchy

1. The source PDF and its visual or document geometry are generation evidence.
2. A generated sidecar is derived evidence and must retain generator version,
   input hash, output hash, corrections, and timing-adequacy provenance.
3. The reference GP is validation-only. It must never influence generation,
   thresholds, recognition, segmentation, tempo, or fingering.
4. Bar and event semantic comparison outranks aggregate counts.
5. Fresh no-reference conversion artifacts outrank unit-test pass totals.
6. Conflicting reports remain unresolved until reproduced at exact revisions.

## Immediate branch and PR containment

Product main at preflight retains the bounded 24pt outer tolerance and 130pt
inherited-bar-width constant. The destructive alternatives described by the
report are primarily on open product PRs 418, 419, and 420, not one merged
baseline. The first task must classify each changed hunk as preserve, replace,
reject, or unproven; it must not revert code that is not on main.

Open governance reports 511, 512, and 513 are evidence inputs, not competing
authorities. Their contradictory claims, especially whether Lesson 5 and 6
expose extractable PDF text, must be empirically adjudicated.

## Target architecture

The architecture review must design deep modules at these seams:

1. Source evidence acquisition — reads text, vector primitives, and raster
   renderings without assigning musical meaning.
2. Document topology — owns pages, systems, paired notation and TAB staves,
   physical barlines, measure identity, and page-continuous indexing.
3. Recognition adapters — independently recognize notation and TAB evidence
   from available modalities and return typed evidence with provenance.
4. Evidence fusion — associates notation, TAB, technique, and structure only
   after topology exists; ambiguity remains explicit.
5. Musical timeline — owns metre, tuplets, voices, rests, onsets, durations,
   and measure capacity. It must not scale durations or invent measures.
6. Fretboard assignment — preserves observed string and fret evidence. An
   optimizer may be a labelled fallback only when TAB is absent and cannot
   claim arranger-fingering equivalence.
7. Score compilation — maps validated evidence to ScoreIR and GPIF and rejects
   unresolved invariants before writing output.
8. Semantic oracle — performs read-only bar and event comparisons and reports
   first divergence without feeding references into generation.

The review must define typed interfaces, invariants, error states, ownership,
migration seams, and compatibility plans. It must identify existing code to
preserve, wrap temporarily, replace, or delete.

## Real-source-only test policy

Synthetic or hand-authored mock score data is banned as proof of conversion,
recognition, grouping, timing, fingering, or GP correctness. New behavioural
tests must execute data obtained from approved real-world PDFs in the sibling
score2gp-private-fixtures repository and must carry source provenance.

The private repository owns raw PDFs, reference GP files, extracted private
oracles, and confidential expected data. The public product repository owns
generic runners, comparators, schemas, and algorithms; it must not embed
private content. Required private-corpus gates must fail clearly when the
corpus is unavailable. Silent skips cannot satisfy a gate.

Every legacy test must be classified as:

- real-source acceptance — retain;
- real-source extracted unit or contract test — retain with provenance;
- pure format or schema test — retain only if it makes no recognition or
  musical-correctness claim;
- synthetic behavioural false oracle — replace, quarantine, then delete;
- refusal-only test — retain only as a safety test and pair it with a
  productive real-source success test for the supported class.

No task may weaken the suite simply by deleting tests. A replacement oracle
must exist and fail against a known-bad branch before a false oracle is removed.

## Programme gates

### Gate 0 — Evidence and branch adjudication

Freeze exact SHAs, reproduce conflicting claims, disposition the six open PRs,
and establish a first-divergence ledger on product main.

### Gate 1 — Real-fixture oracle

The private harness executes Lesson 5 and Lesson 6 from PDF through output,
compares topology and ordered events, and detects every destructive branch.
The generator process cannot read the reference GP.

### Gate 2 — Architecture decision

An independently reviewed architecture names module interfaces, migration
order, deletion plan, selected sidecar strategy, and stop or pivot criteria.

### Gate 3 — Structural and timing viability

Real-source tests prove page-continuous topology, paired-staff alignment, 4/4
triplets, measure balance, voices, and no fabricated scaling across at least
two distinct scores.

### Gate 4 — TAB and fingering viability

Observed TAB digits are recovered with source coordinates and stable string
ownership. Synthesized or optimized fingering is never labelled as observed.

### Gate 5 — End-to-end usefulness

Fresh no-reference conversions write parseable GP files whose measure map,
event sequence, timing, tempo, pitches, string and fret assignments, and
supported techniques pass the real-source oracle.

## Global stop conditions

- Stop if generation needs reference-GP feedback.
- Stop on private filename, coordinate, page, or measure special cases.
- Stop if output passes by dropping events, scaling time, inventing measures,
  or synthesizing unlabeled fingering.
- Stop when a technology decision lacks a reproducible real-source probe,
  licensing and privacy analysis, and continue or pivot criteria.
- Stop if an implementation task spans more than one architectural seam.
- Stop if a green test cannot be shown red on the known-bad implementation it
  claims to prevent.
