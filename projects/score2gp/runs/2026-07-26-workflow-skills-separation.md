# Workflow Skills Separation

## Trigger

CR-04D completed with product PR #390 merged at
`d70d559152c5aa357a7d2eb38e65b09f288bb08f`. The maintainer authorised a
process pass separating reusable skill versioning from PDF-to-GP product work.

## Reusable skills change

- Repository: `tticom/agy-skills`
- PR: `https://github.com/tticom/agy-skills/pull/2`
- Source commit: `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`
- Added: `governed-development-loop`, `identity-safe-git`,
  `durable-handoff`

Validation:

- all three skills passed `quick_validate.py`;
- skill and plugin manifests parsed and listed the promoted skills;
- the identity gate rejected an incorrect Git email and passed with the live
  Codex identity;
- `git diff --check` passed;
- Claude plugin validation was unavailable because the Claude CLI is not
  installed in the Codex workspace.

## AgentOps change

AgentOps now supplies a thin Score2GP workflow profile and skills lock.
Product-specific authority, privacy, conversion evidence, review posture, and
continuation policy remain here. Generic loop, identity, publication, and
handoff mechanics live in the skills repository.

## Activation dependency

The AgentOps profile must not merge or activate until agy-skills PR #2 merges
with the required source commit in `main` history. Both Linux identities must
then pin and link their own skills checkout to that exact revision.

No Score2GP product code, conversion fixture, schema, or product task is
changed or authorised by this process work.
