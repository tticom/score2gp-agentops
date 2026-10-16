# 2026-10-16: queue a day of work for unattended running

**Decision (maintainer, 2026-10-16, quoted):** "Do the push, queue CFW-05 and queue a days worth of tasks. I'll be away most of the day ... My primary motivation is to get, as fast as possible, to a commercially viable product. We still must maintain accuracy of developed code to requirement, and tests that fail if the code is not fit for it's inteded purpose, so no tests that prove the code passes, only tests that prove the code is not fit for purpose."

**What this revision does:** sets `next_task_proposal` to CFW-05 and queues PDFG-01, OUT-01, DUR-02-FU5, SLIDE-01, OMIT-02-FU1, LETRING-01, CFW-03, HOPO-01 and MEM-02, in that order. Each has a prompt under `prompts/next/`. Items that became proposals leave the backlog (a proposal must not duplicate a backlog ID); DUR-02-FU1, DUR-02-FU3, DUR-02-FU4 and DUR-03-FU3 are folded into HOPO-01, SLIDE-01 and LETRING-01.

**Order rationale (commercial viability):** CFW-05 first because the maintainer named it and it is cheap; PDFG-01 because two of the three newest fixtures are refused wholesale; OUT-01 because the product must not ship mislabelled GP6/GP8 files; then technique and layout accuracy on the approved sources; MEM-02 last (a 50 MB report is a usability defect, not a correctness one).

**Test standard written into every prompt:** each new test names the mutant it rejects and shows it failing; happy-path-only tests are not evidence; acceptance rests on approved real sources.

**Scope:** `allowed_paths` is the expected area; the protected set (CI, private fixtures and references, agent instruction files, the control plane) still stops an author, per the 2026-10-15 protected-paths decision.
