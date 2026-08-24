Keep PR #145 draft and make the paired-staff implementation safer.

Required changes:

1. Replace the string-returning staff classifier with a safer structured classification, for example:
   - tab
   - notation
   - incomplete_tab_candidate
   - ambiguous

2. Do not default unknown spacing to TAB.
   If spacing is outside known safe ranges and there is not enough context, return ambiguous/refuse.

3. Actually use fret-digit intersection and local context in the classifier, or remove the unused helper.
   A damaged 5-line TAB candidate may remain a TAB candidate only when spacing/context/fret intersections support it.

4. Add direct unit tests for the classifier:
   - six-line TAB spacing -> tab
   - five-line notation spacing -> notation
   - damaged five-line TAB spacing with fret intersections -> incomplete_tab_candidate
   - five-line ambiguous spacing -> ambiguous
   - no fret/context support -> not promoted to TAB

5. Add guardrail tests for collinear merging:
   - fragmented same staff line merges
   - unrelated columns/systems do not merge
   - notation and TAB line groups are not merged into one group

6. Add or expose a production-callable vertical candidate filter helper and test:
   - true shared barlines accepted
   - notation-only stems rejected
   - TAB rhythm stems rejected as measure boundaries

7. Update the agentops run record to state clearly:
   - strict conversion still fails
   - ScoreIR/GP still not written
   - private Lesson 3 smoke did not yet demonstrate conversion progress
   - this PR is public fixture / guardrail infrastructure for the next layout change
