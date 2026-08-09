# 0046 - M6: Prevent Fret Digit Over-Merging

Status: SKELETON — blocked pending real-source token-classification research. A maximum-fret guard cannot distinguish fret 13 from adjacent fingering digits 1 and 3.

## Objective
Implement a validation check on the horizontal text merging loop in the PDF OMR parser to prevent chronologically adjacent single-digit frets (e.g. `7` and `10`) from merging into impossible guitar frets (> 24).

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `feature/agy/m6-digit-merging-guard`.
3. Read `projects/score2gp/reports/2026-08-09-master-conversion-failure-diagnosis.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract
Modify only `src/score2gp/pdf.py`:
1. **Fret Limit Validation**: In the horizontal text-merging loop, check if the proposed merged string is a digit.
2. **Merge Break**: If it is a digit, ensure `int(proposed) <= 24` before committing the merge operation. If the proposed value exceeds 24, break the merge loop and treat them as separate fret digit candidates.
3. **Real-Source Contract Testing**: Use real examples of multi-digit frets, adjacent notes, fingering, string labels, tempo text, and valid merged values below 24 that must remain separate.

## Validation Commands
1. Run the test suite:
   ```bash
   PYTHONPATH=. .venv/bin/python3 -m pytest
   ```
2. Verify that consecutive fret candidates like `7` and `10` on Lesson-5.pdf Page 1 System 5 are extracted as separate fret number digits.

## Deliverables
- Branch `feature/agy/m6-digit-merging-guard` pushed to `origin`.
- Only `src/score2gp/pdf.py` changed.
- Pull Request opened on GitHub.

## Stop Conditions
- Merge validation causes crashes on non-digit characters.
