# Visual Output Correctness Recovery Programme

## Goal

Make the canonical `score2gp convert` path visibly faithful to source PDF
notation across the approved corpus. The working measure is source-to-output
correctness, not a green suite, an artifact, or absence of a fatal parser risk.

## Control Model

- `projects/score2gp/research/2026-07-17-maintainer-visual-observation-ledger.md`
  is the acceptance input.
- `projects/score2gp/tasks/2026-07-17-visual-output-correctness-backlog.md`
  is the ordered task series.
- Every functional task uses: source evidence -> deterministic intermediate
  representation -> MusicXML -> ScoreIR -> GPIF -> rendered/output facts.
- `--ref-gp` is diagnostic-only. It never informs generation or thresholds.
- Product PRs are small and stacked only when the parent is explicitly open,
  reviewed, and named. No child merges before its parent.

## Priority Order

1. Establish the visual-output probe and locate the first divergence.
2. Correct meter evidence and time-signature emission.
3. Correct event slicing, tuplets, durations, rests, and chord/sequential
   grouping under the proven meter.
4. Correct double/final bars, system/page breaks, and phrase titles.
5. Correct unknown-versus-detected key semantics.
6. Add one fail-closed embellishment attachment class at a time.
7. Refactor naming/module boundaries only after behaviour is pinned.
8. Expand the corpus capability-by-capability; scanned input handling is a
   separate capability, not a silent timeout.

## Non-Negotiable Acceptance

- A normal conversion must not report strict success when meter, timing, or
  grouping is unsafe.
- An approximate output requires explicit user selection and a machine-readable
  approximate status; it is never a strict success.
- The first source/output mismatch, not aggregate counts, selects the next
  task.
- A feature is accepted only with a public structured regression, original
  approved-input evidence, and a distinct-corpus check.
