# Candidate Task: Lesson-5 Tempo Defaulting Mismatch (70 BPM vs 120 BPM)

## Status

CANDIDATE (NON-EXECUTABLE / AWAITING AUTHORIZATION)

## Objective

Investigate and locate the exact pipeline stage where expected tempo `70` BPM (recorded in `2026-07-17-first-divergence-evidence-ledger.json` `source_facts`) is replaced by default `120` BPM (`{'bpm': 120, 'text': None}`) in top-level `ScoreIR` during `Lesson-5.pdf` conversion without a timing sidecar.

## Context & Observed Facts

- **Expected Tempo (`source_facts`)**: `70` BPM.
- **Emitted Tempo (`score.ir.json`)**: `{'bpm': 120, 'text': None}`.
- **Discovered During**: CR-04A current-runtime evidence replay on product base `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.

## Scope & Boundaries

- **No Product Code Authorized**: This is a candidate task record only. No developer implementation or product code modification is authorized.
- **Investigation Boundary**: When authorized, trace tempo resolution through `pdf_vector_extractor`, `notation_omr`, and `build_ir` to identify where tempo defaults to 120 BPM when no explicit tempo text is extracted.
