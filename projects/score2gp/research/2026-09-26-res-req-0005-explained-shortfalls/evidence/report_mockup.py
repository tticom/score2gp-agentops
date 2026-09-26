"""Generate the RES-REQ-0005 user report mock-up from one real run's records.

Builds shortfall records (design 04) from a real `convert` work directory and the product's own
per-bar assembler, then renders the proposed user report (Option B of 03: complete-or-nothing
primary output plus a labelled partial artifact).

By default the rendering is REDACTED: page/system/bar values are replaced by placeholders and
only counts, codes and stage names are printed, so the output may be committed. `--private`
prints real locations; write that only inside the gitignored work directory.

Usage (product venv):
  python report_mockup.py <product-checkout> <run-work-dir> [--private]
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

PRODUCT = Path(sys.argv[1]).resolve()
RUN = Path(sys.argv[2]).resolve()
PRIVATE = "--private" in sys.argv[3:]
sys.path.insert(0, str(PRODUCT / "src"))
from score2gp.tabraw import TabRaw  # noqa: E402
from score2gp.pdf_tab_bar_assembler import assemble_pdf_tab_bar  # noqa: E402
from score2gp.pdf_tab_measure_timing import PdfTabBarAssemblerError  # noqa: E402
from score2gp.pdf_only_chord_event_grouper import PDF_ONLY_CHORD_X_TOLERANCE_PT  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from facts_harness import SAFE  # noqa: E402  (pdf.py:2283-2305 exemption list)

USER = {  # engine code -> (user reason, family, plain-language text, suggested action)
    "pdf_only_tab_ambiguous_duration": (
        "rhythm-ambiguous", "ambiguous_evidence",
        "The note lengths in these bars could be read more than one way.",
        "Check the rhythm in these bars by hand."),
    "pdf_only_tab_measure_overcapacity": (
        "bar-overfull", "contradictory_evidence",
        "The notes read in these bars don't fit the bar's time signature, so at least one note or length was misread.",
        "Check these bars for a misread note or duration."),
}
CAND_USER = {
    "fret-unreadable": {"pdf_fret_optical_bounds_confidence_below_threshold", "pdf_fret_refinement_not_enough_for_build_ir",
                        "pdf_fret_digit_symbol_overlap_ambiguous", "pdf_fret_digits_not_merged_exceeds_max_fret"},
    "note-position-uncertain": {"pdf_string_assignment_missing", "pdf_string_assignment_outside_staff",
                                "pdf_candidates_unassigned_to_string", "pdf_playable_candidate_requires_string_assignment",
                                "ambiguous_bar_assignment", "pdf_barlines_ambiguous", "pdf_bar_box_boundary_ambiguous",
                                "pdf_candidate_boundary_ambiguous", "pdf_candidate_on_bar_boundary",
                                "pdf_candidate_outside_bar", "pdf_candidate_outside_system",
                                "pdf_candidates_unassigned_to_system"},
    "notation-symbol-unread": {"pdf_notation_rhythm_missing_notehead"},
}


def bar_key(c):
    return (c.page_index or 1, c.system_index if c.system_index is not None else -1, c.staff_index or 1,
            c.bar_index if c.bar_index is not None else -1)


def build_records():
    tab = TabRaw.from_json_file(RUN / "tab" / "tab_raw.json")
    fret = [c for c in tab.candidates if (c.parsed_fret is not None and c.kind == "fret") or c.raw_text == "quarter_rest"]
    keys = sorted({bar_key(c) for c in fret})
    records = []
    delivered = []
    for i, k in enumerate(keys, 1):
        bf = [c for c in fret if bar_key(c) == k]
        loc = {"precision": "bar", "page": k[0], "system": k[1], "staff": k[2], "source_bar": k[3]}
        evidence = collections.Counter()
        for c in bf:
            evidence.update(set((c.raw or {}).get("assignment_warnings") or []) - SAFE)
        try:
            bar = assemble_pdf_tab_bar(bf, floating_barlines=tab.floating_barlines, output_bar_idx=i, track_id="t1",
                                       editable_draft=False, tempo_bpm=120, tempo_is_explicit=False,
                                       chord_x_tolerance_pt=PDF_ONLY_CHORD_X_TOLERANCE_PT)
        except PdfTabBarAssemblerError as e:
            records.append({"feature_kind": "bar", "location": loc, "engine_code": e.category, "stage": e.stage,
                            "disposition": "refused_region", "evidence": dict(evidence),
                            "impact": {"notes": len(bf), "bars": 1}})
            continue
        delivered.append(k)
        records.append({"feature_kind": "duration", "location": loc, "engine_code": "pdf_only_tab_inferred_timing",
                        "stage": "measure-assembly", "disposition": "approximated", "evidence": {},
                        "impact": {"notes": len(bf), "bars": 1}})
        if any(ev.is_rest and not ev.provenance for ev in bar.events):
            records.append({"feature_kind": "rest", "location": loc, "engine_code": "measure_fill_rest_synthesised",
                            "stage": "measure-assembly", "disposition": "synthesised", "evidence": {},
                            "impact": {"notes": 0, "bars": 1}})
        for user, codes in CAND_USER.items():
            n = sum(1 for c in bf if set((c.raw or {}).get("assignment_warnings") or []) & codes)
            if n:
                records.append({"feature_kind": "note", "location": loc, "engine_code": f"candidate:{user}",
                                "stage": "tab-extraction", "disposition": "approximated",
                                "evidence": {k2: v for k2, v in evidence.items() if k2 in codes},
                                "impact": {"notes": n, "bars": 1}})
    kinds = collections.Counter(c.kind for c in tab.candidates)
    lyrics = len((tab.model_dump().get("structural_signals") or {}).get("lyrics", []))
    records.append({"feature_kind": "text", "location": {"precision": "document"},
                    "engine_code": "pdf_text_candidate_not_converted", "stage": "build-ir", "disposition": "omitted",
                    "evidence": {}, "impact": {"notes": 0, "bars": 0, "items": kinds.get("candidate-text", 0)}})
    records.append({"feature_kind": "lyric", "location": {"precision": "document"},
                    "engine_code": "pdf_lyrics_not_converted", "stage": "build-ir", "disposition": "omitted",
                    "evidence": {}, "impact": {"notes": 0, "bars": 0, "items": lyrics}})
    return keys, delivered, records


def where(recs):
    locs = [r["location"] for r in recs]
    pages = {loc["page"] for loc in locs}
    systems = {(loc["page"], loc["system"]) for loc in locs}
    if PRIVATE:
        return "; ".join(f"p{loc['page']} s{loc['system']} b{loc['source_bar']}" for loc in locs)
    return (f"{len(locs)} bars on {len(pages)} page(s), {len(systems)} system(s) — "
            f"listed as \"page ‹p›, system ‹s›, bar ‹b›\" in the private report")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    report = json.loads((RUN / "convert-report.json").read_text(encoding="utf-8"))
    keys, delivered, records = build_records()
    refused = [r for r in records if r["disposition"] == "refused_region"]
    approx = [r for r in records if r["engine_code"] == "pdf_only_tab_inferred_timing"]
    synth = [r for r in records if r["disposition"] == "synthesised"]
    out = []
    p = out.append
    p(f"# Score2GP conversion report — PARTIAL\n")
    p(f"**{len(delivered)} of {len(keys)} bars converted, with estimated rhythm. "
      f"{len(refused)} bars not converted.** The file you asked for was not written. "
      f"A labelled partial file was written beside it: `<name>.partial.gp`.\n")
    p("> Today (product at the pinned SHA) this same run shows only: "
      f"`refusal_code: {report.get('refusal_code')}` at stage `{report.get('stage')}`, exit {report.get('exit_code')}, "
      "with no location and no count of affected bars.\n")
    p("## Not converted\n")
    p("| Why (user reason) | What it means | Bars | Where | What you can do |")
    p("|---|---|---|---|---|")
    by = collections.defaultdict(list)
    for r in refused:
        by[r["engine_code"]].append(r)
    for code, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        u = USER[code]
        p(f"| `{u[0]}` | {u[2]} | {len(rs)} | {where(rs)} | {u[3]} |")
    p("")
    p("## Converted, but check before relying on it\n")
    p("| Why (user reason) | What it means | Bars | Notes |")
    p("|---|---|---|---|")
    p(f"| `approximated` | Rhythm in these bars was estimated from note spacing, not read from notation. | {len(approx)} | "
      f"{sum(r['impact']['notes'] for r in approx)} |")
    p(f"| `approximated` | Rests were added to fill these bars to the time signature. | {len(synth)} | — |")
    for user in CAND_USER:
        rs = [r for r in records if r["engine_code"] == f"candidate:{user}"]
        if rs:
            text = {"fret-unreadable": "Some fret numbers could not be read reliably.",
                    "note-position-uncertain": "Some notes could not be placed on a string or bar with certainty.",
                    "notation-symbol-unread": "A rhythm symbol above the tab could not be recognised."}[user]
            p(f"| `{user}` | {text} | {len(rs)} | {sum(r['impact']['notes'] for r in rs)} |")
    p("")
    p("## Not converted at all (feature not supported yet)\n")
    p("| Feature | Items | Why |")
    p("|---|---|---|")
    for r in records:
        if r["disposition"] == "omitted":
            label = {"text": "Text on the page (unclassified)", "lyric": "Lyrics"}[r["feature_kind"]]
            p(f"| {label} | {r['impact']['items']} | `feature-not-supported` |")
    p("")
    p("## Details for support\n")
    p("| Engine code | Stage | Family | Records | Evidence codes (count) |")
    p("|---|---|---|---|---|")
    groups = collections.defaultdict(list)
    for r in records:
        groups[(r["engine_code"], r["stage"])].append(r)
    fam = {"pdf_only_tab_ambiguous_duration": "ambiguous_evidence", "pdf_only_tab_measure_overcapacity": "contradictory_evidence",
           "pdf_only_tab_inferred_timing": "missing_observation", "measure_fill_rest_synthesised": "missing_observation",
           "pdf_text_candidate_not_converted": "unsupported_feature", "pdf_lyrics_not_converted": "unsupported_feature"}
    for (code, stage), rs in sorted(groups.items()):
        ev = collections.Counter()
        for r in rs:
            ev.update(r["evidence"])
        evs = ", ".join(f"`{k}` {v}" for k, v in sorted(ev.items(), key=lambda kv: -kv[1])) or "—"
        p(f"| `{code}` | `{stage}` | {fam.get(code, 'ambiguous_evidence')} | {len(rs)} | {evs} |")
    p("")
    p("## Run\n")
    sha = __import__("subprocess").run(["git", "-C", str(PRODUCT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    p(f"- Product SHA: `{sha}`; route: `pdf-only`; target: GP7")
    p(f"- Status: `partial` (proposed); today: `{report.get('status')}` / exit {report.get('exit_code')}")
    p(f"- Records: {len(records)} (private, `shortfall-records.json`); sanitised aggregate: counts and codes only")
    print("\n".join(out))


if __name__ == "__main__":
    main()
