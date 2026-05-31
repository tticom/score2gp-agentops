# Research Task: Guitar Technique and Articulation Conversion Blocker

## Context

The score2gp pipeline can now produce valid Guitar Pro packages for some aligned guitar TAB inputs, but a new blocker class has appeared.

A one-page melodic soloing score containing standard notation plus TAB produces a valid output file with an empty or near-empty staff. The source page visibly contains playable guitar notes and guitar-specific articulation markings.

The score includes:

* standard notation and TAB
* standard tuning
* tempo marking
* chord symbols such as D, A, Bm, and G
* lead melody sections
* hammer-ons marked `H`
* pull-offs marked `P`
* slides marked `sl.`
* slide direction implied by pitch/fret movement and possibly `/` or `\`
* full bends marked `full`
* bend/release or held-bend curved notation
* parenthesised fret numbers
* slurs connecting notes
* mixed rhythmic durations

This task is research and diagnosis only. Do not implement a broad fix yet.

## Goal

Identify why this class of guitar score produces a valid but empty staff, and design a safe domain-backed implementation plan for preserving playable notes while progressively supporting guitar techniques.

(Full detailed prompt text is recorded durably under the active task manifest in the governance repository)
