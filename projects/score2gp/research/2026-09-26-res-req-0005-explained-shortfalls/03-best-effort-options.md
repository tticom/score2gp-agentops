# 3. Best-effort delivery options, evaluated against the fail-closed rules

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`.

## 3.1 The fail-closed rules used for evaluation

Each rule is quoted or paraphrased from an authority record, and the evaluation cites it by id.

| Rule | Source | Statement |
|---|---|---|
| FC1 No fabrication | [REQ-0001](../../requirements/REQ-0001-native-faithful-pdf-to-gp.md) summary; native plan §3 invariant 2 | Uncertain input is diagnosed, repaired within bounds, or refused, and never guessed. Missing and ambiguous are explicit states, not confident facts. |
| FC2 Non-success when unresolved | L3 plan, final acceptance contract, "Uncertainty" gate | Unresolved cases produce a located diagnostic **and a non-success result**. |
| FC3 Located diagnostic | same gate | Every unresolved case is located. |
| FC4 Coverage | L3 plan, "Whole-document coverage" gate | Every source page, system and measure is accounted for exactly once; no dropped or invented musical material. |
| FC5 No inferred rhythm in success | L3 plan, "Defaults" gate | No defaulted or layout-inferred rhythms in a successful result; only genuinely absent facts may default, with provenance. |
| FC6 No invented padding | L3 plan, "Compilation" gate | No note clamping, partial-chord loss, invented padding or inferred measure fabrication. |
| FC7 Zero false success | REQ-0001 acceptance; native plan qualification gates | No run reports success for an output that is not faithful. |
| FC8 No partial as complete | REQ-0005 requirement 3 | Never present a partial result as complete; label every gap. |

An option **fails** if any rule can be broken without a label reaching the user.

## 3.2 What the runs say a best-effort output could contain today

From the per-bar replay (map §1.3, `evidence/run-matrix-facts.json`), in PDF-only mode across the
seven sources:

| | Bars |
|---|---|
| Source bars (independent layout inventory, map §1.3a) | 277 |
| …reached by the PDF-only builder (≥1 playable candidate) | 275 |
| …never reached: candidate-only 1 (EX2), empty 1 (CFMWH); no output bar, no record (G21) | 2 |
| Pass the product's current per-bar checks | 105 |
| …and contain no candidate with a non-exempt candidate-level code and no synthesised rest | 17 |
| Refused by the current checks | 170 (`pdf_only_tab_measure_overcapacity` 107, `pdf_only_tab_ambiguous_duration` 63) |

Even the 17 "clean" bars have durations chosen from the number of events (`D1`). None of the 277
has observed rhythm. So with tab-only input, a best-effort result can deliver **observed
string/fret content** for some bars, and only **approximated** rhythm. Any design must be able to
say that at bar level. Today, per-bar success is necessary but not sufficient for correctness:
88 of the 105 assembled bars hold low-confidence notes or synthesised rests that nothing labels
(gaps G8, G9).

## 3.3 Options

### Option 0: status quo (for reference)

`--pdf-only-tab` and `--editable-draft` produce a single GP. `status: success`, exit 0, one
document-level warning (`pdf_only_tab_inferred_timing` / `pdf_editable_draft`). The first bad
bar refuses the whole document.

| Rule | Result |
|---|---|
| FC2, FC5, FC7, FC8 | **Broken.** An inferred-rhythm result is reported as `success` (`cli.py:1349-1354`), observed on `PUB`. The GP carries only a title (`build_ir.py:1806`) in pdf-only mode. |
| FC3 | Broken: no per-bar location (G2-G4). |
| FC6 | Broken silently: synthesised rests with confidence 1.0 (G8). |

Not acceptable as the best-effort design. It is listed because it is what ships.

### Option A: one mode switch, gap bars inside a single partial GP

`convert --best-effort` (default off). Bars that pass a **strict per-bar gate** are delivered.
Every other bar is present as a **gap bar**, with a visible GP marker such as
"NOT CONVERTED — rhythm-ambiguous (see report)". Run status `partial`, non-zero exit (new code,
e.g. 6). The report lists every gap.

Strict per-bar gate: all notes from candidates with no non-exempt candidate-level code; no
synthesised content; each field is either observed or carries disposition `approximated` or
`defaulted` with a bar-level label.

| Rule | Result |
|---|---|
| FC1 | Holds if the gate is strict. Approximated rhythm must be labelled per bar, not per document. |
| FC2, FC7 | Holds: `partial` is a non-success status with a non-zero exit. |
| FC3 | Holds: records carry page/system/source bar (design 04). |
| FC4 | Holds only if "every source bar" means the independent layout inventory (map §1.3a). A bar with no playable candidate must become a gap bar too (G21); a builder keyed on playable candidates silently drops it. |
| FC6 | **Risk.** GP has no "unknown" bar content. An empty or gap bar is rendered, and played back, as silence. That is invented material unless the marker is in the file. Whether GPIF can hold a bar with no beats that GP 7/8 opens without repairing to a rest is **Unverified** (maintainer decision D3). |
| FC8 | Holds only while the marker survives in the file. Once the user edits the GP and deletes the marker, the file no longer says it is partial. |

Verdict: **acceptable with conditions**. Gap bars must be labelled inside the file, the status
must be non-success, and the GP gap representation must be verified in the real application
first.

### Option B: complete-or-nothing primary output, plus a separate partial artifact

The primary `--out` is written **only** when the conversion is complete and faithful (today's
contract). When it is not, the run exits non-success, writes no primary output, and writes:

- `<name>.partial.gp`: delivered bars plus labelled gap bars, as in Option A, with the title
  prefixed "PARTIAL — " and a FreeText notice (the draft mode already writes one; `PUB` draft run
  observed it in the GPIF);
- `shortfall-report.html` and `shortfall-records.json` (design 04, mock-up 05).

| Rule | Result |
|---|---|
| FC1, FC3, FC4, FC6 | As Option A, with the same GP gap-bar condition (D3). |
| FC2, FC7 | **Holds strongly.** The file the caller asked for does not exist, so scripts and batch pipelines that test for `--out` cannot mistake a partial result for success. |
| FC8 | Holds: the file name, title and notice all say partial, and a partial file can never overwrite a complete one. |

Verdict: **acceptable; recommended.** It keeps the current strict contract of `--out` and adds
the partial artifact beside it. That also separates the two for pricing (partial output with
located gaps could be priced lower than complete output).

### Option C: per-measure gating always on, no mode

Every run delivers what passes the per-bar gate in `--out`, with gap bars, and reports `partial`.

| Rule | Result |
|---|---|
| FC2, FC7 | Holds only if every caller reads the status. `--out` now exists for partial runs. Existing callers equate a written GP with success: `batch.py:91-92` sets `status = "success"` once `write_gp` returns, and `batch.py:59-75` reports a cached artifact as `success`. **Fails** FC7 for those callers. |
| Others | As Option A. |

Verdict: **rejected.** It changes the meaning of `--out` for every caller, and allows an
unlabelled false success in tools that only check file presence.

### Option D: labelled regions without gap bars (omit failing bars entirely)

Deliver only passing bars, concatenated, and list the missing ones in the report.

| Rule | Result |
|---|---|
| FC4 | **Fails.** Bars are dropped and later bars shift position, so the file's bar numbers no longer match the source. That is an unlabelled wrong result for anyone who reads the GP without the report. |

Verdict: **rejected.**

## 3.4 Summary

| Option | FC1 | FC2 | FC3 | FC4 | FC5 | FC6 | FC7 | FC8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 status quo | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ships today; not acceptable |
| A mode + gap bars | ✓ | ✓ | ✓ | ✓ | ✓ | conditional (D3) | ✓ | conditional (in-file marker) | acceptable with conditions |
| **B separate partial artifact** | ✓ | ✓ | ✓ | ✓ | ✓ | conditional (D3) | ✓ (strong) | ✓ | **recommended** |
| C always-on gating | ✓ | ✗ for file-presence callers | ✓ | ✓ | ✓ | conditional | ✗ | conditional | rejected |
| D omit failing bars | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | rejected |

FC5 holds for A, B and C because approximated rhythm can only appear in a non-success artifact
with per-bar labels. None of the accepted options lets an unlabelled wrong result reach the user.

## 3.5 Preconditions that apply to any accepted option

1. The per-bar gate must include candidate-level codes (fixes G9) and must never synthesise
   content with confidence 1.0 (fixes G8).
2. The PDF-only loop (`build_ir.py:1743-1773`) must collect per-bar outcomes instead of raising
   at the first failure (fixes G4). The replay harness shows the product's own assembler
   supports that without changing its checks.
3. `status: success` must mean complete and faithful. Inferred rhythm moves to a non-success
   status (fixes G7).
4. An independent oracle (REQ-0005 acceptance 2) must check the delivered bars against the
   reference GP. For L3-L7, EX2 and CFMWH the private corpus holds reference `.gp` files, so this
   is feasible locally without committing content.
