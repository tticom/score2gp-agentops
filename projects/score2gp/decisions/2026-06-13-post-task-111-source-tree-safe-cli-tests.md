# Post-Task 111: Source-Tree-Safe Whole-Note CLI Tests

Date: 2026-06-13
Authorised by: Governance Task 112

## Context
Product Task 111 was initiated to address a dependency in the whole-note recognition tests on a globally installed `score2gp` executable. Tests should run robustly against the source tree directly without relying on `PATH` wrapper binaries.

## Completion Record
Product Task 111 was completed across two Product PRs:
1. **Product PR #262**: Addressed the original issue by replacing `subprocess.run(["score2gp", ...])` with `subprocess.run([sys.executable, "-m", "score2gp.cli", ...])`. However, this left a secondary source-tree subprocess import issue when running outside of an editable install context.
2. **Product PR #263**: Fixed the remaining issue by explicitly passing a `PYTHONPATH` containing the repository `src` directory to the subprocess environment. This is the final Task 111 fix.

## Codex Comment Disposition
- Product PR #261 comment: tests should not depend on a globally installed `score2gp` executable.
  - Disposition: accepted as blocker for Product Task 111.
  - Resolution: Product PR #262 replaced direct `score2gp` executable subprocess calls with `sys.executable -m score2gp.cli`.

- Product PR #262 comment: `python -m score2gp.cli` may still fail in an uninstalled `src` checkout because pytest’s `pythonpath = ["src"]` does not propagate into the child subprocess.
  - Disposition: accepted as blocker.
  - Resolution: Product PR #263 explicitly propagated the repository `src` directory through `PYTHONPATH`.

- Product PR #263 comments/review threads:
  - Disposition: none found at post-merge verification.

## Authorisation for Product Task 113
With Product Task 111 complete and CLI tests safe, **Product Task 113** is now authorised.

**Goal:**
Extract or consolidate shared whole-note candidate evidence shaping so diagnostics and whole-note recognition consume the same safe, read-only candidate evidence structure. 

**Constraints:**
- Must remain read-only and diagnostic-derived.
- Must not add ScoreIR, GP output, MusicXML, OCR, pitch inference, rhythm inference, staff-position inference, or full notation recognition.
- Preserve current diagnostic/read-only boundaries.
- Preserve privacy-safe source metadata.
