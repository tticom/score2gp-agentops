# 5. Report mock-up, generated from a real run's records

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`.

## 5.1 How this was produced

- **Run:** L5 (`Lesson-5.pdf`), route `pdfonly` (`convert --pdf-only-tab`), one of the 35 runs
  in the README. Work directory `<product>/work/res-req-0005/L5/pdfonly/` (gitignored).
- **Generator:** `evidence/report_mockup.py <product> <run-work-dir>`, run with the product venv.
  It reads the run's `tab/tab_raw.json` and `convert-report.json` and replays every bar through
  the product's `assemble_pdf_tab_bar`. From that it builds shortfall records in the shape of
  design 04 and renders the report proposed for Option B of 03.
- **Redaction:** the committed rendering below is the default (redacted) mode. Page, system and
  bar values are replaced by counts and a placeholder. The same command with `--private` prints
  the real locations. It was run once, writing only to the gitignored work directory, to check
  that the private path works.
- **What is real and what is proposed:** every count, code and stage below comes from the run.
  The headline status (`partial`), the partial artifact, the user-reason ids and the wording are
  the proposals from 02 and 03. Today the product shows only the one line quoted in the report.

## 5.2 The report (Markdown rendering; HTML would use the same sections)

---

### Score2GP conversion report — PARTIAL

**18 of 35 bars converted, with estimated rhythm. 17 bars not converted.** The file you asked for was not written. A labelled partial file was written beside it: `<name>.partial.gp`.

> Today (product at the pinned SHA) this same run shows only: `refusal_code: pdf_only_tab_ambiguous_duration` at stage `measure-assembly`, exit 2, with no location and no count of affected bars.

#### Not converted

| Why (user reason) | What it means | Bars | Where | What you can do |
|---|---|---|---|---|
| `bar-overfull` | The notes read in these bars don't fit the bar's time signature, so at least one note or length was misread. | 9 | 9 bars on 3 page(s), 6 system(s) — listed as "page ‹p›, system ‹s›, bar ‹b›" in the private report | Check these bars for a misread note or duration. |
| `rhythm-ambiguous` | The note lengths in these bars could be read more than one way. | 8 | 8 bars on 3 page(s), 5 system(s) — listed as "page ‹p›, system ‹s›, bar ‹b›" in the private report | Check the rhythm in these bars by hand. |

#### Converted, but check before relying on it

| Why (user reason) | What it means | Bars | Notes |
|---|---|---|---|
| `approximated` | Rhythm in these bars was not read from the notation. Every note or chord in a bar was given the same length, chosen only from how many there are in the bar: up to 8 become eighth notes, 9 to 16 become sixteenths, 17 to 32 become 32nds. Where they are placed on the page does not change their length. | 18 | 211 |
| `approximated` | Rests were added to fill these bars to the time signature. | 12 | — |
| `fret-unreadable` | Some fret numbers could not be read reliably. | 12 | 41 |
| `notation-symbol-unread` | A rhythm symbol above the tab could not be recognised. | 18 | 211 |

#### Not converted at all (feature not supported yet)

| Feature | Items | Why |
|---|---|---|
| Text on the page (unclassified) | 175 | `feature-not-supported` |
| Lyrics | 10 | `feature-not-supported` |

#### Details for support

Events in converted bars, by how their duration was chosen: count rule (16th 118, eighth 61); explicit duration evidence 0; rest symbols 0.

| Engine code | Stage | Family | Records | Evidence codes (count) |
|---|---|---|---|---|
| `candidate:fret-unreadable` | `tab-extraction` | ambiguous_evidence | 12 | `pdf_fret_digits_not_merged_exceeds_max_fret` 41 |
| `candidate:notation-symbol-unread` | `tab-extraction` | ambiguous_evidence | 18 | `pdf_notation_rhythm_missing_notehead` 211 |
| `measure_fill_rest_synthesised` | `measure-assembly` | missing_observation | 12 | — |
| `pdf_lyrics_not_converted` | `build-ir` | unsupported_feature | 1 | — |
| `pdf_only_tab_ambiguous_duration` | `measure-assembly` | ambiguous_evidence | 8 | `pdf_fret_digits_not_merged_exceeds_max_fret` 1 |
| `pdf_only_tab_inferred_timing` | `measure-assembly` | missing_observation | 18 | — |
| `pdf_only_tab_measure_overcapacity` | `measure-assembly` | contradictory_evidence | 9 | `pdf_fret_digits_not_merged_exceeds_max_fret` 17 |
| `pdf_text_candidate_not_converted` | `build-ir` | unsupported_feature | 1 | — |

#### Run

- Product SHA: `3af19250bcc716ccc8a3e2b2102db897f78e56e5`; route: `pdf-only`; target: GP7
- Status: `partial` (proposed); today: `refused` / exit 2
- Records: 79 (private, `shortfall-records.json`); sanitised aggregate: counts and codes only

---

## 5.3 Design notes on the mock-up

1. **Headline first.** Status and one sentence: how much was delivered and how much was not.
   Today's HTML report puts the refusal at item 111 of 111 (map §1.1).
2. **Grouped by user reason, not by engine code.** Engine codes stay available under "Details
   for support". Evidence-role codes (the 109 `info` items in this run's `warnings.json`) are not
   shown to the user; they appear only as evidence counts.
3. **Every row has a location.** In the private report, "Where" lists page, system and source bar
   for each bar (the source frame, not the output index; see G2). Bars are listed, not just
   counted, because the user's next step is to look at them.
4. **Degraded content is separate from missing content.** "Converted, but check" lists
   approximated rhythm, synthesised rests and uncertain readings. Today none of these is
   reported (G7-G9).
5. **Formats.** The same records render to Markdown (terminal and PR evidence), HTML (users),
   and JSON (`shortfall-records.json`, tools). The sanitised aggregate is a fourth, counts-only
   rendering (design 04 §4.3).
6. **The explanation states the rule actually applied.** The `approximated` rhythm row names the
   product's event-count rule (map D1: `pdf_tab_measure_timing.py:45-66`, called at
   `pdf_tab_bar_assembler.py:78`), not the product's own warning text, which wrongly says
   "horizontal layout positioning" (map E7). The generator derives each delivered bar's methods by
   calling the product's grouper and selector (`duration_methods` in `evidence/report_mockup.py`),
   and stores them in the record's `disposition_detail.method`. In this run all 179 events in
   the 18 delivered bars came from the count rule: 61 eighths (bars with at most 8 events) and 118
   sixteenths (bars with 9-16 events). The rest-symbol and duration-mark exception is printed only
   when it occurs.
7. **Limitation:** "notation-symbol-unread" appears on all 211 delivered notes, because in this
   run every fret candidate carries `pdf_notation_rhythm_missing_notehead`. A real report would
   fold that into the `approximated` rhythm row rather than list it twice. The generator keeps
   the rows separate here so the counts can be checked against the evidence.
