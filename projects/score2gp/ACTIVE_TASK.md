# Active Task

**Task**: Architect research — Next standard-staff recognition capability after same-onset chord grouping
**Authorised Role**: Architect
**Repository**: `tticom/score2gp`

## Status

APPROVED

## Executable Task

Yes

## 1. Baseline
- Product PR #337 merged at `eae13541de67899ff9563a09f48ed747171dea6b`.
- Governance PR #242 merged at `373b6836b2121b82ad815753bcf78bc90e942137`.
- Standard staff recognition baseline allows same-onset chord grouping for eighth/sixteenth note candidates under 1.0 tolerance.

## 2. Context
With Product PR #337 merged, the notation bridge successfully groups same-onset candidates on synthetic fixtures to prevent tick overflow. However, standard-staff recognition remains limited to single-track sequential chords and relies on simple geometric heuristics. We need Architect research to evaluate the next blocker—specifically whether to prioritize OMR candidate extraction robustness (e.g. beam/flag/stem association) or multi-staff/multi-voice timing mapping in the bridge—and establish a viable technical approach.

## 3. Scope
- **Approved**: Research-only investigation of standard-staff recognition and rhythm-semantics expansion. The Architect must assess OMR candidate extraction heuristics (stem/notehead/beam/flag association) on non-trivial layouts, and bridge/timing mapping limitations for multi-staff/multi-voice files.
- **Excluded**: Writing product code, modifying product tests, creating or committing new PDF/GP fixtures, true polyphony or voice separation implementation, and scanned/non-vector PDF support.

## 4. Required Output & Outcome
A self-contained research report under `projects/score2gp/research/2026-07-07-next-recognition-capability-strategy.md` in the product repository (or as a read-only research draft) that strictly separates:
- Facts (direct evidence in existing code, tests, or fixtures);
- Inferences (conclusions drawn from facts);
- Hypotheses (testable propositions for later steps);
- Unknowns (gaps in knowledge).

The report must select exactly one outcome:
- **Outcome A (OMR robustness path viable)**: Propose a next Developer task to harden flag/beam/stem detection or notehead association.
- **Outcome B (Multi-staff/multi-voice path viable)**: Propose a next Developer task to extend `notation_bridge.py` for multiple tracks/staves.
- **Outcome C (No viable path)**: Report the specific blocker and propose a diagnostic task.

## 5. Research Constraints
- Developer implementation is not authorised.
- No private or copyrighted PDFs may be processed.
- No generated PDFs, GP files, or logs may be committed to git.
- Product working tree must remain clean.

## 6. Required Next Review
Reviewer architecture verification.
