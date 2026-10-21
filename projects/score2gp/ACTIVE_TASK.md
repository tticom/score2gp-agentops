# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-02-FU3 — Repeat-dot glyph detection must not depend on the Bravura font name

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-02-fu3-repeat-dots-not-font-name`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Repeat-dot glyph detection must not depend on the Bravura font name. Source: authority item OMIT-02-FU3. Non-blocking follow-up from tticomgov-code's approving round-2 review 5346382223 of tticom/score2gp#469 (OMIT-02) at d7eef3f. Summary item N3: repeat-dot glyph detection matches the music font by name; other SMuFL fonts (for example Petaluma, Leland, or subset-renamed embeddings) are an unverified synthetic risk whose failure would show as an omitted repeat. Identify the glyph by SMuFL codepoint and geometry, or refuse with a located reason when a music font is present but unrecognised; add a public control with a second SMuFL font. Added from tticom-codex's non-blocking note on tticom/score2gp-agentops#729 (thread at ORCHESTRATION_STATE.json:3490): N3 covers an unfamiliar music-font name with no PUA ToUnicode mapping, so a SMuFL-codepoint route alone may not detect it; the acceptance check must include that case (glyph geometry or a located refusal).

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`
- `schemas/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
