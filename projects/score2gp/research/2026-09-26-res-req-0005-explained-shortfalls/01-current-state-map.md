# 1. Current-state map: where Score2GP refuses, degrades or drops, and what the user learns

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`. Code references are `src/score2gp/<file>:<line>`.
Status tags: **Observed** (corpus or `PUB` run), **Code** (code reading only), **Unverified**.

## 1.1 What "reaches the user" means today

A `convert` run has four user-facing surfaces. Everything else is an intermediate artifact that
users would only find by opening the work directory.

| Surface | Written by | What it carries | Location? |
|---|---|---|---|
| stderr / stdout | `cli.py:1233-1234` (refusals), `cli.py:1054` (missing sidecar), `cli.py:1389-1390` (success) | One `refusal_code:` line and one `recommended_action:` line, or a free-text error line | No |
| `--json-report` (`convert-report.json`) | `cli.py:695-740` | `status`, `stage`, `exit_code`, one `refusal_code`, `recommended_action`, `summary_counts`, `pdf_only_diagnostics` | No |
| `conversion-report.html` | `report.py:17-49` | Flat list of `code: message` for every entry in `warnings.json`, then a raw JSON dump of `summary` | Only if the message text contains it; severity and location fields are not rendered |
| Exit code | `cli.py:651-678` | 1 argument/dependency/generic, 2 PDF layout, 3 MusicXML timing, 4 ASCII or PDF-only unsafe grouping, 5 GP write | No |

Intermediate artifacts: `warnings.json` (all warnings, with location fields when the emitter
set them), `diagnostics.json` (the refusal payload), `tab/tab_raw.json` (per-candidate
`assignment_warnings`), `tab/grouping-diagnostics.html`, `symbol-attachment-diagnostics.html`,
`score.ir.json`.

### Observed reach, 28 `convert` runs (**Observed**)

| Source | Route | Exit | Stage | Refusal code | Location in refusal | warnings.json items (info / warning / error) | Refusal share of HTML items |
|---|---|---|---|---|---|---|---|
| L3 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 179 (177 / 0 / 1) | 1 of 179 |
| L3 | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 179 (177 / 0 / 1) | 1 of 179 |
| L3 | draft | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 179 (177 / 0 / 1) | 1 of 179 |
| L3 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 179 (177 / 1 / 0) | 1 of 179 |
| L4 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 225 (223 / 0 / 1) | 1 of 225 |
| L4 | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 225 (223 / 0 / 1) | 1 of 225 |
| L4 | draft | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 225 (223 / 0 / 1) | 1 of 225 |
| L4 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 225 (223 / 1 / 0) | 1 of 225 |
| L5 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 111 (109 / 0 / 1) | 1 of 111 |
| L5 | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 111 (109 / 0 / 1) | 1 of 111 |
| L5 | draft | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 111 (109 / 0 / 1) | 1 of 111 |
| L5 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 111 (109 / 1 / 0) | 1 of 111 |
| L6 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 93 (91 / 0 / 1) | 1 of 93 |
| L6 | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 93 (91 / 0 / 1) | 1 of 93 |
| L6 | draft | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 93 (91 / 0 / 1) | 1 of 93 |
| L6 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 93 (91 / 1 / 0) | 1 of 93 |
| L7 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 219 (217 / 0 / 1) | 1 of 219 |
| L7 | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 219 (217 / 0 / 1) | 1 of 219 |
| L7 | draft | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 219 (217 / 0 / 1) | 1 of 219 |
| L7 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 219 (217 / 1 / 0) | 1 of 219 |
| EX2 | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 54 (26 / 26 / 1) | 1 of 54 |
| EX2 | pdfonly | 4 | `layout-gating` | `pdf_only_tab_grouping_unsafe` | none | 54 (26 / 26 / 1) | 1 of 54 |
| EX2 | draft | 4 | `layout-gating` | `pdf_only_tab_grouping_unsafe` | none | 54 (26 / 26 / 1) | 1 of 54 |
| EX2 | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 54 (26 / 27 / 0) | 1 of 54 |
| CFMWH | native | 2 | `timing-gating` | `pdf_only_tab_missing_timing_evidence` | n/a | 92 (76 / 14 / 1) | 1 of 92 |
| CFMWH | pdfonly | 2 | `measure-assembly` | `pdf_only_tab_ambiguous_duration` | none | 92 (76 / 14 / 1) | 1 of 92 |
| CFMWH | draft | 2 | `measure-assembly` | `pdf_only_tab_measure_overcapacity` | output bar index | 92 (76 / 14 / 1) | 1 of 92 |
| CFMWH | nosidecar | 1 | `orchestration-gate` | `missing_musicxml` | n/a | 92 (76 / 15 / 0) | 1 of 92 |

In every run the stderr carries exactly one reason (21 runs: `refusal_code` plus
`recommended_action` lines; 7 `nosidecar` runs: one free-text error line and no code). In every
run the HTML report lists the refusal as one item among 54-225 items, most of them `info`, with no
severity shown and no recommended action (`recommended_action` is absent from all 28 HTML files).

## 1.2 Whole-run refusals

| ID | Stage | Where | Code emitted | Location recorded | Reaches user | Evidence | Gap |
|---|---|---|---|---|---|---|---|
| R1 | `orchestration-gate` | `cli.py:1052-1077` | `missing_musicxml` | n/a (whole document) | Code in JSON report and HTML; stderr has free text only | Observed 7/7 | Code not on stderr |
| R2 | `timing-gating` | `build_ir.py:1646-1654` | `pdf_only_tab_missing_timing_evidence` | n/a | Yes, with remediation hint | Observed 7/7 | None; correct fail-closed refusal |
| R3 | `layout-gating` | `build_ir.py:1657-1714` | `pdf_only_tab_grouping_unsafe`; the triggering warning is in `details.refusal_warning_code` | No; only the first matching unsafe code is kept (`build_ir.py:1695-1706`) | Category only in stderr and JSON report; the triggering code is only in the HTML message and `diagnostics.json` | Observed EX2 (trigger `pdf_bar_box_construction_not_enough_for_build_ir`, 3 occurrences) | **G1** first-reason-only |
| R4 | `layout-gating` | `build_ir.py:1724-1730` | `pdf_only_tab_grouping_unsafe` | Candidate id in message only | Message text only | Code | Location is an internal id |
| R5 | `measure-assembly` | `pdf_tab_bar_assembler.py:88-101` | `pdf_only_tab_measure_overcapacity` | `details.bar_index` = sequential **output** bar, not page/system/source bar | Not in stderr or JSON report; HTML message only | Observed (first failure in 6 runs) | **G2** location in a frame the user cannot map to the page |
| R6 | `measure-assembly` | `pdf_tab_event_factory.py:102-128` | `pdf_only_tab_ambiguous_duration` | None (`details` is empty) | Code only | Observed (first failure in 6 runs) | **G3** no location at all |
| R7 | PDF-only bar loop | `build_ir.py:1743-1773` | First bar's code only | — | One code for the whole document | Observed via per-bar replay, table 1.3 | **G4** first failure masks every other failing bar and every deliverable bar |
| R8 | `generate-sidecar` | `notation_omr/musicxml_generator.py:135-136`, not caught in `cli.py:1518-1562` | None: uncaught `ValueError` and traceback | Measure index in exception text only | Traceback; no JSON report, no HTML, no stable code | Observed 7/7 (exit 1, 25 stderr lines, 1 traceback) | **G5** crash without a code |
| R9 | `build-ir` (generic) | `cli.py:1263-1288` | `build_ir_failed` for any non-`BuildIrInputRiskError` exception, including `HumanReadableConversionError` (`scoreir_compiler.py:116,198,203`) | Only inside the message string | Message text | Code | **G6** loses the specific reason |
| R10 | `gp-write` | `cli.py:1316-1341` | `gp_write_failed`, exit 5 | No | Yes | Code | Generic |
| R11 | `musicxml-import` / MusicXML gates | `build_ir.py:1479,1492`; `musicxml.py:1203-1713` | `musicxml_timing_risk`, `musicxml_scoreir_polyphony_gate_refused` and ~40 sub-codes | Per-measure in `musicxml-timing-diagnostics.html` | Code in stderr and JSON report | Code (no sidecar could be produced, see R8) | Not observed |
| R12 | ASCII gates | `build_ir.py:684,906-949`; `ascii_alignment.py` | `ascii_*`, exit 4 | Per-system in `ascii-scoreir-gate-diagnostics.html` | Code | Code (no ASCII source in the corpus set) | Not observed |
| R13 | argument validation | `cli.py:868-963` | `pdf_only_tab_invalid_tempo`, `pdf_not_found`, `sidecar_manifest_*`, `musicxml_not_found` | n/a | Yes | Code | None |

### 1.3 What the single refusal hides: per-bar replay (**Observed** via the harness)

The replay calls the product's `assemble_pdf_tab_bar` for every bar the PDF-only builder iterates:
the bars that hold at least one playable candidate (`build_ir.py:1735-1736`). That set is **not** the
source-bar inventory; §1.3a gives the independent inventory and the bars this table cannot see.
"Assembled" means the product's current per-bar checks pass. It does **not** mean the bar is
correct: see D1-D3.

| Source | Mode | Bars replayed (≥1 playable candidate) | Assembled | Refused (by code) | First failure (= product refusal) | Assembled bars with low-confidence candidates | Assembled bars with synthesised rests |
|---|---|---|---|---|---|---|---|
| L3 | pdf-only | 66 | 24 | `pdf_only_tab_ambiguous_duration` 3, `pdf_only_tab_measure_overcapacity` 39 | `pdf_only_tab_measure_overcapacity` | 3 | 11 |
| L3 | draft | 66 | 15 | `pdf_only_tab_ambiguous_duration` 3, `pdf_only_tab_measure_overcapacity` 48 | `pdf_only_tab_measure_overcapacity` | 0 | 11 |
| L4 | pdf-only | 77 | 25 | `pdf_only_tab_ambiguous_duration` 5, `pdf_only_tab_measure_overcapacity` 47 | `pdf_only_tab_measure_overcapacity` | 9 | 11 |
| L4 | draft | 77 | 13 | `pdf_only_tab_ambiguous_duration` 5, `pdf_only_tab_measure_overcapacity` 59 | `pdf_only_tab_measure_overcapacity` | 1 | 10 |
| L5 | pdf-only | 35 | 18 | `pdf_only_tab_ambiguous_duration` 8, `pdf_only_tab_measure_overcapacity` 9 | `pdf_only_tab_ambiguous_duration` | 18 | 12 |
| L5 | draft | 35 | 0 | `pdf_only_tab_ambiguous_duration` 8, `pdf_only_tab_measure_overcapacity` 27 | `pdf_only_tab_measure_overcapacity` | 0 | 0 |
| L6 | pdf-only | 21 | 6 | `pdf_only_tab_ambiguous_duration` 14, `pdf_only_tab_measure_overcapacity` 1 | `pdf_only_tab_ambiguous_duration` | 6 | 6 |
| L6 | draft | 21 | 0 | `pdf_only_tab_ambiguous_duration` 13, `pdf_only_tab_measure_overcapacity` 8 | `pdf_only_tab_ambiguous_duration` | 0 | 0 |
| L7 | pdf-only | 50 | 13 | `pdf_only_tab_ambiguous_duration` 26, `pdf_only_tab_measure_overcapacity` 11 | `pdf_only_tab_ambiguous_duration` | 10 | 9 |
| L7 | draft | 50 | 4 | `pdf_only_tab_ambiguous_duration` 26, `pdf_only_tab_measure_overcapacity` 20 | `pdf_only_tab_ambiguous_duration` | 1 | 3 |
| EX2 | pdf-only | 16 | 14 | `pdf_only_tab_ambiguous_duration` 2 | layout gate first (`pdf_bar_box_construction_not_enough_for_build_ir`); bar replay only | 14 | 14 |
| EX2 | draft | 16 | 7 | `pdf_only_tab_ambiguous_duration` 2, `pdf_only_tab_measure_overcapacity` 7 | layout gate first; bar replay only | 7 | 7 |
| CFMWH | pdf-only | 10 | 5 | `pdf_only_tab_ambiguous_duration` 5 | `pdf_only_tab_ambiguous_duration` | 5 | 5 |
| CFMWH | draft | 10 | 0 | `pdf_only_tab_ambiguous_duration` 5, `pdf_only_tab_measure_overcapacity` 5 | `pdf_only_tab_measure_overcapacity` | 0 | 0 |

Across the seven sources in pdf-only mode, 105 of the 275 replayed bars assemble, and 170 are
refused under 2 codes. The user is told about one of them. The layout inventory has 277 source
bars: 2 more that the builder never reaches (§1.3a).

### 1.3a Independent source-bar inventory (**Observed**)

The inventory is built from layout geometry only. `evidence/facts_harness.py` (`source_inventory`)
runs the product's own staff and barline detector (`pdf.py:4609`, `_detect_tab_systems`) on each
source PDF, and numbers bars as extraction does: one bar per pair of adjacent barlines, or one for a
system with fewer than two barlines, with a running index across systems and pages
(`pdf.py:2423-2426, 5011-5021`). It uses no candidate. `evidence/coverage_check.py` then compares
the inventory with the bars that hold located candidates and the bars that hold playable ones. Its
self-test fails a candidate-only bar and an empty bar, and shows that an inventory taken from the
replayed bars passes both (the weak oracle this replaces).

| Source | Layout source bars | Replayed (≥1 playable) | Candidate-only (located non-playable items only) | Empty (no located candidate) | Unlocated candidates (by kind) | Conservation today |
|---|---|---|---|---|---|---|
| L3 | 66 | 66 | 0 | 0 | candidate-text 31, technique-text 4 | holds |
| L4 | 77 | 77 | 0 | 0 | candidate-text 43, technique-text 9 | holds |
| L5 | 35 | 35 | 0 | 0 | candidate-text 99, technique-text 9 | holds |
| L6 | 21 | 21 | 0 | 0 | candidate-text 836, technique-text 13 | holds |
| L7 | 50 | 50 | 0 | 0 | candidate-text 21, technique-text 6 | holds |
| EX2 | 17 | 16 | 1 (candidate-text 3) | 0 | candidate-text 8, chord-symbol 2, technique-text 2 | **fails**: 1 bar unaccounted |
| CFMWH | 11 | 10 | 0 | 1 | candidate-text 5, chord-symbol 30, technique-text 22 | **fails**: 1 bar unaccounted |
| Total | 277 | 275 | 1 | 1 | 1140 | 2 bars unaccounted |

No source has a system with fewer than two barlines, so the edge-boundary inference in
`pdf.py:868-905`, which uses playable x positions, did not change any inventory. The PDF-only
builder keys output bars only from playable candidates (`build_ir.py:1735-1736`). So the EX2
candidate-only bar and the CFMWH empty bar get no output bar and no record, and every later
output bar index shifts by one (gap **G21**, row X10). Whether the CFMWH slot is a musical bar
(for example a whole-bar rest) or a layout artefact is **Unverified**; either way nothing
accounts for it. Unlocated candidates are not bar-level. The candidate conservation rule in 04
§4.5 covers them.

## 1.4 Degradations in delivered output

These happen on the success path. None of the seven corpus sources reaches it, so the evidence
is code plus the public `PUB` runs.

| ID | Stage | Where | What happens | Code / label | Location | Reaches user | Evidence | Gap |
|---|---|---|---|---|---|---|---|---|
| D1 | PDF-only timing | `pdf_tab_measure_timing.py:45-66`; `pdf_tab_bar_assembler.py:68-117`; `pdf_tab_event_factory.py:83-133`; `build_ir.py:1776-1782` | Every event in a bar gets one duration chosen only from the **number** of event subgroups N in the bar: N ≤ 8 → eighth, 9-16 → 16th, 17-32 → 32nd, 33-64 → 64th (draft: always quarter). x position sets only order and chord grouping; spacing is not an input. Only a rest symbol or explicit per-candidate duration evidence overrides it. Events are then placed back to back and the remainder filled with rests (D3) | `pdf_only_tab_inferred_timing` once per document | None | Warning in HTML; JSON report says `status: success`, `inferred_rhythm_status: applied` (`cli.py:1349-1354`); the GP file carries only the title "PDF-Only Inferred Score" (`build_ir.py:1806`), with no in-file notice | Observed `PUB` pdfonly: GPIF has no notice text | **G7** degraded output reported as success; artifact not labelled |
| D2 | Editable draft | `pdf_tab_measure_timing.py:55-56`; `build_ir.py:1784-1791` | All durations quarter, defaults for tuning/tempo/time signature | `pdf_editable_draft`; GPIF FreeText notice | None | JSON report `status: success`; GP carries notice | Observed `PUB` draft: notice present in GPIF | Labelled, but status `success` |
| D3 | Measure fill | `pdf_tab_bar_assembler.py:35-54, 119-142` | Rests synthesised to fill the bar (whole-bar rest for an empty bar) with `confidence=1.0` and empty provenance | None | — | No | Observed via replay: 11/24 (L3) … 14/14 (EX2) assembled bars contain them | **G8** synthesised content with full confidence and no label |
| D4 | Candidate quality | `pdf.py:2279-2307` caps confidence at 0.65 for non-exempt `assignment_warnings`; PDF-only gate (`build_ir.py:1665-1706`) checks only document-level codes | Notes from low-confidence candidates pass into output | Candidate-level code in `tab_raw.json` only | Candidate id | No: 18-31 distinct candidate-level codes per source never appear in `warnings.json` or any user surface | Observed: table 1.6; replay: 18 of 18 assembled L5 bars contain such notes | **G9** candidate-level doubt invisible to user |
| D5 | GP write | `gpif.py:2345-2371`; `cli.py:1299-1300` | Unrepresentable technique or track shape not written | Every case shares one code, `gp_write_warning`, with a free-text message | ScoreIR event id | HTML message only | Code | **G10** no stable per-reason code; location is internal |
| D6 | Section / repeat markers | `build_ir.py:3922-3985` | Attached to the nearest bar by x-distance with no threshold; dropped silently when no bar matches | None | — | No | Code; sections detected: L7 7, EX2 1, CFMWH 11 | **G11** silent misplacement or drop |
| D7 | MusicXML tempo | `musicxml.py:2294-2307` | Only the first tempo is read; later tempo changes ignored | None | — | No | Code | **G12** |
| D8 | MusicXML pitch | `musicxml.py:2313-2315` | Missing `step`/`octave` default to `C`/`4` | None | — | No | Code (malformed input only) | **G13** fabricated default |
| D9 | MusicXML tuplet | `musicxml.py:2336-2345` | Incomplete `time-modification` → tuplet dropped | None | — | No | Code | **G14** |
| D10 | Sidecar generation | `cli.py:1528-1532` | OMR runs with `assume_treble_clef=True` | None | — | No | Code | **G15** silent assumption |
| D11 | MusicXML durations | `musicxml.py:2021` | Duration truncated at the barline | `musicxml_duration_truncated_to_measure_boundary` | Measure | Warning | Code | Labelled |

## 1.5 Dropped features

| ID | Stage | Where | What is dropped | Code / label | Reaches user | Evidence | Gap |
|---|---|---|---|---|---|---|---|
| X1 | PDF-only build | `build_ir.py:1716`, `1793-1802` | `candidate-text` candidates are filtered out; only `chord-symbol` and `technique-text` get a `tabraw-<kind>-not-aligned` warning | None for `candidate-text` | No | Observed counts: L3 47, L4 69, L5 175, L6 906, L7 47, EX2 61, CFMWH 13 | **G16** dropped without record (some are non-musical text, but nothing distinguishes them) |
| X2 | PDF extraction → build | `pdf.py:258-266` collects `structural_signals.lyrics`; no consumer in `build_ir.py`; GPIF can write lyrics (`gpif.py:1100`) | Lyrics | None | No | Observed detected-lyric counts: L3 13, L4 20, L5 10, L6 27, L7 60, EX2 12, CFMWH 0 | **G17** detected then silently dropped |
| X3 | MusicXML import | `musicxml.py:1992-2081` handles `attributes`, `note`, `harmony`, `backup`, `forward`, repeat/ending `barline` only | `direction` content (dynamics, words, wedges, pedal), other barline styles, lyrics | None | No | Code | **G18** |
| X4 | MusicXML notations | `musicxml.py:2348-2420` handles `slide`, `slur`, `ornaments/wavy-line`, `technical` | Articulations, fermata, glissando, arpeggiate, other ornaments (trill-mark, mordent, turn, tremolo) | None; only unknown `technical` children get `unsupported-technical-notation` | No | Code | **G19** |
| X5 | MusicXML repeats/endings | `musicxml.py:2066-2081` | Repeat barlines and endings ignored | `unsupported-repeat`, `unsupported-ending` | Warning | Code | Labelled |
| X6 | MusicXML → ScoreIR | `build_ir.py:1565, 2242, 2257, 3799` | Extra parts, grace notes without host, zero-duration notes, unattached harmony | `musicxml-extra-parts-ignored`, `musicxml-grace-skipped`, `musicxml-zero-duration-skipped`, `musicxml-harmony-unattached` | Warning | Code | Labelled |
| X7 | MusicXML path | `build_ir.py:2703` | Tab candidates not matched | `tab-candidate-unused` | Warning | Code | Labelled |
| X8 | Unboxed systems | `build_ir.py:1377-1405` | Systems skipped when `--allow-skip-unboxed-systems` | `pdf_unboxed_system_skipped` | Warning | Code | Labelled, opt-in |
| X10 | PDF-only build | `build_ir.py:1735-1736` keys output bars from playable candidates only | Source bars with no playable candidate, whether candidate-only or empty, get no output bar; later output bars shift | None | No | Observed via the layout inventory (§1.3a): EX2 1 (candidate-only), CFMWH 1 (empty) | **G21** |
| X9 | Warning filter | `cli.py:994-1031` | With `--pages`, every page-less `pdf_*`/`ascii_*` warning is removed from `warnings.json` | None | No | Observed (L5, `--pages` probe): all 16 page-less occurrences (5 codes) removed | **G20** document-level warnings silently dropped |

## 1.6 Candidate-level evidence that never reaches a user surface (**Observed**)

| Source | Candidates | Playable frets | candidate-text | chord-symbol | technique-text | Candidate-level code occurrences / distinct | Distinct candidate-level codes absent from warnings.json | Playable with a non-exempt candidate code |
|---|---|---|---|---|---|---|---|---|
| L3 | 524 | 473 | 47 | 0 | 4 | 1500 / 32 | 30 | 24 |
| L4 | 656 | 556 | 69 | 0 | 31 | 1955 / 32 | 30 | 64 |
| L5 | 636 | 440 | 175 | 0 | 21 | 2482 / 33 | 31 | 229 |
| L6 | 1154 | 235 | 906 | 0 | 13 | 6665 / 32 | 30 | 69 |
| L7 | 696 | 624 | 47 | 12 | 13 | 1940 / 32 | 30 | 131 |
| EX2 | 136 | 60 | 61 | 10 | 5 | 598 / 30 | 22 | 60 |
| CFMWH | 362 | 265 | 13 | 30 | 54 | 959 / 21 | 18 | 147 |

"Non-exempt" means not in the informational list at `pdf.py:2283-2305`.

## 1.7 Reporting defects

| ID | Where | Defect | Evidence |
|---|---|---|---|
| E1 | `cli.py:1256` reads `candidates_count`; `extract_tab` (`pdf.py:228-274`) returns no such key | `summary_counts.total_candidates` is always 0 while `playable_candidates` is non-zero | Observed: 21/21 PDF-only/draft/native refusals report `total_candidates: 0` |
| E2 | `cli.py:846`; `strict` is only recorded (`cli.py:728`) | `--strict/--no-strict` changes nothing in `convert` | Observed: L5 pdfonly probe, same stage, code and exit with either flag |
| E3 | `report.py:17-49` | HTML shows no severity, no location fields, no recommended action, and no headline; the refusal is 1 of 54-225 items. The summary section dumps the whole inspection payload, including extracted page text, so the report cannot be shared or aggregated as-is | Observed 28/28 |
| E4 | `cli.py:1054` | `missing_musicxml` stderr line carries no code | Observed 7/7 |
| E5 | `docs/scoreir-to-gpif-coverage.md` vs `gpif.py:8, 738-753, 1296-1331, 2345-2371` | The doc says the writer warns for tuplets, grace timing, MIDI program/channel, bend, let-ring, palm-mute and grace. The code warns for none of these: the last four are in `SUPPORTED_MINIMAL_TECHNIQUES`, and tuplets and MIDI are written. Whether bend points are written in full is **Unverified** | Code |
| E6 | `docs/diagnostics_failure_taxonomy.md` | Covers only raster treble-clef classifier false negatives. It is not the stage/refusal code catalogue that REQ-0005 assumes. No such catalogue exists: 190 distinct `code=`/`category=` literals are spread across modules (165 snake_case, 25 kebab-case) | Code (regex count over `src/score2gp/**/*.py`) |
| E7 | `build_ir.py:1779` | The `pdf_only_tab_inferred_timing` message says durations are "inferred from PDF horizontal layout positioning". The duration selector takes only the event count (D1), so the one explanation the user gets is wrong | Code; selector boundary probe at the pinned SHA: N = 1, 8 → eighth; 9, 16 → 16th; 17, 32 → 32nd; 33, 64 → 64th; draft → quarter |

## 1.8 Silent gaps, named

A gap is **silent** when the product refuses, degrades or drops something and neither the reason
nor the location reaches a user surface.

| Gap | Summary | Kind | Evidence |
|---|---|---|---|
| G1 | Layout gate reports only the first unsafe code | reason partly hidden | Observed |
| G2 | Over-capacity location is an output bar index, not page/system/bar | location unusable | Observed |
| G3 | Ambiguous-duration refusal has no location | location missing | Observed |
| G4 | First failing bar masks all other failing and all deliverable bars | scale hidden | Observed (replay) |
| G5 | `generate-sidecar` crashes with a traceback and no code | reason uncoded | Observed |
| G6 | Generic `build_ir_failed` swallows the specific reason | reason uncoded | Code |
| G7 | Inferred-rhythm output reported as `success`; GP file not labelled | degrade unlabelled in artifact | Observed (`PUB`) |
| G8 | Synthesised rests carry confidence 1.0 and no label | degrade silent | Observed (replay) |
| G9 | Candidate-level doubt (18-31 codes per source) never reaches the user | reason hidden | Observed |
| G10 | GP-writer omissions share one code, internal location | reason uncoded | Code |
| G11 | Section/repeat markers misplaced or dropped without record | drop silent | Code |
| G12 | MusicXML tempo changes after the first are ignored | drop silent | Code |
| G13 | MusicXML missing step/octave default to C4 | fabricated default | Code |
| G14 | Incomplete MusicXML tuplet dropped | drop silent | Code |
| G15 | Sidecar OMR assumes treble clef | assumption silent | Code |
| G16 | `candidate-text` candidates dropped in PDF-only build | drop silent | Observed counts |
| G17 | Detected lyrics dropped | drop silent | Observed counts |
| G18 | MusicXML `direction` content and other barline styles ignored | drop silent | Code |
| G19 | MusicXML articulations, fermata, glissando, arpeggiate, most ornaments ignored | drop silent | Code |
| G20 | `--pages` removes document-level warnings | record lost | Observed |
| G21 | PDF-only build drops source bars with no playable candidate; output bar numbers shift | drop silent | Observed (layout inventory, §1.3a) |

Not claimed: this map covers the `convert` and `generate-sidecar` routes and the modules they
call. The standalone notation export commands (`cli.py:743-835, 1409-1497`), `batch`, `omr`
and `diagnose` were not mapped. No MusicXML or ASCII route could be exercised on this corpus set,
so rows R11, R12, D7-D9, D11, X3-X8 are code-only.
