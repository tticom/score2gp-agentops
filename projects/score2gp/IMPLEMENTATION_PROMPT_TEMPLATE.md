# ScoreToGP Implementation Prompt Template

Reviewer/architect agents must use this template to construct the next implementation prompt for a product developer agent.

---

## 1. Context & Branch

- **Current State**: [Describe the verified baseline and active blocker]
- **Current Branch**: `bugfix/` or `feature/` branch name
- **Base Branch**: `main`

---

## 2. Goal & Non-Goals

- **Active Goal**: [Define the exact single-rung benchmark target]
- **Non-Goals**:
  - Do not implement complex expressiveness techniques or general file format conversions.
  - Do not skip measures, bars, or candidates to make metric rates look better.
  - Do not tune parameters blindly to a private asset without writing a public reproduction test.

---

## 3. Strict Development Invariants

- **No Pitch-Based Shortcuts**: Do not use MusicXML pitches, tuning values, sounding octaves, or transposing offset data to guide system-to-measure alignment or bypass PDF geometry gates.
- **No Unsafe Suppression**: Do not globally suppress grouping, barline, string, or fret warnings. Suppressions must be tightly constrained to unboxed suitability blockers on skipped/recovered systems.
- **No Private Commits**: Do not commit private PDFs, GP packages, MXL files, or derived summaries. Keep all private files strictly in ignored directories.

---

## 4. Development Phases

- **Phase 1: Research & Isolated Defect Isolation**: Locate the mechanical failure and reproduce it using a public synthetic test.
- **Phase 2: Local Code Adjustment**: Adjust local coordinate heuristics, tolerance weights, or logic in a safe, geometry-driven manner.
- **Phase 3: Coherent Verification**: Regenerate a fresh, reconciled artifact suite in a unique work subdirectory.
- **Phase 4: Handoff & Branch Synchronization**: Complete TASKS.md and HANDOFF.md, commit, and push.

---

## 5. Verification Commands

Implementation agents must run and report the full verification matrix before declaring work complete:
```powershell
python -m pytest
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check
git diff -- schemas
git ls-files fixtures/private work
git status --short
git status --branch
```

---

## 6. Private-Safety Audit

- Run `git ls-files fixtures/private work` and confirm the output contains exactly one file:
  `fixtures/private/.gitkeep`
- Verify that no untracked `.pdf`, `.gp`, or `.mxl` files are added to the index.

---

## 7. Handoff & PR Requirements

- **HANDOFF.md**: Must be updated to reflect the actual final pushed state (latest local/pushed commit hash and subject, clean working tree status, and checks run) with absolutely zero placeholders.
- **Draft PR**: Open a Draft PR on the product repository. The PR title must clearly declare either a `Fix`, `Research-Isolation`, or `Infrastructure` status.
