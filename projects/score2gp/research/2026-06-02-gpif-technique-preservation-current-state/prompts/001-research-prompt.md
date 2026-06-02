# Antigravity Task: Research GPIF Technique Preservation Current State v0.1

## Role

You are the **Researcher**. Your job is to inspect the current `score2gp` pipeline and answer one focused question with evidence:

> Where does hammer-on, pull-off, slide, bend, vibrato, or other guitar-technique evidence currently exist in the pipeline: raw PDF candidates, text candidates, ScoreIR, GPIF serialization, or nowhere durable yet?

This is a research task, not an implementation task.

Do not write feature code. Do not attempt technique serialization. Do not update broad project docs unless explicitly instructed. Produce a concise, evidence-backed research report that enables the next developer to implement the smallest safe technique-preservation branch.

---

## Current verified state

Both recent PRs are merged:

* Product PR `tticom/score2gp#157`: melodic soloing barline/layout refinement merged to `main`.
* Governance PR `tticom/score2gp-agentops#20`: run record for melodic soloing refinement merged.

Local `score2gp/main` has been fast-forwarded to the merged product state.

Latest local validation after merge:

```text
442 passed in 10.15s
```

Private quality audit result after merge:

```text
Total Audited Scores: 9

private_input_1                          | fail | gp_output_empty_or_near_empty     | 0   | 0
private_input_2                          | fail | gp_output_empty_or_near_empty     | 0   | 0
private_input_custom                     | fail | gp_output_empty_or_near_empty     | 0   | 0
private_input_custom_lesson_3            | pass | gp_output_technique_loss_expected | 451 | 451
private_input_custom_lesson_4            | pass | gp_output_technique_loss_expected | 546 | 546
private_input_custom_lesson_5            | pass | gp_output_technique_loss_expected | 295 | 295
private_input_custom_lesson_6            | pass | gp_output_technique_loss_expected | 115 | 115
private_input_custom_lesson_7            | pass | gp_output_technique_loss_expected | 624 | 624
private_input_custom_melodic_soloing     | pass | gp_output_fret_matching_suspect   | 16  | 16
```

Private-safety invariant after merge:

```text
git ls-files fixtures/private work
fixtures/private/.gitkeep
```

Interpretation:

* Lessons 3–7 are stable at `gp_output_technique_loss_expected`.
* Melodic soloing now produces non-empty GP output, but remains `gp_output_fret_matching_suspect`.
* The next project risk is not empty output. The next uncertainty is whether guitar-technique evidence is present anywhere durable enough to serialize into GPIF.

---

## Branches

In `score2gp`, create a research branch only if you need to commit a small local research helper or report:

```bash
git switch main
git pull --ff-only origin main
git switch -c research/gpif-technique-preservation-current-state-v0.1
```

In `score2gp-agentops`, create a governance branch for the research record:

```bash
git switch main
git pull --ff-only origin main
git switch -c agent/gpif-technique-preservation-current-state-v0.1
```

If no product-code changes are needed, do not open a product PR. The expected durable output is an agentops research record.

---

## Research question

Answer this precisely:

```text
For each guitar technique category — hammer-on, pull-off, slide, bend, vibrato, trill, tap, harmonic, palm mute, dead note, grace note, tie/slur, and any other technique-like marking already detected — where does evidence currently exist?

Possible locations:
1. raw PDF drawing/vector candidates
2. raw PDF text candidates
3. parsed TAB/fret candidates
4. warning or diagnostic records
5. ScoreIR model/schema
6. MusicXML conversion path
7. GPIF writer / serializer
8. private audit summary
9. nowhere durable yet
```

The goal is to identify the **smallest safe next implementation target**, not to solve all technique preservation.

---

## Non-goals

Do not implement GPIF technique serialization.

Do not modify `src/score2gp/gpif.py`, `src/score2gp/pdf.py`, ScoreIR models, schemas, or public fixtures unless you find that a tiny diagnostic helper is absolutely necessary. If you do add a helper, explain why inspection alone was insufficient.

Do not commit private PDFs, GP files, MusicXML files, ScoreIR outputs, diagnostic overlays, logs, audit JSON, or anything under `work/`.

Do not make claims from memory. Every conclusion must cite file paths, symbols, commands, and observed output.

Do not use private content in the report. Private-safe basenames, counts, categories, warning codes, and artifact paths are allowed.

---

## Required pre-flight checks

Run from `score2gp`:

```bash
git status
git branch --show-current
git log --oneline --decorate --max-count=10
python3 -m pytest
python3 scripts/private_gp_quality_audit.py
git ls-files fixtures/private work
```

Expected private-safety output:

```text
fixtures/private/.gitkeep
```

If the project venv is active and `python` works, using `python` is acceptable. Otherwise use `python3`.

Stop if public tests fail on clean `main`, or if the private-safety invariant is violated.

---

## Inspection commands

Start with broad symbol search:

```bash
rg -n "hammer|pull|slide|bend|vibrato|trill|tap|harmonic|mute|palm|dead|ghost|grace|slur|tie|technique|articulation|ornament|gliss|legato|let ring|let-ring|staccato|accent" src tests scripts
```

Inspect the core pipeline:

```bash
rg -n "class .*Note|dataclass|ScoreIR|Technique|technique|articulation|fret|string|pitch|duration|onset|voice|measure|bar" src/score2gp
rg -n "GPIF|gpif|Technique|Properties|Slides|Bend|Vibrato|Hammer|Pull|Grace|Tie|Slur" src/score2gp
rg -n "warnings|candidate|text_candidates|fret_candidates|non_playable|playable" src/score2gp scripts tests
```

