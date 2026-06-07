# Task List - PDF Notation Diagnostics Smoke Refresh

- `[x]` Run `inspect_pdf` pipeline on all real born-digital and scanned private PDFs in the `score2gp` repository.
- `[x]` Collect and aggregate diagnostic metadata (page counts, kind, layout class, diagnostics status, notation staff counts, primitives count, and font counts).
- `[x]` Verify that all 12 private files run successfully without throwing unhandled exceptions.
- `[x]` Compile and document the aggregated metrics in the `RUN.md` record in `score2gp-agentops`.
- `[x]` Verify strict privacy boundaries (no private filenames, local absolute paths, raw exception tracebacks, or raw coordinate dumps in the commit history).
- `[x]` Push the agentops branch and open PR #62.
