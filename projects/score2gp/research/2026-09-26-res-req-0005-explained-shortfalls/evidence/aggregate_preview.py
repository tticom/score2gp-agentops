"""Corpus aggregate preview for RES-REQ-0005, built only from the committed counts-only evidence.

Reads run-matrix-facts.json (same directory) and writes corpus-aggregate-preview.json: one row per
(user reason, engine code, disposition) with occurrence, bar and source counts, ranked by bars
affected and then by sources affected. The mapping from engine code to family and user reason is
the proposal in 02-reason-code-taxonomy.md. Source bars come from the independent layout inventory
(facts[source]["source_inventory"], built by facts_harness.source_inventory), not from the replay.
Document-level rows count every source bar as affected; bar rows come from the pdf-only replay, plus
the inventory bars the replay never reaches (no playable candidate).

Usage: python aggregate_preview.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
SOURCES = ["L3", "L4", "L5", "L6", "L7", "EX2", "CFMWH"]
# sidecar route, observed 7/7 by the prior-session run matrix (see README): generate-sidecar exit 1, traceback
SIDECAR_CRASH_SOURCES = SOURCES


def row(user_reason, family, code, disposition, level, occurrences, bars, sources, proposed=False):
    """proposed=True marks an engine code or disposition that the taxonomy proposes but the product lacks."""
    return {"user_reason": user_reason, "family": family, "engine_code": code, "disposition": disposition,
            "level": level, "occurrences": occurrences, "bars_affected": bars, "sources_affected": sources,
            "proposed": proposed}


def main() -> None:
    facts = json.loads((HERE / "run-matrix-facts.json").read_text(encoding="utf-8"))
    rows = []

    def source_bars(s):
        return facts[s]["source_inventory"]["source_bars"]

    def bar_codes(mode):
        agg: dict[str, list[int]] = {}
        for s in SOURCES:
            for code, n in facts[s][mode]["bars_refused_by_code"].items():
                a = agg.setdefault(code, [0, 0])
                a[0] += n
                a[1] += 1
        return agg

    user = {"pdf_only_tab_measure_overcapacity": ("bar-overfull", "contradictory_evidence"),
            "pdf_only_tab_ambiguous_duration": ("rhythm-ambiguous", "ambiguous_evidence")}
    for code, (bars, srcs) in bar_codes("sim_pdfonly").items():
        rows.append(row(*user[code], code, "refused_region", "bar", bars, bars, srcs, proposed=True))

    assembled = sum(facts[s]["sim_pdfonly"]["bars_assembled"] for s in SOURCES)
    rows.append(row("approximated", "missing_observation", "pdf_only_tab_inferred_timing", "approximated", "bar",
                    assembled, assembled, sum(1 for s in SOURCES if facts[s]["sim_pdfonly"]["bars_assembled"])))
    synth = sum(facts[s]["sim_pdfonly"]["bars_assembled_with_synthesised_rests"] for s in SOURCES)
    rows.append(row("approximated", "missing_observation", "measure_fill_rest_synthesised", "synthesised",
                    "bar", synth, synth,
                    sum(1 for s in SOURCES if facts[s]["sim_pdfonly"]["bars_assembled_with_synthesised_rests"]),
                    proposed=True))
    unbuilt = {s: facts[s]["source_inventory"]["bars_candidate_only"] + facts[s]["source_inventory"]["bars_empty"]
               for s in SOURCES}
    rows.append(row("bar-content-not-found", "missing_observation",
                    "pdf_only_tab_source_bar_without_playable_candidate", "refused_region", "bar",
                    sum(unbuilt.values()), sum(unbuilt.values()), sum(1 for s in SOURCES if unbuilt[s]),
                    proposed=True))
    low = sum(facts[s]["sim_pdfonly"]["bars_assembled_containing_low_confidence_candidates"] for s in SOURCES)
    notes = sum(facts[s]["tabraw"]["playable_with_unsafe_candidate_code"] for s in SOURCES)
    rows.append(row("fret-unreadable|note-position-uncertain", "ambiguous_evidence",
                    "non_exempt_candidate_level_codes", "approximated|omitted", "note",
                    notes, low, sum(1 for s in SOURCES if facts[s]["tabraw"]["playable_with_unsafe_candidate_code"]),
                    proposed=True))

    doc_refusals: dict[tuple, list[str]] = {}
    for s in SOURCES:
        for route in ("native", "pdfonly", "draft", "nosidecar"):
            r = facts[s]["routes"][route]
            if r["stage"] == "layout-gating" or route in ("native", "nosidecar"):
                doc_refusals.setdefault((r["refusal_code"], r["stage"]), [])
                if s not in doc_refusals[(r["refusal_code"], r["stage"])]:
                    doc_refusals[(r["refusal_code"], r["stage"])].append(s)
    dmap = {"pdf_only_tab_missing_timing_evidence": ("timing-not-in-source", "missing_observation"),
            "missing_musicxml": ("input-required", "invalid_input"),
            "pdf_only_tab_grouping_unsafe": ("layout-unreadable", "ambiguous_evidence")}
    for (code, _stage), srcs in doc_refusals.items():
        bars = sum(source_bars(s) for s in srcs)
        rows.append(row(*dmap[code], code, "refused_document", "document", len(srcs), bars, len(srcs)))
    bars = sum(source_bars(s) for s in SIDECAR_CRASH_SOURCES)
    rows.append(row("internal-error", "internal_error", "sidecar_generation_measure_capacity_invalid",
                    "refused_document", "document", len(SIDECAR_CRASH_SOURCES), bars, len(SIDECAR_CRASH_SOURCES),
                    proposed=True))

    for key, code in (("lyrics", "pdf_lyrics_not_converted"),):
        n = sum(facts[s]["tabraw"]["structural_signal_counts"].get(key, 0) for s in SOURCES)
        srcs = sum(1 for s in SOURCES if facts[s]["tabraw"]["structural_signal_counts"].get(key, 0))
        rows.append(row("feature-not-supported", "unsupported_feature", code, "omitted", "feature", n, None, srcs,
                        proposed=True))
    n = sum(facts[s]["tabraw"]["kinds"].get("candidate-text", 0) for s in SOURCES)
    rows.append(row("feature-not-supported", "unsupported_feature", "pdf_text_candidate_not_converted",
                    "omitted", "feature", n, None,
                    sum(1 for s in SOURCES if facts[s]["tabraw"]["kinds"].get("candidate-text", 0)), proposed=True))

    rows.sort(key=lambda r: (-(r["bars_affected"] or 0), -r["sources_affected"], -r["occurrences"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    out = {"schema": "res-req-0005.aggregate-preview.v0", "sources": len(SOURCES),
           "source_bars_total": sum(source_bars(s) for s in SOURCES),
           "source_bars_replayed_total": sum(facts[s]["sim_pdfonly"]["source_bars"] for s in SOURCES),
           "rows": rows}
    (HERE / "corpus-aggregate-preview.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
