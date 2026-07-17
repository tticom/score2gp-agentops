# Maintainer Visual Observation Ledger

The maintainer's rendered source/output comparison is authoritative. A package
that writes successfully is not accepted unless it satisfies the matching
observation facts below.

## Current Observations

| ID | Scope | Observed source fact | Observed generated defect | Required evidence |
| --- | --- | --- | --- | --- |
| VO-01 | Supplied screenshot pair, fixture identity to confirm | Tempo 70; 4/4; tuplets; printed title; structural double bars | Tempo retained but 12/8 emitted; missing notes; ghost rests; wrong grouping; title and double bars absent | Identify the exact approved input and record source text/geometry, MusicXML, ScoreIR, and GPIF facts without using a reference score to generate output. |
| VO-02 | Lesson-3 | Source-supported double bars, system breaks, phrase titles, and embellishments | Several double bars/system breaks/titles absent; embellishments absent | Separate barline, layout, title, and technique evidence. |
| VO-03 | Lesson-4 | Source notation includes dotted rests, pull-offs, tempo/title changes, and layout boundaries | Ghost rests/timing shifts; missing pull-offs; prior accidental artifacts; source layout not faithfully emitted | Ordered event and source-attachment traces. |
| VO-04 | Lessons 5--7 | Canonical command previously refuses at MusicXML timing | Recovery may write a file, but output correctness is not established | Meter and event-quality evidence before deployment. |
| VO-05 | Melodic Soloing Masterclass | TAB-only layout has no standard-notation timeline | Default conversion refuses; approximate output is only useful when explicitly requested and marked | Safe normal refusal plus explicit approximate-mode contract. |

## Rules

- Do not encode a fixture name, page, bar number, expected measure count, or
  reference score content into product logic.
- Convert these observations into sanitized structured assertions, public
  synthetic tests where feasible, and no-reference source-to-output traces.
- A visual observation remains open until the reviewer records before/after
  evidence on the original approved input and one distinct corpus input.
