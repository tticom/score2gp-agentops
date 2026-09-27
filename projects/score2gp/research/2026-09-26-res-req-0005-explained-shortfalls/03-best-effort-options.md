# 3. Best-effort delivery options, evaluated against the fail-closed rules

Product SHA `3af19250bcc716ccc8a3e2b2102db897f78e56e5`.

## 3.1 The fail-closed rules used for evaluation

Each rule is quoted or paraphrased from an authority record, and the evaluation cites it by id.

| Rule | Source | Statement |
|---|---|---|
| FC1 No fabrication | [REQ-0001](../../requirements/REQ-0001-native-faithful-pdf-to-gp.md) summary; native plan §3 invariant 2 | Uncertain input is diagnosed, repaired within bounds, or refused, and never guessed. Missing and ambiguous are explicit states, not confident facts. |
| FC2 Non-success when unresolved | L3 plan, final acceptance contract, "Uncertainty" gate | Unresolved cases produce a located diagnostic **and a non-success result**. |
| FC3 Located diagnostic | same gate | Every unresolved case is located. |
| FC4 Coverage | L3 plan, "Whole-document coverage" gate | Every source page, system and measure is accounted for exactly once; no dropped or invented musical material. |
| FC5 No inferred rhythm in success | L3 plan, "Defaults" gate | No defaulted or layout-inferred rhythms in a successful result; only genuinely absent facts may default, with provenance. |
| FC6 No invented padding | L3 plan, "Compilation" gate | No note clamping, partial-chord loss, invented padding or inferred measure fabrication. |
| FC7 Zero false success | REQ-0001 acceptance; native plan qualification gates | No run reports success for an output that is not faithful. |
| FC8 No partial as complete | REQ-0005 requirement 3 | Never present a partial result as complete; label every gap. |

An option **fails** if any rule can be broken without a label reaching the user.

## 3.2 What the runs say a best-effort output could contain today

From the per-bar replay (map §1.3, `evidence/run-matrix-facts.json`), in PDF-only mode across the
seven sources:

| | Bars |
|---|---|
| Source bars (independent layout inventory, map §1.3a) | 277 |
| …reached by the PDF-only builder (≥1 playable candidate) | 275 |
| …never reached: candidate-only 1 (EX2), empty 1 (CFMWH); no output bar, no record (G21) | 2 |
| Pass the product's current per-bar checks | 105 |
| …and contain no candidate with a non-exempt candidate-level code and no synthesised rest | 17 |
| Refused by the current checks | 170 (`pdf_only_tab_measure_overcapacity` 107, `pdf_only_tab_ambiguous_duration` 63) |

Even the 17 "clean" bars have durations chosen from the number of events (`D1`). None of the 277
has observed rhythm. So with tab-only input, a best-effort result can deliver **observed
string/fret content** for some bars, and only **approximated** rhythm. Any design must be able to
say that at bar level. Today, per-bar success is necessary but not sufficient for correctness:
88 of the 105 assembled bars hold low-confidence notes or synthesised rests that nothing labels
(gaps G8, G9).

## 3.3 Options

### Option 0: status quo (for reference)

`--pdf-only-tab` and `--editable-draft` produce a single GP. `status: success`, exit 0, one
document-level warning (`pdf_only_tab_inferred_timing` / `pdf_editable_draft`). The first bad
bar refuses the whole document.

| Rule | Result |
|---|---|
| FC2, FC5, FC7, FC8 | **Broken.** An inferred-rhythm result is reported as `success` (`cli.py:1349-1354`), observed on `PUB`. The GP carries only a title (`build_ir.py:1806`) in pdf-only mode. |
| FC3 | Broken: no per-bar location (G2-G4). |
| FC6 | Broken silently: synthesised rests with confidence 1.0 (G8). |
| FC7 on repeat runs | Broken: a refused run leaves an earlier run's `--out` in place, unchanged and unmarked (§3.3a, observed). |

Not acceptable as the best-effort design. It is listed because it is what ships.

### Option A: one mode switch, gap bars inside a single partial GP

`convert --best-effort` (default off). Bars that pass a **strict per-bar gate** are delivered.
Every other bar is present as a **gap bar**, with a visible GP marker such as
"NOT CONVERTED — rhythm-ambiguous (see report)". Run status `partial`, non-zero exit (new code,
e.g. 6). The report lists every gap.

