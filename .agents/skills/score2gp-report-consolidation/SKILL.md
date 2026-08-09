---
name: score2gp-report-consolidation
description: Consolidated multi-branch diagnostic report synthesis and GitHub governance review workflow for Score2GP.
---

# Score2GP Report Consolidation & Review Skill

Use this workflow to audit investigation branches, synthesize overlapping diagnostic reports into a master benchmark report, and submit formal GitHub reviews.

## Workflow Steps

1. **Audit All Investigation Branches**:
   - Inspect git commit history and report markdown files across active investigation branches.
   - Run empirical test conversions against real ground-truth fixtures (`Lesson-5.pdf`, `Lesson-6.pdf`).
   - Audit for false test pass signals and symptom-masking hacks (geometry tolerance expansion, duration scaling, naive digit merging, open-string synthesis).

2. **Synthesize Master Benchmark Report**:
   - Create a single consolidated report in `projects/score2gp/reports/`.
   - Explicitly cite and deconstruct prior branch claims and failure mechanisms.
   - Document ground-truth metric comparisons (bar counts, note counts, tempos, tracks, fingerings).
   - Outline the 4-pillar target architecture (Visual TAB OMR, Topologically Locked System Barlines, Biomechanical Position Optimizer, Ground-Truth CI Harness).

3. **Publish to Master Recovery Branch & Submit GitHub PR Review**:
   - Create a clean master recovery branch in `score2gp-agentops`.
   - Commit and push the consolidated report and recovery programme backlog.
   - Submit formal review verdict (`gh pr review <PR_NUMBER> --approve -F <REVIEW_FILE>`).