Inspect likely files, if present:

```bash
ls src/score2gp
sed -n '1,260p' src/score2gp/gpif.py
sed -n '1,260p' src/score2gp/ir.py || true
sed -n '1,260p' src/score2gp/score_ir.py || true
sed -n '1,260p' src/score2gp/pdf.py
```

Inspect schemas and public fixtures:

```bash
find schemas fixtures tests -maxdepth 4 -type f | sort | rg "schema|score|ir|gpif|pdf|technique|fixture|json|xml|gp"
rg -n "technique|articulation|hammer|pull|slide|bend|vibrato|fret|string" schemas fixtures tests
```

Inspect private-safe generated audit summaries only by path and aggregate fields. Do not paste private content:

```bash
ls -R work/private_gp_quality_audit_v0_1 | sed -n '1,160p'
python3 - <<'PY'
import json
from pathlib import Path

summary = Path("work/private_gp_quality_audit_v0_1/summary.json")
if summary.exists():
    data = json.loads(summary.read_text())
    print(type(data).__name__)
    if isinstance(data, dict):
        print(sorted(data.keys()))
    elif isinstance(data, list):
        print("items", len(data))
        for item in data[:3]:
            if isinstance(item, dict):
                print(sorted(item.keys()))
else:
    print("summary.json not found")
PY
```

Then inspect the private-safe summary structure enough to answer whether technique counts, warning codes, non-playable candidates, or artifact paths are recorded. Do not print private musical content.

---

## Required evidence table

Produce a table with one row per technique category:

```text
Technique | Evidence found? | Earliest pipeline location | Durable model field? | Serialized to GPIF? | Evidence path/symbol | Notes
```

Technique categories to include at minimum:

* hammer-on
* pull-off
* slide
* bend
* vibrato
* trill
* tap
* harmonic
* palm mute
* dead note / ghost note
* grace note
* tie
* slur / legato
* staccato / accent
* let ring
* other technique-like markings found during search

Use these classifications:

```text
raw_only
diagnostic_only
score_ir_durable
gpif_serialized
lost_before_ir
not_detected
unclear_needs_fixture
```

---

## Required pipeline map

Create a concise pipeline map:

```text
PDF drawings/text
  -> PDF candidates
  -> TAB/fret candidates
  -> ScoreIR
  -> GPIF writer
  -> quality audit
```

For each stage, state whether technique evidence exists, is lost, or is not represented.

---

## Required implementation recommendation

Recommend exactly one next implementation branch.

The preferred branch name is:

```text
feature/gpif-hammer-pull-slide-minimal-v0.1
```

But only recommend that if evidence shows hammer/pull/slide information already exists in a durable or recoverable form.

If hammer/pull/slide evidence does not exist durably, recommend a smaller precursor branch, for example:

```text
feature/scoreir-technique-field-minimal-v0.1
```

or:

```text
feature/pdf-technique-candidate-diagnostics-v0.1
```

The recommendation must include:

```text
Branch name:
Why this is the next smallest useful step:
Likely files:
Non-goals:
Acceptance criteria:
Validation commands:
Stop conditions:
```

---

## Required private-safety checks

Before committing any research record, run:

```bash
git status --ignored
git ls-files fixtures/private work
find . -path "./.git" -prune -o -type f -size +10M -print
```

The command:

```bash
git ls-files fixtures/private work
```

must output exactly:

```text
fixtures/private/.gitkeep
```

If any private files, generated GP files, audit JSON, overlays, logs, PDFs, or `work/` contents are tracked or staged, stop and report.

---

## Durable research record

Create this file in `score2gp-agentops`:

```text
projects/score2gp/research/2026-06-02-gpif-technique-preservation-current-state.md
```

The report must include:

1. Purpose.
2. Current verified state.
3. Commands run.
4. Public test result.
5. Private audit result summary, private-safe only.
6. Search terms used.
7. Files inspected.
8. Technique evidence table.
9. Pipeline map.
10. Findings.
11. Recommended next branch.
12. Stop conditions encountered, if any.
13. Private-safety audit result.

Also add a prompt manifest entry if this repository expects prompt manifests for research runs. If there is an established `projects/score2gp/research/README.md` or `projects/score2gp/runs/README.md`, follow it.

---

## Acceptance criteria

This research task is complete when:

* The report clearly identifies where technique evidence currently exists or confirms it does not exist durably.
* The report distinguishes raw PDF/text evidence from ScoreIR durable fields and GPIF serialization.
* The report identifies whether hammer-on, pull-off, and slide are viable for the next minimal implementation branch.
* The report recommends exactly one next branch with acceptance criteria.
* Public tests still pass.
* Private audit still confirms no regression in Lessons 3–7 and melodic soloing remains non-empty.
* Private-safety invariant is intact.
* No implementation changes are made unless explicitly justified as a tiny diagnostic helper.

---

## Stop conditions

Stop and report instead of continuing if:

* `main` is not up to date.
* Public tests fail before research changes.
* Private audit cannot run.
* Private-safety invariant is violated.
* You find that technique evidence is only present in private musical content and cannot be summarized safely.
* You would need to commit private artifacts or generated `work/` files.
* You cannot determine whether technique evidence exists after reasonable search and inspection.

---

## Reporting format

Final response must include:

```text
Verdict:
Current technique evidence state:
Earliest durable location:
Does ScoreIR preserve techniques? yes/no/partial
Does GPIF serialize techniques? yes/no/partial
Recommended next branch:
Why:
Files inspected:
Commands run:
Test results:
Private audit summary:
Private-safety result:
Limitations:
```
