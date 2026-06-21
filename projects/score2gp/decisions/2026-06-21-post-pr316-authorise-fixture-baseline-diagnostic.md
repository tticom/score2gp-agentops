# Decision: Record PR #316 Completion and Authorise Fixture Admission/Baseline Diagnostic

## Context
Product PR #316 proved deterministic sequential event mapping for multiple already-recognised notation candidates in simple generated public notation fixtures.
The next risk is not to start coding rests or tab-only extraction blindly, but to baseline unknown fixture/input behaviour for three target PDFs: `QuarterRestThenNotes.pdf`, `TabOnlySingleNote.pdf`, and `TabOnlyTwoNotes.pdf`.
They must be treated as candidate diagnostic inputs, not admitted fixtures, until safety and usefulness are proven.

## Verified State
* Product PR: `tticom/score2gp#316`
* Branch: `feature/deterministic-multinote-sequencing-v0.1`
* Head SHA: `8086daf8d4ce608ad288a2d86d65c424caba3b0d`
* Merge commit: `442b2b45241ec766dcf0b5e31c599c9f4c19d201`

Capability delivered:
* `build_ir_from_notation_outcomes` can emit multiple deterministic sequential note events from multiple valid notation outcomes.
* Sorting is by page/system/staff/x-position with deterministic tie-breaker.
* `onset_ticks` accumulates sequentially.
* one 4/4 bar duration cap is enforced.
* existing single-note export CLI path rejects multiple-event output.

Evidence:
* targeted tests for deterministic multi-note sequencing and single-note export rejection passed.
* full suite reported as 785 passing.
* CI and Raster Diagnostics Gate Advisory passed.
* Codex P2 thread was accepted, fixed, replied to, and resolved.

Non-capabilities:
* no rest support proven.
* no tab-only support proven.
* no chord/voice support proven.
* no new fixture admission proven.

## Active Blocker
The active blocker is now unknown fixture/input behaviour for:
* a notation PDF containing a rest before notes;
* tab-only single-note input;
* tab-only two-note input.
The project needs decision-useful diagnostic evidence before authorising rest or tab-only implementation.

## Authorised Next Task
We authorise exactly one bounded product diagnostic task: `Fixture Admission and Baseline Classification for Rest/Tab-only Inputs v0.1`.

### Diagnostic Hypothesis
The three candidate PDFs can be classified safely and usefully into one of:
* admissible public diagnostic fixture,
* not safe/admissible as fixture,
* safe for local-only diagnostic but not commit,
* not useful for current pipeline.

### Fixture Set
* `QuarterRestThenNotes.pdf`
* `TabOnlySingleNote.pdf`
* `TabOnlyTwoNotes.pdf`

### Metrics
* file safety/admissibility outcome;
* whether the current production recognition path runs without crashing;
* whether notation candidates are produced;
* whether rest-like symbols are observed or absent;
* whether tab-only staff geometry/string evidence is detected;
* whether any ScoreIR/GP output is produced;
* exact warning/error/blocker reason;
* whether result enables rest-aware sequencing, tab-only extraction architecture, return to architecture, or stop/pivot.

### Pass Threshold
The diagnostic passes if every one of the three files receives:
* safety/admissibility classification;
* production-path run result;
* observed candidate/evidence summary;
* exact blocker classification;
* recommended next task category.

### Fail Threshold
The diagnostic fails if it only says “does not work,” only captures logs, only creates artifacts, or does not force a next decision.

### Stop/Pivot Condition
* If files are unsafe/private/not admissible, stop fixture admission and request safe public/generated replacements.
* If rest notation is detected but unsupported, authorise rest-aware sequencing architecture or implementation only if evidence is sufficient.
* If tab-only input lacks necessary geometry/string evidence, return to architecture for tab-only extraction.
* If tab-only evidence is present and production path exposes it, authorise a narrow tab-only diagnostic/implementation task.
* If none of the files can be used safely, stop and request new generated public fixtures.
