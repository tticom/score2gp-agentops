# Recognition Architecture Replacement Backlog

Status: PROPOSED — only `ORCHESTRATION_STATE.json.task` is executable
Date: 2026-08-27
Architecture: hybrid vector/raster, topology-first, evidence-fusion recognition

## Outcome

Replace feature-by-feature geometry heuristics with a staged recognition system
in which observations describe rendered evidence, hypotheses retain alternatives,
document topology supplies structural context, constrained resolution produces a
typed musical document, and ScoreIR compilation accepts only validated semantics.

The existing ScoreIR and GPIF export path remains the downstream seam. Learned
models are deferred until an annotated graph corpus and deterministic baseline
exist. Every productive recognition claim requires reference-isolated real-source
evidence from at least two structurally distinct scores.

## Programme invariants

- Vector, text, and raster adapters are peer evidence sources.
- Raw primitives and detector outputs never acquire musical meaning in acquisition.
- Absolute PDF-point thresholds cannot be acceptance criteria; policies use local
  scale estimates and retain the measured source values.
- Ambiguity and contradiction are data, not exceptions to suppress or defaults to
  invent.
- Observed TAB string/fret evidence is never replaced by optimized fingering.
- Reference GP data is validation-only and unavailable to the generation process.
- No task spans more than one external module seam.
- Synthetic fixtures may prove schemas and pure algorithms but cannot prove
  recognition or musical correctness.
- A replacement must fail against a known-bad implementation before superseded
  behaviour or tests are deleted.

## Supersession ledger

Completed work remains completed evidence. Supersession changes future ownership;
it does not rewrite history.

| Prior task | Disposition | Replacement |
|---|---|---|
| CRP-01 / M6-2 barline threshold cleanup | COMPLETED CONTAINMENT | REC-04, REC-07 |
| CRP-02 topologically locked barlines | SUPERSEDED | REC-06, REC-07 |
| CRP-03 / M6-3 page offsets and indexing | SUPERSEDED | REC-06, REC-08 |
| M6-4 digit over-merging | SUPERSEDED | REC-09 |
| NPG-03B floating barline isolation | SUPERSEDED AS FUTURE DIRECTION | REC-07 |
| NPG-04C geometric rhythm extraction | SUPERSEDED AS FUTURE DIRECTION | REC-10, REC-12 |
| NPG-04D structural signalling | COMPLETED; implementation retained provisionally | REC-11, REC-14 |
| 0050 document topology skeleton | SUPERSEDED | REC-06 through REC-08 |
| 0051 recognition adapter skeleton | SUPERSEDED | REC-03 through REC-05 |
| 0052 paired-staff fusion skeleton | SUPERSEDED | REC-11, REC-12 |
| 0053 musical timeline skeleton | SUPERSEDED | REC-12, REC-13 |
| 0054 TAB ownership skeleton | SUPERSEDED | REC-09, REC-12 |
| 0055 compiler refactor skeleton | SUPERSEDED | REC-13 |
| 0056 legacy removal skeleton | SUPERSEDED | REC-14 |

## Ordered tasks

### REC-00 — Recognition domain contract and supersession ledger

Repository: `score2gp-agentops`  
Depends on: CRP-01  
Prompt: `prompts/next/rec-00-recognition-domain-contract.md`

Define the ubiquitous language, stage ownership, forbidden leakage, failure
taxonomy, architecture decision, and exact migration/supersession map. No product
behaviour changes.

### REC-01 — Layered semantic oracle

Repository: `score2gp`  
Depends on: REC-00  
Prompt: `prompts/next/rec-01-layered-semantic-oracle.md`

Compare systems/staves, measure boundaries, ordered TAB tokens, string/fret
ownership, onsets/chords, duration/voice, complete measures, and whole-score
results after generation. Prove reference-process isolation and demonstrate red
results against known-bad revisions.

### REC-02 — Recognition contract schemas

Repository: `score2gp`  
Depends on: REC-00  
Prompt: `prompts/next/rec-02-recognition-contract-schemas.md`

Add versioned types and serialization contracts for DocumentObservations,
DocumentTopology, RecognitionGraph, ResolutionResult, and MusicalDocument without
changing current recognition behaviour.

### REC-03 — Canonical vector and text observations

Repository: `score2gp`  
Depends on: REC-02  
Prompt: `prompts/next/rec-03-vector-text-observations.md`

Extract primitive acquisition and canonical stroke/glyph reconstruction from
`pdf.py`. Outputs contain coordinates, provenance, modality and detector facts,
but no staff, barline, string, measure, duration, pitch or event assignments.

### REC-04 — Local scale model

Repository: `score2gp`  
Depends on: REC-03  
Prompt: `prompts/next/rec-04-local-scale-model.md`

Estimate notation staff space, TAB string space, stroke thickness and glyph scale.
Replace acceptance-driving point constants behind the new seam with dimensionless
policies, preserving measured values for diagnostics.

