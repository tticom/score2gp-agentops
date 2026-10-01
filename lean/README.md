# lean/: the replacement framework (inert until cutover)

Nothing in this directory is read by the live framework (dispatcher, authority,
launchers). It is built beside it and promoted at cutover (`../CUTOVER.md`).

| File | Purpose |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | One page of agent guidance, replacing `AGENT-RULES.md`, `AGENTS.md`, `CLAUDE.md` |
| `TASKS.md` | The only task list, replacing the authority state machine |
| `PULL_REQUEST_TEMPLATE.md` | Six-section PR body |
| `hooks/pre-push` | Blocks pushes to `main`/`master`, deletion of them, and force pushes |
| `scripts/install_hooks.py` | Installs, checks or removes the hook (copies it into the clone's shared hooks dir, so worktrees are covered) |
| `scripts/real_fixture_check.py` | Local real-fixture check on the maintainer machine; sanitised summary; PASS / FAIL / NOT_EVALUATED |
| `reports/TEMPLATE.md` | One-page decision report: the only run/analysis record that is versioned, with its evidence |
| `tests/` | Tests for the hook, installer and fixture check (real git repos in temp dirs) |

## What the hook is, honestly

GitHub's free plan has no branch protection or rulesets on private repositories.
So "no direct push to main" is **convention plus a local hook**, not server
enforcement. The hook catches mistakes. It does not stop `git push --no-verify`,
a clone without the hook installed, a different `core.hooksPath`, or someone who
sets the override variables (`LEAN_ALLOW_PROTECTED_PUSH`, `LEAN_ALLOW_FORCE`).
The only server-side control available on the free plan is the agent credential:
an agent identity with no write access to the repository (it pushes to its own
fork). See `../CUTOVER.md` step 10.

## Usage

```text
python lean/scripts/install_hooks.py            # install in this clone
python lean/scripts/install_hooks.py --check    # verify it is active and unmodified
python lean/scripts/install_hooks.py --uninstall

python lean/scripts/real_fixture_check.py --product <path to score2gp checkout> [--fail-on-skips] [--require-clean]
```

`real_fixture_check.py` exit codes: 0 PASS, 1 FAIL, 2 NOT_EVALUATED (fixtures
missing, or a required step could not run). Raw output goes to a log directory
outside the product repo and is never printed.

## Tests

```text
python -m pytest lean/tests
```
