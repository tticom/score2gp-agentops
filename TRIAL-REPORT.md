# TRIAL-REPORT: the lean flow run end to end on one real product task

Date: 2026-10-03. Author: Claude Sonnet 5.5 agent, acting on the maintainer directive "prove the
lean flow". Nothing was pushed to GitHub: the product repo was shallow-cloned to a scratch
directory with a local bare repository as `origin`; the lean files were overlaid at their promoted
paths; the old framework and every `main` were untouched. Raw logs stayed outside every repo.

## Verdict: READY WITH FIXES

The lean flow worked end to end and was much cheaper in ceremony than the old one. It caught one
real error and one real review finding. It is **not** ready to replace the old flow until the three
fixes below are done, because on the product repository today its CI gate would be red and its
local check cannot give a PASS on a machine with a red baseline.

## What was run

| Step | Result |
|---|---|
| Overlay `lean/`, `CLAUDE.md`, `AGENTS.md`, `TASKS.md`, PR template, `ci.yml` on a product clone | worked; a plain copy missed the hidden `lean/.gitattributes` (now noted in `MIGRATION.md`) |
| `install_hooks.py` and `--check` | OK; a push of `main` was refused ("refusing to push to protected branch"); a push of `task/CHK-01` was accepted |
| Claim: `ls-remote`, then push an empty `task/CHK-01` | worked against the local origin |
| Task chosen: **candidate (c)** | see below |
| Implement with tests, `risky` | 9 public tests (all pass); 4 source files touched |
| Real-fixture check (private corpus, counts only) | private steps **PASS** (31 PDFs found, smoke 31 entries, audit 9 entries, safety invariant clean, diff check clean). The full default run reported **FAIL** only because the public suite has 16 failures that also fail on pristine `main` (13 `test_omr_contract`, 1 each `test_agent_automation`, `test_corpus_harness`, `test_raster_diagnostics_gate_report`); 1763 passed |
| Direct conversion of five real lessons (3 to 7) after the change | new warning count 0 on all five; the other warning counts unchanged |
| Advisory review by the other model (`codex exec`, read only, about 3 minutes) | 5 findings, 2 high (below) |
| Agentops suite from the slim worktree after my fixes | full: 599 passed, 2 skipped; lean tests plus backlog test: 149 passed, 1 skipped |

### Why candidate (c)

(a) was already largely honest: Lesson-7 has 0 unjoined accidentals on current `main`, and the 8
`spelling_unevidenced` warnings (18 notes) sit in bars 1 to 20 whose key is read as C major. Choosing
flat or sharp there is a spelling policy, not a defect, and cannot be decided from the PDF. (b) Fb and
Cb notes are white keys; the pitch comes from string plus fret and no code spells white keys, so
there is nothing to fix without a new feature. (c) was a self-contained, measurable, warn-only
addition with a clear acceptance test and no change to any pitch: smallest scope, best evidence.

### The task (in the scratch clone only)

The reader exports the natural pitch class of each notehead (`staff_pitch_classes`); a pure function
`notehead_tab_disagreement` pairs heads with TAB notes one to one within a semitone; the bar assembler
records disagreements and the existing spelling warning pass emits `notehead_tab_pitch_disagrees`
(warning only; pitch stays string plus fret).

## Where the lean steps caught a real error

1. **The real corpus caught a false-positive bug that the first unit tests missed.** My first matcher
   paired greedily; on Lesson-7 it raised 16 false warnings (chord heads C E F A against TAB C Eb F A).
   Only the real file showed it. Fixed with one-to-one matching and a regression test; then 0 on five
   lessons. This is lean rule 6 working as intended. Limit: 0 warnings on real data proves no false
   positives there; detection is proved only by the synthetic unit tests, because the corpus has no
   known disagreement.
2. **The advisory review caught two real limits.** Bass clef, and non-standard tuning or a capo, can
   raise false warnings (the pitch derivation already assumes standard tuning; the clef is not read).
   Recorded as known limits in the function docstring; a follow-up task is needed before the warning is
   promoted from advisory. It also noted that a bar refused for another reason hides disagreements of
   its matched events, and that the record schema string was not bumped. Not fixed (confidence over
   polish).

