# MusicXML Sidecar Generation Alternatives Research Plan

## Decision Required

Select a reproducible way to create a non-empty, timing-safe MusicXML sidecar
for Score2GP's born-digital standard-notation and mixed notation/TAB PDFs, or
record that no evaluated route is currently suitable. This plan authorises
research and evidence collection only. It does not authorise a new production
dependency, private-file upload, product integration, model training, or a
claim of musical correctness.

## Progress Baseline

- FS-03E established that Audiveris 5.7.0 produced structurally valid MXL
  archives with parts and measures but zero `note`, `pitch`, and `rest`
  elements for the two public paired notation/TAB fixtures. No Score2GP-side
  event loss was observed because the sidecar was already empty.
- FS-03F established that the existing explicit `convert --musicxml` route
  works with a valid public sidecar: 8 ScoreIR events and 6 matched playable
  TAB candidates reached `gp-write`.
- The project therefore needs a sidecar-generation decision, not another test
  of whether a valid supplied sidecar can be consumed.
- The selected corpus is predominantly born-digital. A vector-aware extractor
  must be evaluated separately from raster OMR.

## Governing Principles

1. File creation is not success. A candidate that emits parseable but empty or
   timing-invalid MusicXML fails.
2. Use public synthetic fixtures first. Private inputs must not be uploaded to
   any third party or used until the maintainer approves the exact tool, terms,
   retention policy, and fixture scope.
3. Compare candidates through one versioned harness and one oracle contract.
4. Preserve provenance: tool/version, operating mode, input hash, command or
   manual procedure, output hash, elapsed time, corrections, and exit status.
5. Do not tune thresholds or procedures to a private filename, title, bar, or
   reference GP.
6. Opaque model training remains out of scope. Model-based inference is a
   research candidate only and cannot become a dependency without a separate
   architecture and licensing decision.

## Common Evaluation Contract

Every executable candidate must be assessed on the same public fixture set:

1. `generated_standard_staff_whole_note.pdf` — standard notation control.
2. `generated_paired_notation_tab_system.pdf` — mixed notation/TAB.
3. `generated_paired_notation_tab_system_double_barline.pdf` — structural
   mixed-layout variant.
4. `generated_tiny_tab.pdf` with its committed MusicXML — known-good handoff
   oracle and comparison control, not training data.

For each candidate and fixture, record:

- whether the input mode is vector PDF, rendered image, or manual entry;
- MusicXML/MXL existence, package validity, root, part, measure, note, pitch,
  and rest counts;
- divisions, time signatures, voices, chord flags, backup/forward operations,
  ties, dots, tuplets, and per-voice measure balance where present;
- Score2GP timing-analysis errors and warnings;
- explicit `convert --musicxml` status, event count, matched/unmatched playable
  TAB candidates, and first refusal or mismatch;
- determinism across two fresh runs where automation is available;
- setup/runtime cost, processing time, correction time, platform support,
  headless/CLI/API availability, licence, redistribution limits, network use,
  data retention, and recurring price;
- the smallest bar/event-level mismatch against the committed public oracle.

Minimum technical pass for a route to enter the bake-off:

- one validated MusicXML/MXL artifact;
- at least one musical `note` or `rest` on every fixture that visibly contains
  music;
- no fatal Score2GP timing issue on the known-good control;
- no silent empty-success classification; and
- a repeatable export procedure with exact provenance.

These are entry criteria, not proof of musical equivalence.

## Ordered Task List

### MXS-00 — Build the Candidate-Neutral Sidecar Evaluation Harness

**Role**: Developer, product test/tooling task after separate promotion.

Add a public-fixture-only evaluator that accepts a candidate MusicXML/MXL and
writes ignored structured results for the common contract above. Reuse the
existing MusicXML parser, timing analyser, OMR manifest concepts, and explicit
conversion report. The harness must classify `empty_musicxml`,
`timing_invalid`, `handoff_refused`, and `non_deterministic` separately.

**Acceptance**:

- The known-good `generated_tiny_tab.musicxml` passes the non-empty and handoff
  controls.
- A synthetic empty-but-structurally-valid sidecar fails as `empty_musicxml`.
- A parseable timing-invalid sidecar cannot be reported as viable.
- Generated reports and candidate artifacts remain ignored.

**Stop/pivot**: Stop if implementing the harness would change conversion
semantics; split the missing observation into a smaller diagnostics task.

### MXS-01 — Classify the Approved Corpus by Recoverable PDF Evidence

