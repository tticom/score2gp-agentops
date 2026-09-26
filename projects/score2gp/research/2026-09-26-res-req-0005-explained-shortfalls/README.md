# RES-REQ-0005 — Explained shortfalls and best-effort output (research)

- **Task:** `RES-REQ-0005` (authority task record in `projects/score2gp/ORCHESTRATION_STATE.json`)
- **Requirement:** [REQ-0005](../../requirements/REQ-0005-explained-shortfall-reporting.md)
- **Author identity:** `tticom-automation` (implementation role)
- **Date:** 2026-09-26

## Pinned revisions

| Repository | SHA | How obtained |
|---|---|---|
| `tticom/score2gp` (studied, read-only) | `3af19250bcc716ccc8a3e2b2102db897f78e56e5` | `git -C ../score2gp rev-parse HEAD`; equal to `origin/main`; product worktree clean; reflog shows this HEAD before the corpus runs started |
| `tticom/score2gp-agentops` (base) | `9c5f76168979c92ea710519879e5c6408f3e9902` | `main` at task start |

All code references in this directory (`file.py:line`) are to `src/score2gp/` at the product SHA above,
unless a `docs/` or `tests/` path is given.

## Deliverables

| # | Deliverable (task prompt) | File |
|---|---|---|
| 1 | Current-state map, silent gaps named | [01-current-state-map.md](01-current-state-map.md) |
| 2 | Reason-code taxonomy proposal | [02-reason-code-taxonomy.md](02-reason-code-taxonomy.md) |
| 3 | Best-effort delivery options vs fail-closed rules | [03-best-effort-options.md](03-best-effort-options.md) |
| 4 | Shortfall record and aggregation design | [04-shortfall-record-and-aggregation.md](04-shortfall-record-and-aggregation.md) |
| 5 | Report mock-up from a real run's records | [05-report-mockup.md](05-report-mockup.md) |
| 6 | Status proposal, testable criteria, maintainer decisions | [06-status-proposal.md](06-status-proposal.md) |

## Method

1. **Code reading** at the pinned product SHA: `cli.py` (convert orchestration and user-facing
   surfaces), `report.py`, `build_ir.py`, `pdf.py`, `pdf_tab_*`, `musicxml.py`, `gpif.py`,
   `notation_omr/musicxml_generator.py`, and `docs/`.
2. **Real runs** on the seven corpus sources named by the task, using the product venv
   (`<product>/.venv/Scripts/python.exe -m score2gp.cli`), import path
   `<product>/src/score2gp` (recorded in every `convert-report.json`). Raw outputs stay in the
   gitignored `<product>/work/res-req-0005/<source>/<route>/`.
3. **Per-bar replay** (`evidence/facts_harness.py`): the PDF-only builder stops at the first bad
   bar (`build_ir.py:1743-1773`). The harness calls the product's own `assemble_pdf_tab_bar` for
   every bar and records each outcome. It is a research simulation, not product behaviour. Its first
   failure code equals the product's actual refusal code in all 12 routes that reached
   measure assembly, which is the check that it replays the product faithfully.
4. **Counts-only evidence**: `evidence/run-matrix-facts.json` holds counts, codes, stage names and
   flags. `evidence/corpus-aggregate-preview.json` is derived from it alone by
   `evidence/aggregate_preview.py`. Every key and string value in both files matches
   `^[A-Za-z0-9_:.\-|<>]+$` (`<none>` marks a warning with no severity), and every number is a
   count or an exit code.

### Sources

| ID | Private corpus file (file-level identifier only) |
|---|---|
| L3 | `Lesson-3.pdf` |
| L4 | `Lesson-4.pdf` |
| L5 | `Lesson-5.pdf` |
| L6 | `Lesson-6.pdf` |
| L7 | `Lesson-7.pdf` |
| EX2 | `Ex 2 Hands Up.pdf` |
| CFMWH | `Can't Find My Way Home (open chord shenanigans).pdf` |

A public fixture, `tests/fixtures/pdf/generated_pdf_fret_grouped_success.pdf` (id `PUB`), was also
run through the `pdfonly` and `draft` routes. None of the seven corpus sources gets past a refusal,
so `PUB` is the only observed success path.

### Routes (all `convert` runs also pass `--out`, `--work-dir`, `--json-report`)

| Route | Command |
|---|---|
| `native` | `convert --pdf <src> --pdf-only-tab --require-precise-timing --strict` |
| `pdfonly` | `convert --pdf <src> --pdf-only-tab` |
| `draft` | `convert --pdf <src> --editable-draft` |
| `nosidecar` | `convert --pdf <src>` (no `--musicxml`) |
| `sidecar` | `generate-sidecar --pdf <src> --out <mx>`, then `convert --musicxml <mx>` if written |

### Observed outcome summary (35 runs)

| Route | Sources | Outcome |
|---|---|---|
| `native` | 7/7 | exit 2, `timing-gating`, `pdf_only_tab_missing_timing_evidence` |
| `pdfonly` | 7/7 | refused: 2× `pdf_only_tab_measure_overcapacity` (L3, L4), 4× `pdf_only_tab_ambiguous_duration` (L5, L6, L7, CFMWH), 1× `pdf_only_tab_grouping_unsafe` exit 4 (EX2) |
| `draft` | 7/7 | refused: 4× `pdf_only_tab_measure_overcapacity` (L3, L4, L5, CFMWH), 2× `pdf_only_tab_ambiguous_duration` (L6, L7), 1× `pdf_only_tab_grouping_unsafe` (EX2) |
| `nosidecar` | 7/7 | exit 1, `orchestration-gate`, `missing_musicxml` |
| `sidecar` | 7/7 | `generate-sidecar` exit 1 with an uncaught `ValueError` traceback; no sidecar written; `convert` not reached |

No corpus run wrote a GP file. See the map for what each outcome tells the user.

## Privacy

Committed files hold counts, codes, stage names, file-level identifiers and code references only.
No fret, pitch, rhythm, text, coordinate, bar-content or excerpt of a private file is committed.
Where a location is needed in the mock-up, it is shown as a count of distinct locations, or as a
placeholder that names the field.

## Verification status legend

- **Observed**: backed by a run listed above (counts in `evidence/run-matrix-facts.json`).
- **Code**: backed by a code reference at the pinned SHA; not exercised by the corpus runs.
- **Unverified**: inferred; needs a run or test before it is relied on.
