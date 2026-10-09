# PERF-01: Melodic_Expressions.pdf runs for minutes and gigabytes

- **Repository:** `tticom/score2gp`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Requirement:** REQ-0001 (a conversion must finish in a predictable time and memory; resource use is cost)
- **Depends on:** MEM-01, SCALE-01 (both merged)
- **Branch:** `feat/perf-01-melodic-expressions-runtime`

This comes from the 2026-10-08 fixture survey (main `95a6802`). Every number below is a lead: re-measure it. Never commit private content; report counts, codes, sizes and times only.

**Private fixtures.** The corpus is grouped by category on fixtures `main` (49 files); the author launcher flattens it into `fixtures/private/`. **Before starting, verify that `fixtures/private/` contains `Melodic_Expressions.pdf`, `Melodic_Expressions_Chap_19_.pdf`, `Lesson-6.pdf`, `Crossroads.pdf` and `Melodic Soloing Masterclass.pdf`**; if any is missing, stop and say exactly what is missing.

## What was measured (leads to VERIFY)

- With a time limit of 300 s and a memory limit of 3.5 GB, `convert --pdf-only-tab --time-signature 4/4` on **Melodic_Expressions.pdf** was stopped at the time limit with its process tree at about **2.5 GB** working set and still running. Every other source in the survey finished: the slowest converting file was Lesson-6 (29.5 s, 533 MB), the two tab books (about 50 MB of PDF each) took 114 s and 227 s and stayed under 400 MB, and a sibling, Melodic_Expressions_Chap_19_.pdf, converted in 26.6 s at 306 MB.
- Earlier DUR-03 notes recorded false staves on Melodic Expressions and Crossroads: a large number of candidate staves or systems could be what multiplies the work, but that is a hypothesis.
- Nothing is known yet about the page count, the stage, or whether the cost is time, memory or both growing together. The survey guard killed the process, so no output and no refusal exists for this file.
- MEM-02 (the 49 MB pretty-printed barline dump in the conversion report) and MEM-03 (work-directory footprint) are separate tasks tracked in the authority. Do not fix them here, but report the size of any artefact that becomes large on this file.

## Goal

Find the stage where the time and memory grow, show what they grow with, and either fix it with a bounded algorithm that leaves every output unchanged, or add an explicit located resource gate so the conversion refuses with a code instead of running for minutes. A conversion must never end by being killed.

## Acceptance

1. **Profile first.** Per stage: wall time and peak working set on Melodic_Expressions.pdf (allowed to run to completion once, on a host with room, with an overall limit you state), against Melodic_Expressions_Chap_19_.pdf and Lesson-6.pdf: page count, number of candidate staves, systems, strokes and tokens at each stage, and which count the cost follows (counts and measurements only). Name the function and the data structure.
2. **The fix.** Either a bounded algorithm (state the complexity before and after), or a located resource gate with a measured, stated bound and a refusal code that names the count that exceeded it. A gate must not refuse any file that converts today.
3. **The result on Melodic_Expressions.pdf:** it converts or refuses with a located code in **under 120 s and under 1.5 GB** on this workspace's Windows host (the governance-set bound; the slowest converting file today takes 30 s at 533 MB; revise it only with measured evidence). Report what it does.
4. **Real-source tests that bite.** A private-corpus test on Melodic_Expressions.pdf asserts the expensive-operation count (or the located resource gate and its code) at the changed seam, independent of wall-clock time, and a second real source (Lesson-6 and one other) shows the count and the GPIF unchanged; a mutant restoring the old behaviour fails the test on the real file. The growth check on a scalable public synthetic fixture (many staves or strokes; for example a counter at sizes n and 2n with a stated ratio bound) is supplementary non-domain infrastructure only: it makes no recognition or fidelity claim, its rationale is that it is the only way to show growth in CI without the private corpus, and it carries no acceptance weight.
5. **Nothing that worked may change.** Measure the whole private set at base and at head: every file that converts today keeps a byte-identical GPIF, and every refusal keeps its code except files reported. Report time and peak working set before and after for every file (counts and labels only); none may get slower by more than measurement noise, which you state.
6. `python -m pytest` (exact-head CI), export-schema, validate-ir, `scripts/artifact_audit.py` and `git diff --check` pass; list the known Windows baseline failures by ID if they fail locally.

## Rules

- **Domain evidence (AGENT_CONTROL.md):** acceptance rests on genuine approved sources, or reproducible extracts that keep their source provenance and reach the changed seam; general claims need more than one approved corpus input. Synthetic, mocked or generated-notation tests carry zero acceptance weight for recognition, grouping, geometry, timing or fidelity claims; they may supplement non-domain infrastructure only with a stated rationale.
- **Measure on the real file, not on your assumption.** Do not guess the stage. Use an in-process memory sampler (`GetProcessMemoryInfo`, as MEM-01 did) or an equivalent, and say which.
- **Never trade correctness for speed:** no output change on any file that converts today; no gate loosened.
- **Stay inside `allowed_paths`;** if the hot spot is elsewhere, stop and report the path so governance can amend scope.
- **Run the long profile once,** one heavy process at a time, with a hard memory limit you state; the host is shared. Do not leave processes running.
- **Private tests convert under `<repo>/work`** in a `tempfile.TemporaryDirectory`, never pytest's `tmp_path`.
- **Protect what already works:** DUR-02/03, OMIT-01 to OMIT-05, LAYOUT-01, MEM-01, CFW-04, PARTIAL-01, SCALE-01, TUPLET-TAB-01, PDF-GROUP-02.
