# 6. Status proposal

## 6.1 Recommendation

Move REQ-0005 from `PROPOSED` to **`RESEARCHED`** (done in this PR: the requirement file and
the register). **Recommend `ACCEPTED`** once the maintainer has answered the decisions in §6.4.
This PR does not set `ACCEPTED`; only the maintainer can.

Grounds:

- All four open questions have evidence-backed answers (§6.2).
- The draft acceptance criteria are rewritten as testable criteria in
  [REQ-0005](../../requirements/REQ-0005-explained-shortfall-reporting.md#acceptance), each with
  the test that decides it (§6.3).
- The requirement is feasible without weakening the fail-closed rules. Option B in 03 meets all
  eight rules, with one condition (the GP gap-bar representation, decision D3).
- The research found 21 silent gaps (map §1.8). Several of them already break existing fail-closed
  rules in shipped code, independent of REQ-0005: G7 (inferred rhythm reported as `success`), G8
  (synthesised rests at confidence 1.0) and G5 (sidecar crash without a code). That raises the
  requirement's value. It does not decide its priority.

## 6.2 Answers to the open questions

| # | Open question | Answer | Where |
|---|---|---|---|
| 1 | How best effort coexists with strict refusal | A complete-or-nothing primary `--out`, plus a separate labelled `<name>.partial.gp` and report, run status `partial`, non-success exit. Per-bar gating (Option A) is acceptable under conditions. Always-on gating (C) and omitting failing bars (D) are rejected. | [03](03-best-effort-options.md) |
| 2 | Extend the existing codes or define a user-facing layer | Both. Register and freeze the existing engine codes (a stability rule and a completeness test), and add two stable layers above them: 8 reason families and 17 user reasons. Every shortfall also carries a feature kind and a disposition. `docs/diagnostics_failure_taxonomy.md` is a cause taxonomy for one recogniser and becomes an optional `cause` field. | [02](02-reason-code-taxonomy.md) |
| 3 | Where records live, how they are aggregated privately | Private per-run `shortfall-records.json` in the work directory. A sanitised counts-and-codes aggregate, with an enforced privacy validator, is appended to a local ledger. A ranked rollup (bars affected, then sources) may be committed to agentops and feeds backlog proposals. | [04](04-shortfall-record-and-aggregation.md) |
| 4 | What the report looks like, which formats | Headline status and coverage, then "not converted" by user reason with source locations, then "converted but check", then "not supported yet", then support details. Rendered as Markdown, HTML and JSON from the same records. | [05](05-report-mockup.md) |

## 6.3 Traceability: acceptance criteria, gaps and evidence

The criteria text is in the requirement file. This table records what each one closes and what
evidence motivated it.

| Criterion (REQ-0005) | Closes gaps | Motivating evidence |
|---|---|---|
| A1 Records exist and are complete | G1, G4, G6, G9, G11-G19, G21 | Map §1.3-1.6: one code per run; 18-31 candidate codes per source never reach the user; the layout inventory finds 2 source bars that no bar-keyed check sees (§1.3a) |
| A2 Every record is located in the source frame | G2, G3, G20 | Map R5, R6, X9 |
| A3 Every record has a registered reason; no uncoded failure | G5, G6, G10, E6 | 190 unregistered literals; the `generate-sidecar` traceback on 7/7 sources |
| A4 Status honesty | G7, G8, E1, E2 | `PUB` success with inferred rhythm; `total_candidates` 0 on 21/21 runs; `--strict` no-op |
| A5 Best-effort output, checked by an independent oracle | G4, G7, G8, G21 | Replay: 105 of 275 replayed bars assemble, 17 clean; layout inventory 277 |
| A6 User report | E3, E4 | The refusal is 1 of 54-225 HTML items; no location, severity or action shown |
| A7 Corpus aggregate ranks reasons | — | Aggregate preview (04 §4.6) |
| A8 Privacy | — | Evidence validator used in this research |

## 6.4 Decisions left to the maintainer

These are also listed in the requirement file. Each is a choice the research cannot make, with a
recommendation.

| # | Decision | Recommendation |
|---|---|---|
| D1 | Best-effort delivery option: B (separate partial artifact) or A (mode switch, partial GP in `--out`) | B |
| D2 | Whether `--pdf-only-tab` and `--editable-draft` runs with inferred or defaulted rhythm change from `success` to `partial` (a CLI contract change that fixes G7) | Yes; the L3 contract already forbids layout-inferred rhythm in a successful result |
| D3 | How a gap bar is represented in GP, and who verifies it opens in Guitar Pro without being repaired into a rest (**Unverified** today) | Maintainer verifies in the pinned Guitar Pro version before delivery starts |
| D4 | Whether a labelled omission of an unsupported feature (lyrics, text, dynamics) blocks `success` | Blocks `success` (FC2 reading), with a per-feature allowlist the maintainer can grant later |
| D5 | Where committed rollups live, and whether the local ledger is on by default | `projects/score2gp/shortfalls/` in agentops; ledger on by default, local only; nothing sent off the machine |
| D6 | Registry form (Python module or JSON) and whether to canonicalise the 25 kebab-case codes now | Python module exported to JSON; keep kebab codes as aliases |
| D7 | The independent oracle for A5 (the production `compare.py` shares the product's model) | A GP reader that does not import `score2gp`, run locally against the corpus reference `.gp` files |
| D8 | Order of delivery | First the fail-closed defects (G5, G7, G8), then collection and location (G4, G2, G3, G9), then the report, then aggregation |
| D9 | Whether correcting the stale `docs/scoreir-to-gpif-coverage.md` and the mis-described taxonomy doc is part of this requirement | Yes, as a small documentation task |
| D10 | Priority relative to REQ-0001 L3-NATIVE work | Maintainer's call; the fail-closed defects in D8 are arguably REQ-0001 work already |

## 6.5 Limits of this research

- No corpus source reaches the success path, and no MusicXML or ASCII route could run
  (`generate-sidecar` crashes on 7/7 sources). The MusicXML-path rows of the map are code-only.
- The per-bar replay reproduces the product's assembler, not a future gated builder. Its counts
  are upper bounds on what per-bar gating could deliver today.
- Bend-point completeness in the GP writer and GP gap-bar behaviour are **Unverified**.
- The standalone notation-export commands, `batch`, `omr` and `diagnose` were not mapped.
