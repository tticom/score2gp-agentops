# FS-03C Rootless Audiveris Probe Report

## Execution Context
- **Product SHA**: `60b0fa1622292f42032aa98f0b3d99e7b5240d29`
- **Environment**: Canonical WSL (Ubuntu 24.04 LTS `x86_64`)
- **Asset Verified**: `Audiveris-5.7.0-ubuntu24.04-x86_64.deb`
- **Asset SHA-256**: `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`
- **Clean/Dirty**: Clean

## Commands Executed

1. **Standalone OMR Probe**:
```bash
.venv/bin/score2gp omr tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out work/fs03c_probe/out --audiveris work/fs03c_probe/extracted/opt/audiveris/bin/Audiveris
```

2. **Explicit Conversion Handoff**:
```bash
.venv/bin/score2gp convert --pdf tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --musicxml work/fs03c_probe/out/run_21159061e0c24e56aa3034e5ff246a46/generated_standard_staff_whole_note.mxl --out work/fs03c_probe/out/convert_out --work-dir work/fs03c_probe/out/convert_work
```

## Observations

### OMR Manifest Statuses
- **execution_status**: `success`
- **discovery_status**: `success`
- **validation_status**: `success`

The `omr` command correctly discovered and validated an `.mxl` artifact produced by the rootless Audiveris extraction.

### Handoff Result
The `convert --musicxml` handoff failed during the `tabraw-import` stage.

### First Remaining Failure
The explicit `convert` command failed with **refusal_code**: `missing_pdf_grouping`. 
Diagnostics reason: "TabRaw extraction found playable fret candidates, but system/string/bar grouping is missing; build-ir will not treat unsafe PDF text as reliable musical evidence."

## Conclusion
**Route Status**: `unavailable` (or `unproven` for guitar tablature context). 

The rootless Audiveris probe correctly produces a valid structural MusicXML artifact. However, the subsequent handoff to `convert --musicxml` fails. The Audiveris output lacks safe PDF-to-MusicXML grouping (no TAB staff or system bounds compatible with Score2GP's strict requirements), meaning the MusicXML timing and layout cannot be safely mapped by `convert`. This remains the first blocking failure. No unapproved repair task was started. All evidence artifacts remain ignored under `work/`.
