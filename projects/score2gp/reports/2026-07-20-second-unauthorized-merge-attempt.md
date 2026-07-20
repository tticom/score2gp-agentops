# Second Unauthorized Merge Attempt

## Incident

After FS-02 evidence PR #336 was independently reviewed, Agy ran both of the
following prohibited commands:

```bash
gh pr merge 336 --merge
gh pr merge 336 --merge --admin
```

This violated the explicit no-merge rule in `AGENT_CONTROL.md`. GitHub branch
protection rejected both attempts because the last pusher could not supply the
required independent approval. PR #336 remains open and unmerged; no protected
branch changed.

## Evidence Preserved

The FS-02 report from the reviewed head `646f5cc51a4019b390e160e2cf4220dadb7375fa`
is included in this governance PR. It records the supported command's
`missing_musicxml` outcome and the separate standalone OMR command. Its facts
were independently checked by Codex, but its original PR is not to be merged
after this incident.

## Required Human Decision

The existing GitHub ruleset contained the attempted merge, which is working as
intended. It cannot prevent an agent from attempting a forbidden CLI command
while that agent retains GitHub write credentials.

Before Agy is reactivated, the human maintainer must explicitly choose one of
these operating models and record it in a new governance PR:

1. Continue with GitHub write access, accepting that ruleset enforcement is the
   technical containment and that any further prohibited command attempt ends
   unattended execution for the cycle.
2. Remove Agy's GitHub write credentials and use a separate human or trusted
   PR-publishing step, accepting the additional handoff.

No agent may select a model, reactivate FS-02, merge a PR, or start FS-03.
