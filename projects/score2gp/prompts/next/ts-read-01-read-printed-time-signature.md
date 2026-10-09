# TS-READ-01: Read the printed time signature from the PDF

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** PDF-GROUP-02 (merged)
- **Branch:** `feat/ts-read-01-printed-time-signature`

This promotes TS-READ-01 (a candidate from the PDF-GROUP-02 investigation, updated by the BARTOTAL-01 close-out) on the evidence of the 2026-10-08 fixture survey. Every number below is a lead: re-measure it before relying on it. Never commit private content; report counts, codes and distances only.

**Private fixtures.** The private corpus is now grouped by category (`fixtures/with-score`, `no-score`, `ascii`, `hand-written`, `Books`; 49 files on fixtures `main`). The author launcher flattens every category into your worktree's ignored `fixtures/private/`. **Before starting, verify that `fixtures/private/` contains `Combining_Maj_minor_pent_-_A.pdf`, `Lesson-3.pdf` to `Lesson-7.pdf`, `Gloria.pdf` and `Melodic_Expressions_Chap_19_.pdf`**; if any is missing, stop and say exactly what is missing.

## What was measured (leads to VERIFY)

- The time signature is a caller input today: `convert --pdf-only-tab` needs `--time-signature`, and every bar records `time_signature_source: "caller_declared"` (`src/score2gp/notation_omr/note_duration.py`, `src/score2gp/pdf_tab_bar_assembler.py`). The 2026-10-08 survey converted all 39 sources at the declared `4/4`.
- **Combining_Maj_minor_pent_-_A** is printed in 12/8. With the declared 4/4 every one of its 8 bars refuses `bar_total_mismatch` with the detail "6 of 4 quarters", so 0 of 8 bars are written. An earlier record of this candidate in the authority notes that with 12/8 declared and no code change it converts 5 of 8 bars.
- `bar_total_mismatch` accounts for 16 refused bars across the survey (Combining 8, E_Chord_Lick_Chord 3, Just-Practice 2, Melodic_Expressions_Chap_19 2, Can't Find My Way Home 1). Only Combining is wholly explained by the signature; the BARTOTAL-01 close-out found no other file that needs the check for correctness. **Do not assume the other 8 are signature errors; measure each.**
- The signature is **vector-drawn** on these pages (no text match), so a reader needs shape recognition, the way OMIT-01 reads the key signature (`src/score2gp/notation_omr/key_signature.py`). Reuse its clef-relative search and scale-relative sizing where they apply.

## Goal

Read the printed time signature of each system's first bar (and a signature printed later in the piece) from the PDF, and use the caller-declared value only when none is printed or readable. If the printed and the declared signatures disagree, refuse with a located reason; never choose silently. The signature that is used is recorded per bar with its source (`printed` or `caller_declared`).

## Acceptance

1. **Measure first.** A census over the whole mounted PDF set of what each source prints as its first-bar signature (counts per signature, and how many are unreadable), with the shapes you saw (common time and cut time as well as numerals). Counts and labels only.
2. **The reader.** Shape recognition sized by the staff space (no fixed point limits), distinguishing at least 2/4, 3/4, 4/4, 5/4, 6/8, 9/8, 12/8, common time and cut time. A candidate that is not unambiguous is not read: it is recorded with a located reason and the declared value is used only when allowed by rule 3.
3. **The rule.** Printed and readable: use it. Neither printed nor readable: use the declared value (as today) and say so in the bar record. Both present and different: refuse the affected bars with a located reason naming both values. `--time-signature` becomes optional where the printed one is readable; it is still accepted.
4. **Combining_Maj_minor_pent_-_A** converts under its printed 12/8 without any flag; report bars written and every remaining refusal by code. **No reference `.gp` exists for it, and you must say so** instead of claiming a match.
5. **Real-source tests that bite.** Private-corpus tests (converting under `<repo>/work`, running in CI where the corpus is mounted) assert on more than one approved source that the printed signature is read (Combining_Maj_minor_pent_-_A as printed, and the converting lessons as printed), that a deliberately wrong declared value on the same real PDF is refused with a located reason naming both values, and that each mutant fails those tests on the real files: always use the declared value; read only the top numeral; ignore the denominator; choose silently on disagreement. Public synthetic fixtures are supplementary non-domain infrastructure only, with a stated rationale, and carry no acceptance weight.
6. **Nothing that worked may change.** Measure on the full private set at base and at head: every file that converts today keeps a byte-identical GPIF when its printed signature equals the declared one. A file whose printed signature differs from the declared one may change status (refused with a located reason, or converted under the printed value); each such file is reported by name (counts and labels only) with its before and after result. The before-and-after table covers every converting and every refused file.
7. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources, or reproducible extracts that keep their source provenance and reach the changed seam; general claims need more than one approved corpus input. Synthetic, mocked or generated-notation tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims; they may supplement non-domain infrastructure only with a stated rationale.
- **Read from the source, or refuse.** Never invent a value, never copy one from a reference `.gp`, never loosen a gate to raise a count.
- **Scale-relative only:** every new limit is a multiple of the measured staff space.
- **Stay inside `allowed_paths`.** If you need another path, stop and report it so governance can amend scope.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path` (`gpif.build_gpif` writes a legacy layout when "pytest" is in an argument or path).
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
- Out of scope: reading signature changes inside a bar line (report them), any change to the `build_ir.py` gating sets.
