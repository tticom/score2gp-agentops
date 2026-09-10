# `agy-skills` upstream review — 2026-09-10

## Decision

Do not merge or rebase the five upstream commits into `tticom/agy-skills` at
this time. Keep the fork's AGY-specific history and review the individual
ideas later only if a concrete need appears.

This is a deferral, not a claim that the upstream work is defective.

## Repository topology

| Role | Repository / ref |
|---|---|
| Fork and push remote (`origin`) | `https://github.com/tticom/agy-skills.git` / `main` at `583974037dd83a5a8f29d5c543d12bc81f2bcf33` |
| Original repository (`upstream`) | `https://github.com/mattpocock/skills.git` / `main` at `3cca18b368ae95cdbdebbff572ccafa662551015` |
| GitHub relationship | `tticom/agy-skills` is a fork of `mattpocock/skills` |
| Common ancestor | `5b15a47f2d7150f545fbcacbfe381787fc0230dc` |
| Divergence | Fork is 55 commits ahead; upstream is 5 commits ahead |

`origin` is the writable TTICom fork. `upstream` is read-only comparison
source. Neither remote is an automatic merge source.

## Upstream-only commits reviewed

| Commit | Content | Decision | Reason |
|---|---|---|---|
| `8fa1886` | Adds an explicitly non-functional retrospective skill stub and OpenAI metadata | Defer | Potentially useful for future retrospectives, but not operational and not needed by the current AGY cycle |
| `3ec8e23` | Refines the retrospective stub and lists it in the in-progress README | Defer | Depends on the stub and adds no current execution capability |
| `6654f6b` | Adds an `Information access` retrospective category | Defer | Useful only if the retrospective skill is adopted |
| `8666e05` | Stops `misc/` skills being linked into local skill directories | Adapt later | The intent is useful, but the upstream script targets a different `skills/` layout; the fork uses bucket plugins and must implement the policy in its own installer path |
| `3cca18b` | Merge commit for `8666e05` | No independent action | Contains no additional change beyond the merged pull request |

## Why wholesale synchronization is rejected

The upstream branch has since moved toward a different `skills/` layout and
plugin model. A wholesale merge would mix unrelated structural changes with
TTICom's AGY-specific skills and could remove or relocate governed development,
identity-safe Git, hard review, durable handoff, and other pinned capabilities.

The Score2GP AgentOps lock remains pinned to the reviewed fork history, not to
upstream `main`. A future skills update must be a deliberate fork change
followed by an AgentOps lock update.

## Revisit triggers

Re-review a specific upstream commit when one of these becomes true:

1. a retrospective command is needed for the AGY cycle history;
2. the fork's installer or pin activation is changed, making `misc/` leakage a
   live problem; or
3. upstream supplies a concrete fix that maps to a named AgentOps backlog item.

When revisiting, compare the individual commit against the fork's current
layout, run the relevant skill/install tests, and record an adopt/adapt/ignore
decision here before changing the lock.

## Evidence

The review used fetched `origin/main` and `upstream/main` refs and:

```text
git rev-list --left-right --count main...upstream/main
55 5
```

No source files or secrets from upstream were copied into this repository.
