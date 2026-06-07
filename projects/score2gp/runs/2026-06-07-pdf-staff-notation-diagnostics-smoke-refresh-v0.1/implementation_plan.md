# Implementation Plan - PDF Notation Diagnostics Smoke Refresh

This plan describes how we run the private-safe smoke inspection across all real private PDFs in the `score2gp` repository to refresh diagnostics statistics.

## Goals
* Run the PDF inspection pipeline on all real private PDFs.
* Extract and compile diagnostic metrics: page counts, kind, layout classification, diagnostics status, notation staves count, and primitives/font counts.
* Verify exception-free status on all inputs, verifying that exception handling refactoring functions as expected.
* Store the aggregated, anonymized results in `RUN.md` to prevent private data leakage.

## Method
1. Write a scratch script to inspect all PDFs located in `fixtures/private/` of the `score2gp` product repository.
2. Anonymize file names to private-safe neutral labels (`input_001` through `input_012`).
3. Invoke `inspect_pdf` for each file, outputting temporary reports locally in `work/` (git-ignored).
4. Aggregate metadata from the resulting summaries (total pages, layout classes, diagnostics status, notation staff geometry counts, primitives, and fonts).
5. Document everything in `RUN.md`. For scanned-or-raster inputs, document classification metadata only (as scanned PDFs are not supported for extraction).
