# Prompt Record

## Prompt Metadata

- Prompt ID: 002
- Source: human
- Target agent: antigravity
- Date/time: 2026-05-28T08:52:43+01:00
- Supersedes: 001
- Status: executed

## Explicit Prompt Text

```text
You are an expert technical editor and sceptical reviewer working in the ScoreToGP agentops repository.

Repository:
https://github.com/tticom/score2gp-agentops

Current PR:
PR #7 — Research paired notation and TAB staff detection
Branch:
research/paired-staff-tab-system-detection-v0.2

# Goal

Revise PR #7 so the research report is accurate, sceptical, and does not overclaim.

This is a documentation/research correction only.

Do not modify the product repo.
Do not modify ScoreToGP source code.
Do not add benchmark outputs.
Do not add private files.
Do not claim conversion progress.

# Required Context

The current PR #7 report is useful and directionally valuable, but it overstates certainty.

The report currently says things like:

- “Definitive geometric and statistical evidence proves…”
- “The PDF parser conflates standard notation staves…”
- “This proves that 56 standard notation stems…”

Those claims are too strong.

The report’s own findings are more nuanced:

- It reports 21 visible TAB staves but 43 inferred systems.
- It reports 100% of inferred systems cover only part of the visual staff row.
- It reports 0 systems overlap the notation staff instead of TAB.
- It reports the standard notation staff lines are not successfully grouped as standalone 5-line systems.
- It reports notation stems and TAB rhythm stems appear in vertical candidate telemetry.
- It reports one incomplete TAB candidate and many fragmented TAB candidates.

Therefore the better conclusion is:

The paired-staff hypothesis is **strongly supported**, but not “definitively proven.”

The central mechanism should be stated as:

“The detector lacks an explicit paired notation+TAB model. It fragments TAB rows into partial pseudo-systems and allows notation/TAB stems to pollute vertical barline-candidate telemetry.”

Do not state that the standard notation staff is being promoted as a TAB staff unless the report’s own evidence supports that. The current report says that hypothesis is unverified.

# Required Changes

Update:

projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/RUN.md

## Required wording changes

1. Change Summary Verdict from:

“Supported. Definitive geometric and statistical evidence proves…”

to something like:

“Strongly supported. The available private-safe geometry evidence supports the hypothesis that the current detector lacks a paired notation+TAB model. The strongest evidence is inflated inferred-system counts, partial horizontal spans, fragmented TAB candidates, and vertical candidate pollution from notation/TAB stems. This is sufficient to justify a public synthetic fixture and a narrow implementation slice, but it is not yet a fully proven production fix.”

2. Replace “conflates standard notation staves and note stems with authoritative TAB string staves and barlines” with more precise wording:

“The detector fragments TAB rows into partial pseudo-systems and allows notation/TAB stems to enter barline-candidate telemetry. The evidence does not show that five-line notation staves are being successfully promoted as TAB systems.”

3. Replace “This proves that 56 standard notation stems…” with:

“This supports the hypothesis that notation/TAB stems pollute candidate telemetry; the classification is private-artifact-derived and should be validated by a public synthetic fixture.”

4. In “First Mechanical Failure,” avoid claiming a final root cause. Use:

“The first supported mechanical explanation is…”

5. In “Supported Hypotheses,” split the claims:

Supported:
- Collinear horizontal line splitting / partial x-span fragmentation.
- Vertical candidate telemetry pollution from stems.

Strongly supported but still fixture-required:
- Lack of explicit paired notation+TAB model.

Unverified:
- Five-line standard notation staves are promoted as TAB systems.
- This mechanism alone explains every remaining layout blocker.

6. In “Contradicted Hypotheses,” add:

- “Standard notation staves are directly grouped as competing TAB systems” is contradicted or at least not supported by the current report, because it reports 0 notation-overlap systems and says notation staves are too fragmented to form grouped staves.

7. In “Recommended Implementation Slice,” make the order safer:

First:
- add public synthetic paired notation+TAB fixture;

Then:
- implement collinear horizontal segment merging;

Then:
- implement spacing-aware TAB-vs-notation classification;

Then:
- filter vertical barline candidates against the authoritative TAB grid;

Include:
- guardrail for damaged/incomplete TAB rows so a 5-line damaged TAB candidate is not automatically discarded as notation.

8. Avoid saying “exactly” or “always” for private-derived spacing values.

Replace:
- “Always has a line-to-line gap of 8.5”
- “Always has a line-to-line gap of 6.4”

with:

- “In this benchmark run, likely notation staves cluster around…”
- “In this benchmark run, likely TAB staves cluster around…”

9. Add a short “Review Caveats” section:

## Review Caveats

- The report is based on local scratch analysis of private Lesson 3 artifacts.
- The private artifacts are not committed.
- The findings are strong enough to justify a public synthetic reproduction fixture.
- The findings are not yet a production fix.
- Public fixture coverage is required before implementing production parsing changes.

# Required Prompt Chain Update

Update the prompt-chain metadata if necessary.

Add a second prompt record if this correction prompt is part of the same PR:

projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/prompts/002-overconfidence-correction.md

Update:

projects/score2gp/research/2026-05-28-paired-staff-tab-system-detection/prompt-manifest.json

Set operative_prompt_id to 002 if this correction changes the final report conclusion.

# Verification

Run:

git diff --check
git status --short
git status --branch

# PR

Push the update to PR #7.

Do not mark the PR ready for review unless the wording has been corrected.

Final response must include:

- branch name
- commit hash
- files changed
- exact wording classes corrected
- whether prompt chain was updated
- verification results
```

## Notes

* Any local context, branch, or repo state assumptions:
* Any known limitations:
