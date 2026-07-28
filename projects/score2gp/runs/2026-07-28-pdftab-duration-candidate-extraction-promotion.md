# PDF-Tab Duration Candidate Extraction Architecture Promotion

## Verified predecessor

- Product PR #391 merged at `1a013cef0f242f1a75428c1ddfa77c251a2b22f0`.
- AgentOps PR #388 merged at `af37834cfca753017a557b6926e8ffd28bff997c`.
- Synthetic duration fixture `generated_pdf_tab_duration.pdf` committed and verified.
- Permanent `go` and `got` dispatchers active on `origin/main`.

## Selection evidence

With synthetic duration fixture `generated_pdf_tab_duration.pdf` committed to product `main`, a deterministic public test fixture containing visual stem, beam, and flag drawings and an embedded duration oracle is available.

Before developer implementation alters `src/score2gp/pdf_tab_bar_assembler.py` or `src/score2gp/pdf_tab_measure_timing.py`, an architecture specification is required to define spatial association tolerances between fret text spans and drawn stems/beams, dataflow paths through `NotationStaffDiagnostics`, and fallback boundaries for unstemmed staves.

Promoting task `PDFTAB-DUR-03` architecture phase (`0020-pdf-tab-duration-candidate-extraction-architecture.md`) ensures clear dataflow boundaries and testable implementation slices before product source modifications begin.

## Authorisation

Prompt 0020 (`projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`) authorises:
- designing spatial stem/beam association rules for PDF-only tablature;
- defining dataflow interfaces from `NotationStaffDiagnostics` into `assemble_pdf_tab_bar`;
- writing the durable architecture specification in `score2gp` at `docs/design/pdf-tab-duration-candidate-extraction.md`.

Product source code in `src/score2gp/` remains read-only during this phase. No private inputs, reference GP leakage, automatic merge, or product implementation changes are authorised. The architecture task produces one product PR in `tticom/score2gp`.

## Skills

The task uses workflow skills locked at `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`.
