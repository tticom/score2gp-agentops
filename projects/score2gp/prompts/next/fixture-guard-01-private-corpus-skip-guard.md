# FIXTURE-GUARD-01: Private-corpus tests that skip silently

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001 (a green CI must mean the real-source checks ran)
- **Depends on:** SCALE-01 (merged)
- **Branch:** `feat/fixture-guard-01-private-corpus-skip-guard`

This is a small task. It comes from the CI rerun of product `main` at `95a6802` on the categorised fixtures (run 37831924173): attempt 1 on the flat layout had **1784 passed, 10 skipped**; attempt 2 on the categorised layout had **1783 passed, 11 skipped** and the same green result. Every number below is a lead: re-measure it. Never commit private content; report counts and test ids only.

**Private fixtures.** The corpus is grouped by category on fixtures `main` (49 files); the author launcher flattens it into `fixtures/private/`. Before starting, verify that `fixtures/private/` contains `Finger postition tips TAB.pdf` (note the original spelling "postition") and `A7-Blues-Lick.pdf`; if either is missing, stop and say exactly what is missing.

## What was measured (leads to VERIFY)

- The extra skip is `tests/test_scale_01_geometry.py::test_tab_only_private_controls_have_no_notation_staves[Finger postition tips TAB (1).pdf]`. Fixtures PR #5 renamed that file to `Finger postition tips TAB.pdf`, so the test's parameter names a file that no longer exists and the test `pytest.skip`s ("mounted private corpus is unavailable"). It is the SCALE-01 control proving that a TAB-only file does not grow false notation staves, so that protection silently disappeared while CI stayed green.
- CI logs show no skip reasons (pytest runs without `-rs`), so nothing told anyone. The same failure mode threatened `tests/test_pdf_group_02_private.py` (it converts `A7-Blues-Lick.pdf` and `E_Chord_Lick_Chord.pdf` and skips with "private corpus absent" if they are missing) when the seven lick PDFs briefly looked deleted by the fixtures migration.
- Other tests carry their own wording for the same skip ("private corpus absent", "mounted private corpus is unavailable", ...). The census of these strings is part of the task.

## Goal

1. The renamed control test names the current file and runs.
2. When CI has mounted the private corpus, a test that skips because a private file is missing **fails the CI job** instead of passing silently.

## Acceptance

1. **Census first.** Every `pytest.skip` / `skipif` / `importorskip` in `tests/` whose reason depends on the private corpus, grouped by reason string, with counts and test ids (counts and ids only). Say which skips are legitimate and unrelated to the corpus (for example the symlink-privilege skip on Windows).
2. **The renamed control** uses `Finger postition tips TAB.pdf`, runs (is not skipped) with the corpus mounted, and still asserts exactly what it asserted before (no weakened assertion). Check the whole test suite for any other reference to a name that no longer exists in the mounted corpus, and report each.
3. **The guard.** With an environment variable the CI step sets right after the corpus is mounted (name it yourself, for example `SCORE2GP_REQUIRE_PRIVATE_CORPUS=1`), any test that is skipped for a private-corpus reason fails the run with its id listed. Without the variable, behaviour is unchanged for local runs without the corpus. The reason match comes from the census, not from a guess; an unrecognised skip reason is reported, not ignored.
4. **Tests that bite.** The real-source evidence is the renamed control running on the real mounted file and the CI showing 0 private-corpus skips; a mutant that ignores one reason string fails the guard's own test. Public synthetic tests (a skipped private-corpus test makes the guard fail; a legitimate unrelated skip does not) are non-domain infrastructure only: the guard makes no recognition, grouping, geometry, timing or fidelity claim, so synthetic tests are the only way to prove it without the corpus; state that rationale. They carry no acceptance weight for the real-source claim. The guard has its own test and is not itself skippable.
5. **CI proof.** The exact-head CI run shows 0 private-corpus skips, and lists the remaining skips with a reason each. State the before and after counts of passed and skipped.
6. No test deleted, weakened or renamed to avoid the guard; no change to production code under `src/`.
7. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally. `docs/setup.md` explains the guard in a few lines.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources; synthetic, mocked or generated tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims and may supplement non-domain infrastructure only with a stated rationale.
- **Read the situation, do not guess:** the guard's match list comes from the census.
- **Stay inside `allowed_paths`;** if you need another path, stop and report it.
- **Do not let the guard turn a legitimately skipped test into a failure** (for example Windows symlink privilege); only private-corpus reasons.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`.
- **Protect what already works:** the whole suite; every test that passes today still passes.
