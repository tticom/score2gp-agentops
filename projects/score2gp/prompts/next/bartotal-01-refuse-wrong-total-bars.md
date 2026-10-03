# BARTOTAL-01: Bars whose tick total differs from the declared time signature must be refused, not written

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** PDF-GROUP-02 (merged)
- **Branch:** `feat/bartotal-01-refuse-wrong-total-bars`

This comes from the independent hard review of #482 (PDF-GROUP-02) and the governance record of 2026-10-03 (backlog item queued by agentops#766). Main now includes #478 to #482. Never commit private content; report counts, codes and distances only.

## What was measured (leads to VERIFY)

`E_Chord_Lick_Chord` (private fixture in `C:\Users\niall\src\score2gp-workspace\score2gp-private-fixtures\fixtures\private`; verify it is in your mounted `fixtures/private`, which should hold 37 PDFs) at product `28c929e` exits 0 with 16 bars. Bars 2, 4, 10 and 12 are **written with 4080 or 3960 ticks under a declared 4/4** (a 4/4 bar is 3840 ticks) and are NOT refused by the bar-total check. 7 other bars are refused with `pdf_only_tab_bar_refused` (`bar_total_mismatch` 3, `notehead_digit_count_mismatch` 3, `notation_note_without_tab_digit` 1) and are written empty. A written bar whose total is wrong is a false success.

## Investigate first

1. **Why the check does not fire.** Is the bar-total check skipped for some route, or masked by a tolerance? Find the module that computes and checks bar totals (likely `src/score2gp/notation_omr/note_duration.py` or a `pdf*.py` module) and the exact condition under which these four bars pass.
2. **Is 4/4 right for that file?** The maintainer has not confirmed its printed signature. `--time-signature` is a caller input; Combining_Maj_minor_pent_-_A is printed in 12/8 and refuses under 4/4. A quick text probe suggests the time signatures on these pages are drawn as vector shapes, not text. Report what you find (counts and distances only); do **not** build a time-signature reader here (that is a separate candidate, TS-READ-01).
3. **Which converting files would change.** Measure, for every file that converts at base, whether any written bar has a total different from the declared signature.

## Goal

A bar whose summed tick total differs from the declared signature is refused with a located code and warning and is never written as a success. Never invent a value. Do not change exit-code semantics for files with refused bars unless the investigation shows a false success: if it does, report it and propose it rather than changing it silently.

## Acceptance

1. **Investigation reported** as above (the exact gap, the signature question, the list of affected files by label and bar count).
2. **Located refusal.** A bar whose total differs from the declared signature gets a located refusal code and warning (bar, system, total, expected), not a written bar. Any tolerance is justified by measurement and stated.
3. **Tests that bite.** Synthetic public fixtures that fail at base and pass now (a wrong-total bar is refused; a correct-total bar is unchanged); a mutant (check removed, or tolerance widened) fails a test. Tests are CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.
4. **Nothing correct may change.** State the exact number of converting files at base (the author's mounted corpus has 37 private PDFs) and compare each: every converting file stays byte-identical GPIF **except** files containing a wrong-total bar, which are reported by label and bar count as newly refused bars (counts only). The refusal codes of already-refused files are unchanged.
5. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally (the last runs recorded 14 to 15).

## Rules

- **Read from the source, or refuse.** Never invent a value; closing a hole is allowed, loosening a gate to raise a count is not.
- **Stay inside `allowed_paths`:** the module that computes bar totals (the author finds it: `src/score2gp/notation_omr/note_duration.py`, or a `pdf*.py` module), `tests/test_note_duration*.py`, `tests/test_pdf*.py`, `tests/test_bartotal_01_*.py`, `tests/fixtures/pdf/bartotal_01/**`, `docs/design/**`. Not the `build_ir.py` gating sets unless a scope amendment is requested: stop and report it.
- **Stop** if the fix changes a gate's meaning rather than closing a hole, and report what the gate is.
- **One heavy process at a time** on this machine.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content.
- **Protect what already works:** DUR-02/03, OMIT-01/02/03/05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
