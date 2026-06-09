# Skill: Score2GP PR Hard Review

## Purpose
Perform a rigorous, evidence-based review of pull requests in the `score2gp` repository. This skill ensures that code changes meet the active task requirements, preserve evidence boundaries, maintain privacy, and pass all necessary CI/tests before human merge.

This skill is for **review only**. It must not decide the next architecture direction or define new tasks.

## Core Rule
Never trust self-reports. Verify live repository state, changed files, commits, PR status, CI, tests, and evidence before approving.

## Mandatory Pre-flight Checks
For PR review, always run:
```bash
gh pr view <number> --json state,merged,mergeCommit,headRefOid,baseRefName,isDraft,mergeable
gh pr diff <number>
gh pr checks <number>
```

For privacy/artifact checks on the checked-out PR branch:
```bash
git status --ignored
git ls-files | grep -Ei "(private|scratch|tmp|\.pdf$|\.gp$|\.log$|screenshot|output)" || true
find . -path "./.git" -prune -o -type f -size +10M -print
```

## PR Review Checklist
A hard review must verify:

1. **PR state:** open/closed/merged, draft status, base branch, head SHA, mergeability, CI/check status.
2. **Scope:** changed files match the active task, no unrelated refactors, no governance/product boundary violation, no hidden generated artifacts.
3. **Requirement fit:** matches active task, respects non-goals, does not expand into future tasks.
4. **Evidence:** exact commands run, targeted tests, full suite or justified subset, empirical smoke where required, CI status, known limitations.
5. **Privacy:** no private PDFs, no GP files unless explicitly intended, no screenshots/logs/debug dumps, no local work artifacts, no secrets/tokens.
6. **Architecture:** preserves evidence, does not synthesize data, avoids semantic inference unless explicitly authorised, keeps models and boundaries stable.

## Review Verdict Format
Use this exact structure for your response:

```text
Verdict: merge / needs changes / do not merge / cannot verify

Evidence reviewed:
- PR state
- head SHA
- changed files
- checks/tests
- patch areas inspected

Strengths:
- What is correct or useful

Problems:
- Defects, missing checks, weak assumptions, privacy risks, or process gaps

Required fixes:
- Specific blocking changes

Suggested next task:
- The next smallest safe step (to inform the orchestrator)
```

## Stop Conditions
Stop and report instead of continuing if:
- Required prerequisite PR is unmerged.
- Task requires private files or generated artifacts.
- Task introduces fake geometry, placeholder coordinates, or synthetic evidence.
- Tests fail for unclear reasons.
- Scope expands beyond the active task.
- Semantic inference would be introduced before governance authorises it.
- PR depends on another unmerged PR but is not explicitly stacked.
