# OMIT-02-FU3: Repeat-dot glyph detection must not depend on the Bravura font name

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-02
- **Branch:** `feat/omit-02-fu3-repeat-dots-not-font-name`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

Repeat-dot glyph detection must not depend on the Bravura font name. Source: backlog OMIT-02-FU3. Non-blocking follow-up from tticomgov-code's approving round-2 review 5346382223 of tticom/score2gp#469 (OMIT-02) at d7eef3f. Summary item N3: repeat-dot glyph detection matches the music font by name; other SMuFL fonts (for example Petaluma, Leland, or subset-renamed embeddings) are an unverified synthetic risk whose failure would show as an omitted repeat. Identify the glyph by SMuFL codepoint and geometry, or refuse with a located reason when a music font is present but unrecognised; add a public control with a second SMuFL font. Added from tticom-codex's non-blocking note on tticom/score2gp-agentops#729 (thread at ORCHESTRATION_STATE.json:3490): N3 covers an unfamiliar music-font name with no PUA ToUnicode mapping, so a SMuFL-codepoint route alone may not detect it; the acceptance check must include that case (glyph geometry or a located refusal).

## Acceptance

1. Measure first: where the music-font name is matched and which real corpus sources use which music fonts (counts only).
2. A repeat dot is identified by SMuFL codepoint and geometry; a music font that is present but unrecognised, including one with no PUA ToUnicode mapping, gives a located refusal, never a silently omitted repeat.
3. Controls with a second SMuFL font and with an unmapped renamed subset font pass; on the real corpus every repeat read today is read identically; a mutant that restores the font-name match, or ignores geometry, fails.
4. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
