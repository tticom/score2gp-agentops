# CP-10: Decode gh output as UTF-8 in the control plane

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-10-decode-gh-output-as-utf-8`
- **Depends on:** none

## Goal

`run_json` and `capture_live_state` in `scripts/score2gp_orca_control.py`, and the `gh` calls in `scripts/score2gp_got_bootstrap.py`, call `subprocess.run(text=True)` with no encoding, so on Windows they use the locale codec and crash with a cp1252 `UnicodeDecodeError` on UTF-8 review text (seen: `snapshot --pull-request 700`, byte 0x9d; the merge executor on #708; a false governance-audit violation on #712 because the gh read returned no comments). Launchers force `PYTHONUTF8=1` as a stopgap. Fix the cause so the stopgap is no longer needed.

## Acceptance

1. Measure first: list every `subprocess` call in `scripts/` that reads `gh` (or `git`) output as text without an explicit encoding, and reproduce the crash on the base with `PYTHONUTF8` unset and a stub `gh` that emits non-cp1252 UTF-8 bytes (for example byte 0x9d inside valid UTF-8 text).
2. Every such call passes `encoding="utf-8"` (and an explicit `errors` policy stated in a code comment). A grep-style test over `scripts/` fails if a text-mode subprocess call without an encoding is reintroduced.
3. A test feeds non-cp1252 UTF-8 bytes through `run_json` and `capture_live_state` and passes; the same test fails (UnicodeDecodeError or wrong text) on the base. Name the mutants it rejects: drop the encoding, use `latin-1`, swallow the error and return empty output.
4. The governance audit and the merge executor give the same result with `PYTHONUTF8` unset as with it set, on this machine; record both.
5. The stopgap is not removed from launchers in this task; list where it is set so a later task can remove it.
6. Validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate, and do not change what a gate accepts; this task changes only how bytes are decoded.
- Tests must be able to fail: for each new test, name the wrong implementation it rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if a change to a gate is needed.
