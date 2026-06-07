# Run Prompt: pdf-staff-notation-diagnostics-smoke-refresh-v0.1

Goal: Execute the governance run `run/pdf-staff-notation-diagnostics-smoke-refresh-v0.1` by performing a private-safe smoke inspection on all real born-digital PDFs in the `score2gp` product repository.

Success Criteria:
* Run the `inspect_pdf` pipeline on the private PDFs.
* Collect and aggregate diagnostic metadata (page counts, status counts, diagnostic warnings/status categories, notation staff counts, and primitive/font count summaries).
* Document these metrics in a new run record in `score2gp-agentops`.

Scope & Privacy Boundaries:
* Do **not** commit private PDFs, generated GP/GPIF/MusicXML, raw diagnostics JSONs, screenshots, overlays, raw coordinate dumps, local absolute paths, or private fixture names.
* Maintain strict privacy: only aggregate counts and warning codes are safe to commit.
* Stop at the Pull Request stage; never commit directly to or merge into `main` in either repository.
