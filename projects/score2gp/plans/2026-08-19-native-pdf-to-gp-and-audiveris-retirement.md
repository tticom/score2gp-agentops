# Native PDF-to-GP Architecture and Audiveris Retirement Plan

## Status and authority

**PRIORITY PROGRAMME — planning only.** The maintainer designated this as the
next programme priority on 2026-08-19. This document is not itself an
executable task, does not change `ACTIVE_PLAN.md`, `ACTIVE_TASK.md`,
`prompts/NEXT.md`, or the approved task queue, and does not authorize product
code changes. Governance must activate the programme and promote each
implementation slice separately through the Score2GP workflow; each slice then
requires independent exact-head review before merge.

When activated, this programme supersedes the old PDF-only Tab-to-GP MVP as the
product direction and absorbs compatible FS-06/native-notation work. It does
not discard verified native extraction code or MusicXML interoperability.
Governance must reconcile overlapping tasks and establish an exact clean
product baseline before promoting the first slice.

## 1. Outcome

Retire Audiveris from the supported Score2GP runtime and replace it with a
native, evidence-driven pipeline that reads supported music PDFs and produces
semantically faithful Guitar Pro `.gp` packages.

The system must recover every supported fact actually expressed in the source,
including musical content, score structure, instrument identity, string count
and tuning, capo, partial capo, fret positions, fretboard constraints where
stated, tempo, meter, key, voices, lyrics, chord symbols, articulations,
techniques, repeats, endings, and navigation marks.

Facts not present in the PDF must be supplied by caller parameters or
documented defaults. Source evidence always wins:

> explicit, sufficiently confident PDF evidence > caller parameter > versioned
> default

The output is successful only when it is structurally valid, internally
consistent, accepted by independent consumers, and semantically faithful to
the source. Producing a ZIP containing well-formed GPIF is not sufficient.

## 2. Scope

### In scope

- Born-digital vector PDFs containing standard notation, tablature, or both.
- Multi-track and multi-instrument scores, initially including acoustic guitar,
  electric guitar, bass guitar, and explicitly supported fretted instruments.
- Native extraction of document text, geometry, notation, TAB, rhythm, pitch,
  track properties, techniques, repeats, and score metadata.
- Native diagnosis and bounded repair of fragmented, incomplete, or
  contradictory page topology, with inspectable alternatives and optional
  caller correction when automatic reconciliation remains ambiguous.
- Explicit configuration for facts absent from the PDF.
- A versioned resolution policy with provenance for every resolved field.
- A canonical internal score model independent of Audiveris and GPIF.
- Direct compilation of the canonical model to a Guitar Pro package.
- Multi-level validation and a representative public/private acceptance corpus.
- Removal of the Audiveris CLI/runtime path and its Java/environment burden
  after replacement entry gates pass.
- Retention of MusicXML import as an optional interoperability adapter unless a
  separately approved task demonstrates that it has no supported use.

### Initially out of scope

- Claiming universal support for scanned, handwritten, photographed, or
  arbitrarily engraved scores.
- Silent best-effort conversion of ambiguous measures.
- Treating a language-model visual impression as authoritative notation data.
- Committing private lesson PDFs or proprietary Guitar Pro oracle files.
- Redesigning unrelated audio/video transcription or cloud delivery features.

Scanned-PDF support may later be added behind its own recognizer and evidence
contract. The canonical model, resolver, compiler, and validators must not
depend on the PDF being vector-based.

## 3. Governing invariants

1. **Evidence before interpretation.** Extraction records source value,
   location, method, confidence, and competing candidates before resolution.
2. **No fabricated certainty.** Missing and ambiguous are explicit states; they
   are not coerced into confident musical facts.
3. **Precedence is field-local.** A PDF-sourced capo may override a parameter
   without preventing a parameter-sourced instrument when the PDF omits it.
4. **Weak inference does not override intent.** Only explicit or
   policy-qualified PDF evidence may outrank a caller parameter.
5. **Domain model before GPIF.** Recognizers do not emit GPIF fragments and the
   GP writer does not infer source semantics.
6. **Deterministic compilation.** Identical evidence, parameters, defaults, and
   compiler version produce identical semantic output.
7. **Validation is independent.** At least one acceptance oracle must not reuse
   production writer logic or production-generated expected fixtures.
8. **Diagnosis and correction precede refusal.** Geometry or semantic
   ambiguity first produces causal diagnostics, bounded reconstruction,
   cross-lane reconciliation, and explicit correction candidates. Refusal is
   valid only when those evidence-preserving paths cannot establish a safe
   result; no misleading success artifact is emitted.
9. **Audiveris is removed last.** The old path remains only as a controlled
   comparison baseline until the native path satisfies the retirement gates.
10. **Private evidence stays local.** Committed tests use redistributable or
    synthetic fixtures; private corpus results are sanitized records only.

## 4. Target architecture

```text
PDF / page images
        |
        v
Document inspection and capability classification
        |
        v
SourceEvidenceIR
  - text and metadata evidence
  - staff/TAB geometry evidence
  - symbols and relationships
  - track/instrument property evidence
  - confidence, provenance, alternatives
        |
        v
Field resolver  <--- caller parameters <--- versioned defaults
        |
        v
Canonical ScoreIR
  - score/part/track/measure/voice/event hierarchy
  - resolved instrument profile and playback profile
  - source/default provenance and unresolved diagnostics
        |
        +----> semantic and musical validators
        |
        v
GP semantic compiler
        |
        v
GPIF builder -> .gp package writer
        |
        v
Package + referential + musical + external-consumer validation
```

