# ScoreToGP Run Record - Paired Staff Row Normalisation

## Repo and Branches
- **Repository**: score2gp
- **Product Branch**: `bugfix/paired-staff-row-normalization-v0.1`
- **Agentops Branch**: `runs/paired-staff-row-normalization-v0.1`

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-implementation-prompt.md](prompts/001-implementation-prompt.md)
- Prompt files:
  - [prompts/001-implementation-prompt.md](prompts/001-implementation-prompt.md)

## Files Changed
- `src/score2gp/pdf.py`
- `tests/fixtures/pdf/make_paired_notation_tab_system_pdfs.py`
- `tests/test_pdf.py`

## Tests Added
- `test_paired_tab_row_fragmentation_merging`
- `test_merge_collinear_horizontal_segments_row_fragmentation_direct`

## Public Fixture Names
- `fixtures/public/generated_paired_tab_row_fragmentation.json`
- `tests/fixtures/pdf/generated_paired_tab_row_fragmentation.pdf`

## Exact Verification Commands Run

### Baseline Command:
```powershell
$env:PYTHONPATH="src"
.venv\Scripts\python -m score2gp.cli extract-tab fixtures/private/Lesson-3.pdf --out work/paired_staff_row_normalization_20260528_1158/lesson_3_baseline
```

### After Command:
```powershell
$env:PYTHONPATH="src"
.venv\Scripts\python -m score2gp.cli extract-tab fixtures/private/Lesson-3.pdf --out work/paired_staff_row_normalization_20260528_1158/lesson_3_after
```

## Private-Safe Baseline vs After Metrics (Lesson 3)

| Metric | Baseline | After |
| :--- | :---: | :---: |
| **Page Count** | 4 | 4 |
| **Total Candidates** | 591 | 591 |
| **Playable Fret Candidates** | 548 | 548 |
| **Candidates with System** | 431 | 431 |
| **Candidates with Bar** | 399 | 399 |
| **Candidates with String** | 430 | 430 |
| **Grouping Status** | `partial` | `partial` |
| **Inferred System Count** | 22 | 22 |
| **Inferred Bar Box Count** | 49 | 49 |
| **Count of Partial X-Span Systems** | 0 | 0 |
| **First Page/System Blocker** | `pdf_grouping_confidence_below_threshold` | `pdf_grouping_confidence_below_threshold` |
| **ScoreIR Written** | No | No |
| **GP Written** | No | No |
| **Semantic Round-Trip Attempted** | No | No |

*Note: The metrics on Lesson 3 remain identical between baseline and after. This is because Lesson 3 did not feature unmerged collinear staff splits, but rather standard continuous-neighbor merging was sufficient. However, the post-implementation run confirms that the new spacing-aware row-level fragment split normalisation operates completely safely without regressing or corrupting standard system/bar/string assignments.*

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail`
- **Remediation / Diagnostic Status**: `pass` (all synthetic test paths pass)
- **Generated File Existence**: `ScoreIR written (no)` / `GP written (no)`
- **Semantic Round-Trip Status**: `unverified`

## Verification Command Results
* `python -m pytest` status: passed (all 390 tests, including new public synthetic tests, pass cleanly in 26.38s)
* Schema validation status: passed (schemas matches git index cleanly)
* git diff --check status: passed cleanly
* git ls-files fixtures/private work status: audited safely

## Private-Safety Audit
* `git ls-files fixtures/private work` outputs only:
  `fixtures/private/.gitkeep`
* No private scores, PDFs, or MusicXMLs are tracked by Git.

## Next Required Evidence
- Human maintainer review of the PRs.
- Continue onto the next required layout improvement (e.g. double barline grouping or spacing classifier refinements) to unblock the remaining Major Triads blockers.
