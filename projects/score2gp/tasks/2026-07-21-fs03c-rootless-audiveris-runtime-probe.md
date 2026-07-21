# FS-03C: Rootless Audiveris Runtime Probe

## Objective

Determine whether the reviewed standalone OMR artifact contract can be
exercised in the canonical Ubuntu WSL environment without system installation
or a product-code change.

## Fixed Inputs

- Product base: fresh `origin/main`, after product merge
  `df6e5c8178794f0ea7f98d69e069a1be3593f176`.
- PDF: `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`.
- Audiveris package: `Audiveris-5.7.0-ubuntu24.04-x86_64.deb` from the official
  Audiveris 5.7.0 release.
- Package SHA-256:
  `b7d26b9a90136af8ffaaba789f842c7e1593180fc0200faa82256c5c51eae426`.

## Procedure

1. Complete every startup, identity, WSL, edit-coherency, and runtime
   provenance gate in `AGENT_CONTROL.md`.
2. Verify Ubuntu 24.04 and `x86_64`. Verify `work/` is ignored before creating
   a unique probe directory beneath it.
3. Download the exact fixed package only to that ignored directory. Verify its
   full SHA-256 before extraction.
4. Extract with `dpkg-deb -x`; do not use `sudo`, `apt`, or modify package
   content. Locate and invoke only the supplied launcher.
5. Run `score2gp omr` with that launcher. Inspect the generated manifest.
6. Only when the manifest yields one validated MusicXML artifact, invoke
   `score2gp convert --musicxml` with that exact path and inspect its JSON
   report.
7. Write one sanitized governance report and open one governance PR. Do not
   change product-tracked files, create a product PR, self-review, or merge.

## Decision Rules

- `supported`: the launcher executes, OMR manifest reports a validated artifact,
  and the explicit conversion reaches a recorded result.
- `unavailable`: platform/hash/extraction/launcher failure prevents an OMR
  artifact; report exact stderr/refusal and stop.
- `unproven`: a manifest or handoff is ambiguous, invalid, or incomplete; report
  the first boundary that failed and stop.

Neither `supported` nor a written GP file proves musical correctness. The report
must name the first remaining timing, parsing, or conversion failure.
