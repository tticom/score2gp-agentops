# 2. Reason-code taxonomy proposal

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`.

## 2.1 Starting point, as found

REQ-0005 names `docs/diagnostics_failure_taxonomy.md` and "stable per-stage warning and refusal
codes" as the starting point. At the pinned SHA:

- `docs/diagnostics_failure_taxonomy.md` has five **cause** categories for one recogniser (raster
  treble-clef false negatives): stylised fonts, extraneous symbol overlap, raster degradation or
  fragmentation, edge clipping, grand-staff merging. It is a cause taxonomy, not a code catalogue.
- The codes themselves are 190 distinct string literals set via `code=` / `category=` across
  `src/score2gp/**/*.py` (165 snake_case, 25 kebab-case, e.g. `musicxml-grace-skipped` beside
  `musicxml_duration_missing`). No registry, no owner stage, and no test that a code is known.
  Some are templated (`info_{code}` at `pdf.py:1016`, `tabraw-{kind}-not-aligned` at
  `build_ir.py:1797`).
- Severity is free text (`info`, `warning`, `error`, or absent). On the corpus runs 76-223 of each
  run's `warnings.json` items are `info` barline-candidate rejections. These are evidence, not
  shortfalls, yet the HTML report lists them beside the refusal (map E3).
- Many "codes" are really **evidence**: why a candidate was rejected or down-weighted
  (`info_pdf_barline_too_short`, `pdf_string_assignment_nearest_line`). Others are **outcomes**:
  what the product did about a feature (`pdf_only_tab_measure_overcapacity`,
  `musicxml-grace-skipped`). Today both share one namespace.

## 2.2 Proposal: three layers and two axes

Keep every existing engine code. Put two stable layers above them, and add two small closed
vocabularies that every shortfall carries.

```text
user reason   (layer 3, ~16 stable ids, plain language, what the user can do)
   ▲ many-to-one
