# Review: Contain Regressions From the Second Teamwork Correction

## Verdict

`reject implementation` and `NOT READY` for product commit `34159062`.

## Maintainer evidence

The generated score still does not show the requested newline and phrase-title
improvement. It now has unwanted accidental symbols and unwanted legato/slide
markings. There is a visible tempo change near bar 65, missing natural
semantics, unrecognised chordal vibrato/chords, and only partial legato output.
This is a regression, not a successful M3/M4 completion.

## Independent findings

| Claim | Evidence inspected | Classification | Required action |
| --- | --- | --- | --- |
| Generic key handling | `deterministic_musicxml.py` now defaults to `C Major` when no override is supplied | contradicted | Represent unknown key rather than treating C as recognised. |
| Generic phrase titles | `whole_note_recogniser.py` uses a closed title-word regex | partially verified | Replace with generic text-block role/geometry evidence. |
| Safe embellishment output | Raw drawings are still converted directly into HO/PO/slide state | contradicted | Disable normal emission until a diagnostic candidate proves source-to-target ownership. |
| Technique comparator coverage | Comparator fields were added, but they only compare serialized flags; they do not validate whether the PDF evidence justifies them | partially verified | Add source-evidence diagnostics and true/false association tests. |
| Visible system/title improvement | Maintainer screenshots show none | contradicted | Add end-to-end propagation trace before re-claiming the feature. |

## Scope

Execute the regression-containment section of the active programme immediately.
Do not revert unrelated working duration/pitch improvements, but do not merge,
ship, or call the current accidental/embellishment/layout path successful.
