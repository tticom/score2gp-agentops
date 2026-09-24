# L3-01 — Paired-staff barline acceptance for the Lesson 3 first system

- **Status**: PROMOTED (the `task` in `ORCHESTRATION_STATE.json`, authority revision 46). Executable by the implementation role.
- **Repository**: `tticom/score2gp`
- **Branch**: `feat/l3-01-paired-staff-barline-acceptance`
- **Owner Role**: `implementation`
- **Reviewer Role**: `reviewer`
- **Delivery Action**: `pull_request`
- **Prerequisites**: `L3-00`

## 1. Requirement and authority

This is the first "First complete system" checkpoint of
[L3-NATIVE](../../plans/2026-09-05-lesson3-native-working-slice.md) (§5). It is
the single seam that L3-00 proposed, with evidence (tticom/score2gp#462, "Proposed
next seam", claims 9 and 10). L3-00 was merged at
`1672d5de4560f9fa76913274f9ee41bac46fc36b`.

## 2. Evidence baseline

At product `d60a8de`, whose `src/` is unchanged at `71535f381584615a96667d026ef5a579c4c356d5`:

- On Lesson 3 page 1 system 1, the product finds 8 barline boundaries. The PDF has 4, so it builds 7 bar boxes for 3 printed measures (`grouping_status: partial`).
- The TAB-staff filter (`filter_tab_barline_candidates`, `src/score2gp/pdf.py:4321`) accepts the 4 correct boundaries.
- The 4 extra boundaries all sit on full-height notation-staff note stems. The notation-staff partner path adds them: `other_filtered` at `pdf.py:4358`, then the `raw_coverage_ratio >= 0.98` selection at `pdf.py:4359`, then inheritance at `pdf.py:4362-4382`, then the union at `pdf.py:4415`.
- Systems reported as `grouped` also begin at the wrong bar index (8, 13 and 30, where the PDF has 4, 6 and 14). This is observed, not root-caused.
- The PDF-only topology rule measured by L3-00, with no product code or reference involved, gives 23 systems of `[15, 22, 19, 10]` = 66 measures, which matches the reference.

## 3. Hypothesis and a known risk

**Hypothesis H1 (falsifiable):** a notation-staff (partner) candidate becomes a
system barline only when the TAB staff independently has a barline stroke at
the same x, within the existing inheritance tolerance. A note stem has no
matching TAB stroke.

**Risk:** partner inheritance exists to restore barlines that the TAB filter
misses (`c76d30e`, covered by `tests/test_barline_recovery.py` and `tests/test_pdf.py`).
Taken literally, H1 would make inheritance a no-op and could regress that recovery.
First determine whether the TAB evidence H1 needs is a TAB-staff stroke that the
TAB filter *rejected*, rather than an accepted one. If H1 cannot keep the existing
recovery tests passing unchanged, stop H1 and test **H2**: reject a partner
candidate that is a note stem. A stem has a notehead at one end, or does not span
from the top staff line to the bottom one. Record the counterexample for H1 before
switching. A third hypothesis needs a new architect decision (plan §6).

## 4. Scope

Allowed paths:

- `src/score2gp/pdf.py`: only the partner-staff candidate selection and inheritance block, and helpers it calls.
- `tests/test_paired_staff_barline_acceptance.py`: new focused tests.
- `tests/test_lesson3_native_acceptance.py`: only to re-pin `test_baseline_red_is_verified_and_exactly_classified` to the new exact red classification. It must not be weakened (see L3-00 PR, pre-submit challenge 4).

- `tests/test_pdf.py` and `tests/test_npg_05_irregular_layout_real.py`: only to re-pin expectations
  that encoded the stem over-segmentation, justified against reference GP measure counts. These
  were added at promotion (authority revision 46) after a read-only probe of the H2 fix. It gives
  Lesson 3 66/66 and Lesson 7 50/50 measures, against 131 and 121 before.

No change to the acceptance coordinator, the reference reader, the IR, the
writer, the CLI, dependencies or governance. No private musical content,
coordinates or generated artifacts may be committed.

## 5. Acceptance

1. A partner candidate that is a notation-staff note stem is rejected with a named rejection reason recorded in `details`. A genuine paired barline is still accepted.
2. Lesson 3 page 1 system 1, run through production code on the original PDF, gives exactly the 4 adjudicated boundaries and 3 bar boxes.
3. Production system topology on the whole original PDF reproduces 23 systems of `[15, 22, 19, 10]` = 66 measures. If not, report each remaining divergence by exact system and count; do not relax this criterion.
4. Existing barline-recovery tests (`tests/test_barline_recovery.py`, `tests/test_pdf.py`) pass unchanged. Other private real-source tests, such as Lessons 5 and 6, are unchanged or any difference is explained.
5. Synthetic tests cover a stem-only partner candidate, a genuine paired barline, and a TAB-missed barline recovered through the partner path. A negative control shows that the new test fails when the new check is disabled.
6. Re-running the L3-00 coordinator on the original PDF shows the first-system barline divergence resolved and reports the next earliest divergence. The baseline pin is updated to that exact classification, and the product may still be red.
7. Generation still cannot read the reference, and `artifact_audit.py` passes.

## 6. Validation commands

```text
python -m pytest tests/test_paired_staff_barline_acceptance.py tests/test_barline_recovery.py tests/test_pdf.py
python -m pytest tests/test_native_slice_acceptance.py tests/test_lesson3_native_acceptance.py
python -m pytest
python scripts/artifact_audit.py
git diff --check
```

Full-suite failures must be compared by test ID against the same host's baseline
at `71535f3`. L3-00 found 16 failures there that already existed; any new
failure is a regression.

## 7. Stop conditions

- `reference_data_leaks_to_generation`
- `private_artifact_committed`
- `required_edit_outside_promoted_scope`
- `acceptance_weakened_to_match_output`
- `existing_barline_recovery_regressed` (switch from H1 to H2 as in §3; stop after H2)

## 8. Review

The independent reviewer uses `devils-advocate-review` (plan §7). It must replay
the first-system counterexample, attack stem/barline confusion and fixture
coupling to Lesson 3 coordinates, and publish a formal APPROVE or
REQUEST_CHANGES at the exact head.
