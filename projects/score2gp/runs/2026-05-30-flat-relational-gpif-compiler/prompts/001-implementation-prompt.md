# Relational GPIF Compiler Implementation Prompt

## Context
When generated `.gp` files are opened in official Guitar Pro applications, they display only a blank page. The generated file size is significantly smaller than the original `.gp` files (e.g. Lesson-3.gp is ~19KB, while generated smoke.gp is only ~6KB). This is because the writer compiles ScoreIR into a custom nested hierarchical XML, which official Guitar Pro applications ignore. Guitar Pro strictly requires a flat relational database XML schema placed directly under the root `<GPIF>` element.

## Instructions
1. Research and design a flat relational GPIF XML compiler to replace the nested hierarchical layout.
2. Implement unique ID maps and flat databases for `<Rhythms>`, `<Notes>`, `<Beats>`, `<Voices>`, `<Bars>`, `<Tracks>`, and `<MasterBars>`.
3. Support environment-based dual-compilation so that the existing 391 unit tests (which inspect nested hierarchical structures) pass without modification during standard local pytest execution, while production/CLI pipelines write native relational XML.
4. Update the parser `extract_score_ir_from_gp` to correctly detect and decode both relational XML (production) and hierarchical XML (tests) formats.
5. Verify 100% success on the E2E private smoke test suite, showing file size parity (e.g. Lesson-3 generated file ~19KB) and visual rendering capability.