**Role**: Architect/Researcher, evidence-only.

Classify each approved public input, and private inputs only locally after
explicit approval, as vector notation, raster scan, mixed vector/raster, or
unknown. Record embedded fonts, vector paths/text, page rendering needs, and
whether notation objects appear recoverable without raster recognition.

**Acceptance**: Produce a privacy-safe matrix and choose the vector-first and
raster-first fixture subsets. Do not infer that vector presence guarantees
semantic recovery.

**Decision enabled**: Whether PDFtoMusic Pro-style vector extraction deserves
priority over raster OMR for the real corpus.

### MXS-02 — Establish the Current Audiveris Control

**Role**: Researcher, evidence-only.

Repeat the common contract with the current supported Audiveris release and
its documented batch transcription/export invocation. Treat this as the
control, not an alternative. Compare it with the historical 5.7.0 result and
record whether the first zero boundary changes.

**Acceptance**: Exact release/hash/runtime, command, logs, output structure,
two-run determinism, and fixture matrix are recorded. A newer release number
alone is no progress.

**Stop/pivot**: If the current release remains empty on both mixed fixtures,
do not begin Audiveris integration work; continue to independent candidates.

### MXS-03 — Evaluate Vector-PDF Extraction with PDFtoMusic Pro

**Role**: Researcher, licensed desktop feasibility probe.

Evaluate PDFtoMusic Pro because its documented route reads notation data from
PDFs produced by notation software and exports MusicXML. Run only the vector
fixture subset. Record whether it supports unattended invocation, stable
exports, and acceptable licensing for the intended workflow.

**Acceptance**: Apply the common contract and compare the output at bar/event
level with the known-good public oracle. Explicitly classify raster-only input
as unsupported rather than a recognition failure.

**Continue criterion**: At least one mixed public fixture produces non-empty,
timing-safe MusicXML and a non-zero Score2GP handoff without manual semantic
re-entry.

### MXS-04 — Evaluate Local Open-Source OMR Challengers

**Role**: Architect/Researcher, isolated feasibility probes.

Evaluate credible maintained local engines that export MusicXML, beginning
with `homr`/`oemer`-class systems. Record repository revision, licence, model
provenance, model-download hashes, CPU/GPU requirements, supported notation,
offline operation, and whether PDF rendering/preprocessing is required.

Each engine is a separate row and isolated environment; a dependency or model
failure for one engine must not contaminate another candidate's verdict.

**Acceptance**: Apply the common contract, include cold-start and repeat-run
results, and inspect exported XML rather than relying on screenshots or MIDI
playback.

**Stop/pivot**: Reject an engine from integration consideration if its model or
licence provenance cannot be established, it requires unapproved training, or
it cannot run reproducibly in the isolated Linux environment. Preserve the
research result without adding it to product dependencies.

### MXS-05 — Evaluate Commercial Desktop OMR as Assisted Sidecar Producers

**Role**: Researcher with maintainer-operated UI where required.

Evaluate ScanScore, SmartScore, PhotoScore, and PlayScore independently. Do
not assume automation: first establish supported input types, MusicXML export,
trial limitations, platform, licence, and whether a CLI/SDK/API exists. For UI
tools, use a written procedure and record recognition time separately from
human correction time.

**Acceptance**: Each available tool receives the same fixture contract and a
verdict of `viable_automated`, `viable_assisted`, `not_viable`, or
`not_evaluated` with an exact blocker. Marketing accuracy claims are not
evidence.

**Stop/pivot**: Do not purchase or subscribe without maintainer approval. A
tool that requires manual correction may remain viable only if its measured
correction effort beats the manual-entry control while preserving timing.

### MXS-06 — Evaluate Cloud/API Routes Behind a Privacy Gate

**Role**: Architect/Researcher, terms-first.

Inventory services that can ingest notation images/PDFs or host editable
notation and export MusicXML. Soundslice's documented MusicXML export API is a
candidate only if an approved path exists to create notation from the input;
export API availability alone is not PDF-recognition evidence. Record API
availability, authentication, pricing, rate limits, ownership, retention,
training use, deletion, regional processing, and automation terms.

**Acceptance**: No upload occurs until the maintainer approves a named service
and the task records the exact public fixture and current terms. Initial probes
use public synthetic inputs only. Apply the common contract to downloaded
MusicXML and record request/response provenance without committing secrets.

**Stop/pivot**: Reject any route with unclear retention/training terms, no
lawful automation path, no MusicXML export, or no reliable deletion mechanism.

