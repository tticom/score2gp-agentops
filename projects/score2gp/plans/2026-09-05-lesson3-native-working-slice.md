# Native Score2GP requirement and Lesson 3 working slice

Status: maintainer-requested requirement and delivery plan; implementation
promotion pending. Date: 2026-09-05. Immediate milestone: L3-NATIVE.

## 1. Authority and settled direction

The maintainer requested a plan for one working native slice using
`Lesson-3.pdf`, with the full ultimate requirement preserved. Audiveris has
been evaluated and does not meet this project's needs; no suitable third-party
recognition replacement was found. Building Score2GP's own recognition is the
settled direction. This programme is not a vendor-selection exercise.

This document specializes the
[native PDF-to-GP programme](2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md)
and makes Lesson 3 the first proof source, ahead of the earlier Lesson 5 golden
case. It changes delivery order, not the ultimate capability requirement.
Low-level PDF parsing/rendering libraries remain tools, not outsourced musical
recognizers. Independent output readers are validators, never generators.

This planning task does not implement product changes, retire runtime code,
close PRs, or replace `ORCHESTRATION_STATE.json.task`. REC-04 / product PR #459
is still active. On its explicit disposition, governance should promote the
[L3-00 prompt](../prompts/next/l3-00-native-source-contract-and-acceptance.md)
instead of automatically advancing the generic REC sequence. Do not interrupt,
merge, or discard REC-04 under authority of this document.

## 2. Ultimate product requirement, preserved in full

Score2GP must read supported born-digital music PDFs and produce editable,
semantically faithful Guitar Pro `.gp` files through its own recognition and
compilation pipeline, without Audiveris, Java, or a mandatory MusicXML sidecar.
The PDF supplies musical truth. The product must preserve the following:

| ID | Ultimate obligation | Lesson 3 application | Later qualification |
|---|---|---|---|
| U01 | Standard notation, TAB, and paired notation/TAB input classes | Paired staves across the complete source | Notation-only, TAB-only, other engraving/layout families |
| U02 | Pages, systems, reading order, tracks, logical measures, voices, pickups, cross-page continuation | All source pages and measures; distinguish physical divisions from measures | Multi-track, multi-instrument, irregular and fragmented layouts |
| U03 | Exact notes, rests, pitch, onset, duration, dots, ties, tuplets and chord simultaneity | Every feature present, including rests, sustained/dotted rhythms and final chords | Further rhythms, polyphony, ties/tuplets where absent here |
| U04 | Observed string/fret assignments and source fingering | Read single/multi-digit frets and every chord member | Other fretboard layouts and instruments; never replace observed fingering with optimization |
| U05 | Instrument identity/variant, strings, tuning, capo, partial capo, transposition and stated fret limits | Extract expressed properties; explicitly resolve absent ones | Bass, acoustic/electric variants, other string counts and partial capo |
| U06 | Tempo, meter, key and local changes | Extract the printed evidence rather than infer from exercise titles | Changes within a score, compound meters and other keys |
| U07 | Titles, credits, track labels, section/chord labels, lyrics and navigation text | Preserve source title/credits and instructional section labels; timestamps remain label text | Lyrics, harmony and other text semantics absent from this source |
| U08 | Articulations, guitar techniques, ornaments, expressive notation and playback meaning | Preserve observed rolled/arpeggiated chords and any other adjudicated source technique | Bends, slides, vibrato, harmonics, grace notes and other absent techniques |
| U09 | Repeats, endings, barline kinds and navigation relationships | Preserve present ordinary/double/final divisions and section structure | Repeat loops, alternate endings, coda/segno and other absent navigation |
| U10 | Field-local resolution: qualified PDF evidence > explicit caller parameters > versioned defaults | Every resolved property records its origin; absent playback details may default | Track-scoped parameter targeting and conflict handling across instruments |
| U11 | Evidence, uncertainty, bounded repair/reconciliation and correction before refusal | Preserve observations and alternatives; diagnose source conflicts without fabrication | General correction workflow and graphical editor |
| U12 | Canonical musical document independent of PDF technology and GPIF | Compile typed resolved data to the existing production ScoreIR | Additional acquisition modalities and optional MusicXML interoperability |
| U13 | Deterministic semantics, complete GP reference graph, independent parsing and real application acceptance | Required at the first complete slice | Additional explicitly supported Guitar Pro versions |
| U14 | Privacy, repeatable evidence, capability-specific qualification and honest refusal | Private artifacts stay local; one-source success is labelled one-source success | Held-out public/private corpus and per-input-class release thresholds |

