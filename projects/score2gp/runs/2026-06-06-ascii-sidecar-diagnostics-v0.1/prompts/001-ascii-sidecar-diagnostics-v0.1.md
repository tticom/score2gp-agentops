Title: Fix ASCII sidecar gate remediation hint key mismatch

Context:
You are working in the `score2gp` product repository.

This task follows the completed investigation in `score2gp-agentops` PR #48:

`docs: investigate ASCII sidecar diagnostics`

The investigation found a bounded diagnostics bug:

- ASCII gate refusal details are populated in `build_ir.py` using the key `expected_next_remediation`.
- `cli.py` reads `exc.details.get("remediation_hint")`.
- Because of this key mismatch, CLI stderr and `--json-report` fall back to:
  `Check the intermediate diagnostics report for details.`
- The correct specific remediation is already available from `_ascii_gate_remediation(...)`, but it is not surfaced through the key consumed by the CLI.

Recent product baseline:
- Product PR #174 merged.
- Merge commit: `385de47d630a88c9557377b5b26e120d51de20e5`
- Feature added mandatory SHA-256 source hash validation for ASCII alignment sidecars.
- Stale/hashless/missing/malformed/mismatched sidecars refuse with:
  - category: `ascii_alignment_stale_sidecar_hash`
  - CLI exit code: `4`

Goal:
Fix the remediation key mismatch so that ASCII sidecar gate refusals surface the specific remediation hint in both CLI stderr and `--json-report`.

Branch:
`feature/ascii-sidecar-diagnostics-v0.1`

Non-goals:
Do not implement ASCII conversion.
Do not implement rhythm inference.
Do not add OCR.
Do not change the sidecar schema version.
Do not redesign diagnostics output.
Do not add detailed hash-status text to stderr in this increment.
Do not alter non-ASCII conversion paths.
Do not commit private/generated artifacts.

Required pre-flight checks:
Run:

git status --short --branch
git fetch --all --prune
git switch main
git pull --ff-only origin main
gh pr view 174 --repo tticom/score2gp --json number,title,state,mergedAt,headRefName,headRefOid,mergeCommit,url
git log --oneline --decorate --max-count=10

Stop if PR #174 is not merged into local `main`.

Create the branch:

git switch -c feature/ascii-sidecar-diagnostics-v0.1

Likely files to inspect:
- `src/score2gp/build_ir.py`
- `src/score2gp/cli.py`
- `tests/test_cli_convert.py`
- `tests/test_ascii_scoreir_gate.py`

Implementation guidance:
In `src/score2gp/build_ir.py`, inspect `_apply_ascii_gate_refusal_details`.

The expected minimal fix is to include both keys in the refusal details:

- existing key:
  `expected_next_remediation`
- CLI-consumed key:
  `remediation_hint`

Do not remove `expected_next_remediation`, because HTML diagnostics or existing tests may rely on it.

The likely intended logic is:

details.update({
    ...
    "expected_next_remediation": _ascii_gate_remediation(primary),
    "remediation_hint": _ascii_gate_remediation(primary),
    ...
})

Avoid duplicating logic unnecessarily; if a local variable is cleaner, use one.

Test requirement:
Add or update a CLI test in `tests/test_cli_convert.py`.

Suggested test name:

`test_cli_convert_hash_refusal_contains_specific_remediation_hint`

The test should trigger `ascii_alignment_stale_sidecar_hash` through the real CLI convert path using a stale/hashless/malformed ASCII sidecar fixture or tmp_path setup.

Assertions:
- CLI exits with code `4`.
- CLI stderr contains the specific remediation hint, not the generic fallback.
- `--json-report` contains the same specific remediation hint as `recommended_action`.
- The refusal category remains `ascii_alignment_stale_sidecar_hash`.
- No GP output is produced for the refused conversion.

Expected remediation text:
Use the actual value from `_ascii_gate_remediation("ascii_alignment_stale_sidecar_hash")`.

Current expected text is likely:

`re-align the source PDF and MusicXML files to update the stale hashes`

But verify from the code rather than hard-coding from memory if possible.

Validation:
Run:

PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_ascii_scoreir_gate.py

If those pass, run:

PYTHONPATH=. .venv/bin/python3 -m pytest

Private safety checks:
Run:

git diff --check
git ls-files fixtures/private work

The private safety invariant must output exactly:

fixtures/private/.gitkeep

Also run:

git status --ignored --short
git ls-files | grep -E 'fixtures/private|work/|\.pdf$|\.gp$|\.gpif$|\.musicxml$|\.mxl$|\.json$|\.log$|\.png$|\.jpg$|\.jpeg$|\.html$' || true

If this catches legitimate tracked public test fixtures, inspect before acting. Do not remove legitimate existing tracked fixtures without evidence.

Acceptance criteria:
- Specific remediation hint appears in CLI stderr for ASCII stale/hash refusal.
- Specific remediation hint appears in `--json-report` as `recommended_action`.
- Generic fallback is not used when `remediation_hint` is available.
- Existing `expected_next_remediation` behavior is preserved.
- Exit code remains `4`.
- Refusal category remains `ascii_alignment_stale_sidecar_hash`.
- No non-ASCII paths are changed.
- No sidecar schema change.
- Tests pass.
- No private/generated artifacts are tracked.

Stop conditions:
Stop and report if:
- Fix requires changing sidecar schema version.
- Fix affects non-ASCII conversion paths.
- Test setup would require committing private files.
- The CLI is intentionally using the generic fallback for a reason found in code.
- Public tests fail for unrelated reasons.
- The working tree contains unrelated changes.

Commit and PR:
If validation passes:

git status --short
git add src/score2gp/build_ir.py tests/test_cli_convert.py
git commit -m "fix: surface ASCII sidecar remediation hints"
git rev-parse HEAD
git push -u origin feature/ascii-sidecar-diagnostics-v0.1

Open a product PR:

gh pr create \
  --repo tticom/score2gp \
  --base main \
  --head feature/ascii-sidecar-diagnostics-v0.1 \
  --title "fix: surface ASCII sidecar remediation hints" \
  --body "Fixes the remediation hint key mismatch so ASCII sidecar gate refusals surface the specific remediation in CLI stderr and --json-report. Preserves exit code 4, refusal category ascii_alignment_stale_sidecar_hash, and existing diagnostics behavior. No ASCII conversion, OCR, rhythm inference, schema change, or private/generated artifacts."

Reporting format:
Report:
- Branch
- Commit hash
- PR number and URL
- Files changed
- Exact implementation summary
- Commands run
- Test results
- CLI stderr/json-report behavior verified
- Private-safety result
- Any limitations
