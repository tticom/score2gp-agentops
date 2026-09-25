# REQ-0005 — Explained shortfalls and best-effort output

- **Status:** `PROPOSED`. Research task RES-REQ-0005.
- **Owner:** maintainer (`tticom`)
- **Recorded:** 2026-09-25, from maintainer direction

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
4. **Learning over time.** Shortfall records are kept and aggregated across runs and sources, so the most frequent and most costly reasons become visible and drive the backlog.

Maintainer direction (2026-09-25), verbatim:

> "I want a system that knows what didn't work, or couldn't be done but crucially why! So I proposed logging that records enough information to produce a report that shows the user why a feature couldn't be completed by score2gp, not just fail. And the system should do what it can, and render something the best that can be done. By recording what we can't do over time, we'll discover how to complete the conversions but not if we don't know why we couldn't or what we couldn't convert."

## Relationship to existing rules

- **Fail-closed gates** (REQ-0001, recovery design): no guessed or fabricated musical content. Best effort must not weaken this. What cannot be established correctly is left out and explained, never invented. The open question is how a partial result is delivered (a mode, a separate artifact, or labelled regions) without an unlabelled wrong result.
- **Existing diagnostics:** stable per-stage warning and refusal codes (`docs/diagnostics_failure_taxonomy.md`) and `build-ir-failure-diagnostics` sidecars. These are the starting point for the reason-code taxonomy.
- **REQ-0002:** a target's declared degradations and refusals are shortfalls too.
- **Commercial:** partial output with located gaps could be priced lower than complete output (maintainer idea, 2026-09-25).

## Open questions (for RES-REQ-0005)

1. How best-effort output coexists with strict refusal: a mode, per-measure gating, or a separate "partial" artifact.
2. The reason-code taxonomy: extend the existing codes or define a user-facing layer above them.
3. Where shortfall records live and how they are aggregated without exposing private content.
4. What the user report looks like, and in which formats.

## Acceptance (draft, to be completed by research)

1. Every refused or degraded feature in a conversion has a shortfall record with kind, location, reason code, evidence and disposition. A test proves no gap is silent.
2. A best-effort conversion of a source with known unsupported features produces output for the supported parts and a report listing each gap and its reason. An independent oracle confirms the delivered parts are correct.
3. An aggregate over the corpus ranks reasons by frequency.