Native recognition replacement is mandatory. Audiveris may remain dormant in
old code until removal is separately validated; it must not execute in the L3
path, contribute recognition evidence, or be required for its acceptance.
MusicXML import remains an optional interoperability feature, not an input
requirement for this goal. Audio/video transcription, cloud delivery and billing
are separate programmes. Universal scanned/handwritten/photo support remains
outside the initial product claim, without constraining future acquisition.

## 3. Immediate goal and exact meaning of done

From the original complete `Lesson-3.pdf`, one reproducible production CLI run
must produce a Guitar Pro file containing the complete source score, with
correct musical semantics and editable notation/TAB. It must open, play through,
save, close and reopen in the declared supported Guitar Pro application without
a repair dialog or material semantic loss. No manual editing of the resulting
GP or per-note transcription input may be used to obtain this milestone.

One working slice means one source document through the entire native product,
not one detector, schema, successful page, or generated package. First-system
and first-page results are intermediate checkpoints only. No claim of broad
PDF support follows from Lesson 3 success.

### Source binding and observed baseline

Planning inspected these immutable baselines:

- Product: `16cba3a41dc831cf0b44a3b44a205e8c095a3cb6`.
- AgentOps base: `1d428ee782a6465e8ff5eb916979848d470d1972`.
- Installed workflow skills: `439404f7342f4e324147efb6b0276f698fbf2bdb`.
- Approved PDF: sibling private-fixture repository, `fixtures/private/Lesson-3.pdf`.
- PDF SHA-256: `fbd44cefad9e33adac992a5bd73c5cc46202c7cfc64d0586bb94cf42d3b41004`.
- Candidate reference: the same fixture directory's `Lesson-3.gp`.
- GP SHA-256: `9e1ca7b682ecce6b401da83820020650b8a3c122807c51b37029dc441c36516d`.

Direct PyMuPDF inspection and visual inspection of all four rendered pages
confirmed four 612 x 792 point pages with extractable text/vector paths. Page
drawing counts were 343, 495, 458 and 286; no embedded images were reported by
`get_images()`. These are acquisition observations, not recognition accuracy.
The visible score includes paired notation/TAB, section labels, multi-digit
frets, rests, beamed notes, whole/half/dotted rhythms and rolled chords. The
first system includes a sustained note after beamed runs; do not choose only
the repeated easy rhythm for the first demonstration.

A separate standard-library XML traversal of the reference's
MasterBars -> Bars -> Voices -> Beats -> Notes links counted 66 master bars,
465 beat occurrences, 473 note occurrences, two rest occurrences and two chord
occurrences. There are only 94 Beat definitions and 30 Note definitions because
records are reused. Counting XML definitions is not counting performed events.
These aggregates are provisional reference observations, not an adjudicated
oracle. They must be reconciled with the PDF before becoming expected results.
No pitches, transcription, glyph coordinates or expected event lists belong
in this public planning record.

At the pinned product head the complete PDF-only CLI run, both strict and
non-strict, exited 4 with `pdf_only_tab_grouping_unsafe`, caused by
`pdf_bar_box_construction_not_enough_for_build_ir`; no GP was written.
Earlier pass reports and different historical counts are not current evidence.
Neither suppressing that warning nor matching 473 extracted candidates proves
source fidelity. The current PDF-only assembler also uses event-count/grid
timing and remainder rests, which cannot satisfy this native goal unchanged.

Reproduce the baseline from the product root with an explicitly fresh ignored
output directory (create `work/l3-baseline` only if unused):

```bash
.venv/bin/python -m score2gp.cli convert \
  --pdf ../score2gp-private-fixtures/fixtures/private/Lesson-3.pdf \
  --pdf-only-tab --strict \
  --out work/l3-baseline/result.gp \
  --work-dir work/l3-baseline/intermediates \
  --json-report work/l3-baseline/report.json
```

### Final acceptance contract

