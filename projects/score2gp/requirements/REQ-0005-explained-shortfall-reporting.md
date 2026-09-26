# REQ-0005 — Explained shortfalls and best-effort output

- **Status:** `RESEARCHED` (2026-09-26, RES-REQ-0005). `ACCEPTED` is recommended once the maintainer answers the decisions below.
- **Owner:** maintainer (`tticom`)
- **Recorded:** 2026-09-25, from maintainer direction
- **Research:** [2026-09-26-res-req-0005-explained-shortfalls](../research/2026-09-26-res-req-0005-explained-shortfalls/README.md), at product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`

## Requirement

Score2GP must know what it could not convert, and crucially **why**, and tell the user.

1. **Shortfall record.** For every source feature Score2GP cannot convert, or converts only in degraded form, it records:
   - what the feature is (its kind);
   - where it is (page, system, measure, beat or region);
   - why, as a stable reason code with the evidence that led to it (missing observation, ambiguity, unsupported feature, contradiction, capability limit of the output target);
   - what was done instead (omitted, degraded and how, or refused);
   - the provenance of the run (see REQ-0004).
2. **User report.** From those records, a report shows the user what was not converted and why, in terms the user understands, not just a failure status.
3. **Best effort.** Score2GP does what it can and renders the best result that can be done. It produces output for everything it can convert correctly, labels every gap, and never presents a partial result as complete.
4. **Learning over time.** Shortfall records are kept and aggregated across runs and sources, so the most frequent and most costly reasons become visible and drive the task authority's backlog.

Maintainer direction (2026-09-25), verbatim:

> "I want a system that knows what didn't work, or couldn't be done but crucially why! So I proposed logging that records enough information to produce a report that shows the user why a feature couldn't be completed by score2gp, not just fail. And the system should do what it can, and render something the best that can be done. By recording what we can't do over time, we'll discover how to complete the conversions but not if we don't know why we couldn't or what we couldn't convert."

## Relationship to existing rules

- **Fail-closed gates** (REQ-0001, recovery design): no guessed or fabricated musical content. Best effort must not weaken this. What cannot be established correctly is left out and explained, never invented. The open question is how a partial result is delivered (a mode, a separate artifact, or labelled regions) without an unlabelled wrong result.
- **Existing diagnostics:** per-stage warning and refusal codes and `build-ir-failure-diagnostics` sidecars are the starting point for the reason-code taxonomy. Research correction: `docs/diagnostics_failure_taxonomy.md` covers only raster treble-clef classifier failure causes. The codes themselves are 190 unregistered string literals spread across `src/score2gp` ([map E6](../research/2026-09-26-res-req-0005-explained-shortfalls/01-current-state-map.md#17-reporting-defects)).
- **REQ-0002:** a target's declared degradations and refusals are shortfalls too.
- **Commercial:** partial output with located gaps could be priced lower than complete output (maintainer idea, 2026-09-25).

## Open questions (answered by RES-REQ-0005)

1. How best-effort output coexists with strict refusal: a mode, per-measure gating, or a separate "partial" artifact.
   **Answer:** the primary `--out` stays complete-or-nothing. When a conversion is not complete, the run exits non-success with status `partial`, writes no primary output, and writes a labelled `<name>.partial.gp` beside it: delivered bars, plus a marked gap bar for each refused bar. ([options](../research/2026-09-26-res-req-0005-explained-shortfalls/03-best-effort-options.md))
2. The reason-code taxonomy: extend the existing codes or define a user-facing layer above them.
   **Answer:** both. Register and freeze the existing engine codes, and add 8 reason families and 16 stable user reasons above them. Every shortfall also carries a feature kind and a disposition. ([taxonomy](../research/2026-09-26-res-req-0005-explained-shortfalls/02-reason-code-taxonomy.md))
3. Where shortfall records live and how they are aggregated without exposing private content.
   **Answer:** a private per-run `shortfall-records.json` in the work directory. A sanitised counts-and-codes aggregate, enforced by a validator, goes to a local ledger. A ranked rollup may be committed. ([design](../research/2026-09-26-res-req-0005-explained-shortfalls/04-shortfall-record-and-aggregation.md))
4. What the user report looks like, and in which formats.
   **Answer:** headline status and coverage, then what was not converted (by user reason, with source locations), what was converted with caveats, and what is not supported yet. Markdown, HTML and JSON render from the same records. ([mock-up](../research/2026-09-26-res-req-0005-explained-shortfalls/05-report-mockup.md))

## Research findings (summary)

At product SHA `3af1925`, 35 real runs on Lessons 3-7, Ex 2 Hands Up and Can't Find My Way Home
refused in every route. Each run gives the user one reason code. The per-bar replay shows that
code stands for up to 52 failing bars in a source, alongside up to 25 bars that pass the product's
own per-bar checks. At most 10 of those are free of candidate-level doubt and synthesised rests, and
all of them have inferred rhythm. The
[current-state map](../research/2026-09-26-res-req-0005-explained-shortfalls/01-current-state-map.md#18-silent-gaps-named)
names 20 silent gaps (G1-G20). Three of them already contradict existing fail-closed rules:
inferred rhythm reported as `success` (G7), synthesised rests at confidence 1.0 (G8), and
`generate-sidecar` crashing without a code (G5).

## Acceptance

Testable criteria, replacing the 2026-09-25 draft. G-numbers refer to the silent gaps in the
research map. "Corpus" means the seven sources above, run locally; only counts and codes from
those runs may be committed.

1. **A1 — Records exist and are complete.** Every `convert` run, whatever its outcome, writes `shortfall-records.json`. On a public fixture set with known unsupported, ambiguous and over-full features, a conservation test passes: every source bar is delivered clean or covered by a record, and every extracted candidate is consumed by a delivered note or referenced by a record (covers G1, G4, G9, G11-G19). A registry test fails if any emitted `code=`/`category=` literal in `src/score2gp` is not registered with stage, role, family and user reason.
2. **A2 — Located.** Every record whose engine code is bar-level or finer has a source-frame location (page, system, source bar) at bar precision or finer. A test fails any bar-level code recorded at document precision (G2, G3). With `--pages`, document-level records are kept (G20).
3. **A3 — Reasoned.** Every record has a registered engine code, family and user reason. A fault-injection test raising an unexpected exception in `convert` and in `generate-sidecar` yields a record with an `internal_error` family and the stage name, not a bare traceback (G5, G6). GP-writer omissions use per-reason target codes (G10).
4. **A4 — Honest status.** `status: success` and exit 0 only when there are no records other than `defaulted` records with policy provenance. `approximated`, `synthesised`, `omitted` and `refused_region` records make the status `partial` with a non-zero exit (G7). No delivered event has confidence 1.0 with empty provenance unless a `synthesised` record covers it (G8). `summary_counts` in the JSON report match the extraction (E1).
5. **A5 — Best effort, independently checked.** On a public fixture with known failing bars, and locally on at least one corpus source with a reference `.gp`: `--out` is not written, `<name>.partial.gp` is written, and its bar count equals the source bar count. Each refused bar is a marked gap bar. Every delivered bar's string, fret and pitch content equals the reference, as read by an oracle that does not import `score2gp`. Approximated fields are labelled per bar in the file and in the records.
6. **A6 — User report.** Every run writes a report, rendered from the records, with: headline status and bar coverage; "not converted" grouped by user reason with location and suggested action; "converted but check"; "not supported yet"; and support details. A test proves that each record appears in exactly one user-facing section, and that evidence-role codes never appear outside the details section.
7. **A7 — Aggregate.** A rollup over the corpus ranks reasons by bars affected, then by sources affected. It is produced from sanitised aggregates only.
8. **A8 — Private.** A validator rejects any sanitised aggregate that contains free text, coordinates, page/system/bar values, candidate ids or an unhashed input identity. The test includes a seeded adversarial record.

## Decisions for the maintainer (before `ACCEPTED`)

1. **D1** Delivery option: separate partial artifact (recommended) or a mode switch writing the partial GP to `--out`.
2. **D2** Whether PDF-only and editable-draft runs with inferred or defaulted rhythm change from `success` to `partial` (a CLI contract change; recommended yes).
3. **D3** How a gap bar is represented in Guitar Pro, and who verifies in the pinned Guitar Pro version that it is not repaired into a rest (unverified today).
4. **D4** Whether a labelled omission of an unsupported feature (lyrics, text, dynamics) blocks `success` (recommended: yes, with an allowlist the maintainer can grant).
5. **D5** Where committed rollups live (recommended `projects/score2gp/shortfalls/`), and whether the local ledger is on by default (recommended: on, local only).
6. **D6** Registry form (recommended: Python module exported to JSON) and whether to canonicalise the 25 kebab-case codes now (recommended: keep them as aliases).
7. **D7** The independent oracle for A5 (recommended: a GP reader that does not import `score2gp`).
8. **D8** Delivery order (recommended: fail-closed defects G5, G7, G8 first; then collection and location; then report; then aggregation).
9. **D9** Whether correcting `docs/scoreir-to-gpif-coverage.md` and the description of `docs/diagnostics_failure_taxonomy.md` is in scope (recommended: yes).
10. **D10** Priority relative to REQ-0001 L3-NATIVE.
