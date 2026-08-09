# Rule: Prohibition of Destructive Conversion Hacks

1. **Do NOT Expand Geometry Tolerances**: Expanding spatial snapping tolerances (e.g. `outer_tolerance = 300.0`) to suppress `partial_pdf_grouping` warnings is strictly prohibited.
2. **Do NOT Scale Durations**: Applying float duration scaling factors (`scale_durations = D_measure / tot_dur`) to force overfull measures to fit is strictly prohibited.
3. **Do NOT Merge Digits Without Semantic Guards**: Merging text digits based purely on spatial distance (`gap <= 5.0`) without semantic category checks (distinguishing frets from fingering numbers) is strictly prohibited.
4. **Do NOT Synthesize Open-String TAB Defaults**: Replacing missing visual TAB readings with naive open-string pitch synthesis defaults (`synthesize_missing_tab=True`, mapping `E4` -> String 1 Fret 0) is strictly prohibited.
