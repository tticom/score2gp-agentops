# PARTIAL-01: Write the boxed systems and refuse only the unboxed one instead of refusing the whole file (pdf_partial_grouping_one_system_unboxed)

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** DUR-03
- **Branch:** `feat/partial-01-per-system-refusal`

This comes from the read-only investigation `docs/investigations/accuracy-gaps.md` (tticom/score2gp-vector-parser, finding 1, product main `8b03fb6`, model-written: treat every number as a lead and re-measure it).

## What the investigation measured (leads to VERIFY)

Of 17 private PDFs that finished in that run, 11 exit 4 `pdf_only_tab_grouping_unsafe`. In 9 of those 11 exactly one system is unboxed (`pdf_partial_grouping_one_system_unboxed`, with 1 to 23 `pdf_bar_box_construction_not_enough_for_build_ir` warnings) and the whole file is refused, although the other systems have valid bar boxes. The warning is emitted in `src/score2gp/pdf.py` (partial-grouping check, boxed versus unboxed systems) and the whole-file refusal is the unsafe-layout gate in `src/score2gp/build_ir.py` (`pdf_only_tab_grouping_unsafe`); read both, and read how the PDF-only assembler (`src/score2gp/pdf_tab_bar_assembler.py`) already refuses single bars with located reasons. The root cause of the unboxed system (barline height versus string gaps) is NOT known and is not this task's job: do not try to make the unboxed system boxed.

## Goal

When exactly the readable systems can be written unambiguously, write them and refuse the unboxed system with a located reason (page, system index, bars or digits affected). Never invent a value, never loosen a gate to raise a count, and anything ambiguous stays refused (whole file where today it is whole file).

## Acceptance

1. **Measure first.** On the private corpus (counts and codes only) list every PDF refused with `pdf_only_tab_grouping_unsafe`, the refusal warning code, the number of boxed and unboxed systems, and which of them have exactly one unboxed system; confirm or correct the 9-of-11 lead.
2. **A stated per-system rule.** Define which systems are written (a system with its own complete string lines, valid non-overlapping bar boxes, every candidate assigned to a string and a bar, and notation bars that pair with its TAB digits through the existing assembler) and which one is refused. A system is refused, not written, if any of its candidates is unassigned, its boxes are narrow, overlapping or outside the system, or its bar count or pairing is ambiguous. Where the written systems would leave a gap in the bar sequence the result must say so; if the order or bar numbering would be ambiguous, refuse the whole file as today.
3. **Located refusal, no silent loss.** Each refused system is reported through the existing report and diagnostics with page, system index and a specific code; no digit of a refused system is written to another bar; the report must not say the file converted completely.
4. **Pairing check.** Re-measure counts only on the private corpus: the files that change from whole-file refusal to a partial write, and the bars written per file. Compare every written bar through the independent GPIF reader with the reference `.gp` where one exists (note count, string, fret, written value) and report the real numbers; **a bar paired wrongly is worse than a refused system**.
5. **Nothing that worked may change.** Every file that already converts (Lessons 3-7 and every other converting PDF) produces a byte-identical GPIF at base and head (compare the full XML; report any change with evidence). Files that stay refused keep their refusal code, except the files that become a partial write.
6. **Tests that bite.** Public synthetic fixtures (engraved like the real source: several systems, exactly one unboxed) that fail at the base and pass now; a fixture with two unboxed systems, a fixture whose boxed systems are ambiguous, and an all-boxed fixture that prove they stay as today. Mutants (no per-system refusal so the unboxed system is written; refuse-all kept; unboxed system written with guessed boxes) must each fail a test. Tests must be CI-safe: create `<repo>/work` before using it and prove them on a clean `git archive` copy without `work/`.
7. `python -m pytest` (exact-head CI), `python -m score2gp.cli export-schema --out schemas`, `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`, `python scripts/artifact_audit.py` and `git diff --check` pass.

## Rules

- **Read from the source, or refuse.** Never invent a value, never copy one from the reference `.gp`, never loosen a gate to raise a count; do not weaken `pdf_bar_box_*`, string-assignment or barline gates, only change what a refusal covers.
- **Protect what already works:** DUR-02/03 bars, OMIT-01/02/03/04/05, LAYOUT-01, MEM-01, CFW-04.
- **Stay inside `allowed_paths`;** if you need another path (for example `schemas/**`, `src/score2gp/ir.py`, `src/score2gp/gpif.py`), stop and report it so governance can amend scope. A partial result must be expressible with the existing report and IR fields.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`. Commit no private content; counts, codes and distances only.
- **Stop conditions** as in CFW-04: `value_invented_or_copied_from_reference`, `gate_loosened`, `dur_02_regression`, `private_content_would_be_committed`.
- **Pass the product checklist** above; exact-head CI is the full-suite result. List the two known Windows baseline failures by ID if they fail locally.
