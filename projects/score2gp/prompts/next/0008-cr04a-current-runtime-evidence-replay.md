# 0008 - CR-04A Current-Runtime Lesson-5 Evidence Replay

## Objective

Determine whether the false 1920-tick half rest recorded by the historical
Lesson-5 ledger still enters the current conversion path at product
`ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f` or later `origin/main`. Produce the
smallest next decision from current evidence. Do not modify product code.

## Authorised Role

Architect evidence collection only.

## Start

1. Work only in canonical Ubuntu WSL repositories below
   `/home/tticom/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Architect skill, this prompt,
   product `AGENTS.md`, and the historical first-divergence ledger/report.
4. Require clean governance and product worktrees.
5. Fetch both repositories and use current product `origin/main`; record its
   exact SHA and prove it contains
   `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.
6. Create governance branch `agy/cr04a-current-runtime-evidence-replay`.

## Runtime Provenance

Record in ignored `work/` output:

- product `git rev-parse HEAD` and `git status --short`;
- `command -v score2gp`;
- resolved `score2gp.__file__`;
- exact private Lesson-5 input path class and SHA-256;
- exact diagnostic and conversion commands;
- external output/report paths and exit statuses;
- MusicXML sidecar path and SHA-256 if one is used.

Use the approved private fixture only in place. Do not commit or copy the PDF,
generated output, screenshots, overlays, or raw logs.

## Evidence Collection

Run the current supported notation diagnostics and the maintainer-equivalent
strict conversion path. Record sanitized facts sufficient to answer:

1. Does current recognition emit any `half_rest_candidate`, `half_rest`, or
   1920-tick rest? Include candidate IDs, source fields, staff/system ownership,
   and bounding boxes only as rounded sanitized coordinates.
2. Does the current notation bridge accept or reject half-rest outcomes?
3. Does generated ScoreIR, MusicXML, or GPIF contain a half rest in the first
   affected measure?
4. What meter and per-voice durations are emitted?
5. At what earliest current stage does observed output first differ from the
   approved source facts?

Compare these facts with the historical ledger. Clearly label historical
facts, current observations, inferences, and unknowns.

## Decision Gate

Choose exactly one:

- `DEFECT_REPRODUCED`: the false half rest exists on current `main`; identify
  its first current stage and queue the smallest provenance instrumentation
  task only if its extractor/source remains unknown.
- `DEFECT_CHANGED`: current output is still wrong but the half-rest path no
  longer matches the historical ledger; define the new first divergence and
  smallest bounded next task.
- `DEFECT_NOT_REPRODUCED`: the false half rest is absent; do not implement the
  obsolete suppression. Record any remaining visible mismatch as a separate
  candidate task.
- `REPLAY_BLOCKED`: current approved input/runtime cannot be executed; state
  the exact missing prerequisite and smallest unblocker.

Do not authorize product implementation unless current evidence identifies a
specific committed-code injection point and a public-testable rule.

## Deliverables

Commit governance artifacts only:

- `projects/score2gp/reports/2026-07-24-cr04a-current-runtime-replay.md`;
- a versioned next prompt only when the decision gate supports one;
- synchronized `ACTIVE_TASK.md` and `prompts/NEXT.md`.

Run `git diff --check`, push the governance branch, and open one governance PR
with the decision and sanitized evidence. Stop for Codex review. Do not modify
product files, enable auto-merge, or merge.
