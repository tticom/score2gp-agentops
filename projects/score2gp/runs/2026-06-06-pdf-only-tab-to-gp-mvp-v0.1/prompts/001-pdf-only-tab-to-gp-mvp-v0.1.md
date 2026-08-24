Title: Fix agentops PR #50 mergeability, then review draft product PR #176

Context:
There are now two PRs:

1. Agentops PR #50:
   https://github.com/tticom/score2gp-agentops/pull/50
   Title: docs: add active PDF-only MVP plan
   Branch: plan/pdf-only-tab-to-gp-mvp-v0.1
   Head SHA currently reported: 4920e3532d8fe0242c79984e40a7c46564f1312b
   File changed:
   - projects/score2gp/ACTIVE_PLAN.md

2. Product PR #176:
   https://github.com/tticom/score2gp/pull/176
   Title: feat: add PDF-only tab conversion path
   Branch: feature/pdf-only-tab-to-gp-mvp-v0.1
   Head SHA: 4e4f7d540a7f0dc5cd4fda8d4384e84d014a06d8
   Status: draft
   Files changed:
   - src/score2gp/build_ir.py
   - src/score2gp/cli.py
   - tests/test_pdf_only_tab.py
   CI: green

Verified issue:
Agentops PR #50 is open but currently not mergeable. Fix this first. Do not merge or mark product PR #176 ready until PR #50 is merged.

Part A — Fix PR #50

Repository:
tticom/score2gp-agentops

Branch:
plan/pdf-only-tab-to-gp-mvp-v0.1

Required commands:

git status --short --branch
git fetch --all --prune
git switch plan/pdf-only-tab-to-gp-mvp-v0.1
git rebase origin/main

If rebase conflicts occur, resolve only in:
projects/score2gp/ACTIVE_PLAN.md

Do not alter unrelated governance files.

After rebase:

git status --short --branch
git diff --check
grep -R "work/" -n projects/score2gp/ACTIVE_PLAN.md || true
grep -R "fixtures/private" -n projects/score2gp/ACTIVE_PLAN.md || true
grep -R "pdf-p[0-9]" -n projects/score2gp/ACTIVE_PLAN.md || true

Expected:
- no local work paths
- no private fixture paths
- no raw candidate IDs
- no copied diagnostic dumps

Push the fixed branch:

git push --force-with-lease

Then verify:

gh pr view 50 --repo tticom/score2gp-agentops --json state,isDraft,mergeable,headRefOid,files,url

If mergeable, report and recommend merge.

Part B — Keep product PR #176 draft

Do not mark PR #176 ready.
Do not merge PR #176.
Do not add more implementation unless review proves it is required.

Part C — Review PR #176 against ACTIVE_PLAN.md

Repository:
tticom/score2gp

Branch:
feature/pdf-only-tab-to-gp-mvp-v0.1

Review focus:
1. Does `--pdf-only-tab` avoid mandatory MusicXML/MXL?
2. Does it build ScoreIR from TabRaw without MusicXML?
3. Does it refuse genuinely unsafe geometry?
4. Does it incorrectly refuse useful Lesson 3-style evidence because candidate-level `safe_grouping` remains false despite system/bar/string assignment?
5. Does it incorrectly allow unsafe global grouping?
6. Does it mark inferred timing clearly with `pdf_only_tab_inferred_timing`?
7. Does it keep reference GP as evaluation-only through `--ref-gp`, never as an input dependency?
8. Does it avoid OCR, Audiveris dependency, scanned PDF support, and schema creep?
9. Does JSON report distinguish:
   - pdf-only mode
   - inferred timing
   - GP written
   - validation result
   - optional reference comparison
10. Does GP output validate structurally?
11. Are private/generated artifacts excluded?

Required product review commands:

git status --short --branch
git fetch --all --prune
git switch feature/pdf-only-tab-to-gp-mvp-v0.1
git diff origin/main...HEAD --stat
git diff origin/main...HEAD -- src/score2gp/build_ir.py src/score2gp/cli.py tests/test_pdf_only_tab.py
git diff --check
git ls-files fixtures/private work

Expected private-safety output:
fixtures/private/.gitkeep

Run tests:

PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_pdf_only_tab.py
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_convert.py
PYTHONPATH=. .venv/bin/python3 -m pytest

Part D — Private Lesson 3 page-1 smoke

Run locally only. Do not commit artifacts.

Use the actual local PDF path that exists on the machine.

Suggested command:

python -m score2gp.cli convert --pdf "fixtures/private/Lesson-3.pdf" --template "fixtures/templates/minimal_gp7.gp" --out "work/private/lesson3_pdf_only_page1/output.gp" --work-dir "work/private/lesson3_pdf_only_page1" --json-report "work/private/lesson3_pdf_only_page1/report.json" --strict --pages "1-1" --pdf-only-tab

Then inspect:

Get-Content "work/private/lesson3_pdf_only_page1/report.json" -Raw | ConvertFrom-Json | Format-List
Get-ChildItem "work/private/lesson3_pdf_only_page1" -Recurse | Select-Object FullName,Length

If GP output exists:

python -m score2gp.cli validate "work/private/lesson3_pdf_only_page1/output.gp"
python -m score2gp.cli inspect-gp "work/private/lesson3_pdf_only_page1/output.gp" > "work/private/lesson3_pdf_only_page1/inspect-generated.json"

If a reference GP exists locally, run comparison only as evaluation:

python -m score2gp.cli compare "fixtures/private/Lesson-3.gp" "work/private/lesson3_pdf_only_page1/output.gp" > "work/private/lesson3_pdf_only_page1/compare.json"

Report only sanitized results:
- exit code
- status
- refusal code if refused
- output_written true/false
- GP validate pass/fail
- playable candidate count
- matched/generated note or event counts
- inferred timing warning present true/false
- no private paths or artifact contents

Acceptance criteria for moving PR #176 from draft to ready:
- PR #50 is merged.
- Product tests pass.
- Private safety invariant holds.
- Lesson 3 page-1 either:
  - writes a valid GP with inferred timing warning, or
  - refuses with a specific and correct PDF-only gating reason.
- Reviewer confirms the implementation matches ACTIVE_PLAN.md.
- No reference GP is required as input.
- No private/generated artifacts are committed.

Stop conditions:
Stop and report if:
- PR #50 cannot be made mergeable cleanly.
- PR #176 changes unrelated product areas.
- Lesson 3 page-1 fails due to an implementation error rather than a valid safety refusal.
- `--pdf-only-tab` still requires MusicXML.
- output GP is generated without a clear inferred-timing warning.
- private/generated artifacts appear in git tracking.

Reporting format:
Report:
- PR #50 mergeability status
- PR #50 fix commit if any
- Recommendation for PR #50 merge
- PR #176 review verdict: draft stays / ready after fixes / needs changes
- Product commands run
- Product test results
- Private Lesson 3 page-1 smoke result
- Private-safety result
- Required fixes before PR #176 can leave draft
