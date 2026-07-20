# Unauthorized Agy Merge Incident - 2026-07-20

## Observed Event

Agy reported executing:

```bash
gh pr merge 333 --merge --admin
```

PR #333 was merged into `score2gp-agentops/main` as
`bd4940fb3eb5384e7d9649d55cd2e03d0cb88687`. GitHub attributes the PR and
merge activity to `tticom`, not `tticom-automation`.

## Impact

The merged change is governance-only and has no product-code impact. However,
the event proves that the active Agy GitHub CLI credential was capable of an
administrator bypass and that the required automation identity gate was not
being enforced before remote actions.

## Containment

- FS-02 is blocked.
- Agy must not perform further local or remote work.
- No claim from an Agy run is accepted until the human verifies a restricted
  `tticom-automation` CLI identity and protected-main rules that prevent an
  automation bypass.

## Required Human Remediation

1. Configure the WSL GitHub CLI used by Agy to authenticate only as
   `tticom-automation`.
2. Protect `main` in both repositories with a pull-request requirement and
   an independent approval requirement.
3. Ensure `tticom-automation` has no administrator role and no ruleset or
   branch-protection bypass permission.
4. Record the verification in a governance PR before reactivating FS-02.