Strict per-bar gate: all notes from candidates with no non-exempt candidate-level code; no
synthesised content; each field is either observed or carries disposition `approximated` or
`defaulted` with a bar-level label.

| Rule | Result |
|---|---|
| FC1 | Holds if the gate is strict. Approximated rhythm must be labelled per bar, not per document. |
| FC2, FC7 | Holds for callers that follow the run-bound output contract (§3.3a): `partial` is a non-success status with a non-zero exit, recorded against the caller's `run_id`. A partial GP at `--out` misleads any caller that tests only for the file, so the contract's consumer rule is mandatory here. |
| FC3 | Holds: records carry page/system/source bar (design 04). |
| FC4 | Holds only if "every source bar" means the independent layout inventory (map §1.3a). A bar with no playable candidate must become a gap bar too (G21); a builder keyed on playable candidates silently drops it. |
| FC6 | **Risk.** GP has no "unknown" bar content. An empty or gap bar is rendered, and played back, as silence. That is invented material unless the marker is in the file. Whether GPIF can hold a bar with no beats that GP 7/8 opens without repairing to a rest is **Unverified** (maintainer decision D3). |
| FC8 | Holds only while the marker survives in the file. Once the user edits the GP and deletes the marker, the file no longer says it is partial. |

Verdict: **acceptable with conditions**. Gap bars must be labelled inside the file, the status
must be non-success, and the GP gap representation must be verified in the real application
first.

### Option B: complete-or-nothing primary output, plus a separate partial artifact

The primary `--out` is written **only** when the conversion is complete and faithful (today's
contract). When it is not, the run exits non-success, does not write the primary output, and
writes the artifacts below. "Does not write" is not enough on a repeat run: an earlier run's file
can already be at `--out`. Option B therefore includes the **run-bound output contract** of §3.3a,
and the verdict below holds only with it.

- `<name>.partial.gp`: delivered bars plus labelled gap bars, as in Option A, with the title
  prefixed "PARTIAL — " and a FreeText notice (the draft mode already writes one; `PUB` draft run
  observed it in the GPIF);
- `shortfall-report.html` and `shortfall-records.json` (design 04, mock-up 05).

| Rule | Result |
|---|---|
| FC1, FC3, FC4, FC6 | As Option A, with the same GP gap-bar condition (D3). |
| FC2, FC7 | **Holds only for callers that follow the run-bound output contract (§3.3a).** The file at `--out` can be an earlier run's complete output, and a failed rerun can leave it unchanged (observed at the pinned SHA, §3.3a run S2). No file-system rule removes that for every run: a refused rerun without `--overwrite`, or a run that dies before its first write, still leaves the old file (§3.3a model, control 2). So the contract does not promise "this run's output or absent". It defines success as the caller's own run record (matching `run_id`, `status: success`, exit 0, and the SHA-256 of the file at `--out` equal to the recorded hash), and it states that **file presence alone is never proof of success**. A caller that tests only for the file is outside the contract, and FC7 is not claimed for it. |
| FC8 | Holds with the contract: the file name, title and notice all say partial, a partial file is never published to `--out`, and with `--overwrite` a stale partial from an earlier run is moved out of place before a later run's stages start (§3.3a, case S3′). |

Verdict: **acceptable; recommended, conditional on the run-bound output contract (§3.3a).** It
keeps the strict contract of `--out` and adds the partial artifact beside it. That also separates
the two for pricing (partial output with located gaps could be priced lower than complete
output). The recommendation assumes every consumer that decides "success" (the CLI user,
`batch`, integrators) reads the run record. Callers that only test for the file, such as
`batch.py:91-92` today, must change; the design does not make them safe.

### 3.3a Repeat runs and stale outputs (applies to every option)

**Observed at the pinned SHA.** Runs used the product venv, with outputs under the gitignored
`<product>/work/res-req-0005/probe/stale/`:

| Run | Input | Arguments | Exit | Report `status` / `output_written` | File at `--out` after the run |
|---|---|---|---|---|---|
| S1 | public `PUB` fixture | `convert --pdf-only-tab --out out.gp --work-dir w1 --json-report r1.json` | 0 | `success` / true | written by S1 |
| S2 | L5 | same `--out out.gp`, `--work-dir w2`, `--json-report r2.json` | 2 (`pdf_only_tab_ambiguous_duration`) | `refused` / false, `output_path` null | **S1's file, unchanged** (same SHA-256 and mtime) |
| S3 | L5 | same `--out`, `--work-dir w1` and `--json-report r1.json` reused | 2 | `refused` / false (report rewritten) | S1's file, unchanged |

