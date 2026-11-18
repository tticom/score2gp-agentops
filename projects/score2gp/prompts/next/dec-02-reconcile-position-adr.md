# DEC-02 — Reconcile ADR-006 and product ADR-0004 into one position ADR

- **Kind:** decision (authority item `DEC-02`, promoted to a task 2026-11-18 on the maintainer's instruction)
- **Repository:** `tticom/score2gp-agentops` (records only); read-only inspection of `tticom/score2gp`
- **Requirement:** `REQ-0001:U04`
- **Maintainer position (2026-09-25):** "Position is the TAB's super power."

## Goal

Two accepted records contradict each other about where string and fret positions come from:

- **ADR-006** (`projects/score2gp/ARCHITECTURE_DECISIONS.md`, approved 2026-08-13) forbids inferring biomechanical hand positions. Output must rest on explicit TAB evidence; notes without explicit fretboard ownership are dropped or raise a clear error.
- **Product ADR-0004** (`doc/architecture/decisions/0004-retention-of-biomechanical-position-optimization.md` in `tticom/score2gp`, accepted 2026-08-15) retains the `BiomechanicalPositionOptimizer` to infer positions for standard-notation notes, on the stated ground that TAB extraction and fusion were not yet implemented.

Produce one reconciling decision record that states a single rule. The proposed rule, from the maintainer's position, is: **observed TAB positions are authoritative; inference is permitted only for notation-only notes, and every inferred position carries its provenance (labelled as inferred, never presented as observed).**

## Deliverables

1. **Current-state facts.** On current product `main`, state with file and line references what actually happens today: where observed TAB string and fret enter the pipeline, whether TAB fusion into the timeline is now implemented (ADR-0004's premise was that it was not), whether `BiomechanicalPositionOptimizer` still exists and where it is called, and how a note's provenance (observed versus inferred) is or is not recorded. Cite what you read; do not assume ADR-0004's premise still holds.
2. **One reconciling ADR.** A single decision record with status **Proposed** (the maintainer accepts it; do not mark it Accepted or Approved yourself), stating the rule above or the closest rule the current-state facts support, its reason, and the consequences. Register it in `ARCHITECTURE_DECISIONS.md` with the next free ADR number.
3. **Supersession proposal.** Say exactly how ADR-006 and product ADR-0004 would be marked superseded or amended once the new ADR is accepted. Write the proposal in the new record only. Do not edit ADR-006's text, and do not edit the product repository: migrating the product ADRs is the separate item `DEC-03`.
4. **Gaps and questions.** List any case where the current code diverges from the proposed rule (for example an inferred position that is not labelled), as located findings for the maintainer. Do not fix them here.

## Constraints

- Records only: no product code, test, fixture, dependency or gate change. No edit to the product repository.
- Governance owns ADRs; the architect role cannot edit product code (governance README).
- No private musical content (hashes, counts and file references only).
- Leads, not facts: re-read the code and the two ADRs rather than relying on this prompt's summary of them.

## Acceptance

- One new decision record, status Proposed, registered in `ARCHITECTURE_DECISIONS.md`.
- Its current-state section is sourced to product `main` with a revision and file references a reviewer can reproduce.
- The supersession proposal names both ADR-006 and product ADR-0004 and what changes in each.
- Divergences between the code and the proposed rule are listed as findings, none fixed.
- Validation: `python -m pytest`, `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`, `git diff --check`.
