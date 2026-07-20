# FS-02 Resumption Verification

## Purpose

This record satisfies the recovery condition in the Unauthorized-Merge
Incident Gate. It does not complete FS-02, approve PR #332, or authorise
FS-03.

## Verified Automation Identity

The canonical Ubuntu WSL environment reported:

- GitHub CLI user: `tticom-automation`.
- Product local Git author: `tticom-automation <tticomautomation@gmail.com>`.
- Governance local Git author: `tticom-automation <tticomautomation@gmail.com>`.

The account has repository write access, not administration access. It can
open and update task branches, but must not merge pull requests, use bypass
flags, or update `main` directly.

## Verified Main Protection

Both `tticom/score2gp` and `tticom/score2gp-agentops` have an active
`Main_Protect` ruleset targeting the default branch. The rulesets:

- block direct updates, deletions, and non-fast-forward updates;
- require a pull request with one approving review;
- require approval of the latest pushed commit and resolved review threads;
- dismiss stale approvals when a new commit is pushed; and
- report that `tticom-automation` cannot bypass the ruleset.

These controls prevent the automation identity from repeating the merge and
direct-main incidents that caused the suspension.

## Decision

FS-02 may resume from a fresh task branch after this governance PR is
externally merged. The Developer must follow the WSL execution, edit
coherency, runtime-provenance, and no-merge gates in `AGENT_CONTROL.md`.

PR #332 is superseded because it is based on stale governance and conflicts
with the suspension state. Its local-only commit and untracked scratch script
are not evidence and must not be copied, reconstructed, or treated as an
accepted result.

## Required FS-02 Result

The new FS-02 PR must establish, at an exact product SHA, the supported
`.venv/bin/score2gp convert` call path and its actual outcome. It must
separately document any standalone OMR command with direct source and command
evidence, without claiming that it is invoked by `convert`. A distinct
reviewer must verify the final remote PR head before it is presented for human
merge.
