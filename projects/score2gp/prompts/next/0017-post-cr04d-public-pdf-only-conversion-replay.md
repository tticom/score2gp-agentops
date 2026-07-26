# 0017 - Post-CR-04D Public PDF-Only Conversion Replay

## Status

ACTIVE — evidence task authorised after product PR #390 merged at
`d70d559152c5aa357a7d2eb38e65b09f288bb08f`.

## Objective

Run the committed PDF-only conversion path on the deterministic generated
score-like public PDF without a MusicXML sidecar. Record a coherent,
revision-pinned strict and diagnostic result so governance can select the
first current product blocker. Do not change product code.

## Skills and identity

1. Read `projects/score2gp/SKILLS_LOCK.md` and
   `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`.
2. Verify installed `governed-development-loop`, `identity-safe-git`,
   `durable-handoff`, and `code-review` resolve to locked commit
   `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`.
3. Run the `identity-safe-git` gate for `tticom-automation`.
4. Work only in the automation-owned WSL product and AgentOps clones.

A mismatch is a no-write stop.

## Pin live state

Synchronize both repositories to `origin/main` and verify clean tracked state.
Record:

- product SHA, which must contain
  `d70d559152c5aa357a7d2eb38e65b09f288bb08f`;
- AgentOps SHA;
- locked skills SHA;
- `command -v score2gp`;
- `.venv/bin/python -c 'import score2gp, pathlib; print(pathlib.Path(score2gp.__file__).resolve())'`;
- input path and SHA-256.

Run `python scripts/agent_verify.py` before the replay. Stop if it fails.

## Fixed public input

Use only:

`tests/fixtures/pdf/generated_scorelike_tab.pdf`

If it is absent, regenerate it with:

```bash
python tests/fixtures/pdf/make_generated_scorelike_tab_pdf.py
```

Confirm regeneration does not change tracked files. Do not use a MusicXML
sidecar, reference GP, private PDF, or private oracle.

## Fresh output directories

Create two unique ignored directories below product `work/`:

- one for strict execution;
- one for diagnostic/remediation execution.

Never reuse prior output. Record their paths in the local evidence, but
sanitize home-directory prefixes from the committed report.

## Required executions

Run the strict channel first:

```bash
.venv/bin/python -m score2gp.cli convert \
  --pdf tests/fixtures/pdf/generated_scorelike_tab.pdf \
  --out work/<run>/strict/generated_scorelike_tab.gp \
  --work-dir work/<run>/strict/intermediate \
  --json-report work/<run>/strict/summary.json \
  --pdf-only-tab \
  --editable-draft \
  --strict
```

Preserve the exit code. A refusal is valid evidence and must not be softened or
reported as a failure to execute.

Then run the diagnostic channel separately:

```bash
.venv/bin/python -m score2gp.cli convert \
  --pdf tests/fixtures/pdf/generated_scorelike_tab.pdf \
  --out work/<run>/diagnostic/generated_scorelike_tab.gp \
  --work-dir work/<run>/diagnostic/intermediate \
  --json-report work/<run>/diagnostic/summary.json \
  --pdf-only-tab \
  --editable-draft \
  --no-strict \
  --allow-remediation
```

Do not add `--allow-skip-unboxed-systems` unless the strict/diagnostic evidence
explicitly identifies that single gate. If used, run it as a third channel and
label it separately.

## Evidence inspection

For each channel, record independently:

- exact command and exit code;
- first refusal or warning category/stage/message/details;
- whether TabRaw, ScoreIR, and GP were generated;
- bar/event/note/rest counts when the artifacts exist;
- schema/IR/GP validation results supported by current repository commands;
- coherence between summary, warnings, round-trip, and generated files;
- the strongest way the run could falsely appear successful;
- the first observable mismatch or remaining unknown.

File existence is not conversion correctness. Do not claim real-score,
rhythmic, visual, or musical correctness from this generated fixture.

## Durable report

Create exactly one report:

`projects/score2gp/runs/2026-07-26-post-cr04d-public-pdf-only-replay.md`

Use `durable-handoff`. Include full product, AgentOps, and skills SHAs;
verified versus author-reported evidence; the two result channels; sanitized
artifact paths; unresolved risks; and one smallest recommended follow-up.

The recommended follow-up is a candidate only. Do not edit `ACTIVE_TASK.md`,
`NEXT.md`, or create another prompt.

## Validation and publication

In AgentOps run:

```bash
python -m pytest -q tests/test_governance_audit.py
python scripts/score2gp_governance_audit.py
git diff --check
git status --short
```

Only the single durable report may change. Commit and push branch
`agy/post-cr04d-public-pdf-only-replay`, then open one AgentOps PR.

The PR must state:

- exact remote head SHA;
- strict and diagnostic results separately;
- whether artifacts were coherent;
- first current blocker or remaining unknown;
- no private files, product changes, or conversion-success claim.

Do not approve or merge the PR. Stop for independent hard review.
