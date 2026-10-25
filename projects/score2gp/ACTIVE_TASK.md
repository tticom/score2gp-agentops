# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-01-FU2 — Guard the refusal when an attached accidental also fits the next signature slot on approved real sources, or record it as unverified

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-01-fu2-ambiguous-accidental-fixture`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Guard the refusal when an attached accidental also fits the next signature slot on approved real sources, or record it as unverified. Source: authority item OMIT-01-FU2. Non-blocking follow-up from tticomgov-code's approving round-4 review of tticom/score2gp#468 (OMIT-01) at 6a40e82. Thread at src/score2gp/notation_omr/key_signature.py:221: this refusal branch has no committed test; mutant B (ambiguous = False) passes every test in tests/test_omit_01_key_signature.py, because mid_system_ambiguous.pdf reaches the out-of-order branch instead. Reviewer probes P2 (2 flats + attached A-slot flat) and P2c (2 sharps + attached G-slot sharp) are refused at this head and read -2/+2 under mutant B; they are invented layouts, so they are leads and diagnostics only. Find out whether any approved real source reaches the ambiguous-slot case; if one does, guard the branch on it, otherwise record mutant B as not killed and the branch as unverified on real sources, with counts.

## Allowed paths

- `tests/**`
- `fixtures/public/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