reason family (layer 2, 8 stable ids, REQ-0005's "why" classes)
   ▲ many-to-one
engine code   (layer 1, the existing literals, registered, never renamed)
   + cause    (optional; e.g. the five clef-failure causes of docs/diagnostics_failure_taxonomy.md)

axes on every shortfall record:  feature kind  ×  disposition
```

### Layer 1: engine codes (existing)

- A single registry (proposed `src/score2gp/reason_codes.py`, or a JSON file plus a loader) lists
  every code with: `stage`, `role` (`evidence` or `shortfall`), `family`, `user_reason`, default
  `feature_kind`, and `introduced_in` version.
- **Stability rule:** a registered code is never renamed or reused. A rename registers the new
  code and keeps the old one as an alias. The 25 kebab-case codes stay valid as aliases of a
  snake_case canonical form.
- **Completeness test:** an AST scan of `src/score2gp` fails if any `code=`/`category=` literal
  (including template prefixes) is not registered. That scan is the same one that produced the
  count of 190 above. It stops new silent codes from appearing.
- `role=evidence` codes never produce a shortfall on their own. They are attached to one as
  evidence. That takes the 76-223 `info` items per run out of the user's headline.

### Layer 2: reason families (REQ-0005 requirement 1, "why")

| Family id | Meaning | REQ-0005 wording |
|---|---|---|
| `missing_observation` | The source does not show what is needed (no rhythm in tab-only PDF, no barline found) | missing observation |
| `ambiguous_evidence` | Evidence exists, but it supports more than one reading | ambiguity |
| `contradictory_evidence` | Two observations or sources disagree | contradiction |
| `unsupported_feature` | Score2GP recognises the feature but cannot convert it yet | unsupported feature |
| `target_limit` | The chosen output target cannot represent it (REQ-0002) | capability limit of the output target |
| `invalid_input` | The input is malformed or not the expected kind | (new) |
| `environment` | A tool, dependency or configuration is missing | (new) |
| `internal_error` | Score2GP failed unexpectedly; this is always a defect | (new; covers G5, G6) |

### Axis A: feature kind (REQ-0005 requirement 1, "what")

`document`, `page`, `system`, `bar`, `note`, `rest`, `duration`, `string_assignment`, `fret`,
`tuning`, `tempo`, `time_signature`, `key_signature`, `technique`, `chord_symbol`,
`section_marker`, `repeat_or_ending`, `lyric`, `text`, `direction`, `articulation`, `ornament`,
`tuplet`, `grace`, `track`.

### Axis B: disposition (REQ-0005 requirement 1, "what was done instead")

| Disposition | Meaning | Allowed in delivered output? |
|---|---|---|
| `refused_document` | Nothing delivered | n/a |
| `refused_region` | That region is left out and marked as a gap; the rest is delivered | Yes, with a visible gap marker |
| `omitted` | The feature is left out; its host region is delivered | Yes, labelled |
| `approximated` | Delivered from inference, not observation (e.g. rhythm from the per-bar event-count rule, map D1) | Only in an output labelled as approximate (see 03) |
| `defaulted` | Delivered using a documented default (e.g. tempo 120) | Yes, labelled |
| `synthesised` | Content created to satisfy a container rule (e.g. rests filling a bar) | Only if labelled; never with confidence 1.0 |
| `preserved_not_written` | Kept in ScoreIR, not written by the target | Yes, labelled |

`approximated`, `defaulted` and `synthesised` exist so that today's silent cases (G7, G8, G13,
G15) get a name. Whether each may appear in delivered output is decided by the fail-closed
analysis in [03](03-best-effort-options.md).

### Layer 3: user reasons (REQ-0005 requirement 2)

Stable ids, with a plain-language sentence and a suggested action. The id is the contract; the
wording may be edited or localised.

| User reason id | Family | Plain-language text (template) | Suggested action |
|---|---|---|---|
| `timing-not-in-source` | missing_observation | "This tab shows which frets to play but not how long to hold them, so exact rhythm can't be read." | Supply a MusicXML sidecar, or accept an approximate-rhythm draft. |
| `rhythm-ambiguous` | ambiguous_evidence | "The note lengths in {location} could be read more than one way." | Check the rhythm here by hand. |
| `bar-overfull` | contradictory_evidence | "The notes read in {location} don't fit the bar's time signature." | Check this bar for a misread note or duration. |
| `layout-unreadable` | missing_observation / ambiguous_evidence | "We couldn't reliably find the staff lines, systems or barlines on {location}." | Use a cleaner PDF, or mark the region. |
| `note-position-uncertain` | ambiguous_evidence | "We found a fret number in {location} but can't tell which string or bar it belongs to." | Check this bar. |
| `fret-unreadable` | ambiguous_evidence | "A fret number in {location} can't be read reliably." | Check the fret numbers here. |
| `notation-symbol-unread` | missing_observation | "A notation symbol in {location} couldn't be recognised." | Check this bar. |
| `feature-not-supported` | unsupported_feature | "{feature} markings ({count}) aren't converted yet." | None; recorded for the backlog. |
| `target-cannot-represent` | target_limit | "The selected Guitar Pro version can't store {feature}." | Choose a newer target (REQ-0002). |
| `sources-disagree` | contradictory_evidence | "The PDF and the sidecar disagree about {location}." | Check which one is right. |
| `input-invalid` | invalid_input | "The file couldn't be read as {expected}." | Check the file. |
| `approximated` | missing_observation | "{feature} in {location} was not read from the notation; it was set by {method}." (`method` is the record's `disposition_detail.method`, e.g. the event-count rule of map D1, so the text states the rule actually applied) | Check before relying on it. |
| `defaulted` | missing_observation | "No {feature} was given, so {default} was used." | Set it if you know it. |
| `setup-required` | environment | "{tool} is needed for this step and isn't available." | Install or configure it. |
| `input-required` | invalid_input | "{input} is needed for this conversion." | Supply it. |
| `internal-error` | internal_error | "Score2GP failed unexpectedly at {stage}. This is a defect, not a problem with your file." | Report it; the run record has the details. |

## 2.3 Mapping the observed codes

Every code observed in the corpus runs, plus the refusal codes on the map. The ~150 codes not
listed here would be mapped when the registry is built; the completeness test enforces that.

| Engine code | Role | Stage | Family | User reason | Feature kind | Disposition |
|---|---|---|---|---|---|---|
| `pdf_only_tab_missing_timing_evidence` | shortfall | timing-gating | missing_observation | timing-not-in-source | duration | refused_document |
| `missing_musicxml` | shortfall | orchestration-gate | missing_observation | input-required | duration | refused_document |
| `pdf_only_tab_measure_overcapacity` | shortfall | measure-assembly | contradictory_evidence | bar-overfull | bar | refused_document today; refused_region proposed |
| `pdf_only_tab_ambiguous_duration` | shortfall | measure-assembly | ambiguous_evidence | rhythm-ambiguous | duration | refused_document today; refused_region proposed |
| `pdf_only_tab_grouping_unsafe` | shortfall | layout-gating | ambiguous_evidence | layout-unreadable | system | refused_document |
| `pdf_bar_box_construction_not_enough_for_build_ir` | evidence | tab-extraction | missing_observation | layout-unreadable | bar | (evidence) |
| `pdf_only_tab_inferred_timing` | shortfall | measure-assembly | missing_observation | approximated | duration | approximated |
| `pdf_editable_draft` | shortfall | measure-assembly | missing_observation | defaulted | duration | defaulted |
| `musicxml-tempo-missing` | shortfall | musicxml-import | missing_observation | defaulted | tempo | defaulted |
| `pdf_string_assignment_missing`, `pdf_string_assignment_outside_staff`, `pdf_candidates_unassigned_to_string`, `pdf_playable_candidate_requires_string_assignment` | evidence (shortfall when the candidate is dropped) | tab-extraction | ambiguous_evidence | note-position-uncertain | string_assignment | omitted |
| `ambiguous_bar_assignment`, `pdf_barlines_ambiguous`, `pdf_bar_box_boundary_ambiguous`, `pdf_candidate_boundary_ambiguous`, `pdf_candidate_on_bar_boundary`, `pdf_candidate_outside_bar`, `pdf_candidate_outside_system`, `pdf_candidates_unassigned_to_system` | evidence | tab-extraction | ambiguous_evidence | note-position-uncertain | note | (evidence) |
| `pdf_fret_optical_bounds_confidence_below_threshold`, `pdf_fret_refinement_not_enough_for_build_ir`, `pdf_fret_digit_symbol_overlap_ambiguous`, `pdf_fret_digits_not_merged_exceeds_max_fret` | evidence | tab-extraction | ambiguous_evidence | fret-unreadable | fret | (evidence) |
| `pdf_notation_rhythm_missing_notehead` | evidence | tab-extraction | missing_observation | notation-symbol-unread | duration | (evidence) |
| `info_pdf_barline_*` (8 codes), `pdf_barline_double_secondary`, `pdf_bar_boxes_constructed`, `pdf_grouping_complete`, `pdf_layout_details`, `pdf_tuning_standard_detected`, `pdf_timing_mapping_not_implemented`, `tab-extraction-incomplete` | evidence | tab-extraction | — | — | — | (not a shortfall) |
| `unsupported-repeat`, `unsupported-ending`, `unsupported-technical-notation` | shortfall | musicxml-import | unsupported_feature | feature-not-supported | repeat_or_ending / technique | omitted |
| `musicxml-grace-skipped`, `musicxml-zero-duration-skipped`, `musicxml-extra-parts-ignored`, `musicxml-harmony-unattached`, `tab-candidate-unused` | shortfall | build-ir | ambiguous_evidence / unsupported_feature | note-position-uncertain / feature-not-supported | grace / note / track / chord_symbol | omitted |
| `gp_write_warning` | shortfall | gp-write | target_limit | target-cannot-represent | technique / track | preserved_not_written |
| `build_ir_failed`, `gp_write_failed` | shortfall | build-ir / gp-write | internal_error | internal-error | document | refused_document |

## 2.4 New engine codes for the silent gaps

Each gap in map 1.8 needs a registered code before it can be recorded. The names below are
proposals.

| Gap | Proposed engine code | Family | User reason | Disposition |
|---|---|---|---|---|
| G1 | keep `pdf_only_tab_grouping_unsafe`; record **all** matching trigger codes as evidence | ambiguous_evidence | layout-unreadable | refused_document |
| G2, G3 | (no new code) carry source location: page, system, source bar | — | — | — |
| G4 | (no new code) a record per failing bar | — | — | — |
| G5 | `sidecar_generation_measure_capacity_invalid` (and a catch-all `unhandled_exception` with stage) | internal_error / contradictory_evidence | internal-error | refused_document |
| G6 | keep the specific code of `HumanReadableConversionError`; `build_ir_failed` only as a fallback | — | — | — |
| G7 | `pdf_only_tab_inferred_timing` gains a per-bar record and an artifact label | missing_observation | approximated | approximated |
| G8 | `measure_fill_rest_synthesised` | missing_observation | approximated | synthesised |
| G9 | promote non-exempt candidate codes to a per-note record when the note is delivered | ambiguous_evidence | fret-unreadable / note-position-uncertain | approximated or omitted |
| G10 | split `gp_write_warning` into `gp_target_technique_unrepresented`, `gp_target_track_shape_unrepresented` | target_limit | target-cannot-represent | preserved_not_written |
| G11 | `section_marker_unplaced`, `repeat_marker_unplaced`, and a distance threshold | ambiguous_evidence | feature-not-supported | omitted |
| G12 | `musicxml_tempo_change_ignored` | unsupported_feature | feature-not-supported | omitted |
| G13 | `musicxml_pitch_incomplete` (refuse the note; no default) | invalid_input | input-invalid | omitted |
| G14 | `musicxml_tuplet_incomplete` | invalid_input | input-invalid | omitted |
| G15 | `sidecar_clef_assumed_treble` | missing_observation | defaulted | defaulted |
| G16 | `pdf_text_candidate_not_converted` (count per kind) | unsupported_feature | feature-not-supported | omitted |
| G17 | `pdf_lyrics_not_converted` | unsupported_feature | feature-not-supported | omitted |
| G18 | `musicxml_direction_not_converted` (subtype: dynamics, words, wedge, pedal) | unsupported_feature | feature-not-supported | omitted |
| G19 | `musicxml_notation_not_converted` (subtype: articulation, fermata, glissando, arpeggiate, ornament) | unsupported_feature | feature-not-supported | omitted |
| G20 | (no new code) the `--pages` filter must keep document-level records | — | — | — |

## 2.5 How the existing cause taxonomy fits

The five categories of `docs/diagnostics_failure_taxonomy.md` are **causes** that explain an
`ambiguous_evidence` or `missing_observation` shortfall in a recognition stage. The proposal
keeps them as an optional `cause` field (`stylised_font`, `symbol_overlap`,
`raster_degradation`, `edge_clipping`, `grand_staff_merge`) and lets other recognisers add
causes the same way. Aggregation (see 04) can then rank causes within a family, which is the
"learning over time" loop REQ-0005 asks for.

## 2.6 Open points for the maintainer

1. Registry form: a Python module (import-time checks, easy AST test) or a JSON file (usable by
   non-Python report tools). Recommendation: Python module, exported to JSON at build time.
2. Whether to canonicalise the 25 kebab-case codes now (aliases kept) or leave them.
3. User-reason wording owner and language (English only for now is assumed).
