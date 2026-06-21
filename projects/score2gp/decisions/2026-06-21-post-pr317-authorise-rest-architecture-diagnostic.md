# Post-PR 317: Authorise Rest-Aware Sequencing Architecture Diagnostic

## Context
Product PR #317 is merged (`8efb3e73ad41b338278500a4ca1ff882acd8ed5f`, merge commit `0c631d78dd3f9063630d88625941ff500586ce82`). It successfully admitted exactly three diagnostic PDFs as tracked public fixtures without implementing product behaviour.

The baseline diagnostic from prior tasks found that:
- `QuarterRestThenNotes.pdf` parses but fails single-note export due to multiple candidates. Rest geometry is skipped, leading to note squashing, blocked by the lack of rest-aware sequencing implementation.
- `TabOnlySingleNote.pdf` and `TabOnlyTwoNotes.pdf` fail notation extraction because tab staff geometry is missing (`missing_staff_geometry`), preventing fret candidate association.

## Decision
1. **Record PR #317 fixture admission as complete.**
2. **Set the active blocker to rest-aware sequencing architecture.** `QuarterRestThenNotes.pdf` cannot yet be converted with rest-aware timing because the pipeline has not proven structural rest detection or a rest-event representation/mapping strategy.
3. **Authorise one bounded architecture diagnostic solely for `QuarterRestThenNotes.pdf`.** The diagnostic must determine whether rest-aware sequencing is viable using current parsed evidence.
4. **Explicitly defer tab-only work.** Tab-only geometry extraction is a separate blocker requiring distinct architecture focus. Tab-only work is not authorised in this iteration.

## Active Task
The active task is strictly bounded to an architecture diagnostic of rest structure using `QuarterRestThenNotes.pdf`. The Architect must provide a concrete rest evidence map, propose an event/timing model, and choose exactly one of three outcomes:
- Outcome A: rest-aware sequencing is viable using current parsed evidence.
- Outcome B: current evidence is insufficient but another bounded approach is viable.
- Outcome C: no viable approach is proven.

No product implementation or test changes are authorised by this decision.
