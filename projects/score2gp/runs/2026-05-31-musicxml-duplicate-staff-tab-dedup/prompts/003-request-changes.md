REQUEST CHANGES

Required before merge:
1. Suppress duplicate TAB rests/events, not only duplicate pitched TAB notes.
2. Add a public regression test for a confirmed duplicate pair with a TAB-staff rest that previously poisoned target-staff selection.
3. Use dedup_tab_note_source_path in TAB provenance.
4. Add/adjust a provenance test to assert the TAB provenance source path is the TAB note source path.
5. Clean the PR body and remove the “all dual-staff guitar scores” overclaim.
6. Re-run full tests and private smoke.
