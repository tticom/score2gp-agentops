Proceed with the Layout Class and Missing Sidecar Safety Gates v0.1 implementation using the revised plan.

Required additional guardrails:
- Use constants or enum-like values for layout classes and refusal warning codes.
- In build_ir.py, gate only known refusal-class layout warnings, not every future pdf_layout_warning.
- Before changing build_ir_with_diagnostics_from_files to allow musicxml_path=None, inspect all callers and update tests so missing sidecar behaviour is explicit.
- Preserve private_input_1 default-flow success, Lessons 3–7 stability, and Melodic Soloing at 82 matched notes.
- Do not commit private/generated artifacts.

1. Keep layout class values stable and machine-readable.
   Prefer enum-like strings or constants over free text spread across modules.

2. Do not make every pdf_layout_warning fatal by default unless it is explicitly a refusal-class warning.
   Some future layout warnings may be diagnostic only. Gate only the known refusal codes.

3. Be careful with `build_ir_with_diagnostics_from_files(musicxml_path=None)`.
   Check all callers first. If existing callers assume a required path, update tests so missing sidecar behaviour is intentional rather than silently changing API behaviour.
