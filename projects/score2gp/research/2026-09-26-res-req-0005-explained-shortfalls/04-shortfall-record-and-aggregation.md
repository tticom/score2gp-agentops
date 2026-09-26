# 4. Shortfall record and aggregation design

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`. Vocabularies (family, user reason,
feature kind, disposition) are from [02](02-reason-code-taxonomy.md).

## 4.1 Principles

1. **One record per shortfall occurrence.** "Occurrence" means one feature at one location with
   one reason. Evidence codes attach to a record; they do not create records.
2. **Collected, not raised.** Stages append records to a per-run collector instead of raising on
   the first problem. A stage may still stop the run; its stopping record then carries
   `disposition: refused_document` and the collector is flushed first. This fixes G4 and keeps
   the stage's fail-closed decision where it is.
3. **Completeness is testable.** Every place that drops, degrades or refuses must emit a record
   with a registered engine code. The registry test (02 §2.2) plus a conservation test (§4.5)
   enforce this.
4. **Two tiers.** A **private run record** has everything needed to locate and explain the
   shortfall to the user, and never leaves the user's machine or the local work directory. A
   **sanitised aggregate** holds counts and codes only, and is the only form that may be
   committed or sent anywhere.

## 4.2 Private run record (per run, local)

File: `<work-dir>/shortfall-records.json`, written on every run, success or not.

```json
{
  "schema_version": "shortfall-records.v1",
  "run": {
    "run_id": "<uuid>",
    "provenance_ref": "<path or id of the REQ-0004 runtime provenance record>",
    "product_version": "<version>",
    "product_sha": "<40-hex>",
    "input_sha256": "<64-hex>",
    "route": "pdf-only | editable-draft | musicxml-sidecar | ascii-alignment",
    "target": "gp7 | gp8 | ...",
    "status": "success | partial | refused | failed",
    "source_bar_count": 0,
    "delivered_bar_count": 0
  },
  "records": [
    {
      "id": "<run_id>:<seq>",
      "feature_kind": "duration",
      "location": {
        "precision": "document | page | system | bar | beat | note",
        "page": 1, "system": 1, "staff": 1, "source_bar": 1,
        "beat": "3/8",
        "output_bar": 12,
        "bbox": [0, 0, 0, 0]
      },
      "reason": {
        "engine_code": "pdf_only_tab_ambiguous_duration",
        "family": "ambiguous_evidence",
        "user_reason": "rhythm-ambiguous",
        "stage": "measure-assembly",
        "cause": null
      },
      "evidence": [
        {"engine_code": "pdf_notation_rhythm_missing_notehead", "count": 2, "candidate_ids": ["..."]}
      ],
      "disposition": "refused_region",
      "disposition_detail": {"method": null, "default_value_policy": null},
      "impact": {"notes": 4, "bars": 1},
      "message": "<developer message, private>"
    }
  ]
}
```

Field rules:

- `location.precision` is mandatory and says how precise the location is. A record with
  `precision: document` is allowed only for document-level reasons (for example
  `timing-not-in-source`). The test in §4.5 fails a bar-level engine code with document precision,
  which catches G2 and G3.
- `location.source_bar` is the source-frame bar (page/system/bar), not the output index. G2 is the
  case where only an output index exists today. `output_bar` is added when the region is delivered.
- `bbox`, `candidate_ids` and `message` may contain coordinates, internal ids or extracted text.
  They exist only in the private tier.
- `provenance_ref` links to the REQ-0004 record. PROV-01 is not yet wired into `convert`: no
  `runtime_provenance` import in `cli.py` at the pinned SHA. Until it is, the run block repeats the
  fields `convert-report.json` already records.
- The REQ-0002 output target is part of `run`, so `target_limit` records are attributed to the
  target that caused them.

Where it lives: the work directory, beside `convert-report.json`, which gains
`shortfall_summary` (counts by user reason and disposition) and `shortfall_records_path`.

## 4.3 Sanitised aggregate (committable)

A pure function `sanitise(records) -> aggregate` keeps only these fields:

| Kept | Dropped |
|---|---|
| `schema_version`, `product_version`, `product_sha`, `route`, `target`, `status` | `run_id`, `provenance_ref` paths, `input_sha256` (replaced, see below) |
| per (`engine_code`, `family`, `user_reason`, `feature_kind`, `disposition`, `stage`, `location.precision`, `cause`): `occurrences`, `bars_affected`, `notes_affected` | `location.page/system/bar/beat/bbox`, `candidate_ids`, `message`, `evidence[].candidate_ids` |
| `source_bar_count`, `delivered_bar_count` | any free text |
| `source_key`: a keyed hash (HMAC) of `input_sha256` with a workspace-local secret, so runs of the same source group together but the source cannot be identified from the aggregate | the raw `input_sha256` |

The aggregate for a run is a list of counts under code tuples. It has no location finer than
`precision`. It contains no text, so it cannot carry musical content or coordinates.

**Privacy guard (enforced):** a validator rejects any aggregate that has a key outside the
allowlist, a string value that does not match the code pattern `^[A-Za-z0-9_:.\-]+$`, or a number
that is not a non-negative integer. This is the same check applied to
`evidence/run-matrix-facts.json` in this research.

## 4.4 Aggregation across runs and sources (REQ-0005 requirement 4)

- **Ledger.** Each run appends its sanitised aggregate as one line to a local ledger
  (`<workspace>/shortfalls/ledger.jsonl`). The ledger is append-only and deduplicated by
  `(source_key, product_sha, route, target)`.
- **Rollup.** `score2gp shortfalls rollup` (proposed) groups ledger lines by reason tuple and
  reports, for each tuple:
  - `occurrences`: total records;
  - `sources_affected`: distinct `source_key`;
  - `bars_affected`: bars not delivered or delivered degraded because of this reason; a
    `refused_document` record counts every source bar;
  - `latest_product_sha`: so a reason that a fix removed shows as gone.
- **Ranking.** Default order: `bars_affected` descending, then `sources_affected`, then
  `occurrences`. `bars_affected` is the proposed "cost": the amount of the user's score the
  reason kept out or degraded.
- **Committed form.** The rollup, which holds counts and codes only, may be committed to
  `score2gp-agentops` (proposed location `projects/score2gp/shortfalls/<date>-rollup.json`) and
  cited by governance when proposing backlog items. That location is a maintainer decision (D5).
- **Backlog feed.** Governance reads the latest committed rollup and, for the top N reasons that
  have no open task, drafts backlog candidates in `ORCHESTRATION_STATE.json`. The maintainer
  still promotes them; the rollup only proposes.

## 4.5 Tests that make "no gap is silent" checkable

| Test | What it proves |
|---|---|
| Registry completeness (AST scan) | Every emitted `code=`/`category=` literal is registered with family, user reason, stage and role. |
| Conservation, per route, on public fixtures | `source_bar_count == delivered_clean_bars + bars covered by records with disposition in {refused_region, approximated, synthesised, omitted}`, and every input candidate is either consumed by a delivered note or referenced by a record. `source_bar_count` must come from an inventory derived **independently** of the candidates being checked: layout geometry (staff lines and barlines), as `evidence/facts_harness.py` `source_inventory` does. An inventory built from the playable candidates cannot see a candidate-only or empty bar (map §1.3a). Negative controls: a fixture bar with only non-playable text and a fixture bar with no candidates must each fail the test until a record covers it (`evidence/coverage_check.py` self-test). Today `candidate-text` (G16), lyrics (G17) and bars with no playable candidate (G21) break this. |
| Location precision | No bar-level engine code is recorded with `precision: document` (G2, G3). |
| No confident synthesis | No delivered event has `confidence == 1.0` with empty provenance unless it has a `synthesised` record (G8). |
| Status honesty | `status == success` implies no record with disposition other than `defaulted` (U10 defaults only); `approximated` or `synthesised` imply `partial` (G7). |
| Privacy guard | `sanitise()` output passes the validator for every public fixture and a seeded adversarial record containing text and coordinates. |
| Pages filter | With `--pages`, document-level records survive (G20). |

The conservation test is the one that proves "no gap is silent" (REQ-0005 draft acceptance 1).
It needs public fixtures with known unsupported features; fixture construction is a delivery
task, not part of this research.

## 4.6 Preview: a real corpus aggregate

`evidence/aggregate_preview.py` builds this table from `evidence/run-matrix-facts.json` alone,
which is counts only. It uses the proposed mapping and the pdf-only replay. It is a preview of
the rollup, not product output. Totals: 7 sources, 277 source bars from the independent layout
inventory (275 reached by the replay).

| Rank | User reason | Family | Engine code | Disposition | Level | Occurrences | Bars affected | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | `timing-not-in-source` | missing_observation | `pdf_only_tab_missing_timing_evidence` | refused_document | document | 7 | 277 | 7 |
| 2 | `input-required` | invalid_input | `missing_musicxml` | refused_document | document | 7 | 277 | 7 |
| 3 | `internal-error` | internal_error | `sidecar_generation_measure_capacity_invalid` (proposed) | refused_document | document | 7 | 277 | 7 |
| 4 | `bar-overfull` | contradictory_evidence | `pdf_only_tab_measure_overcapacity` | refused_region (proposed) | bar | 107 | 107 | 5 |
| 5 | `approximated` | missing_observation | `pdf_only_tab_inferred_timing` | approximated | bar | 105 | 105 | 7 |
| 6 | `approximated` | missing_observation | `measure_fill_rest_synthesised` (proposed) | synthesised | bar | 68 | 68 | 7 |
| 7 | `fret-unreadable` / `note-position-uncertain` | ambiguous_evidence | non-exempt candidate-level codes | approximated or omitted (proposed) | note | 724 | 65 | 7 |
| 8 | `rhythm-ambiguous` | ambiguous_evidence | `pdf_only_tab_ambiguous_duration` | refused_region (proposed) | bar | 63 | 63 | 7 |
| 9 | `layout-unreadable` | ambiguous_evidence | `pdf_only_tab_grouping_unsafe` | refused_document | document | 1 | 17 | 1 |
| 10 | `bar-content-not-found` | missing_observation | `pdf_only_tab_source_bar_without_playable_candidate` (proposed) | refused_region | bar | 2 | 2 | 2 |
| 11 | `feature-not-supported` | unsupported_feature | `pdf_text_candidate_not_converted` (proposed) | omitted | feature | 1318 | — | 7 |
| 12 | `feature-not-supported` | unsupported_feature | `pdf_lyrics_not_converted` (proposed) | omitted | feature | 142 | — | 6 |

What it already says, from real data: without a sidecar, the three document-level reasons block
everything. Behind them, over-full bars (rank 4) and ambiguous durations (rank 8) are the two bar
reasons to fix, and over-full bars cost more. Rank 10 exists only because the source bars now come
from the layout inventory: 2 bars that the playable-candidate replay never sees. The count of 1318
dropped text candidates shows why G16 needs its own record: without one, nobody can tell how much of that text is musical.
Rows 1-3 overlap: each is a different route over the same 277 bars. A real rollup would keep
routes apart (`route` is part of the key); the preview merges them to stay small.
