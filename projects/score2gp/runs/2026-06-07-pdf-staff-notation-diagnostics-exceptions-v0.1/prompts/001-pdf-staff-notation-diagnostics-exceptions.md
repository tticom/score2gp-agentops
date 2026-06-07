# Operative Prompt: PDF notation diagnostics exceptions v0.1

refactor/pdf-staff-notation-diagnostics-exceptions-v0.1

On that branch, copy/selectively re-use the good tests from #183, then replace the two silent-exception tests with tests asserting the new desired behaviour: a private-safe diagnostic warning/status such as pdf_notation_geometry_diagnostics_failed, with no raw exception text, no local path, no raw score content.
