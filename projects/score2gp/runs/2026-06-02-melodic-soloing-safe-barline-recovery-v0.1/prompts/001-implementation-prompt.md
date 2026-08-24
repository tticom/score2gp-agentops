# Melodic Soloing Note Loss Remediation v0.1 — Safe Barline Recovery Pass

## Context
The melodic soloing investigation identified the first failing stage as candidate-to-TAB association loss. Lessons 3–7 are stable, but `private_input_custom_melodic_soloing` still produces only 16 matched notes.

## Plan
1. For the double-barline tolerance, use a named constant, and use `<= DOUBLE_BARLINE_CLUSTERING_TOLERANCE`.
2. For inheritance, only accumulate partner rejection reasons and details if barlines are actually inherited. Gate inheritance behind `if len(valid_barlines) < 3:`.
3. In `build_ir.py`, ignore warnings with `severity == "info"`.
4. Verify `private_input_custom_melodic_soloing` matched-note count improves above 16.