After S3, `w1/` still holds S1's `score.ir.json` and `symbol-attachment-diagnostics.html`
(S1's mtime) beside S3's `tab/tab_raw.json`, `warnings.json` and `diagnostics.json`. The stale
`score.ir.json` names `w1/tab/tab_raw.json` as its source, and that file now holds a different
input. Code: `cli.py:1296-1309` writes `temp_output.gp` and moves it to `--out` only on success.
No refusal or failure path removes or marks an existing `--out` (the refusal branches only pass
`output_written=False` to the report, e.g. `cli.py:1252, 1283, 1336`), and no stage clears the work
directory. `batch.py:91` writes straight to its output path; a failing payload leaves an earlier file there
(observed, map §1.9 B4). `batch.py:59-75` reports a cache hit as `success`.

So a file's presence alone never proves "this run succeeded", today or under any option. The
JSON report is rewritten on every run that reaches a handled exit. It does not cover a run that
dies before `_write_convert_report` (the `generate-sidecar` traceback, G5, has no report at all).

**Run-bound output contract** (proposed; required for Option B and for A).

The contract's rule for consumers comes first, because no file-system behaviour can replace it.
**File presence at `--out`, or at `<name>.partial.gp`, is never proof of success.** A refused
rerun without `--overwrite` leaves the earlier file in place by design (rule 3), and a run that
dies before its first write (argument error, kill, crash in start-up) cannot remove anything. A
consumer accepts a run as successful only when all of these hold:

- the process exit code is 0;
- the run record (the JSON report) carries the `run_id` the consumer supplied for this run
  (`--run-id`; when absent, the product generates one and prints it on stdout before any stage);
- the record says `status: success` and lists exactly one `primary` output;
- the SHA-256 of the file at `--out` equals the hash recorded for it.

A stale report fails the `run_id` check; a stale or replaced file fails the hash check. The CLI
help, the report schema and the user documentation must state this rule. `batch` and every other
in-product consumer must apply it (today `batch.py:91-92` sets `success` once `write_gp`
returns).

Producer rules:

0. **Path-safe run ID and containment.** The `run_id` becomes a path component (rules 2-4), so it
   is validated before any path is derived from it. It must fully match `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`
   (one component of 1-64 characters: no `/`, `\`, `:`, drive letter, UNC prefix, whitespace or
   newline), must not contain `..`, must not end in `.`, and must not be a Windows device name
   (`CON`, `PRN`, `AUX`, `NUL`, `COM0-9`, `LPT0-9`, with or without an extension). A generated
   UUID4 matches. Any other value is refused at argument validation with the stable code
   `invalid_run_id` (family `invalid_input`, user reason `input-invalid`), exit 1, and a record
   with `run_id: null` (the rejected value is not echoed), before rule 1 and with no mkdir, write
   or move under the output or work directory. Then, before any mkdir, write or move of prior
   output, every derived path is checked by resolved-path containment: with every symlink and
   junction resolved, the run root must be exactly `<resolved out-dir>/.score2gp-runs`, the
   staging directory exactly `<resolved run root>/<run_id>` and must not already exist, and each
   `previous/` target and staged artifact exactly the expected child of that staging directory.
   A failure refuses with `run_path_escape` (family `invalid_input`, exit 1, record `refused` for
   this `run_id`) and touches neither the existing outputs nor anything else. The staging path is
   re-checked after it is created. Rule 4's `<work-dir>/runs/<run_id>/` follows the same rule.
1. **Run record first.** Before any stage and before the preflight, atomically write the report
   with `status: running`, the `run_id`, `output_written: false` and an empty output list. Rewrite
   it atomically at every handled exit. A run that dies after this point leaves `running` for its
   own `run_id`, never a stale `success`.
2. **Run-unique staging and atomic publish.** Every artifact is built in
   `<out-dir>/.score2gp-runs/<run_id>/` (same file system as `--out`), validated and hashed there,
   and only then published with one atomic rename: to `--out` on `success`, to
   `<name>.partial.gp` on `partial`, nowhere on refusal. The GP carries the `run_id` in its notice or
   metadata, and `shortfall-records.json` carries it too. The final record lists each published
   artifact with its role, path and SHA-256. This keeps `temp_output.gp` → validate → move
   (`cli.py:1296-1309`), makes the temporary path unique per run, and applies the same pattern to
   `batch.py:91`.
3. **Preflight.** If `--out` or `<name>.partial.gp` exists and `--overwrite` was not given, refuse
   with a new code `output_exists` (family `invalid_input`, user reason `input-invalid`), exit 1,
   record `status: refused` and touch neither file. The old file stays, and the record for this
   `run_id` says no output was written, so a conforming consumer rejects the run. With
   `--overwrite`, move both existing files into `.score2gp-runs/<run_id>/previous/` before any
   stage. A non-success rerun then leaves nothing at `--out`, and the earlier file is kept, not
   deleted. This is defence in depth for careless readers; it is not the success signal.
4. **Per-run work directory.** Intermediate artifacts go to `<work-dir>/runs/<run_id>/`, or the
   known artifact names are removed at preflight. Stale `score.ir.json` next to a newer
   `tab_raw.json` (S3) cannot then happen.
5. **Cache.** The batch cache key already hashes options and input contents (`cache.py:14-47`);
   add the product version, so that a hit cannot serve an artifact built by different code. A
   cache hit gets its own `run_id` and record, with the artifact hash.

**Repeat-run cases the contract must pass** (acceptance negative controls; REQ-0005 A5). Each case
is checked with three consumers: the conforming rule above, a presence-only consumer (file exists
at `--out`) and a status-only consumer (report says `success`, no `run_id` or hash check).

| Case | Before the run | Run | Required state after | Conforming | Presence-only | Status-only |
|---|---|---|---|---|---|---|
| S2′a | complete `--out` from an earlier run | partial, no `--overwrite` | exit 1 `output_exists`; old file untouched; record for this `run_id` `refused`, no outputs | reject | **false success** | reject |
| S2′b | same | partial, `--overwrite` | exit 6; no file at `--out`; `<name>.partial.gp` from this run; earlier file under `previous/` | reject | reject | reject |
| S2′c | same | refused, `--overwrite` | exit 2; no file at `--out`, no partial | reject | reject | reject |
| S2′d | complete `--out` and `success` report from an earlier run | dies before its first write | both files unchanged; no exit code | reject | **false success** | **false success** |
| S3′ | stale `<name>.partial.gp` | complete, `--overwrite` | `--out` from this run, no `.partial.gp` left | accept | accept | accept |
| S4′ | report from an earlier successful run | uncaught exception after rule 1 | record for this `run_id` `running`, never `success` | reject | reject | reject |
| S5′ | work directory from an earlier run | any | no artifact in this run's work directory predates the run | — | — | — |
| S6′ | this run's successful `--out` | file replaced afterwards | hash differs from the record | reject | **false success** | **false success** |
| S7′a | complete `--out` from an earlier run | `--run-id` with traversal or an invalid form (`../../outside/leak`, `..`, `a/../b`, 65 characters, `NUL`, ...), `--overwrite` | exit 1 `invalid_run_id`; old file untouched in place; nothing created or moved anywhere except the report | reject | **false success** | reject |
| S7′b | same | absolute `--run-id` (POSIX, drive, drive-relative, UNC), `--overwrite` | same as S7′a | reject | **false success** | reject |
| S7′c | same, and the run root or the staging directory is a symlink or junction to a sibling directory | valid `--run-id`, `--overwrite` | exit 1 `run_path_escape`; old file untouched in place; nothing written through the link | reject | **false success** | reject |
| S7′d | same | valid explicit `--run-id`, complete, `--overwrite` (positive control) | exit 0; earlier file under `.score2gp-runs/<run_id>/previous/`, inside the resolved run root | accept | accept | accept |

The bold cells are the point of the controls. S2′a and S2′d show that a presence-only consumer is
given a false success under the contract, so the contract forbids that consumer rather than
claiming to protect it. S2′d and S6′ show why the status alone is not enough: the `run_id` and
the hash are required. The conforming consumer accepts only the successful runs. S7′a-c show that
an unsafe `run_id` or a linked run root cannot relocate an earlier output outside the run root
(the review probe moved it to a sibling directory before rule 0 existed).

**Model check.** `evidence/run_contract_check.py` models the producer rules on a temporary
directory (no product import) and runs the three consumers through S2′a-d, S3′, S4′, S6′, S7′a-d
and a fresh-success positive control: 13 traversal or invalid IDs and 8 absolute IDs, each with
`--overwrite` over an earlier output, a symlink or junction at the run root and at the staging
directory, and one valid explicit ID. Every S7′ refusal is checked against a snapshot of the whole
temporary tree: only the report changed. Its self-test passes (32 controls): the conforming
consumer accepts exactly the three successful runs, and the presence-only and status-only
consumers give the false successes marked above. With the grammar or the containment check
disabled, the S7′ controls fail (an ID of `../../outside/leak` then exits 0 and moves the earlier
file out of the run root). S5′ is not modelled. This is a check of the design's logic, not of the
product.

Status of the contract: **Unverified in the product**. The product has no `--run-id`,
`--overwrite`, run-ID validation, run staging or preflight today. Case S2′a is the observed failure S2 turned into a
test, and its required result is that a conforming consumer rejects the run, not that the old file
disappears.

### Option C: per-measure gating always on, no mode

Every run delivers what passes the per-bar gate in `--out`, with gap bars, and reports `partial`.

| Rule | Result |
|---|---|
| FC2, FC7 | Holds only if every caller reads the status. `--out` now exists for partial runs. Existing callers equate a written GP with success: `batch.py:91-92` sets `status = "success"` once `write_gp` returns, and `batch.py:59-75` reports a cached artifact as `success`. **Fails** FC7 for those callers. |
| Others | As Option A. |

Verdict: **rejected.** It changes the meaning of `--out` for every caller, and allows an
unlabelled false success in tools that only check file presence. Option B does not make such
tools safe either (§3.3a, S2′a and S2′d), but it never publishes a non-success output at `--out`,
so on a fresh path or with `--overwrite` a presence-only tool is not misled. Under C even a
first run on a fresh path misleads it.

### Option D: labelled regions without gap bars (omit failing bars entirely)

Deliver only passing bars, concatenated, and list the missing ones in the report.

| Rule | Result |
|---|---|
| FC4 | **Fails.** Bars are dropped and later bars shift position, so the file's bar numbers no longer match the source. That is an unlabelled wrong result for anyone who reads the GP without the report. |

Verdict: **rejected.**

## 3.4 Summary

| Option | FC1 | FC2 | FC3 | FC4 | FC5 | FC6 | FC7 | FC8 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 status quo | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ships today; not acceptable |
| A mode + gap bars | ✓ | conditional (§3.3a) | ✓ | ✓ | ✓ | conditional (D3) | conditional (§3.3a) | conditional (in-file marker) | acceptable with conditions |
| **B separate partial artifact** | ✓ | conditional (§3.3a) | ✓ | ✓ | ✓ | conditional (D3) | conditional (§3.3a) | ✓ with §3.3a | **recommended, with the run-bound output contract** |
| C always-on gating | ✓ | ✗ for file-presence callers | ✓ | ✓ | ✓ | conditional | ✗ | conditional | rejected |
| D omit failing bars | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | rejected |

FC5 holds for A, B and C because approximated rhythm can only appear in a non-success artifact
with per-bar labels. FC2 and FC7 hold for A and B only for consumers that follow the run-bound
output contract of §3.3a. A stale earlier output at `--out` survives a failed rerun (observed
S2), and under the contract it still can (S2′a, S2′d). The contract therefore makes the caller's
own run record, not file presence, the only evidence of success. With that consumer rule, none of
the accepted options lets a consumer take a wrong or stale result as this run's success. A
consumer that relies on file presence alone is outside the contract, and no option protects it.

## 3.5 Preconditions that apply to any accepted option

1. The per-bar gate must include candidate-level codes (fixes G9) and must never synthesise
   content with confidence 1.0 (fixes G8).
2. The PDF-only loop (`build_ir.py:1743-1773`) must collect per-bar outcomes instead of raising
   at the first failure (fixes G4). The replay harness shows the product's own assembler
   supports that without changing its checks.
3. `status: success` must mean complete and faithful. Inferred rhythm moves to a non-success
   status (fixes G7).
4. The run-bound output contract (§3.3a) is in place, and every in-product consumer (`batch`
   included) follows its consumer rule. A stale primary output, partial artifact, report or
   intermediate cannot pass the `run_id` and hash checks as this run's result (fixes G22). File
   presence is documented as never being proof of success.
5. An independent oracle (REQ-0005 acceptance 2) must check the delivered bars against the
   reference GP. For L3-L7, EX2 and CFMWH the private corpus holds reference `.gp` files, so this
   is feasible locally without committing content.