### REC-05 — Raster observation adapter

Repository: `score2gp`  
Depends on: REC-02  
Prompt: `prompts/next/rec-05-raster-observation-adapter.md`

Add deterministic rendering and typed raster observations. Raster evidence may
support or contradict vector evidence but cannot mutate it or become final truth.

### REC-06 — Staff and system topology

Repository: `score2gp`  
Depends on: REC-04, REC-05  
Prompt: `prompts/next/rec-06-staff-system-topology.md`

Reconstruct pages, reading order, systems, notation/TAB staff regions, pairings
and stable identities. Retain competing hypotheses and refuse unsupported layout.

### REC-07 — Physical divisions and measure topology

Repository: `score2gp`  
Depends on: REC-06  
Prompt: `prompts/next/rec-07-measure-topology.md`

Treat vertical evidence as physical-division hypotheses, then resolve measure
boundaries using staff span, paired-staff alignment, neighbouring divisions and
measure plausibility. Cover fragmented, floating, double and repeat-adjacent cases.

### REC-08 — Page-continuous topology

Repository: `score2gp`  
Depends on: REC-07  
Prompt: `prompts/next/rec-08-page-continuous-topology.md`

Establish stable system and measure identities across pages without leaking
cumulative coordinate offsets or mutable running indexes into callers.

### REC-09 — TAB token evidence

Repository: `score2gp`  
Depends on: REC-04, REC-06  
Prompt: `prompts/next/rec-09-tab-token-evidence.md`

Detect glyph tokens before resolving multi-digit frets. Preserve alternatives
until string, spacing and onset context distinguish `10` from adjacent `1 0` or
`7 10`. Do not assign final events.

### REC-10 — Rhythm evidence

Repository: `score2gp`  
Depends on: REC-04, REC-06  
Prompt: `prompts/next/rec-10-rhythm-evidence.md`

Produce notehead, stem, beam, flag, rest, dot and tuplet hypotheses with explicit
relationships and provenance. Do not assign final duration or voice.

### REC-11 — Recognition graph assembler

Repository: `score2gp`  
Depends on: REC-08, REC-09, REC-10  
Prompt: `prompts/next/rec-11-recognition-graph.md`

Assemble typed nodes and bounded candidate relations including IN_STAFF,
ON_TAB_STRING, IN_MEASURE, ATTACHED_TO_STEM, GROUPED_BY_BEAM, SAME_ONSET,
PAIRED_NOTATION_TAB, SUPPORTS_BOUNDARY, DERIVED_FROM and CONFLICTS_WITH.

### REC-12 — Constrained semantic resolver

Repository: `score2gp`  
Depends on: REC-11  
Prompt: `prompts/next/rec-12-semantic-resolver.md`

Resolve boundaries, measures, string ownership, onsets, chords, durations and
voices under hard and soft constraints. Return Resolved, Ambiguous, Unsupported
or Contradictory outcomes; never coerce inconsistent music into capacity.

### REC-13 — MusicalDocument and ScoreIR compiler seam

Repository: `score2gp`  
Depends on: REC-12  
Prompt: `prompts/next/rec-13-musical-document-compiler.md`

Introduce a typed MusicalDocument and make the new ScoreIR compiler path accept
that interface rather than `list[Any]`, dictionary introspection or implicit
fallback shapes. Preserve GPIF behaviour.

### REC-14 — Shadow mode, calibration, cutover and legacy retirement

Repository: `score2gp`  
Depends on: REC-01, REC-13  
Prompt: `prompts/next/rec-14-shadow-cutover.md`

Run old and new paths side by side, calibrate measure/score acceptance on held-out
inputs, authorize generation only for proven input classes, and delete legacy
logic only after replacement evidence is independently reviewed. Evaluate learned
relation models only as a later subtask with an annotated corpus and deterministic
baseline.

## Dependency graph

```text
REC-00 ─┬─ REC-01 ───────────────────────────────────────────┐
        └─ REC-02 ─┬─ REC-03 ─ REC-04 ─┬─ REC-06 ─ REC-07 ─ REC-08 ─┐
                   └─ REC-05 ───────────┘        │                  │
                                      ├─ REC-09 ─┤                  │
                                      └─ REC-10 ─┴─ REC-11 ─ REC-12 ─ REC-13
                                                                       │
REC-01 ─────────────────────────────────────────────────────────────────┴─ REC-14
```

## Global stop conditions

- Generation can access a reference GP or reference-derived expected values.
- A rule branches on fixture name, hash, page number or stored coordinates.
- A stage must assign semantics owned by a later stage to make its test pass.
- Success requires dropping events, scaling durations, inventing measures or
  silently selecting optimized fingering.
- A private corpus is absent for a productive acceptance claim.
- A learned model is proposed before graph schema, annotation provenance,
  deterministic baseline and offline reproducibility exist.
