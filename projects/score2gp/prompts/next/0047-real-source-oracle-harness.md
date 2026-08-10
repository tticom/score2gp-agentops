# 0047 — Real-Source Oracle Harness & Process Isolation (CRP-04)

Status: MERGED

## Objective

Enforce process-level reference isolation during PDF-to-GP generation in `scripts/private_e2e_smoke.py` and create `tests/test_real_source_oracles.py` to evaluate post-conversion output against reference `.gp` files without reference contamination during generation.

## Start

1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `agy/crp-04-real-source-oracle-harness`.
3. Read `docs/design/2026-08-09-real-source-testing-architecture.md` and `docs/design/2026-08-09-conversion-module-migration-map.md`.
4. Verify standard tests pass.

## Implementation Scope & Seam Contract

Modify `scripts/private_e2e_smoke.py` and create `tests/test_real_source_oracles.py`:
1. **Process-Level Reference Isolation**: Update `scripts/private_e2e_smoke.py` (`run_pipeline_for_input`) to ensure `gp_template` is not automatically set from `pdf_path.with_suffix(".gp")` during PDF conversion generation. Generation must run strictly without reference template inputs.
2. **Post-Conversion Oracle Evaluation**: Add `tests/test_real_source_oracles.py` to evaluate generated `.gp` files against reference `.gp` files in a post-conversion oracle step after generation completes.
3. **Falsification Suite**: Ensure post-conversion oracle assertions fail red against known-bad historical mutations (such as measure index reset or line Y coordinate drift).

## Validation Commands

1. Run `agent_verify.py`:
   ```bash
   python3 scripts/agent_verify.py
   ```
2. Run oracle tests:
   ```bash
   python3 -m pytest tests/test_real_source_oracles.py
   ```
3. Run private smoke runner:
   ```bash
   python3 scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-5.pdf
   ```

## Deliverables

- Branch `agy/crp-04-real-source-oracle-harness` pushed to `origin`.
- Only `scripts/private_e2e_smoke.py` and `tests/test_real_source_oracles.py` created/modified.
- Pull Request opened on GitHub.
