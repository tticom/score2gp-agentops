# FND-02: Replace silent ScoreIR clamps with rejecting validators

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001:U13
- **Depends on:** none
- **Branch:** `feat/fnd-02-reject-instead-of-clamp`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Replace silent ScoreIR clamps with rejecting validators. Source: authority item FND-02. Contradicts the L3 'no note clamping' gate; target limits belong in capability checks (ADR-008).

## Acceptance

1. Measure first: list every place a ScoreIR or GPIF value is silently clamped or coerced (start at ir.py around lines 99, 268 and 516-528 and gpif.py around 833; re-locate them) with the input that triggers each and what is written instead.
2. Each clamp becomes a validator that rejects the out-of-range value with a located reason code; target-format limits are NOT enforced in the IR (they belong to capability checks, ADR-008), and the handback names which clamp is which kind.
3. On the whole private set no previously converting source starts to refuse and the GPIF for every converting source is byte-identical before and after, shown in the handback; any source that would now refuse is listed, not hidden.
4. A named mutant (restore one clamp) fails a test; the L3 'no note clamping' statement is cited with the tests that now hold it.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
