"""Bar conservation check for RES-REQ-0005, with negative controls.

The conservation check (design 04 section 4.5, REQ-0005 A1) must compare the bars a run accounts for
against a source-bar inventory that is derived independently of the bars it checks. If the inventory
is built from the same playable candidates that the replay assembles, a source bar that holds only
non-playable text, or nothing at all, is missing from both sides and the check passes. This module
holds the pure check (no product import) and a self-test that proves:

1. a fully accounted source passes;
2. a source bar with only non-playable candidates fails;
3. a source bar with no candidates fails;
4. a bar the replay invents outside the inventory fails;
5. the narrowed oracle (inventory = replayed bars) passes cases 2 and 3, so it cannot detect them.

Bar keys are (page, system, staff, bar) tuples. They stay in memory; only counts are written.

Usage: python coverage_check.py   (runs the self-test; exit 0 only if every control behaves as stated)
"""
from __future__ import annotations

import sys


def conservation(inventory: set, located: set, replayed: set, accounted: set) -> dict:
    """Compare an independent source-bar inventory with the bars a run accounts for.

    inventory: source bars from layout geometry (staff lines and barlines), not from candidates.
    located:   bars that hold at least one located candidate of any kind.
    replayed:  bars that hold a playable candidate (what the PDF-only builder iterates).
    accounted: bars delivered or covered by a record.
    """
    unaccounted = inventory - accounted
    return {
        "source_bars": len(inventory),
        "bars_replayed": len(replayed & inventory),
        "bars_candidate_only": len((located - replayed) & inventory),
        "bars_empty": len(inventory - located),
        "bars_unaccounted": len(unaccounted),
        "bars_outside_inventory": len((replayed | accounted) - inventory),
        "conservation_ok": not unaccounted and not (replayed | accounted) - inventory,
    }


def self_test() -> list[str]:
    bar = [(1, 1, 1, b) for b in range(1, 5)]
    failures = []

    def expect(name, result, ok):
        if result["conservation_ok"] is not ok:
            failures.append(f"{name}: conservation_ok={result['conservation_ok']}, expected {ok}")
        print(f"{name}: {'PASS' if result['conservation_ok'] is ok else 'FAIL'} "
              f"(conservation_ok={result['conservation_ok']}, expected {ok})")

    full = set(bar)
    expect("control-1 fully accounted", conservation(full, full, full, full), True)
    # bar 4 holds only candidate-text: located, not replayed, so not accounted by today's builder
    expect("control-2 candidate-only bar", conservation(full, full, set(bar[:3]), set(bar[:3])), False)
    # bar 4 holds nothing
    expect("control-3 empty bar", conservation(full, set(bar[:3]), set(bar[:3]), set(bar[:3])), False)
    # the replay yields a bar the layout does not have
    extra = full | {(1, 1, 1, 9)}
    expect("control-4 bar outside inventory", conservation(full, extra, extra, extra), False)
    # the weak oracle: inventory taken from the replayed bars hides controls 2 and 3
    narrowed = set(bar[:3])
    expect("control-5 narrowed oracle, candidate-only bar",
           conservation(narrowed, full, narrowed, narrowed), True)
    expect("control-5 narrowed oracle, empty bar",
           conservation(narrowed, narrowed, narrowed, narrowed), True)
    return failures


if __name__ == "__main__":
    bad = self_test()
    print("self-test:", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)
