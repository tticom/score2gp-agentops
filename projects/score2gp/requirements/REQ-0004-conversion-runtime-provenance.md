# REQ-0004 — Runtime provenance recorded for every conversion

- **Status:** `ACCEPTED`. It was approved as programme work in July 2026 (FS-01, FS-02) and is only partly implemented.
- **Owner:** maintainer (`tticom`)
- **Recorded in the register:** 2026-09-25, at the maintainer's request to check the earlier logging requirement.
- **Task authority backlog item:** PROV-01

## Requirement

Every conversion run, not only corpus smoke runs, records a private-safe provenance record. The record contains:
- product git SHA and dirty state;
- resolved executable and import paths;
- the exact command, sanitised so that no private path or file name appears;
- input classification;
- sidecar path, hash and provenance, where a sidecar is used;
- exit code, refusal code and strict mode.

The structured conversion report (`convert-report.json`) carries the same identifying fields, so a result can always be traced to the exact code that produced it.

## Source

- FS-01 "Runtime Provenance Baseline and Corpus Harness":
  - programme `projects/score2gp/programmes/2026-07-19-runtime-provenance-functional-stabilisation.md` (removed by PLAN-01; readable at commit `9a37927`);
  - prompt `projects/score2gp/prompts/next/0036-fs01-runtime-provenance-baseline.md`.
- FS-02 "Canonical Entry-Point Reconciliation": `projects/score2gp/reports/2026-08-06-fs02-canonical-entry-point-architecture.md` (§3 step 5, §4 constraint 2).

## Implementation state (product `3af1925`)

| Part | State |
|---|---|
| `src/score2gp/runtime_provenance.py` and its tests | Implemented (tticom/score2gp#409, after #376 was reverted by #377) |
| Provenance record on corpus smoke runs | Implemented (`scripts/private_e2e_smoke.py`, `scripts/private_diagnostic_smoke.py`) |
| Provenance record on `score2gp convert` | **Missing**: the CLI does not create the record |
| `convert-report.json` identifying fields | **Partial**: it has status, stage, exit and refusal codes, strict mode, interpreter and import path, and sidecar info, but **no product git SHA or dirty state** |
| General application logging | Not required by FS-01/FS-02. Only `pdf_geometry.py` uses Python `logging` |

## Acceptance criteria

1. `score2gp convert` writes a provenance record for every run, including refused and failed runs, with every field above. A test asserts each field.
2. `convert-report.json` includes the product git SHA and dirty state. A dirty-state failure defaults to dirty, as FS-01 required.
3. No private path, file name or musical content appears in either record. A test with a private-looking input path proves the sanitisation.
