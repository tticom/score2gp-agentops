# 0031 - CR-06A Key Signature Evidence Contract & Fallback Removal

## Objective

Implement bounded Developer slice `CR-06A` in `tticom/score2gp`, as authorized by the merged architecture report `docs/design/cr06-key-signature-semantics-architecture.md`.

Introduce explicit `logical_key_signature` status handling (`EVIDENCED`, `UNKNOWN`, `AMBIGUOUS`) in `src/score2gp/notation_omr/pitch.py` and `src/score2gp/cli.py`. Remove the hardcoded `"C Major"` default fallback for unevidenced notation staves so that unevidenced staves apply 0 key alterations without asserting a recognized C Major key signature in CLI or report metadata.

## Authorized Product Files

- `src/score2gp/notation_omr/pitch.py`
- `src/score2gp/cli.py`
- `tests/test_cr06_key_signature_semantics.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not edit `docs/design/cr06-key-signature-semantics-architecture.md` during this Developer implementation slice.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0031-cr06a-key-signature-evidence-contract.md`, `docs/design/cr06-key-signature-semantics-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr06a-key-signature-evidence-contract` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/notation_omr/pitch.py`**:
   - In `map_clef_resolved_staff_pitch`, replace hardcoded `key_sig = "C Major"` default with explicit `key_signature_status`.
   - When key signature candidate is provided and valid, set `key_signature_status = "EVIDENCED"` and apply key alterations.
   - When key signature candidate is absent or `None`, set `key_signature_status = "UNKNOWN"`. Apply 0 key alterations without asserting a recognized `"C Major"` key signature in outputs.

2. **`src/score2gp/cli.py`**:
   - Update semantic summary formatting for key signature: display `Key Signature: Unknown` when `logical_key_signature` status is `UNKNOWN` or missing.

3. **`tests/test_cr06_key_signature_semantics.py`**:
   - Add unit tests verifying that unevidenced staves report `Key Signature: Unknown` and do not assert `"C Major"`.
   - Add unit tests verifying explicit key signatures apply alterations correctly when `EVIDENCED`.

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_cr06_key_signature_semantics.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Visual accidental glyph extraction near clefs is deferred to follow-up slice CR-06B.
- Multi-staff key signature synchronization across grand staves is deferred.