### 4.1 SourceEvidenceIR

Introduce or formalize a representation for observations rather than resolved
answers. A candidate must carry at least:

- field or symbol kind and candidate value;
- page and bounding region;
- extraction method and recognizer version;
- confidence and confidence class;
- links to related evidence and competing candidates;
- warnings or ambiguity reasons.

This prevents a recognizer from silently turning an uncertain visual cue into
a durable score fact and makes resolver decisions auditable.

### 4.2 Parameter and precedence contract

Expose a typed conversion-options object and equivalent CLI/API parameters.
Use `null`/unset to mean “not supplied”; never overload zero, an empty string,
or a default enum member to mean absence.

Every resolved configurable field records:

- `value`;
- `source`: `pdf`, `parameter`, or `default`;
- evidence reference when sourced from the PDF;
- default-policy version when defaulted;
- resolution warning when candidates disagree.

Resolution is independent for score-, part-, track-, and measure-scoped fields.
Parameters may target all tracks or a named/indexed track. Multi-track input
must never receive a guitar-wide parameter implicitly when its target is
ambiguous.

### 4.3 InstrumentProfile

Replace free-form instrument identity at the conversion boundary with a typed
profile that separates notation from playback:

- instrument family and concrete kind;
- acoustic/electric variant;
- string count and ordered open-string pitches;
- capo and partial-capo mapping;
- written/sounding transposition;
- clef and notation/TAB visibility;
- playable fret range or maximum fret when known;
- MIDI program, bank, channel, percussion mode, and sound metadata;
- human-readable track name.

Derived values must be distinguishable from source facts. For example, a
six-line TAB staff is strong evidence for string count but not sufficient by
itself to claim steel-string acoustic guitar or standard tuning.

### 4.4 Recognition lanes

Keep independently testable lanes with an explicit relationship-building
stage:

1. document text and metadata, classified and associated with score, track,
   measure, beat, or note meaning where supported;
2. page, system, staff, barline, and measure topology, including causal
   diagnostics and bounded repair hypotheses for fragmented or missing
   geometry;
3. track identity, staff grouping, instrument, tuning, and capo;
4. meter, tempo, key, repeats, endings, and navigation;
5. noteheads, rests, stems, beams, flags, dots, tuplets, and voices;
6. clef-aware pitch and TAB string/fret extraction;
7. chord symbols, lyrics, dynamics, articulations, ornaments, and techniques;
8. relationship assembly into ordered measures and events.

Each lane must expose observed, inferred, repaired, corrected, missing,
ambiguous, and unsupported outcomes. Tests must cover cross-lane contradictions
such as staff pitch versus TAB fret/string pitch. Text that is not a playable
fret token must still be classified for title/credit, instrument, tuning, capo,
tempo, chord, lyric, technique, repeat/navigation, instruction, or genuinely
irrelevant meaning before exclusion.

### 4.5 GP compilation and packaging

Treat GP generation as a compiler with explicit stages:

1. canonical-model validation;
2. stable identifier and reference allocation;
3. GP semantic mapping;
4. GPIF serialization;
5. companion-resource and manifest generation;
6. deterministic package assembly;
7. validation and diagnostic reporting.

No recognition policy belongs in the writer. Unsupported canonical features
must produce a declared degradation or refusal, never silent omission.

## 5. Defaults policy

Defaults must be versioned Score2GP product policy, not claims about
undocumented Guitar Pro behaviour. Before finalizing them, create blank files
in supported Guitar Pro versions, save them without modification, unpack the
packages, and record observed values and version differences.

