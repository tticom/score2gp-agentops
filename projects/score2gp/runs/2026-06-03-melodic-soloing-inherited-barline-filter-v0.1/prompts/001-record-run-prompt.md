I approve the direction, but tighten the implementation before coding.

This is the right next blocker. The plan does the important thing: it visually classifies the suspicious verticals as tuplet/bracket hooks, not real barlines, and it grounds the proposed 130.0 threshold in the Lesson 3–7 width audit rather than guessing. That is much stronger than “just increase 30 to 120.”

The proposed constant is defensible:

MIN_INHERITED_INTERNAL_BAR_WIDTH = 130.0

The audit says Lessons 3–7 have no inherited barlines creating measures below 130.0, and all sub-130 legitimate narrow measures are explicit TAB barlines, not inherited ones. That is exactly the distinction we need.

But I would revise the algorithm before implementation.

The risk is sequential filtering can become order-dependent. If you process partner_valid one candidate at a time, the first false bracket hook may be accepted, and the second may be rejected because it is too close to the first. That still leaves one false inherited barline in the system. The fix needs to reject candidates that participate in sub-threshold inherited intervals, not merely reject whichever candidate happens to be processed second.

Tell the developer to implement it as a batch/anchored filter:

Build candidate set:
- explicit TAB valid_barlines are anchors
- partner inherited barlines are optional candidates

Reject inherited candidates if:
- adding them would create any adjacent interval < MIN_INHERITED_INTERNAL_BAR_WIDTH
- or they participate in a close inherited/inherited pair below the threshold

Never reject explicit TAB barlines via this filter.

Also require a regression test using the actual suspicious spacing pattern, but with synthetic coordinates only. For example, create a synthetic inherited candidate set where two inherited barlines are around 82.65 points apart and assert both false inherited candidates are rejected, not just one.

I would add these required changes to the plan:

Required revisions before implementation:

1. Add `pdf_barline_inherited_too_close` to the default rejection reason map in `filter_tab_barline_candidates` / inheritance diagnostics, otherwise the new rejection reason may be inconsistently counted.

2. Do not mutate `other_filtered["details"]` in place. Copy each detail row before changing `final_decision`, `rejection_reason`, or `inherited`.

3. Avoid order-dependent sequential filtering. The inherited-barline filter must reject all inherited candidates that create or participate in sub-130 false measure intervals.

4. Apply `MIN_INHERITED_INTERNAL_BAR_WIDTH` only to inherited internal barlines. Explicit TAB barlines must not be rejected by this filter.

5. Add a synthetic test proving the bracket-hook pattern is fully rejected:
   - two inherited candidates close together, e.g. ~82.65 points apart
   - both are rejected as inherited-too-close
   - no narrow false measure is produced

6. Keep the acceptance criterion honest:
   - “near full coverage / 82 notes” is a target, not a hard merge requirement.
   - If the false barline fix is correct but melodic soloing remains below 82, report the next remaining loss stage rather than broadening the patch.

So: approved with those revisions. The plan is evidence-based, but the implementation must avoid the “reject the second false hook, keep the first false hook” failure mode.
