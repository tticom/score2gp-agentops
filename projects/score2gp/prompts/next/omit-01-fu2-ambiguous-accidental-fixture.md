# OMIT-01-FU2: Guard the refusal when an attached accidental also fits the next signature slot on approved real sources, or record it as unverified

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-01
- **Branch:** `feat/omit-01-fu2-ambiguous-accidental-fixture`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Guard the refusal when an attached accidental also fits the next signature slot on approved real sources, or record it as unverified. Source: authority item OMIT-01-FU2. Non-blocking follow-up from tticomgov-code's approving round-4 review of tticom/score2gp#468 (OMIT-01) at 6a40e82. Thread at src/score2gp/notation_omr/key_signature.py:221: this refusal branch has no committed test; mutant B (ambiguous = False) passes every test in tests/test_omit_01_key_signature.py, because mid_system_ambiguous.pdf reaches the out-of-order branch instead. Reviewer probes P2 (2 flats + attached A-slot flat) and P2c (2 sharps + attached G-slot sharp) are refused at this head and read -2/+2 under mutant B; they are invented layouts, so they are leads and diagnostics only. Find out whether any approved real source reaches the ambiguous-slot case; if one does, guard the branch on it, otherwise record mutant B as not killed and the branch as unverified on real sources, with counts.

## Acceptance

1. Measure first: reproduce reviewer probes P2 (2 flats plus an attached A-slot flat) and P2c (2 sharps plus an attached G-slot sharp); both are refused at base and read -2 / +2 under mutant B (ambiguous = False).
2. Reproduce P2/P2c only as reviewer diagnostics; they are invented layouts and are not committed as tests of key-signature recognition. Acceptance rests on approved real sources: the handback states with counts whether any approved real source reaches the ambiguous-slot case. If one does, a test over it fails under mutant B (ambiguous = False). If none does, mutant B is recorded as not killed and the branch as unverified on real sources, never claimed guarded by a synthetic layout. The handback shows with counts that real key-change controls (Lesson 7) are unchanged.
3. No production behaviour changes; the mid-system key change tests and real Lesson 7 controls are unchanged.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant) and show that mutant failing. Acceptance rests on genuine approved sources (the private corpus, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
