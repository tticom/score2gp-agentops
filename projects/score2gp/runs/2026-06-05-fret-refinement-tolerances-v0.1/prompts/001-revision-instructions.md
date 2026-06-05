Send this revision to the developer:

Approved with required implementation guardrails:

1. Before implementing `_is_plausible_narrow_fret_digit`, verify where `_candidate_confidence` is called in the pipeline.
   - If system/bar/string assignments are already available there, use them.
   - If they are not available, do not change pipeline ordering just to make the helper work.
   - Instead, base the helper on evidence available at that stage: digit text, width, height, aspect ratio, TAB-zone proximity if known, and exclusion from prose/header text.

2. Tighten `_should_warn_unmerged_fret_digits` for repeated digit pairs.
   - Distinct sequential notes like `8` then `8` must not warn.
   - But genuine multi-digit frets like `11` and `22` must still be able to warn or merge correctly.
   - Do not solve this by blanket-skipping equal digits.
   - Use geometry: tight x-gap, same string/baseline, similar y position, plausible combined fret number, and absence of separate-note spacing evidence.

3. Keep `2.8pt` as the lower safety bound unless diagnostics prove otherwise.
   - Widths `< 2.8pt` should still be penalised.
   - Widths between `2.8pt` and `4.0pt` should only avoid the penalty when the candidate is otherwise plausible.

4. Add one extra public test:
   - repeated digits that are genuinely multi-digit, e.g. `1` + `1` as fret `11`, still merge or warn appropriately.
   - repeated sequential same-string notes, e.g. `8` then `8` with wider note spacing, do not warn.

5. Acceptance must include:
   - private_input_1 succeeds without `allow_skip_unboxed=True`;
   - Lessons 3–7 remain stable;
   - Melodic Soloing remains at 82;
   - multi-digit fret handling does not regress.