## Friction, honestly

| Step | Verdict | Notes |
|---|---|---|
| Read `CLAUDE.md`, `TASKS.md`, hook, scripts | useful, short | one page is enough; rule 1 ("agents never merge") contradicted the 2026-10-03 standing instruction. **Fixed** |
| Seed `TASKS.md`, claim by pushing a branch | cheap, useful | two commands with a local origin; not tried against GitHub |
| Hook | caught the push to `main` | worked first time; CRLF is covered by `lean/.gitattributes`, but only if that hidden file is copied |
| `repo_scan` and CI gate on the product tree | **found a defect** | 244 findings: 222 public fixture PDFs and PNGs (forbidden extension), 22 local paths, some real user names in docs and some placeholders such as `/home/user/` (a false positive). **Partly fixed**: placeholder users no longer flagged; the product still needs a `.scan-allow` and a docs cleanup |
| `ci-slim.yml` | **found a defect** | installed only `pytest`, so the product suite could not import its code. **Fixed**. It also drops the old CI's lint and private-fixture job; intended, but say so |
| Real-fixture check | useful, but slow and opaque | no progress output for 32 minutes (summary only at the end); the public-suite step takes 32 minutes here; a red baseline makes the whole result FAIL with no baseline comparison; "audit 9 of 9 fail" is an unexamined number because a clean failure is counted, not judged. The private steps alone take 16 minutes |
| Implement, tests, clean-head pre-flight | normal engineering | |
| Advisory review | **worth it** | 3 minutes, 2 high findings; no handback or promotion needed |
| Remove the task from `TASKS.md` in the PR | trivial | |
| Draft PR from the template | not run | no GitHub writes allowed in the trial |
| Pure bureaucracy | about 5 percent | the claim push and the PR template; both small |

### Cost against the old flow

Old flow per task (known): two governance PRs, an exact-head handback, a review round, and a merge
executor run, each with its own gate and wait. Lean flow here: 0 governance PRs, 0 handbacks, 1
advisory review (3 minutes), 0 merge executors, one PR to open. Measured: about 90 minutes elapsed
and about 85 tool calls for the whole trial including reading, investigating three candidates,
building the scratch repo and fixing the framework; roughly 50 minutes of that were machine waits
(the 32 minute public suite and the 16 minute private check). Implementing and testing the task itself
took about 12 tool calls. The comparison is indicative, not controlled.

## Top three fixes before the lean flow can replace the old one

1. **Make the fixture check usable on a real baseline.** Print progress per step, accept a
   known-failures baseline (the 16 pre-existing public failures) so it can say "no new failures", add a
   fast mode, and compare the audit status counts with the previous run instead of only counting them.
2. **Make the CI gate green on the product repository.** Add a product `.scan-allow` for the public
   fixtures (`tests/fixtures/pdf/*`, `fixtures/public/*`), remove the real user names from the product
   docs, and decide whether the old workflow's lint and private-fixture job are kept.
3. **Run the GitHub half of the trial and keep one merge rule.** `CLAUDE.md` rule 1 now states the
   standing instruction (independent review plus green CI, as `tticom`); one `normal` and one `risky`
   task still need to run against a real scratch GitHub repository with Actions and a draft PR, which
   this trial could not do.

## Fixes made on `slim-governance` (agentops)

- `lean/ci-slim.yml`: install the project's own dependencies before the suite.
- `lean/scripts/repo_scan.py` and its test: placeholder users in paths (`user`, `you`, `<name>`) are not leaks.
- `lean/CLAUDE.md`, `lean/AGENTS.md`: the merge rule matches the standing instruction of 2026-10-03.
- `CUTOVER.md` renamed to `MIGRATION.md` and reworked per `MERGE-READINESS.md` (fresh-repository option
  removed, reversibility labels, scans and irreversible items kept); references updated.

## What remains

The three fixes above; the follow-up task for the clef, tuning and capo limits of the new warning (it
exists only in the scratch clone and has not been proposed to the product repo); the real GitHub scratch
run; the protections gate (G1 to G3, G5 to G7) and the `--names-file` scan from `MERGE-READINESS.md`.
Until then the old framework keeps running on `main` and nothing here should be cut over.
