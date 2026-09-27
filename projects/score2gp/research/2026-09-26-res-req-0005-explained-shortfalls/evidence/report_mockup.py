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
from score2gp.pdf_only_chord_event_grouper import PDF_ONLY_CHORD_X_TOLERANCE_PT, PdfOnlyChordEventGrouper  # noqa: E402
from score2gp.pdf_tab_bar_assembler import split_tab_candidates_by_floating_barlines  # noqa: E402
from score2gp.pdf_tab_measure_timing import select_pdf_tab_grid_spacing_and_duration_name  # noqa: E402
from score2gp.pdf_tab_event_factory import _REST_CANDIDATE_MAP  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from facts_harness import SAFE, source_inventory  # noqa: E402  (SAFE: pdf.py:2283-2305 exemption list)
from coverage_check import conservation  # noqa: E402

USER = {  # engine code -> (user reason, family, plain-language text, suggested action)
    "pdf_only_tab_ambiguous_duration": (
        "rhythm-ambiguous", "ambiguous_evidence",
        "The note lengths in these bars could be read more than one way.",
        "Check the rhythm in these bars by hand."),
    "pdf_only_tab_measure_overcapacity": (
        "bar-overfull", "contradictory_evidence",
        "The notes read in these bars don't fit the bar's time signature, so at least one note or length was misread.",
        "Check these bars for a misread note or duration."),
    "pdf_only_tab_source_bar_without_playable_candidate": (
        "bar-content-not-found", "missing_observation",
        "These bars are on the page, but no fret numbers were found in them. Today they are missing from the output.",
        "Check whether these bars are empty, rests, or hold notes that were not read."),
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


def duration_methods(bf, floating_barlines, draft=False):
    """How each event's duration was chosen in one assembled bar, mirroring pdf_tab_bar_assembler.py:56-117.

    The assembler groups candidates into events by x position (PdfOnlyChordEventGrouper), then asks
    select_pdf_tab_grid_spacing_and_duration_name (pdf_tab_measure_timing.py:45-66) for one duration
    from the number of events N only: N <= 8 eighth, <= 16 16th, <= 32 32nd, else 64th. An event keeps
    that duration unless it is a rest symbol or carries explicit duration evidence
    (pdf_tab_event_factory.py:83-133). Spacing between events is never an input.
    Returns a Counter of method labels ("count_rule:<duration>", "explicit_evidence", "rest_symbol").
    """
    grouper = PdfOnlyChordEventGrouper(tolerance=PDF_ONLY_CHORD_X_TOLERANCE_PT)
    measures = split_tab_candidates_by_floating_barlines(bf, floating_barlines) if floating_barlines else [bf]
    methods = collections.Counter()
    for m in measures:
        groups = grouper.group_bar_candidates(m)
        _, name = select_pdf_tab_grid_spacing_and_duration_name(len(groups), editable_draft=draft)
        for g in groups:
            if any((c.raw_text or "").lower() in _REST_CANDIDATE_MAP for c in g):
                methods["rest_symbol"] += 1
            elif any(c.duration_evidence is not None and (c.duration_evidence.source == "visual_morphology" or (
                    not c.duration_evidence.is_fallback_placeholder and c.duration_evidence.duration_ticks > 0))
                    for c in g):
                methods["explicit_evidence"] += 1
            else:
                methods[f"count_rule:{name}"] += 1
    return methods


def build_records():
    tab = TabRaw.from_json_file(RUN / "tab" / "tab_raw.json")
    fret = [c for c in tab.candidates if (c.parsed_fret is not None and c.kind == "fret") or c.raw_text == "quarter_rest"]
    keys = sorted({bar_key(c) for c in fret})
    # Source bars come from layout geometry, independent of candidates (facts_harness.source_inventory).
    inventory, _ = source_inventory(tab.source_pdf)
    located = [c for c in tab.candidates if c.bar_index is not None and c.system_index is not None]
    records = []
    delivered = []
    for k in sorted(inventory - set(keys)):
        here = [c for c in located if bar_key(c) == k]
        records.append({"feature_kind": "bar",
                        "location": {"precision": "bar", "page": k[0], "system": k[1], "staff": k[2], "source_bar": k[3]},
                        "engine_code": "pdf_only_tab_source_bar_without_playable_candidate", "stage": "build-ir",
                        "disposition": "refused_region",
                        "evidence": dict(collections.Counter(f"candidate_kind:{c.kind}" for c in here)),
                        "candidate_ids": [c.id for c in here], "impact": {"notes": 0, "bars": 1}})
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
                        "disposition_detail": {"method": dict(duration_methods(bf, tab.floating_barlines))},
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
    # One record per dropped feature, at the finest location extraction gave it (G16, G17).
    for c in tab.candidates:
        if c.kind != "candidate-text":
            continue
        if c.bar_index is not None and c.system_index is not None:
            loc = {"precision": "bar", "page": c.page_index or 1, "system": c.system_index,
                   "staff": c.staff_index or 1, "source_bar": c.bar_index}
        elif c.page_index is not None:
            loc = {"precision": "page", "page": c.page_index}
        else:
            loc = {"precision": "document"}
        records.append({"feature_kind": "text", "location": loc, "engine_code": "pdf_text_candidate_not_converted",
                        "stage": "build-ir", "disposition": "omitted", "evidence": {}, "candidate_ids": [c.id],
                        "impact": {"notes": 0, "bars": 0, "items": 1}})
    for ly in (tab.structural_signals or {}).get("lyrics", []):
        if ly.get("system_index") is not None:
            loc = {"precision": "system", "page": ly.get("page_index"), "system": ly.get("system_index"),
                   "staff": ly.get("staff_index")}
        elif ly.get("page_index") is not None:
            loc = {"precision": "page", "page": ly.get("page_index")}
        else:
            loc = {"precision": "document"}
        records.append({"feature_kind": "lyric", "location": loc, "engine_code": "pdf_lyrics_not_converted",
                        "stage": "build-ir", "disposition": "omitted", "evidence": {},
                        "impact": {"notes": 0, "bars": 0, "items": 1}})
    accounted = {(r["location"]["page"], r["location"]["system"], r["location"]["staff"], r["location"]["source_bar"])
                 for r in records if r["feature_kind"] in ("bar", "duration")}
    check = conservation(inventory, {bar_key(c) for c in located}, set(keys), accounted)
    return sorted(inventory), delivered, records, check


def where_items(recs):
    """Where omitted features are, by location precision. Redacted: counts of distinct places only."""
    by = collections.defaultdict(list)
    for r in recs:
        by[r["location"]["precision"]].append(r["location"])
    if PRIVATE:
        return "; ".join(f"{prec}: " + ", ".join(sorted({"/".join(str(v) for k, v in loc.items() if k != "precision")
                                                           for loc in locs})) for prec, locs in by.items())
    parts = []
    for prec, locs in sorted(by.items()):
        places = {tuple(v for k, v in loc.items() if k != "precision") for loc in locs}
        parts.append(f"{len(locs)} located to {prec} ({len(places)} distinct)")
    return "; ".join(parts) + " — listed in the private report"


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
    keys, delivered, records, check = build_records()
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
    rule = collections.Counter()
    for r in approx:
        for method, n in r["disposition_detail"]["method"].items():
            rule[method] += n
    by_dur = ", ".join(f"{m.split(':', 1)[1]} {n}" for m, n in sorted(rule.items()) if m.startswith("count_rule:"))
    kept = rule.get("explicit_evidence", 0) + rule.get("rest_symbol", 0)
    p(f"| `approximated` | Rhythm in these bars was not read from the notation. Every note or chord in a bar was "
      f"given the same length, chosen only from how many there are in the bar: up to 8 become eighth notes, "
      f"9 to 16 become sixteenths, 17 to 32 become 32nds. Where they are placed on the page does not change "
      f"their length{' (except rest symbols and notes with a readable duration mark)' if kept else ''}. "
      f"| {len(approx)} | {sum(r['impact']['notes'] for r in approx)} |")
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
    p("| Feature | Items | Where | Why |")
    p("|---|---|---|---|")
    omitted = collections.defaultdict(list)
    for r in records:
        if r["disposition"] == "omitted":
            omitted[r["feature_kind"]].append(r)
    for kind, rs in omitted.items():
        label = {"text": "Text on the page (unclassified)", "lyric": "Lyrics"}[kind]
        p(f"| {label} | {sum(r['impact']['items'] for r in rs)} | {where_items(rs)} | `feature-not-supported` |")
    p("")
    p("## Details for support\n")
    p("Events in converted bars, by how their duration was chosen: "
      + (f"count rule ({by_dur}); " if by_dur else "")
      + f"explicit duration evidence {rule.get('explicit_evidence', 0)}; rest symbols {rule.get('rest_symbol', 0)}.\n")
    p("| Engine code | Stage | Family | Records | Evidence codes (count) |")
    p("|---|---|---|---|---|")
    groups = collections.defaultdict(list)
    for r in records:
        groups[(r["engine_code"], r["stage"])].append(r)
    fam = {"pdf_only_tab_ambiguous_duration": "ambiguous_evidence", "pdf_only_tab_measure_overcapacity": "contradictory_evidence",
           "pdf_only_tab_inferred_timing": "missing_observation", "measure_fill_rest_synthesised": "missing_observation",
           "pdf_text_candidate_not_converted": "unsupported_feature", "pdf_lyrics_not_converted": "unsupported_feature",
           "pdf_only_tab_source_bar_without_playable_candidate": "missing_observation"}
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
    p(f"- Source bars (layout inventory): {check['source_bars']}; bars with a playable candidate: "
      f"{check['bars_replayed']}; candidate-only: {check['bars_candidate_only']}; empty: {check['bars_empty']}; "
      f"not accounted for by a delivered bar or a record: {check['bars_unaccounted']}")
    p(f"- Records: {len(records)} (private, `shortfall-records.json`); sanitised aggregate: counts and codes only")
    print("\n".join(out))


if __name__ == "__main__":
    main()
