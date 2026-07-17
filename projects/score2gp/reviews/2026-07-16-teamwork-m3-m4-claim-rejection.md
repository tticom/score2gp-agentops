# Review: Reject Teamwork M3/M4 Completion Claim

## Verdict

`needs implementation changes` and `NOT READY`.

The maintainer reports no visible improvement in the generated Guitar Pro
output. The product change `7edfe968` cannot be accepted as a fix for layout,
phrase titles, dotted rests, or embellishments.

## Evidence ledger

| Claim | Evidence inspected | Classification | Consequence |
| --- | --- | --- | --- |
| Generic key-signature recognition | `deterministic_musicxml.py` branches on `Lesson-3` and `Lesson-4` filenames | contradicted | Remove the fixture-specific logic before claiming recognition. |
| Generic phrase-title detection | `whole_note_recogniser.py` considers only text containing `Example` | contradicted | Replace with geometry/text-role evidence and tests. |
| Pull-off and slide recognition | New matcher has no staff or vertical-coordinate constraint and suppresses every exception | not verified | Do not claim any embellishment output is correct. |
| Comparator verifies embellishments | `StandardizedNote` and `StandardizedBeat` record pitch/tie/rhythm but no technique state | contradicted | Add technique-aware comparator representation and synthetic mismatch tests. |
| System/page layout visibly improved | Output user inspection says no; source changes were not accompanied by an end-to-end renderer/output assertion | not verified | Preserve the work but return it for output-evidence repair. |
| Dotted-rest repair | Greedy dot-to-rest matching has no regression test for its association boundary | not verified | Add public true/false association tests before acceptance. |

## Required correction boundary

Follow the mandatory correction gate in
`projects/score2gp/programmes/2026-07-16-teamwork-corpus-conversion-accuracy.md`.
This is a narrow evidence-and-implementation repair, not permission for another
large mixed commit. Do not use literal filenames, bar indices, phrase text, or
reference-GP contents to make a score pass.

## Continuation decision

Continue immediately with the correction gate. A real stop condition has not
been reached.
