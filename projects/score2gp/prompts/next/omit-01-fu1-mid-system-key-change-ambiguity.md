# OMIT-01-FU1: A one-accidental mid-system key change followed closely by a note at that pitch is read or refused, never carried as the old key

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001
- **Depends on:** OMIT-01
- **Branch:** `feat/omit-01-fu1-mid-system-key-change-ambiguity`

Private fixtures: the corpus is grouped by category on fixtures `main`; the author launcher flattens it into `fixtures/private/`. Verify the files named below exist there before starting; if any is missing, stop and say exactly what is missing. Every number below is a lead: re-measure it.

## Goal

A one-accidental mid-system key change followed closely by a note at that pitch is read or refused, never carried as the old key. Source: authority item OMIT-01-FU1. Non-blocking follow-up from tticomgov-code's approving round-4 review of tticom/score2gp#468 (OMIT-01) at 6a40e82. Thread at src/score2gp/notation_omr/key_signature.py:217 (PLAUSIBLE): with no prefix, an attached candidate is always treated as a note accidental, so a single flat in slot 0 followed within 1.5 sp by a note at its pitch keeps the previous key with status read and no diagnostic (probe P3: gaps 0.5-1.4 sp read +1; 1.6 sp or another pitch read -1). Real-source evidence from the review (thread 4121094267, review 5337254165): note accidentals usually sit 0.19-0.31 sp from their head, but four genuine chord-displaced accidentals in Lesson 7 sit 1.34-1.46 sp away, inside the 1.5 sp window, and no real input reaches the P3 case. Decide by source geometry or refuse with a located reason, and include a displaced-note negative control (a genuine chord-displaced note accidental at 1.3-1.5 sp must stay a note accidental, not be refused or read as a key change).

## Acceptance

1. Measure first: reproduce probe P3 (single flat in slot 0 followed within 1.5 sp by a note at its pitch keeps the old key with status read) and count real-corpus cases (the review found none).
2. Decide by source geometry, or refuse with a located reason; the case no longer reads the old key silently.
3. A negative control on real Lesson 7 passes: the four genuine chord-displaced note accidentals at 1.34-1.46 sp stay note accidentals (not refused, not a key change); mutants (always key change; always note accidental; window widened to swallow them) fail.
4. Maintainer exception (emailed 2026-10-22, 'b approved'): no genuine corpus source reaches the detached slot-0 key-change ambiguity branch (the 42-PDF census found none), so a CONSTRUCTED P3 regression test may carry acceptance for that one branch only. It must be labelled constructed in its name and docstring, must fail when the new key reader is replaced by the base reader, and must show each named mutant failing (restore the base silent carry; always key change; always note accidental). The Lesson 7 negative control stays on real source and no other recognition, geometry or fidelity claim may rest on constructed input.
5. Nothing that worked may change; validation commands pass; handback complete.

## Rules (all tasks, maintainer direction 2026-10-16)

- **Commercial goal.** The product must convert real engraved guitar tab PDFs to Guitar Pro files correctly. Prefer the change that makes more real bars come out right over polish; never trade correctness for coverage. A bar that cannot be written correctly stays refused with a located reason.
- **Tests must be able to fail.** Write only tests that fail when the code is unfit for its purpose: for every new test name the wrong implementation it rejects (a mutant: drop the feature, hard-code the value, invert the condition, restore the old behaviour) and show that mutant failing. A test that only shows the happy path passing is not evidence and must not be added. Acceptance rests on genuine approved sources (the private corpus and its reference `.gp` files, counts and labels only, never content); synthetic or generated fixtures carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity and may only supplement non-domain infrastructure with a stated rationale. The single exception for this task is acceptance item 4.
- **Never** invent a value, copy it from a reference file into code, loosen a gate, delete or skip a test, or weaken an assertion. A test that encodes behaviour this task deliberately changes is updated with the reason stated in the handback; every numeric and reference check it had is kept.
- **Nothing that worked may change:** measure the whole private set at base and at head. Every file and bar written today keeps a byte-identical GPIF unless the task says otherwise and the handback lists the file, bar and reason.
- **Scope.** `allowed_paths` is the expected area, not a wall. Edit what the task needs and list each path outside the area, with the reason, in the handback. Never edit CI, private fixtures or reference files, agent instruction files or the control plane (`scripts/score2gp_*`, `ORCHESTRATION_STATE.json`, prompts, skills): stop and name the path if one is needed.
- **Private content** is never committed. Report counts, codes, sizes and times only. Private tests convert under `<repo>/work` in a `tempfile.TemporaryDirectory`.
- **Validation:** `python -m pytest` (list the known Windows baseline failures by ID if they fail locally), export-schema, validate-ir, `scripts/artifact_audit.py`, `git diff --check`. Complete the handback with every acceptance item PASS and the evidence for each.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02, UNREAD-01/02, PERF-01.
