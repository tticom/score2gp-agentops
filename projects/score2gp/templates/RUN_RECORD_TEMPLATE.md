# ScoreToGP Run Record

## Repo and Branch
- **Repository**: score2gp
- **Branch**: [e.g. feature/my-feature]

## Command(s) Run
```bash
[e.g. python -m pytest]
```

## Input Availability
- **Inputs**: [e.g. tiny_score.xml (private-safe basenames only)]

## Output Directory Path
- **Output**: `work/` or ignored subdirectory path

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` / `fail`
- **Remediation / Diagnostic Status**: `pass` / `fail` / `skipped`
- **Generated File Existence**: `ScoreIR written (yes/no)` / `GP written (yes/no)`
- **Semantic Round-Trip Status**: `pass` / `fail` / `unverified`

## Blocker and Diagnostics
- **Exact Blocker Category**: [e.g. pdf_barline_too_short_absolute or None]
- **Diagnostic warnings encountered**:
  - [List of warning codes]

## Private-Safe Metrics
- Page Count: 
- Total Candidates: 
- Playable Fret Candidates: 
- Candidates with System: 
- Candidates with Bar: 
- Candidates with String: 
- Unassigned-to-System Count: 
- Unassigned-to-Bar Count: 
- Unassigned-to-String Count: 

## Verification Matrix
- `python -m pytest` status:
- Schema validation status:
- git diff --check status:

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`: `yes` / `no`
- No private score details, pitch steps, lyrics, chord symbols, or raw PDF/MusicXML text are committed: `yes` / `no`

## Next Required Evidence
- [Define next required evidence or implementation step]