| Gate | Required observable result |
|---|---|
| Generation inputs | Original PDF, declared non-musical configuration/defaults and production code only; no reference GP, reference-derived facts, sidecar timing, pretranscribed notes or fixture identity lookup |
| Whole-document coverage | Every adjudicated source page/system/measure accounted for exactly once; no dropped or invented musical material; 66 measures is provisional until source-pair adjudication |
| Musical fidelity | 100% exact match for adjudicated source note/rest occurrences, string/fret, sounding pitch, rational onset/duration, chord membership, dots and present techniques; no aggregate permits a wrong measure to pass |
| Structure and text | Exact source-supported meter/key/tempo, section order and labels, barline/navigation meaning, title/credit/track properties; compare text with explicitly documented whitespace normalization only |
| Defaults | Only genuinely absent facts may default; every such field has policy/version provenance; no defaulted or layout-inferred rhythms in a successful Lesson 3 result |
| Uncertainty | Zero unresolved musical ambiguities or silently omitted source features in the final artifact; unresolved cases produce a located diagnostic and a non-success result |
| Compilation | No note clamping, partial-chord loss, order-dependent durations, invented padding, semantic scaling or inferred measure fabrication |
| Output validity | ZIP/XML plus complete unique/reachable GP references, valid timing and independent semantic parsing; package existence is a separate channel |
| First-party acceptance | Pinned Guitar Pro version opens, plays, saves and reopens without repair or material source-semantic change; full playback and visual inspection of all pages, including sustained/rest/dotted/chord cases |
| Reproducibility | Same PDF/configuration/version yields identical normalized semantics on two clean runs; record artifact hashes even if ZIP timestamps differ |
| Isolation | Generation environment cannot read the reference directory or oracle manifests; mounting only a renamed PDF still produces identical semantics |

The existing general >90%/>95% fret/string thresholds do not define completion
for this deliberately bounded first source. Byte-identical GP files, identical
pagination, typography and proprietary sound presets are not required. Source
section/system organization must remain inspectable; any cosmetic reflow is
reported separately from musical fidelity. An unverified application check is
`NOT_EVALUATED`, never a pass.

Normalize comparison independently of storage IDs: logical measure order,
track/voice identity, rational quarter-note offsets/durations, ordered event
occurrences and unordered chord membership. Record GP-to-IR string-numbering
and written-to-sounding-pitch conventions explicitly. Distinguish a scored
chord onset from its arpeggiated playback spread. Compare only PDF-expressed
properties against the source oracle; hidden GP playback settings are not
PDF facts and are checked against the declared defaults instead. Cosmetic
normalization must never merge distinct notes, rhythms, techniques or sections.

## 4. Technical approach and evidence status

Use native vector/text acquisition first on this vector-rich source, with
rendered crops as inspection evidence and bounded raster analysis only where
a specific glyph cannot be resolved from extracted geometry. Do not build a
general raster subsystem before identifying a Lesson 3 need.

```text
original PDF -> immutable observations -> provisional paired-staff topology
             -> TAB tokens + notation rhythm/expressive hypotheses
             -> bounded joint resolution -> typed MusicalDocument
             -> strict ScoreIR mapping -> existing GP writer -> result.gp

separate validator: result.gp + source-adjudicated oracle -> exact comparison
separate application check: result.gp -> open/play/save/reopen -> comparison
```

1. Reuse `recognition/observations.py` and `recognition/schemas.py`. Verify
   character-level boxes before relying on merged text spans for multi-digit
   frets. Acquire glyphs, paths, stroke width/fill and source transforms without
   assigning music at this stage.
2. Recover local staff/string scales and paired regions. Reuse REC-04 only
   after its reviewed merge and relevant source checks. Pair by local layout
   evidence; retain alternatives around fragmented lines, stems, brackets and
   double/final boundaries. A physical vertical path is not automatically a
   measure boundary. Never use page-global snapping tolerances.
3. Retain provisional measure boundaries while rhythmic and paired-lane
   evidence is evaluated. Observations stay immutable; interpretations may
   change with an explicit derivation. Only resolved topology is locked.
4. Recognize TAB glyphs and competing concatenations using character geometry
   and local spacing, then string ownership. Read rhythm from notation
   noteheads, stems, beams, flags, rests and dots; do not distribute duration
   by event count or horizontal distance. Treat simultaneous pitches as chord
   members, and preserve rolled-chord direction rather than splitting a chord
   into arbitrary sequential beats.
5. Align the paired lanes within provisional measures using ordered candidate
   relations and notation evidence. Resolve duration/voice/ownership jointly
   under exact rational timing. Bar capacity rejects impossible solutions but
   cannot select between multiple source-plausible rhythms. Search must have
   a measured bound; exhaustion is reported distinctly from contradiction.
6. Produce the existing typed MusicalDocument and map it explicitly to
   `score2gp.ir.ScoreIR`. Add only source-required missing typed fields, with
   schema/serialization tests. Do not introduce another canonical score model
   or adopt the disconnected sibling-core model during this slice.
7. Reuse `gp_package.write_gp` and its writer, fixing only demonstrated
   Lesson 3 preservation/compatibility defects. Use an independent GP reader
   in validation; a separate implementation must not import the production
   writer/parser to generate its expected answers. No exporter rewrite or
   replacement recognizer procurement is part of this plan.