### MXS-07 — Measure Assisted Manual Entry as the Accuracy/Cost Control

**Role**: Researcher with maintainer-operated notation editor.

Enter the public control score in a MusicXML-capable notation editor using a
fixed procedure. Measure active time, corrections, and final contract results.
This is the control for deciding whether imperfect OMR plus correction saves
meaningful effort.

**Acceptance**: Produce timing-safe MusicXML that matches the public oracle at
bar/event level, plus elapsed and active-entry time. Do not treat manual entry
as a scalable product solution without the measured comparison.

### MXS-08 — Run the Blind Comparative Bake-Off

**Role**: Architect, followed by independent Reviewer.

Run every candidate that passed its feasibility gate against the same frozen
fixture set and scoring rubric. Candidate names must be hidden from the person
performing semantic mismatch scoring where practical. Report both raw export
and corrected-export results; never combine them.

Score these dimensions separately:

- note/rest precision and recall at bar/event level;
- onset, duration, voice, chord, tie, dot, and tuplet agreement;
- time/key/measure structure;
- Score2GP handoff and TAB-candidate consumption;
- deterministic automation and WSL deployability;
- human correction minutes per page;
- licence, privacy, cost, and operational risk.

No weighted aggregate may hide a fatal timing error, empty output, private-data
risk, or non-reproducible runtime.

### MXS-09 — Architecture Decision and Smallest Next Implementation

**Role**: Architect, independently reviewed.

Choose exactly one outcome:

- **Outcome A — Adopt an automated route**: name the exact candidate/version,
  supported input class, licence/deployment boundary, measurable acceptance,
  and smallest integration task.
- **Outcome B — Adopt an assisted route**: define the human correction and
  validation boundary, provenance manifest, acceptance, and smallest workflow
  task.
- **Outcome C — No viable route**: name the failed gates and the smallest
  prerequisite that could change the decision. Authorise no integration.

The Reviewer must reproduce the winning route on the exact public fixtures,
create at least one malformed/empty/timing-invalid counterexample, and verify
that the harness rejects it before approving Outcome A or B.

## Candidate Evidence Sources

These sources establish only that a candidate warrants evaluation:

- Audiveris documents MusicXML/MXL export and an editable OMR intermediate:
  <https://audiveris.github.io/audiveris/_pages/reference/outputs/README/>
- PDFtoMusic Pro documents vector-PDF interpretation and MusicXML export:
  <https://www.myriad-online.com/resources/docs/pdftomusicpro/english/index.htm>
- ScanScore documents MusicXML export and warns that incomplete/overcomplete
  bars require correction before export:
  <https://scan-score.com/files/support/manual.pdf>
- SmartScore documents PDF recognition and MusicXML export:
  <https://www.musitek.com/smartscore-online-help/professional/note_editor/export.php?os=mac&sc=>
- PhotoScore documents PDF input, MusicXML output, and guitar-TAB recognition:
  <https://www.neuratron.com/photoscore.htm>
- PlayScore documents PDF playback and MusicXML export:
  <https://www.playscore.co/blog/faq-items/page/2/>
- oemer documents local image-to-MusicXML inference:
  <https://github.com/BreezeWhite/oemer>
- Soundslice documents MusicXML export for existing notation through its data
  API; this does not by itself establish PDF recognition:
  <https://www.soundslice.com/help/data-api/>

## Incremental Progress Check

- **New evidence**: a common rejection-capable harness, corpus input-class
  matrix, and comparable output evidence for distinct sidecar-generation
  routes.
- **Must not repeat**: FS-03E's empty Audiveris observation or FS-03F's valid
  supplied-sidecar handoff without testing a materially different generator,
  release, or input mode.
- **Project-forward result**: a reviewed Outcome A/B/C decision with an exact
  supported input class and smallest next task.
- **Duplicate/no-progress stop**: a task only confirms that an XML/MXL file is
  written, reruns the historical Audiveris command unchanged, or inventories
  tools without executing the common contract or recording an exact blocker.
- **Smallest next decision enabled**: whether Score2GP should integrate an
  automated generator, formalise an assisted sidecar workflow, or stop sidecar
  integration pending a named prerequisite.

## Programme Stop Conditions

Stop and return to governance if a task would require private upload,
unapproved purchase, new production dependency, model training, licence
acceptance, product semantic change, or scope beyond sidecar generation and
validation. Candidate failures are valid results; they must not be hidden by
changing fixtures, suppressing timing errors, or accepting empty output.
