# Score2GP PR Evidence Contract

## Purpose

This is the author-side counterpart to adversarial review. It is designed to
surface missing proof before a PR is opened, so review can test a compact set
of falsifiable claims rather than repeatedly correct a plausible narrative.

It applies to every Score2GP product and governance PR. It does not authorise
work, replace review, or permit an agent to merge a PR.

## Required PR Body

Every PR body must contain these sections. Use `unproven` rather than filling a
gap with inference.

### 1. Scope

- **Task and exact outcome:** the authorised task identifier and one sentence
  describing the intended observable change.
- **Baseline:** base branch and full base SHA; for runtime work, the exact
  executable, import path, input class, and sidecar provenance.
- **Changed files:** an explicit list. Any file outside the authorised scope is
  a blocker until separately authorised.
- **Non-goals:** concrete excluded behaviour.

### 2. Claim Ledger

Use this table for every material claim:

| Claim | Evidence inspected or command | Exact revision and input | Observed result | Limit or remaining unknown |
|---|---|---|---|---|

Valid claims are narrow and testable. "Works", "supported", "stable",
"complete", "fixed", and "ready" are not evidence. A passing unit test alone
does not prove a conversion, recognition, or visual-output claim.

For architecture PRs, the ledger must cite exact source paths and line numbers
at a full product SHA. It must classify each route as `supported`, `unproven`,
`unavailable`, or `uncontrolled`; the report must not promote an `unproven`
route by implication.

For product PRs, the ledger must include the product-level acceptance output
required by the active task, plus the first known remaining mismatch or
refusal. Runtime claims must record the committed command, executable, import
path, input class, sidecar hash when applicable, and exit status.

### 3. Pre-submit Challenge

The author must answer these before opening the PR:

1. What is the strongest way this could appear successful while failing the
   product outcome?
2. Which command, source inspection, generated artifact, or regression test
   rules that out?
3. Which failure modes remain untested, and do they limit the claim?
4. Is any assertion based only on fixture-specific coordinates, bar numbers,
   filenames, titles, reference GP data, aggregate counts, or file creation?
   If yes, the PR is not ready unless the active task explicitly permits it.
5. Does the evidence come from the exact remote head intended for review? If
   not, the PR is `PR_OPEN`, not ready.

### 4. Validation And Handoff

Record exact validation commands, results, and any intentionally unrun checks.
After push, state only:

```text
PR state: PR_OPEN — awaiting independent review
Head SHA: <40-character remote head>
Unresolved risks: <list>
```

The author may revise the same branch for accepted review findings, then
repeat this contract for the new remote head. Do not amend published commits,
force-push, create self-review noise, or invoke a merge command.

## Review Efficiency Rules

- A reviewer should return one consolidated set of currently known blockers,
  ordered by severity, against the exact remote head.
- An author must address every blocker in one evidence-backed revision when
  feasible, rather than drip-feeding cosmetic corrections.
- New blockers discovered only after a revision are normal review findings,
  not a process failure. They must be added to the next claim ledger.
- If a required fact cannot be proved, narrow the task to evidence collection
  or artifact validation. Do not claim a functional capability.