The new native route must not inherit `build_ir_from_tabraw_only`'s timing
approximation or unconditional precise-timing refusal. Proposed final CLI
contract uses existing flags, after implementation:

```bash
.venv/bin/python -m score2gp.cli convert \
  --pdf <original-pdf> --pdf-only-tab --require-precise-timing --strict \
  --out <fresh-output>/result.gp --work-dir <fresh-output>/intermediates \
  --json-report <fresh-output>/report.json
```

This command is a target contract, not a claim that current code supports it.
Select the route by observable input capability, never basename/hash/page
number. Existing draft behavior remains separately labelled. A failure may
retain diagnostics but cannot leave a stale/partial file at the success path.

### Claim and reference ledger

| Claim | Evidence and location | Classification and limitation |
|---|---|---|
| Vector/text is available on this source | Direct all-page inspection above; `recognition/observations.py:observe_pdf` | Verified acquisition; semantic recognition still unproven |
| PDF primitives can be read without interpreting music | PyMuPDF project, [Page API](https://pymupdf.readthedocs.io/en/latest/page.html), `get_drawings`, `get_text`; [TextPage API](https://pymupdf.readthedocs.io/en/latest/textpage.html), `extractRAWDICT` | External direct API evidence: paths and character data, not a musical oracle |
| Existing interfaces can carry recognized music | `recognition/schemas.py:MusicalDocument`; `ir.py:Event`, including arpeggio fields | Verified source interfaces; complete field mapping is an implementation obligation |
| Current assembly is not precise native timing | `build_ir.py:build_ir_from_tabraw_only`; `pdf_tab_bar_assembler.py:assemble_pdf_tab_bar` | Verified source behavior; bypassing a refusal does not implement recognition |
| Reference records must be expanded | Direct reference XML link traversal above | Verified aggregates; full source-pair equivalence remains to adjudicate |
| A bounded vector-led recognizer can cover this document | Visible evidence and reuse seams above | Hypothesis to falsify at the first-system checkpoint, not established feasibility of the whole score |

Architect outcome B applies only to the bounded vector/text-led route and
first experiment: raster-first replacement is not justified for this source
while readable vector/text evidence is available. This is not a claim that
raster recognition is impossible. No full-score recognition approval is
implied. If a necessary symbol has insufficient vector evidence, compare a
bounded crop recognizer with vector reconstruction and record A/B/C for that
specific blocker. The response to failure stays within native capability.

## 5. Delivery sequence: one vertical goal, measurable checkpoints

These are milestone checkpoints, not independently executable task authority.
Each promoted implementation PR changes one external module seam; the work
continues toward the same full-document outcome. Carry the last passing
end-to-end example into every subsequent check.

| Checkpoint | Required new evidence/capability | Continue condition | Scope boundary |
|---|---|---|---|
| L3-00: Source contract and red acceptance | Adjudicated private feature/semantic manifest, independent reference expansion, red native CLI acceptance, exact first divergence on the first system | A fixed, discriminating oracle and a bounded first topology/token task; existing layout refusal alone is not a new result | Validation seam; no recognizer or compiler behavior changes |
| First complete system | Original page context -> resolved first system including its sustained ending -> GP -> independent comparison | Exact system semantics and an early Guitar Pro compatibility check | Minimal topology, token, rhythm, compiler seams, promoted separately only as necessary |
| Feature-complete first page | First page through the same CLI path, including multi-digit frets and section boundaries | All adjudicated page-one semantics exact; first-system result retained | Expand evidence coverage, not a second pipeline |
| Complete four-page document | Carry page continuity and all present rest/dotted/chord/expressive cases through the same path | Every measure exact; no unresolved feature exclusions | Remaining Lesson 3 features only |
| L3-NATIVE acceptance | Repeat clean isolated generation, independent comparison, full application open/play/save/reopen and adversarial review | All final gates pass at the exact reviewed head | Qualifies Lesson 3 only; broader release and Audiveris deletion remain separately gated |

Before the first-system implementation, L3-00 must pin its exact source-region
identity in the private manifest. Page/region selection is a test control, not
production fixture knowledge. At full-document acceptance no crop, `--pages`,
skip-system, no-strict or editable-draft option is allowed.

### Anti-overfitting and adversarial controls

- Rename/move the input and strip non-musical file metadata: identical music.
- Uniformly translate/scale the rendered coordinate system and permute input
  observation order: unchanged semantics under the documented transform.
- Distinguish adjacent digits from one multi-digit fret, notes from page/bar
  numbers, dots from irrelevant marks, and stems from measure divisions.
- Remove one required chord ownership relation or change one member duration:
  fail or preserve explicit ambiguity, never silently drop/select a member.
- Change reference pitch, onset, duration, rest, chord member, dot, arpeggio,
  tempo, key, section order or final barline: the relevant oracle layer fails.
- Wrong/missing/aliased reference, missing source, stale output and inaccessible
  corpus must fail the acceptance harness, not skip to green.
- Unknown feature and exhausted hypothesis search yield located refusal;
  neither can be replaced by a confident default.
- Reused GP definitions are expanded in order and references are validated;
  duplicate IDs, dangling references and missing beats cannot pass.

Transformed real-source inputs remain real-source derivations with provenance;
synthetic cases are supporting algorithm tests. Lesson 3 is openly the
development source, not a held-out test. Other approved PDFs can expose
regressions without becoming a prerequisite for this first-source milestone.
Claims of general recognition capability require distinct sources later.

## 6. Decisions, budgets and failure handling

Every checkpoint begins with a measured baseline and an exact expected delta.
One bounded cycle may collect missing decisive evidence. A second cycle on the
same blocker must test a different named hypothesis or change product behavior.
After two cycles without that delta, stop the failing approach, record the
counterexample and choose the smallest native alternative at that seam. Do
not restart architecture discovery for the whole programme or reopen Audiveris.

Source/reference disagreement is resolved against the visible PDF and, when
musically ambiguous, the maintainer. Keep the disagreement localized: other
unambiguous source regions can continue. Do not silently edit the reference,
modify acceptance to match generated output, or claim the whole slice is done.
Missing GP application access blocks only its acceptance receipt while other
work continues; final completion remains unavailable until that receipt exists.

Optional user corrections are part of U11 but not a way to pass this initial
automatic Lesson 3 goal. Developer annotations stay oracle-only. If manual
musical corrections prove unavoidable, record the evidence and request an
explicit milestone change; do not quietly redefine a working native converter.

## 7. Ownership, verification and handoff

- Architect: source contract, hypothesis/evidence mapping, smallest changed
  seam, bounded experiment and stop/continue decision.
- Developer: requirement-driven implementation and production-path tests on
  the promoted branch; no access to reference-derived inputs during generation.
- Independent reviewer: explicitly use `devils-advocate-review`, replay original
  counterexamples and attack oracle contamination, partial success, semantic
  loss and fixture coupling. Publish exact-head evidence in the PR.
- Maintainer: adjudicate genuinely ambiguous musical/source facts, perform or
  witness Guitar Pro application acceptance, and authorize merges.
- Governance: resolve PR #459, promote L3-00 through the single machine authority,
  then promote only the smallest evidence-backed seam. Reuse REC-02/03 and
  accepted REC-04 work; pull REC-06..13 portions forward as demanded by the
  slice. Generic REC-05..14 ordering is deferred, not deleted or marked done.

Record product/AgentOps/skills heads, executable/import path, dependency
versions, input/config/output hashes, exact command/exit code and independently
read results. Keep recognition fidelity, generation status, structural
validation, independent semantic validation and GP application acceptance as
separate fields. Expected manifests and source coordinates stay private.

For each product change run focused tests, required repository verification,
artifact audit and diff/schema checks. Recognition changes require actual
source-bearing assertions. Full-suite failures must be classified and cannot
be relabelled passes. A validator failure does not permit oracle weakening.
Schema export checks should write to a temporary comparison directory where
possible, rather than mutate tracked schemas during review.

Durable authority is this requirement plus the promoted prompt/state; exact
implementation receipts and review verdicts belong on the PR. No raw private
artifact or copied musical transcription may enter governance or product Git.

Planning handoff: this is a separate architect-authoring task requested after
the workspace review. It captures requirements and proposed sequencing only.
Product implementation, full source-pair adjudication, independent application
acceptance and full-corpus qualification have not been performed by this plan.
The next product action is L3-00 after governance promotion, not an inferred
permission to start the rest of the checkpoints.

Local planning branch: `codex/lesson3-native-working-slice-plan`, based on the
AgentOps SHA recorded above. The captured scope is this plan, the L3-00 prompt,
and pointers in `ACTIVE_PLAN.md` and `PLANNING_DATA.md`. No feature-branch remote
or planning PR has been published in this authoring task. Product and machine
authority are unchanged. The local commit containing these paths is the exact
planning handoff revision; implementation must repin live state on promotion.
