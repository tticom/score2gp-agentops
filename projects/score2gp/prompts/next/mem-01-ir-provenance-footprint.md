# MEM-01: Stop copying full raw candidates into every IR event and note

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001 (a conversion must be practical to run; resource use is cost)
- **Branch:** `feat/mem-01-ir-provenance-footprint`

This comes from the maintainer's direction on 2026-09-29: "Resource use ultimately costs money so this becomes a priority at some point, might as well be now."

## Goal

Cut the size of `score.ir.json`, and the memory used to build it, by referencing raw extraction candidates by id instead of copying them into every event and note.

Governance measurement (2026-09-29, main 2e8c00b, Windows host):
- Lesson 3 (66 bars) produces `score.ir.json` at 25 MB compact and 51 MB on disk.
- Each event carries about 25 KB of provenance (the full raw candidate, bbox and grouping evidence), duplicated again on each note.
- One CLI conversion peaks at about 400 MB working set and takes 30 s.
- The whole work directory is 160 MB (MEM-02 and MEM-03 cover the report and the other files).

## Acceptance

1. Event and note provenance keeps only what the writer, diagnostics and reports consume: the raw candidate id, page, system, bar and bbox. The full raw candidate stays once, in `tab_raw.json`, and is reachable by id. Any schema change is intended and documented, with contract versions bumped.
2. `score.ir.json` for Lesson 3 shrinks by at least 80%. Record peak working set and IR size before and after for Lessons 3 and 6, measured the same way (in-process `GetProcessMemoryInfo` or an equivalent, stated).
3. A regression budget test fails if IR bytes per bar exceed a stated bound on a public fixture.
4. Every consumer of the removed fields (diagnostics, conversion report, symbol attachment, audits) still works, or reads by id. `grep` evidence lists each consumer.
5. The GP output is byte-identical before and after for Lessons 3-7 (`score.gpif`), or every difference is explained and approved as intended.
6. No regression in DUR-02, OMIT-01 or OMIT-02.

## Rules

- **Behaviour-preserving refactor:** outputs must not change. The GP comparison in acceptance 5 is the guard.
- **Test first:** the budget test fails at the base.
- **Private tests convert under `<repo>/work`** (see OMIT-02-FU4).
- **Pass the product checklist:** pytest (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check`.
- **Keep private material out of the repo.** Commit sizes and counts only.