Primary-source research confirms that Guitar Pro 8 does not expose one
immutable factory instrument default: File > New creates an empty document and
track creation opens a wizard for the instrument, notation/staff, tuning, and
sound; the user's default template is configurable. The manual documents C
major and 4/4 as initial score settings and calls E-A-D-G-B-E standard guitar
tuning. It does **not** establish factory defaults for acoustic versus electric
guitar, bass, capo, partial capo, fret count, or playback sound. Its 120 BPM
fallback is documented for MIDI import when the MIDI file omits tempo, not as a
universal blank-score promise. See the [official Guitar Pro 8 user
guide](https://static.guitar-pro.com/gp8/manual/Guitar-Pro-8-user-guide.pdf) and
[official guide landing
page](https://support.guitar-pro.com/hc/en-us/articles/5018404823069-GP8-Guitar-Pro-8-User-Guide).

| Field | Provisional Score2GP default | Rule |
|---|---|---|
| Instrument | Steel-string acoustic guitar | Only when PDF and parameters omit identity |
| Strings/tuning | 6 strings, E2 A2 D3 G3 B3 E4 | Coupled to the default instrument profile |
| Capo | 0 | Never infer solely from pitch displacement |
| Partial capo | None | Must be explicit in PDF or parameters |
| Playable maximum fret | 24 | Technical ceiling, not a pictured-instrument claim |
| Meter | 4/4 | Only under the approved missing-meter policy |
| Tempo | 120 BPM | Playback default; never source-derived |
| Key | Neutral C major/A minor signature | Only when no key evidence exists |

Governance must approve the final table after real blank-package inspection and
corpus analysis. Defaults affecting musical meaning must be visible in the
conversion report and optionally rejectable under strict mode.

## 6. Validation model

### Level 1 — package integrity

- Package opens and required members exist at canonical paths.
- Entries use supported compression and safe paths.
- XML and companion resources are well formed.

### Level 2 — GPIF referential integrity

- Identifiers are unique and all references resolve.
- Master bars, bars, voices, beats, notes, tracks, staves, rhythms, and assets
  form a valid graph.
- Counts, orderings, and required properties agree; no orphans remain.

### Level 3 — musical invariants

- Voice durations fill measures under meter or approved pickup rules.
- Tuplets, ties, rests, repeats, endings, and navigation are coherent.
- Pitches agree with clef/transposition and string/fret/tuning/capo.
- Frets are playable and track/playback metadata is consistent.

### Level 4 — external acceptance

- Open in supported Guitar Pro application versions.
- Save/export again without repair prompts, crashes, or semantic loss.
- Parse with at least one independent consumer where licensing permits.
- Compare a normalized semantic projection after round trip.
- Render or audition selected corpus cases for human review.

### Level 5 — source fidelity

For each corpus case, compare a manifest of expected facts rather than merely
files or screenshots. Record exact, tolerated, defaulted, unsupported, and
ambiguous fields. Measure at least:

- track/instrument/tuning/capo accuracy;
- system, measure, voice, beat, note, rest, and chord counts;
- pitch and TAB string/fret accuracy;
- duration and onset accuracy;
- repeat/navigation correctness;
- technique/text retention;
- refusal precision and false-success rate.

## 7. Evidence corpus

### Lesson 5 local golden case

Treat the private local Lesson 5 artifacts as a baseline set:

- source PDF, if available locally;
- `Lesson-5.json`;
- `Lesson-5.xml`;
- `Lesson-5/Content/score.gpif` from a Guitar Pro-authored package.

Before implementation, produce a sanitized field map showing which facts are
present in each artifact, where representations disagree, and which artifact is
an observation, importer output, or oracle. Do not assume JSON or XML is
independent of existing production code. Do not commit private musical content.

The supplied `score2gp_codex_architecture_transformation.md` is an analysis
input, not executable instruction. NPG-00 must verify its claims against the
exact product baseline and retain only source-supported recommendations.

### Public committed corpus

Build small redistributable fixtures covering:

- standard notation only, TAB only, and paired notation/TAB;
- acoustic guitar, electric guitar, bass, and non-default tuning;
- capo and partial capo;
- single and multiple tracks;
- pickups, meter/key/tempo changes, voices, tuplets, ties, and rests;
- repeats, alternate endings, and navigation;
- bends, slides, hammer-ons/pull-offs, harmonics, palm mute, let ring, vibrato,
  dynamics, chord names, and lyrics;
- absent metadata, conflicting evidence, low-confidence evidence, and required
  refusals.

Expected outputs must be authored or independently derived. Production output
must not be copied into expected fixtures and then used to prove itself.

## 8. Delivery programme

Each item is a proposed programme slice. Governance must convert it into a
source-grounded prompt with an exact baseline SHA, changed-path allowlist,
validation commands, disconfirmation probes, rollback, and separate review.

### NPG-00 — Baseline and decision record

- Map the committed PDF-to-ScoreIR-to-GP call graph and every Audiveris entry
  point, dependency, test, document, CI job, container, and script.
- Inspect the supplied architecture analysis and Lesson 5 artifacts.
- Record real Guitar Pro blank-package defaults by supported version.
- Establish sanitized baselines for native and Audiveris paths.
- Decide supported PDF classes and Guitar Pro target versions.
- Publish canonical terminology and the architecture decision.

**Exit gate:** reviewed baseline, provenance map, defaults evidence, and explicit
scope; no product behaviour change.

### NPG-01 — Resolution and provenance contracts

- Add typed conversion parameters, `InstrumentProfile`, evidence provenance,
  and field-local resolver semantics.
- Characterize existing callers and serialized ScoreIR compatibility.
- Test PDF > parameter > default, multi-track targeting, and low-confidence
  conflicts.

**Exit gate:** deterministic, observable resolution that cannot silently discard
a caller value.

### NPG-02 — Canonical evidence boundary

- Introduce `SourceEvidenceIR` or adapt existing evidence models behind one
  stable facade.
- Separate observation from resolution and recognizers from GPIF.
- Preserve approved behavior using characterization and corpus records.

**Exit gate:** all native recognizers emit inspectable evidence with locations
and ambiguity; no recognition expansion is hidden in the refactor.

### NPG-03 — Document topology and track identity

- Consolidate page/system/staff/measure topology.
- Associate paired notation/TAB staves and tracks.
- Extract score metadata, instrument labels, strings, tuning, capo, and
  fretboard properties when explicit.
- Add contradiction diagnostics and parameter fallback.

**Exit gate:** public fixtures and Lesson 5 sanitized metrics prove topology and
field provenance, including missing/ambiguous cases.

### NPG-04 — Rhythm, voices, and navigation

- Recognize meter, tempo, stems, beams, flags, rests, dots, tuplets, voices,
  repeats, endings, and navigation.
- Enforce measure-capacity and pickup rules in the canonical model.
- Remove layout-density timing as an unlabelled success path; retain only an
  explicit approximation mode if governance approves it.

**Exit gate:** exact fixtures pass and unsafe ambiguity refuses with stable,
actionable diagnostics.

### NPG-05 — Pitch, TAB, techniques, and text

- Reconcile clef-aware written pitch with TAB string/fret/tuning/capo.
- Recognize supported articulations, ornaments, guitar techniques, dynamics,
  chord symbols, and lyrics.
- Define explicit degradation behavior for every unsupported feature.

**Exit gate:** cross-representation pitch checks pass, fret assignments are
playable, and support reporting is complete.

### NPG-06 — GP semantic compiler hardening

- Deepen the canonical-score-to-GP boundary and make all ID/reference
  allocation deterministic.
- Expand validation beyond well-formed XML.
- Add versioned target profiles when GP versions differ.
- Add independent parser and Guitar Pro open/resave acceptance harnesses.

**Exit gate:** every supported public golden case passes Levels 1–4 and
deliberately corrupted packages are rejected by the expected validator.

### NPG-07 — End-to-end corpus qualification

- Run the full native pipeline on the public matrix and sanitized private
  corpus.
- Compare source-fact manifests with independently authored GP oracles.
- Classify every mismatch as defect, unsupported feature, ambiguity, or oracle
  problem.
- Establish thresholds per input class; do not hide failures in one aggregate.

**Exit gate:** zero false-success safety violations, accepted external round
trips, and human approval of the capability matrix.

### NPG-08 — Default-path cutover

- Make native PDF recognition the sole supported PDF conversion path.
- Preserve an explicit temporary comparison-only Audiveris path if needed for
  one release window.
- Update CLI/API help, diagnostics, telemetry, installation, and migration docs.

**Exit gate:** clean installation and conversion do not require Java or
Audiveris; rollback is documented and rehearsed.

### NPG-09 — Audiveris retirement

- Delete the Audiveris command, subprocess wrapper, configuration, environment
  detection, dependencies, fixtures, CI paths, containers, and documentation.
- Remove dead MusicXML plumbing only when it exists solely for Audiveris;
  preserve the supported general MusicXML adapter.
- Add negative checks preventing reintroduction of Audiveris/Java dependencies.

**Exit gate:** clean-environment builds and supported conversions pass with no
Audiveris installation, invocation, variable, or documentation dependency; an
independent hard review finds no stranded path.

## 9. Required review strategy

Every implementation slice requires a separate exact-head review. NPG-06
through NPG-09 require adversarial review attempting to disprove:

- fixture independence and external-consumer acceptance;
- source-field precedence and musical equivalence;
- clean-environment independence from Audiveris and Java;
- absence of production-generated test oracles;
- claimed support for private corpus cases.

Review evidence must distinguish “tests passed,” “file generated,” “file
opened,” and “source semantics matched.” None implies the next.

## 10. Retirement gates

Audiveris may be removed only when all are true:

- the supported-input contract is explicit;
- the native path directly converts every supported input class;
- configured fields obey PDF > parameter > default with durable provenance;
- package, GPIF, musical, external, and fidelity gates pass;
- Lesson 5 has a reviewed sanitized semantic comparison;
- clean installation and CI do not require Audiveris or Java;
- CLI/API/docs no longer direct users through Audiveris;
- a rollback release point exists;
- an independent adversarial review approves retirement.

If a gate fails, retire neither code nor comparison evidence. Record the
failure, narrow the supported-input contract if product-appropriate, and return
through governance with a revised bounded slice.

## 11. Risks and countermeasures

| Risk | Countermeasure |
|---|---|
| “Valid GP” is reduced to ZIP/XML | Five validation levels and external round trips |
| PDF text is discarded or assigned the wrong meaning | Semantic text classification, spatial/track relationships, competing candidates, and confidence |
| Defaults overwrite source data | Field-local resolver, provenance, conflict tests |
| Instrument and playback sound are conflated | Separate notation profile from playback metadata |
| TAB contradicts staff pitch | Cross-lane invariant and contradiction diagnostic |
| Golden data is production-generated | Provenance audit and independent oracle |
| Private corpus overfitting | Public feature matrix plus sanitized private smoke |
| Big-bang Audiveris deletion removes fallback | Comparison window and retirement gates |
| Refactor and behavior change become unreviewable | One boundary or capability per PR |
| GP version assumptions drift | Versioned profiles and real-app acceptance records |

## 12. Definition of programme completion

The programme is complete when a clean supported installation converts the
declared PDF classes directly to `.gp` without Audiveris, Java, or mandatory
MusicXML; every resolved optional field has correct precedence and provenance;
the output passes independent structural, musical, application, and
source-fidelity checks; unsupported or ambiguous inputs refuse honestly; and
all Audiveris-specific product and operational surfaces have been removed under
an independently reviewed task.

## 13. Grounded implementation baseline

This section converts the target architecture into work that can be promoted.
It was grounded against product revision
`3aa43b0e13eb7040567c7b76ef4184fade0b0628` on 2026-08-19. The product worktree
was clean when inspected. Promotion must still re-pin the then-current full
SHA; paths and symbols below are planning evidence, not a permanent allowlist.

### 13.1 Existing modules to deepen, not duplicate

| Concern | Existing implementation evidence | Planned seam |
|---|---|---|
| Canonical score | `src/score2gp/ir.py`, `schemas/scoreir.v0.1.schema.json` | Versioned canonical-score interface plus a v0.1 compatibility adapter |
| Native evidence | `notation_omr/*`, `pdf.py`, `pdf_geometry*`, `pdf_tab_*`, `tabraw.py` | One `EvidenceBundle` facade retaining recognizer-specific internal seams |
| Canonical compilation | `scoreir_compiler.py`, `build_ir.py`, `notation_bridge.py` | One compiler interface accepting evidence, resolved options, and policy |
| Timing | `musicxml.py`, `pdf_tab_measure_timing.py`, `pdf_tab_bar_assembler.py` | Rational, meter-derived measure/voice solver |
| GP compilation | `gpif.py`, `gpif_builder.py`, `gp_package.py` | One production GP target profile and independent validators |
| Diagnostics | `diagnostics.py`, `report.py`, recognition outcomes and overlays | Stable result/reason-code contract with field provenance |

Current constraints that the first tasks must characterize rather than assume:

- `Track.instrument` is a free-form string and `Track.capo` is a scalar from
  zero through 24. Tuning is typed, but partial capo and the distinction
  between notation identity and playback sound are not represented at the
  conversion interface.
- `ScoreIR` has global `Bar.events`; voice identity is stored inside
  `Timing`, not owned by an explicit `TrackBar -> Voice -> Beat` hierarchy.
- `Note.pitch` is checked directly against open-string pitch plus fret. Written
  pitch, concert pitch, transposition, and capo semantics need an explicit
  migration contract before this invariant changes.
- `ScoreIRCompiler` currently defaults to one guitar track, standard tuning,
  4/4, 120 BPM, and can create a 3840-tick rest bar. Several PDF timing modules
  and tests also encode 3840 ticks. These are characterization targets, not
  acceptable hidden defaults in the new pipeline.
- The Audiveris runtime surface is concentrated in the `omr` CLI command and
  its contract tests, while Audiveris terminology and assumptions also appear
  in setup/workflow documentation, ScoreIR conversion provenance, MusicXML
  timing fixtures, and historical diagnostics. Retirement must remove runtime
  coupling without deleting useful vendor-neutral MusicXML regression cases.

### 13.2 Supplied Lesson 5 evidence

The new `project-files/` folder contains a diagnostic JSON file, a one-measure
MusicXML file, and a Guitar Pro package, but no source PDF. The files must remain
local and must not be copied into either repository.

| Artifact | SHA-256 | Sanitized observation |
|---|---|---|
| `Lesson-5.json` | `df97fad9b5c9e434ce0826e0477c626f327853338ce6af11ba36530f6ecbfc6d` | Read-only derived diagnostics: 14 semantic candidates, 14 staff-geometry records, 14 timeline records, 488 fret-position ownership records, and 6702 recognition outcomes |
| `Lesson-5.xml` | `f3c9c609be413ec152427807326563e9dee0a1923408f6a20f8880093a8ff35f` | One Guitar part, one 4/4 measure, `divisions=8`, and 43 note/rest elements |
| `Lesson-5.zip` | `57dc217b9aca553beb171db320365d3428fc426b4cb746fe262a1741033ebd32` | GP package with 45 master bars; track declares electric guitar, Clean Strat/MIDI program 27, 12/8, six-string standard tuning, capo 0, partial capo 0, and fret count 24 |

These artifacts disagree structurally and are not interchangeable oracles. The
GP package supplies a reference interpretation; the JSON and XML may be derived
from older Score2GP/Audiveris behavior. NPG-00 must locate the exact PDF, record
its hash and provenance, adjudicate visually whether it corresponds to the GP
reference, and create a field-by-field private manifest before any Lesson 5
claim is used as acceptance evidence.

## 14. Conversion interface and complete field-resolution contract

The external seam should remain small:

```python
convert_pdf(
    source: DocumentRef,
    options: ConversionOptions | None = None,
) -> ConversionResult
```

`ConversionResult` owns the generated package only on success and always owns
the evidence manifest, resolution report, validation results, warnings, and
refusal. CLI flags and future HTTP/job payloads are adapters to the same typed
`ConversionOptions`; recognizers and the GP writer must not read CLI state.

### 14.1 Scope and targeting

Options are unset by default. A track-scoped override uses an explicit selector
(`track_id`, zero-based input index, or exact source label) plus the value.
Selectors resolving to zero or multiple tracks refuse. Global shorthand is
allowed only when the document resolves to one track.

```text
ConversionOptions
├── target: GP target profile and strictness
├── score: missing score metadata and global musical context
├── tracks[]: selector + InstrumentProfile overrides
└── policies: ambiguity, defaults, approximation, and unsupported features
```

The initial public contract must cover these fields:

| Scope | Fields | PDF evidence examples | Parameter/default behavior |
|---|---|---|---|
| Score metadata | title, subtitle, artist, composer, album, transcriber, copyright | title block and labelled text | Parameters fill only missing values; harmless strings may default empty/unknown rather than invent authorship |
| Global timeline | initial meter, meter changes, tempo and changes, key and changes, pickup | notation symbols and tempo text | Parameters may provide missing initial context; changes must be observed or explicitly targeted; strict mode rejects meaning-changing defaults |
| Track identity | name, family, concrete kind, acoustic/electric variant | part label, instrument text, notation conventions | Typed parameter fills missing identity; a generic “Guitar” label does not prove acoustic or electric |
| Staff form | standard notation/TAB visibility, staff count, string count | staff grouping and TAB line count | Derived line count may resolve string count but never concrete instrument/tuning by itself |
| Tuning | ordered open-string sounding pitches and optional name | explicit tuning labels/string labels | Parameter or instrument-profile default fills absence; ordering convention is fixed and reported |
| Capo | full capo fret | explicit “capo” instruction | Parameter/default fills absence; pitch displacement alone is insufficient PDF evidence |
| Partial capo | fret plus exact affected-string bitset/map | explicit partial-capo diagram/text | No inference from ordinary pitches; parameter or none |
| Fretboard | maximum/playable fret count | explicit instrument specification, if any | Parameter/profile technical limit fills absence |
| Per-note guitar position | string and fret number | TAB line and fret token | This is musical content, never a global default. Missing positions are solved from pitch/tuning/capo or refused when ambiguous under policy |
| Pitch roles | written pitch, concert pitch, transposition | clef/key/accidental plus instrument convention | Instrument-profile transposition applies only after identity resolution and remains provenance-bearing |
| Playback | MIDI program/bank/channel, sound label/path, percussion mode | explicit source direction only when semantically clear | Parameter/profile supplies playback choice; playback must not change notation identity |
| Layout intent | track order, TAB visibility, optional view hints | staff order and document layout | Parameters may fill presentation only; unsupported cosmetics degrade explicitly |

### 14.2 Resolution algorithm

For every field independently:

1. Collect all PDF candidates with evidence references and confidence class.
2. Reject candidates failing the field's admissibility rule; retain rejection
   reasons in the report.
3. If one explicit, sufficiently confident candidate remains, resolve from
   PDF even when it differs from the parameter.
4. If multiple materially conflicting qualified candidates remain, refuse or
   return explicit correction candidates. After a caller correction, rerun the
   same resolver with that correction recorded as provenance. Do not pick an
   unrelated parameter merely to suppress conflict.
5. If no qualified PDF candidate remains, use the exactly targeted caller
   parameter when present.
6. Otherwise apply the versioned profile default when the selected policy
   permits it; strict mode refuses meaning-changing defaults.
7. Validate cross-field consistency, then record value, source, evidence,
   policy version, alternatives, and warnings.

Confidence is not a universal numeric threshold. Each field owns an
admissibility rule. For example, explicit `Capo 3` text associated with a track
can qualify; a classifier's weak acoustic-guitar guess cannot override an
explicit electric-guitar parameter.

### 14.3 Instrument profiles and provisional product defaults

Define named, versioned profiles rather than scattering literals. The first
profile catalogue should include at least steel-string acoustic guitar,
electric guitar, four-string electric bass, and a custom fretted instrument.
Each profile bundles identity, tuning, string count, transposition, clef/staff
defaults, fret ceiling, and playback defaults, while allowing field-level
overrides and provenance.

The programme's fallback profile remains provisionally steel-string acoustic
guitar, standard six-string E2-A2-D3-G3-B3-E4, no capo, no partial capo, and a
24-fret technical ceiling. Meter 4/4, tempo 120 BPM, and neutral key are
separate musical defaults. These are Score2GP policy proposals, not assertions
about Guitar Pro. Of these, only 4/4, neutral C-major key, and the name
“standard guitar tuning” have related official documentation; that still does
not make the whole profile a fixed Guitar Pro template. NPG-00 must replace or
approve the proposals using Guitar Pro-created blank-package evidence,
supported-version observations, and corpus needs.

## 15. Executable dependency graph

```text
NPG-00 baseline/defaults/source manifest
  -> NPG-01 option + resolver contracts
  -> NPG-02 evidence facade
       -> NPG-03 topology + track properties
       -> NPG-04 rhythm/voices/navigation
       -> NPG-05 pitch/TAB/techniques/text

NPG-01 + canonical invariants
  -> NPG-06A canonical vNext + v0.1 adapter
  -> NPG-06B deterministic GP semantic compiler
  -> NPG-06C package/referential/musical validators
  -> NPG-06D external application acceptance harness

NPG-03 + NPG-04 + NPG-05 + NPG-06D
  -> NPG-07 corpus qualification
  -> NPG-08 native default cutover
  -> NPG-09 Audiveris runtime and documentation removal
```

NPG-03 through NPG-05 may proceed as bounded vertical slices after the evidence
and resolver interfaces stabilize. NPG-06A can be developed in parallel with
recognition work, but production cutover cannot occur until one end-to-end
slice uses it. NPG-09 is strictly last.

## 16. Promotion-ready work breakdown

Each row is one independently reviewable task or small PR. Governance must
create the exact prompt, baseline, allowlist, commands, and reviewer identity.

| ID | Objective and principal deliverable | Depends on | Required disconfirmation / exit evidence |
|---|---|---|---|
| NPG-00A | Pin a clean baseline and inventory every PDF, Audiveris, MusicXML, canonical, GPIF, package, test, documentation, dependency, environment, and CI path | none | A repository-wide search and call graph account for every executable Audiveris/Java route; historical fixture names are classified separately from runtime dependencies |
| NPG-00B | Build a sanitized Lesson 5 field manifest from the source PDF, JSON, XML, and GP package | 00A and source PDF | Human-reviewed page/measure/track map; disagreements are recorded without declaring generated JSON/XML an oracle |
| NPG-00C | Record blank-score/blank-track packages from each supported Guitar Pro version and approve Score2GP defaults v1 | 00A | Raw local packages, hashes, extraction script/report, and cross-version diff; undocumented behavior is labelled observed, not guaranteed |
| NPG-00D | Approve ADR, glossary, supported born-digital input classes, target GP versions, refusal posture, and capability matrix | 00A–00C | Every support claim has a fixture/oracle and threshold; scanned input remains explicitly unsupported or separately gated |
| NPG-01A | Add typed `ConversionOptions`, track selectors, strictness and target-profile options without changing current conversion output | 00D | Serialization, CLI mapping, unset-vs-zero tests, invalid/ambiguous selector tests |
| NPG-01B | Add versioned `InstrumentProfile` catalogue and custom profile validation | 01A | Acoustic/electric/bass/custom tests; tuning length, string numbering, transposition, capo, partial-capo, and fret-range contradictions reject |
| NPG-01C | Implement a pure field resolver and resolution report | 01A–01B | Table-driven PDF > parameter > default tests for every field; conflicting strong PDF evidence refuses; input objects remain unchanged |
| NPG-02A | Specify `SourceEvidenceIR` identities, locations, confidence classes, alternatives, relationships, and schema version | 00D | Round-trip schema tests; unknown/ambiguous/unsupported are not collapsed into missing |
| NPG-02B | Adapt current PDF text, TAB, geometry, and native notation outcomes to the evidence facade | 02A | Characterization parity plus source-to-evidence trace; text retains semantic candidates beyond fret tokens; no GPIF or resolution policy enters recognizers |
| NPG-03A | Produce page/system/staff/track topology and pair notation/TAB staves | 02B | Multi-system/multi-track, orphan-staff, false-pairing, and ambiguous-pairing fixtures with overlays |
| NPG-03B | Produce observed/rejected/inferred/repaired barline candidates and a global measure grid, with causal failure classification and correction candidates | 03A | Stem/bracket negatives, fragmented/missing geometry repair cases, system-edge cases, multi-staff alignment, deterministic ordering, and Lesson 5 private overlay; fixtures prove repair is bounded and does not widen tolerances globally |
| NPG-03C | Extract track labels, instrument candidates, string count, tuning, capo/partial capo, and explicit fretboard constraints | 03A, 01C | Acoustic/electric/bass/capo/partial-capo/missing/conflict matrix; no six-line-TAB-to-acoustic shortcut |
| NPG-04A | Replace fixed 4/4/3840 capacity with one rational meter utility and characterize legacy behavior | 01C | 4/4, 12/8, cut time, pickups, meter changes, exact/non-exact TPQ tests; repository search finds no unapproved capacity literal |
| NPG-04B | Add explicit canonical master measures, track bars, voices, beats, rhythms, and a v0.1 adapter | 04A | Monophonic compatibility, two voices, chords, rests, empty voice slots, deterministic IDs, and declared adapter loss report |
| NPG-04C | Implement rhythm hypotheses and a bounded measure/voice solver for stems, beams, flags, rests, dots, and tuplets | 02B, 03B, 04B | Exact fill/non-overlap properties, runner-up ambiguity, search-limit refusal, and no silent layout-density success |
| NPG-04D | Add repeat barlines, endings, tempo/meter/key changes, and navigation relationships | 03B, 04C | Hand-authored semantic fixtures and malformed-cycle/refusal cases |
| NPG-05A | Separate staff/written/concert/MIDI pitch and implement clef/key/accidental/transposition state | 04B | Guitar octave, bass, accidental carry/reset, key change, and MusicXML semantic round-trip tests |
| NPG-05B | Reconcile TAB positions and pitch; add capo-aware, chord-aware bounded fingering solver for missing positions | 03C, 05A | Source TAB wins, capo equation holds, no same-string chord collision, maximum-fret and low-margin ambiguity cases |
| NPG-05C | Attach chord symbols, lyrics, dynamics, articulations, ornaments, and supported guitar techniques | 04C, 05B | Capability table maps every recognized feature to exact preservation, declared degradation, or refusal |
| NPG-06A | Replace process-state/test-dependent GPIF behavior with one explicit production target profile | 04B | Production CLI and tests invoke the same serializer profile; environment/pytest presence cannot change semantic output |
| NPG-06B | Build deterministic MasterBar/Bar/Voice/Beat/Note/Rhythm allocation and GP semantic mapping | 05A, 06A | Referential graph validator, deterministic permutation tests, rests/chords/polyphony/multi-track cases, unsupported-feature report |
| NPG-06C | Harden package writer and independent Levels 1–3 validators | 06B | Corrupt ZIP paths, XML, duplicate/dangling/orphan refs, timing, pitch, capo and fret packages fail at the intended layer |
| NPG-06D | Establish supported Guitar Pro open/save/reopen and independent-parser harness | 00C, 06C | Captured application version, input/output hashes, repair-dialog result, normalized semantic diff, and no production-generated expected oracle |
| NPG-07A | Build the redistributable feature corpus and independently authored fact manifests | 00D | Fixture licensing/provenance audit and coverage across instruments, metadata, structure, ambiguity, and techniques |
| NPG-07B | Run per-input-class native qualification plus sanitized private qualification | 03–07A | Per-field precision/recall/fidelity and refusal metrics; zero false-success safety violations; no aggregate hides a failed class |
| NPG-08A | Route supported PDF classes to native conversion by default and retain comparison-only Audiveris behind an explicit temporary option | 07B | Clean native install converts without Java; unsupported classes refuse; rollback release point and differential evidence exist |
| NPG-08B | Migrate CLI/help/setup/workflow/telemetry to the supported native contract | 08A | Fresh-user rehearsal contains no mandatory sidecar/Audiveris step and reports parameters/default provenance clearly |
| NPG-09A | Remove Audiveris executable discovery, subprocess command, configuration, manifests, operational tests, packaging, and Java requirements | 08B | Clean-environment installation/test/conversion plus negative dependency/search checks; MusicXML import still passes independently |
| NPG-09B | Remove or rename stale Audiveris-only documentation/provenance while preserving vendor-neutral regression semantics | 09A | No user-facing Audiveris promise or stranded field; useful fixtures are renamed only with evidence and history preserved |
| NPG-09C | Independent exact-head adversarial retirement review | 09A–09B | Reviewer attempts runtime invocation, dependency reintroduction, oracle-coupling, unsupported-input false success, and source-precedence violations |

## 17. Validation commands and evidence contract

Exact commands depend on the promoted baseline, but every task prompt must
select from this minimum contract and record command output, revision, dirty
state, executable/import path, fixture hashes, and test counts:

```bash
python -m pytest <focused tests for the changed seam>
python -m pytest tests
python -m ruff check src tests
python -m mypy src/score2gp
python -m score2gp.cli validate-ir <fixture.ir.json>
python -m score2gp.cli inspect-gp <generated.gp>
```

If a command is unavailable on the baseline, the first relevant task must add
or document the equivalent; a prompt must never claim it ran. GP application
acceptance is a separate controlled protocol, not a unit-test checkbox.

Each task handoff must include:

- exact source and output hashes;
- product and agentops revisions and dirty-state disclosure;
- changed-path list and schema/interface changes;
- focused, full-suite, static-analysis, and negative-test results separately;
- public fixture provenance and private-safe aggregate evidence;
- capability/default/degradation changes;
- unresolved risks, rollback, and the next gate.

## 18. Cutover scorecard

Governance must set numeric thresholds in NPG-00D. Until then, “mostly
equivalent” is not a pass criterion. The scorecard must report each supported
input class and each field family separately:

| Gate | Required evidence before native default | Required evidence before deletion |
|---|---|---|
| Source classification | Supported/unsupported classes correctly identified; unsupported inputs refuse | Same in clean installation with no Audiveris detection |
| Metadata and track properties | Exact match or approved default provenance for instrument, variant, tuning, strings, capo/partial capo, fret ceiling, and playback profile | No regression across public and private-safe corpus |
| Topology and timing | Adjudicated systems/measures/tracks/voices; every accepted voice satisfies meter/pickup rules | Native-only run passes thresholds and Lesson 5 no longer collapses to one bar |
| Notes and techniques | Per-field pitch, onset, duration, string/fret, text, and technique metrics | All release-supported features pass; unsupported features refuse or degrade as declared |
| GP validity | Package, reference, musical, and independent-parser validation | Supported Guitar Pro versions open/save/reopen without repair or critical semantic loss |
| Safety | Zero false-success cases in qualification corpus | Adversarial clean-environment review finds no fallback or hidden Java/Audiveris path |

The cutover decision must link to evidence for every cell. A generated `.gp`, a
passing ZIP/XML check, or an Audiveris differential alone cannot satisfy it.

## 19. External-source constraints

- Arobas states that Guitar Pro 8 cannot convert PDF files into Guitar Pro
  files. Native PDF recognition is therefore Score2GP-owned behavior, not an
  invocation of a hidden Guitar Pro importer: [official PDF support
  statement](https://support.guitar-pro.com/hc/en-us/articles/19237871925021-GP8-Can-I-convert-a-PDF-file-into-a-Guitar-Pro-file-with-Guitar-Pro-8).
- Arobas documents `.gp` as the current Guitar Pro format and lists supported
  legacy/import formats, but publishes no complete `.gp`/GPIF writer schema,
  supported writer SDK, or headless package validator: [official Guitar Pro
  features and formats](https://www.guitar-pro.com/c/14-guitar-pro-features).
- The official manual's “Check Bar Duration” behavior makes open/import plus
  bar-duration inspection a useful first-party acceptance step: incomplete
  bars are reported as false rhythm, and notes exceeding bar duration are not
  played. This does not replace semantic source comparison.
- alphaTab documents a GP7+ exporter and describes the modern `.gp` container,
  but it is a third-party, reverse-engineered implementation, not an Arobas
  specification. It may provide an independent parser/export experiment, never
  the sole validity oracle: [alphaTab exporter
  documentation](https://alphatab.net/docs/guides/exporter).

These sources justify empirical target-version profiles and real-application
acceptance. They do not justify copying opaque package values from one example
or calling Score2GP's product defaults “Guitar Pro defaults.”
