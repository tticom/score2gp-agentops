# Active Task

**Task**: Task 91: Deep Root-Cause Research and Programme Reset
**Authorised Role**: Project Director, Corpus Analyst, Output Verifier, Architect, and Reviewer
**Repository**: `tticom/score2gp-agentops`, `tticom/score2gp`, and the approved local fixture repository

## Status

APPROVED

## Task Authorised

Yes, research only.

## Reason For This Pivot

The maintainer continues to observe fatal timing refusals in the canonical CLI
for Lessons 5 through 7 and no timeline for Melodic Soloing Masterclass. The
same canonical command also shows no reliable visible improvement in Lessons 3
and 4. Meanwhile, recovery-branch reports claim timing or corpus success from
different source-first commands, non-strict runs, and tests that do not prove
visible score quality.

Do not attempt another implementation fix until this task produces a
reproducible explanation of that discrepancy and a ranked, evidence-backed
implementation sequence.

## Start State

- Canonical product worktree:
  `/home/tticom/work/score2gp-workspace/score2gp`
  on frozen `feature/teamwork-corpus-conversion-accuracy-v0.1`.
- Recovery worktree:
  `/home/tticom/work/score2gp-workspace/score2gp-recovery`
  at `b7a2aa79`.
- The editable virtual environment is known to import canonical source unless
  the recovery invocation explicitly sets `PYTHONPATH=.:src`.
- Read the Task 89 review before beginning:
  `projects/score2gp/reviews/2026-07-17-task-89-timing-milestone-and-release-blockers.md`.

## Required Contract

Read and execute:

`projects/score2gp/research/2026-07-17-deep-root-cause-research-contract.md`

It is the complete requirement, evidence, and completion contract for this
task.

## Permissions and Boundaries

- Tier 1 research/documentation only.
- Do not modify product source, product tests, package installation, product
  configuration, branches, pull requests, or generated artifacts.
- Do not delete the maintainer's root-level generated outputs or `tmp` trees.
- Create only the authorized sanitized research report and evidence ledger in
  `score2gp-agentops`; commit, push, review, and merge their governance PR if
  clean.
- Temporary diagnostics must live outside repositories. Use external run
  directories under `/home/tticom/work/score2gp-runs/`.
- Do not infer product behaviour from `--ref-gp`, private references, prior
  agent summaries, a generated GP file, or a green unit suite.

## Completion Evidence

1. The requested research report and sanitized evidence ledger exist and pass
   `git diff --check`.
2. The report identifies the exact import/worktree identity for every tested
   command and explains the canonical-versus-recovery discrepancy.
3. It gives an earliest-stage failure map for the stated representative corpus.
4. It audits which current validations are predictive of visible output and
   which are not.
5. The Reviewer records a ranked next-task sequence and immediately promotes
   the smallest credible next task. Do not stop at the research handoff when a
   safe continuation exists.
