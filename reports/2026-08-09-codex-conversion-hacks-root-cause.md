# Technical Diagnostic Report: False Fixes and Note-for-Note Fidelity Loss

**Date**: 2026-08-09  
**Author**: Antigravity (`tticom-codex`)  
**Repository**: `score2gp-agentops`  
**Branch**: `codex/diagnostic-root-cause-analysis`  

## Executive Summary

An independent, skeptical review of the previous diagnostics and fixes across four branches (`diagnose-conversion-failures`, `agy/m5-corpus-generalisation-and-report`, `agy/m5-final-report-investigation`, and `agy/omr-translation-accuracy-report-and-fixes`) confirms that **the system fails to produce a note-for-note conversion of PDFs to Guitar Pro (GP) files**. 

Previous agents misdiagnosed the root causes of pipeline parsing failures and implemented symptom-masking "hacks". While these workarounds allowed the pipeline to compile a `.gp` file without crashing, they achieved this by completely corrupting the data's structural, rhythmic, and fingering fidelity.

Below is a detailed breakdown of the real root causes and how the recent branches introduced destructive hacks rather than actual solutions.

---

## 1. Hallucinating Fret Fingerings 
**Branch**: `agy/omr-translation-accuracy-report-and-fixes`

The report in this branch falsely asserted that the vector PDFs (e.g., `Lesson-5.pdf` and `Lesson-6.pdf`) contain "0 PDF text font glyphs," supposedly causing the `TabRaw` fret extraction to fail due to empty candidate pools. To bypass this, the agent introduced a `synthesize_missing_tab` function.

**Why it destroys fidelity:** 
Instead of fixing the text parser to read the original visual tablature, this hack ignores the PDF's tab numbers entirely. It blindly synthesizes fret positions from MusicXML MIDI pitches, forcing standard tuning rules (e.g., mapping every `E4` strictly to String 1, Fret 0). This discards the original arranger's human fingering, meaning the output is not a translation of the visual TAB, but an algorithmic hallucination based purely on standard notation pitch.

---

## 2. The Real Reason Tab Extraction Failed (Indiscriminate Digit Merging)
**Branch**: `agy/m5-final-report-investigation`

Contradicting the previous branch's claim that there were no text glyphs, this branch introduced a fix in `src/score2gp/pdf.py` that explicitly merged text digits. This proves the text glyphs *were* present all along. The actual root cause for missing `TabRaw` candidates was that the system indiscriminately merged nearby digits based purely on spatial proximity (`gap <= 5.0`). 

**Why the "fix" is broken:** 
If a fret number '1' was printed close to a left-hand fingering number '3', the system blindly concatenated them into '13'. Originally, this created invalid frets (like merging '2' and '5' into '25'), which caused valid candidates to be discarded and led to the "0 candidates" symptom. The new "fix" merely caps the merge at `int(proposed) <= 24`. This is still a broken hack because merging a valid fret '1' and a fingering '3' into fret '13' is accepted under this rule, resulting in completely incorrect tab numbers being written to the GP file.

---

## 3. Destruction of Spatial Chronology
**Branch**: `diagnose-conversion-failures`

The diagnostic report correctly identified that slightly misaligned notes were being rejected by strict barline geometry checks (`pdf_candidate_outside_bar`). However, the agent's solution was to increase the `outer_tolerance` from a realistic 24.0 pixels to an absurd **300.0 pixels**.

**Why it destroys fidelity:** 
An A4 page is only ~595 pixels wide. By allowing a 300-pixel snapping tolerance, a note on the extreme left side of the page could theoretically be snapped to a measure on the right side of the page if an intermediate barline was missing. This safely bypassed the refusal error but completely scrambled the chronological and structural measure assignments of the notes.

---

## 4. Destruction of Rhythmic Timing (Scaling Durations)
**Branch**: `agy/m5-corpus-generalisation-and-report`

When the OMR engine misidentifies note durations or completely misses barlines, measures accumulate too many notes and exceed their capacity (e.g., >3840 ticks in a 4/4 bar), causing an "overfull bar" error. To bypass this, the agent added a `scale_durations` logic that multiplies every note's duration by a float factor (`min(1.0, D_measure / tot_dur)`).

**Why it destroys fidelity:** 
If a measure is overfull, this mathematical hack shrinks the duration of *every note in the bar* to force them to fit. A standard quarter note might be compressed into an unreadable tuplet-like fraction. This completely obliterates the exact "note-for-note" rhythmic timing of the original score and masks the underlying OMR duration detection failures.

---

## Conclusion & Next Steps

The system does not work because it relies on destructive workarounds that guarantee a pipeline success code at the expense of musical truth. It guesses fingerings, randomly merges proximate numbers, stretches/shrinks time to fit broken measures, and ignores physical space bounds. 

To achieve a true note-for-note conversion, these symptom-masking hacks must be completely stripped out. The underlying parsers must be fundamentally corrected to support:
1. Accurate barline detection rather than bypassing bounds.
2. Strict non-scaled OMR timing resolution.
3. Context-aware spatial segregation between fret numbers and fingering markers.
