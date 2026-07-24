# 0007 - Address Codex Review on PR #383

## Objective

Fix all blocking findings in the Codex review comment on product PR #383:

https://github.com/tticom/score2gp/pull/383#issuecomment-5070345248

Update the existing `agy/cr03d-local-triplet-association` branch and PR #383.
Do not create a new branch or PR.

## Identity and Start

1. Work only under `/home/tticom/work/score2gp-workspace` in Ubuntu WSL.
2. Before any GitHub write, run:

```bash
gh auth switch --hostname github.com --user tticom-automation
test "$(gh api user --jq .login)" = "tticom-automation"
```

3. In both repositories set and verify local commit identity:

```bash
git config user.name tticom-automation
git config user.email tticom-automation@users.noreply.github.com
test "$(git config user.name)" = "tticom-automation"
```

4. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Developer skill, this prompt,
   the original `0006` prompt, and the complete Codex review comment.
5. Fetch product origin. Require a clean worktree. Switch to the existing
   `agy/cr03d-local-triplet-association` branch and fast-forward it only.
6. Confirm the starting head is
   `5828d672c2eb0b66e9edc783da3b0d8c09b8b5fb`. If the remote head has advanced,
   inspect the new commits and stop if they were not produced by this fix task.
7. Do not reset, clean, force-push, amend published commits, or recreate PR
   #383.

## Required Fixes

### 1. Derive ownership; never invent it

- Production `page.get_text("words")` elements do not carry system, staff,
  kind, or span.
- Derive page/system/staff from committed staff geometry using unambiguous
  spatial ownership.
- Derive an explicit measure/span from committed barline or measure geometry
  before association.
- If either ownership cannot be established uniquely, produce no association
  and surface a diagnostic reason. Never default to system 1, staff 1, or
  `span_001`.
- Outcomes missing page/system/staff/span must not enter a matching group.
- Add a production-shaped integration regression using raw word tuples or
  dictionaries containing only text, bbox, and page.

If committed diagnostics cannot derive explicit span ownership, follow the
original prompt: remove unsafe pipeline integration, keep any justified pure
diagnostic helper, and report the precise observability gap. Do not invent a
span model.

### 2. Missing geometry must fail closed

- Remove the fallback that derives the staff top from the marker bbox.
- Require valid five-line staff geometry and positive finite spacing.
- Missing, malformed, ambiguous, or non-finite geometry must produce no
  association or an explicit refusal diagnostic.
- Add the exact regression: valid marker plus three notes plus empty geometry
  must not associate.

### 3. Preserve real timeline/refusal diagnostics

- If pipeline integration remains, preserve tuplet association status and
  marker/candidate ownership in timeline diagnostic events.
- Test the actual field and value, not merely `duration_ticks`.
- An ambiguous association must identify the competing candidate groups or
  affected candidates so its status can be surfaced; an empty candidate-ID
  tuple is not an adequate event diagnostic.
- Add associated and ambiguous production-path tests.

### 4. Remove unsafe hard-coded timing mutation

- Remove `duration_ticks = 320`.
- CR-03D is diagnostic association unless duration can be derived generically
  from committed source timing, divisions, meter, and the existing event
  duration.
- Do not overwrite recognized timing simply because a marker was associated.
- Do not broaden this PR into MusicXML, ScoreIR, or GP timing changes.

## Disconfirmation Tests

In addition to the original public contract, prove:

- a plain raw word `3` near a different staff cannot inherit staff 1;
- raw TAB/measure-label `3` text without a pre-labelled `kind` cannot pass
  solely because its literal is `3`;
- missing staff geometry cannot associate;
- missing explicit span ownership cannot associate;
- `tuplet_association` or the documented refusal survives into the actual
  timeline diagnostic;
- ambiguous groups retain enough identity for inspection;
- no code path writes a literal `duration_ticks = 320`.

## Verification

Run:

```bash
.venv/bin/python -m pytest -q tests/test_notation_omr_tuplet.py
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

Also run the three reproductions from the Codex review:

- production-shaped extraction reports derived or refused ownership, never
  `(1, 1, "span_001")` by default;
- empty staff geometry produces zero associations;
- actual timeline event keys include the documented tuplet status when
  integration remains.

## Publish to Existing PR

1. Commit only the approved fixes and tests.
2. Push normally to `origin/agy/cr03d-local-triplet-association`.
3. Do not force-push or open a new PR.
4. Comment on PR #383 as `tticom-automation` with:
   - new head SHA;
   - each Codex finding and its disposition;
   - targeted and full test results;
   - the three reproduction results;
   - any observability gap or deliberately removed integration.
5. Do not mark the PR ready and do not merge. Stop for Codex re-review.
