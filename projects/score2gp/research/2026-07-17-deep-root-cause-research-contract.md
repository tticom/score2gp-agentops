# Deep Root-Cause Research Contract

## Purpose

Determine why repeated product changes, passing tests, and claimed corpus
improvements have not produced reliable user-visible PDF-to-Guitar-Pro output.
This is a research-only task. It must produce a decision-quality evidence base
for the next implementation series, not another feature branch or success
report.

## Boundaries

- Inspect the canonical product worktree, recovery worktree, governance
  repository, approved private fixture repository, and external run outputs.
- Do not modify product source, product tests, product configuration, package
  installation, Git branches, pull requests, or generated output in this task.
- Do not delete user-created root artifacts or `tmp` trees. Classify them in
  the report and leave them untouched.
- Temporary diagnostic scripts belong outside repositories. Do not commit
  private inputs, screenshots, raw generated artifacts, or reference-score
  contents.
- `--ref-gp` may be used only as a read-only diagnostic comparator, never as an
  input to generation or a source of implementation rules.

## Questions to Answer

### 1. Execution identity

For each command form below, identify the exact imported `score2gp` path,
Python executable, Git worktree and commit:

- canonical `.venv/bin/score2gp`;
- canonical `python -m score2gp.cli`;
- recovery `python -m score2gp.cli` with `PYTHONPATH=.:src`;
- any generated command recommended by a script or README.

State whether each command can exercise the recovery branch. Produce one
canonical, user-facing command for a deployed implementation only after the
report establishes which worktree is authoritative.

### 2. End-to-end failure map

Trace the complete path for representative inputs:

- Lessons 3 through 7;
- Melodic Soloing Masterclass;
- one born-digital non-Lesson PDF;
- one scanned or mixed PDF.

For each, record the earliest failing stage and its evidence:

`PDF inspection -> staff detection -> candidate extraction -> clef/pitch ->
timeline -> MusicXML -> parsed timing -> TabRaw/ScoreIR -> GPIF package`.

Record a refusal only at its first causal stage. Do not describe an output file
as usable merely because it was written.

### 3. Test-to-output validity audit

Classify every relevant test and corpus runner assertion as one of:

- source-level unit behaviour;
- integration behaviour;
- parsed MusicXML validity;
- ScoreIR/GPIF structural validity;
- user-visible score-quality proxy; or
- non-predictive for user-visible output.

Identify why the current full suite and smoke matrix can be green while the
canonical CLI still refuses or emits incorrect scores. Call out fixtures,
worktree/import mismatches, non-strict paths, and assertions that only prove an
artifact exists.

### 4. Capability taxonomy

Build a small capability matrix across the approved corpus. Cluster failures by
layout and recognition capability, not PDF name:

- born-digital versus scanned/mixed;
- standard notation, tab, or combined layout;
- staff/system discovery;
- meter/timing;
- key/tempo/title/layout metadata;
- note/rest/dot/chord timing;
- tab assignment;
- embellishment evidence.

Distinguish missing evidence from a recognised-but-unimplemented feature.

### 5. Root-cause ranking and programme reset

Rank root causes by impact and confidence. For each, state the smallest
evidence-backed next task, required regression form, acceptance evidence,
cross-corpus check, and pivot condition. The proposed order must prioritise
reliable deployment and observability before broad notation features.

## Required Deliverables

1. A research report in `projects/score2gp/research/` with a concise executive
   finding, command identity table, stage failure map, test-validity audit,
   capability matrix, ranked root causes, and ordered implementation backlog.
2. A sanitized machine-readable evidence ledger in
   `projects/score2gp/research/` that contains paths, commit identifiers,
   stages, severities, and counts only.
3. A Reviewer section that challenges every proposed next task and rejects any
   claim unsupported by direct source-first evidence.
4. A continuation decision that promotes the first smallest implementation or
   diagnostic task automatically. Do not stop at the report if a credible next
   task exists.

## Completion Criteria

- The report explains the current canonical refusals without relying on memory
  or agent summaries.
- It identifies the executable-import mismatch or proves it absent.
- It separates the Lessons 3--7 timing result from actual visual correctness.
- It explains the Masterclass no-timeline failure at the earliest observable
  stage.
- It gives a bounded, ordered next implementation series with measurable
  acceptance and explicit no-overfitting constraints.
