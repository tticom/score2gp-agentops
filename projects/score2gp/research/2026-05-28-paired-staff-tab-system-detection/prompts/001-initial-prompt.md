# Prompt Record

## Prompt Metadata

- Prompt ID: 001
- Source: human
- Target agent: antigravity
- Date/time: 2026-05-28T08:23:14+01:00
- Supersedes: None
- Status: executed

## Explicit Prompt Text

```text
You are an expert Python engineer and diagnostic investigator working across the ScoreToGP product repo and agentops governance repo.

# Repositories

Product repo:
https://github.com/tticom/score2gp

Governance repo:
https://github.com/tticom/score2gp-agentops

# Current Situation

The Major Triads Lesson 3 benchmark still fails before strict ScoreIR and GP generation.

The latest visual overlays suggest an important hypothesis:

The layout detector may not correctly model Guitar Pro paired staff systems.

A Guitar Pro printed row usually contains:

1. a standard notation staff above,
2. a TAB staff below,
3. shared/aligned barlines,
4. fret numbers on the six TAB string lines.

For ScoreToGP’s current purpose, the TAB staff is authoritative for string/fret geometry. The standard notation staff above should not be treated as TAB string geometry. It should not create competing TAB systems. It should not cause notation stems/beams to be interpreted as TAB barlines.

# Critical Warning

Do not assume the hypothesis is true.

Your task is to prove whether paired-staff conflation is:

* supported,
* unverified,
* contradicted.

Do not implement a production fix in this task.

Do not implement the 5-line-vs-6-line mask yet.

The exact line-count rule is risky because a broken TAB staff may itself be detected as 5 lines. If you mask all 5-line groups as notation, you may throw away damaged TAB evidence.

# Branches

In `score2gp`, create from clean `main`:

`research/paired-staff-tab-system-detection-v0.2`

In `score2gp-agentops`, create from clean `main`:

`research/paired-staff-tab-system-detection-v0.2`

Use `v0.3` if either branch already exists.

# Mandatory Prompt Chain Record

Before completing the task, create a run/research directory in `score2gp-agentops`:

```text
projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/
  RUN.md
  prompt-manifest.json
  prompts/
    001-initial-prompt.md
```

Store this entire prompt exactly in:

```text
prompts/001-initial-prompt.md
```

Record the prompt in `prompt-manifest.json`.

The task is incomplete without the prompt-chain record.

# Required Reading

From `score2gp-agentops`, read:

* `projects/score2gp/README.md`
* `projects/score2gp/REVIEW_RULES.md`
* `projects/score2gp/ACCEPTANCE_TARGETS.md`
* `projects/score2gp/BENCHMARK_LADDER.md`
* `projects/score2gp/MAJOR_TRIADS_BENCHMARK.md`
* `projects/score2gp/templates/RUN_RECORD_TEMPLATE.md`
* `projects/score2gp/templates/RESEARCH_REPORT_TEMPLATE.md`
* `projects/score2gp/templates/PROMPT_CHAIN_README.md` if present
* `projects/score2gp/templates/PROMPT_MANIFEST_TEMPLATE.json` if present

From `score2gp`, read:

* `AGENTS.md`
* `HANDOFF.md`
* `docs/architecture.md`
* `docs/limitations.md`
* `src/score2gp/pdf.py`
* all PDF parsing tests
* all tests related to system detection, barline detection, string assignment, and edge-boundary fallback

# Required Inputs

Use the existing private Lesson 3 diagnostic artifacts locally if available:

* `summary.json`
* `warnings.json`
* `tab_raw.json`
* `grouping-diagnostics.html`
* `pdf-edge-boundary-report.json`
* `pdf-edge-boundary-report.html`
* `page-001-grouping.png`
* `page-002-grouping.png`
* `page-003-grouping.png`
* `page-004-grouping.png`
* clean page images if available

If artifacts are missing, regenerate them into a fresh output directory.

Do not delete old output directories.

Do not commit artifacts.

Do not print private fret sequences or private musical text.

# Investigation Goal

Determine whether the parser is:

1. splitting one real TAB row into multiple pseudo-systems;
2. mixing notation-staff geometry into TAB-staff detection;
3. treating note stems/beams from the standard notation staff as barline candidates;
4. failing because it lacks an explicit paired notation+TAB layout model.

# Research Questions

## RQ1: Visual TAB rows vs detected systems

For each page, produce private-safe counts:

* visually apparent TAB rows per page,
* detected/inferred systems per page,
* systems with overlapping y-ranges,
* systems with overlapping x-ranges,
* systems with fewer than six string lines,
* systems that cover only part of a visible TAB row’s x-span,
* systems that appear to overlap the notation staff instead of the TAB staff.

Do not report private notes/frets.

## RQ2: Are 5-line notation staves entering TAB detection?

Classify detected horizontal-line groups as one of:

* likely six-line TAB staff,
* likely five-line standard notation staff,
* incomplete TAB candidate,
* fragmented TAB candidate,
* ambiguous / cannot classify safely.

Use geometry only.

Important: do not hard-code “5 lines = notation” as a fix. The report must explain how to distinguish an actual five-line notation staff from a damaged/incomplete TAB staff.

## RQ3: Are notation stems/beams being treated as TAB barlines?

For rejected vertical candidates on failing systems, classify private-safe geometry only:

* inside notation staff,
* inside TAB staff,
* spanning both notation and TAB,
* outside both,
* likely notation stem/beam artifact,
* likely true shared barline,
* ambiguous.

Report counts, not musical content.

## RQ4: What is the first actual mechanical failure?

Use page/system indices and warning codes.

Do not say “system is ambiguous” only. Explain the mechanism.

Examples of acceptable mechanical conclusions:

* “One visible TAB row is split into two horizontal systems due to x-fragmentation.”
* “A notation staff is incorrectly included in the same horizontal-line cluster as a TAB staff.”
* “The detector identifies a five-line notation staff as an incomplete TAB staff.”
* “The barline validator is testing vertical candidates against the wrong y-range.”
* “The evidence is insufficient; current diagnostics do not expose enough geometry to conclude.”

Only use a conclusion if supported.

## RQ5: What public fixture would prove the issue?

Design a public synthetic fixture, but do not implement it yet unless explicitly safe and small.

The fixture should model:

* one standard notation staff above,
* one six-line TAB staff below,
* shared barlines,
* notation stems/beams above,
* fret digits on TAB lines,
* optionally a damaged/incomplete TAB line case.

Expected assertions:

* detector identifies exactly one TAB staff row;
* standard notation staff is not counted as TAB strings;
* notation stems are not treated as TAB barlines;
* damaged TAB staff is not discarded merely because it has five detected lines;
* ambiguous cases refuse safely.

# Required Output In Agentops

Write the durable research report:

```text
projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/RUN.md
```

Use this structure:

[report structure omitted for brevity in nested block]
```

## Notes

* Any local context, branch, or repo state assumptions:
* Any known limitations:
