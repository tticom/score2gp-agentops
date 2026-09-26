"""RES-REQ-0005 evidence harness: counts, codes, stage names and flags only.

Reads the gitignored run directories under <product>/work/res-req-0005/<source>/<route>/ produced by
`score2gp convert` and writes a JSON summary that holds no fret, pitch, text, coordinate or bar values.
It also replays the PDF-only bar loop (build_ir.py:1716-1773 at the pinned SHA) bar by bar, calling the
product's own assemble_pdf_tab_bar, so that every bar's outcome is recorded instead of only the first
failure. The replay is a research simulation, not product behaviour.

Usage (product venv): python facts_harness.py <product-checkout> <out.json>
"""
import ast
import collections
import json
import re
import sys
from pathlib import Path

PRODUCT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(PRODUCT / "src"))
from score2gp.tabraw import TabRaw  # noqa: E402
from score2gp.pdf_tab_bar_assembler import assemble_pdf_tab_bar  # noqa: E402
from score2gp.pdf_tab_measure_timing import PdfTabBarAssemblerError  # noqa: E402
from score2gp.pdf_only_chord_event_grouper import PDF_ONLY_CHORD_X_TOLERANCE_PT  # noqa: E402

W = PRODUCT / "work" / "res-req-0005"
SRCS = ["L3", "L4", "L5", "L6", "L7", "EX2", "CFMWH"]
ROUTES = ["native", "pdfonly", "draft", "nosidecar"]
LOC = {"page", "page_index", "page_number", "system", "system_index", "bar", "bar_index", "measure",
       "measure_index", "measure_number", "beat", "region", "bbox", "location", "staff_index"}
LOCWORD = re.compile(r"\b(page|system|bar|measure|beat)\b", re.I)
# pdf.py:2283-2305 exemption list (informational assignment warnings)
SAFE = {"pdf_string_assignment_nearest_line", "pdf_multidigit_fret_string_assigned",
        "pdf_non_playable_text_not_string_assigned", "pdf_fret_single_digit_extracted",
        "pdf_fret_multidigit_extracted", "pdf_fret_digits_merged", "pdf_fret_split_text_span_merged",
        "pdf_fret_technique_marker_excluded", "pdf_fret_chord_text_digit_excluded",
        "pdf_fret_page_or_legend_number_excluded", "pdf_tuning_standard_detected",
        "pdf_tuning_explicit_strings_detected", "pdf_tuning_string_labels_aligned",
        "pdf_tuning_label_outside_system", "pdf_tuning_label_unassociated",
        "pdf_tuning_text_preserved_non_playable", "pdf_tuning_not_used_for_string_assignment",
        "pdf_tuning_not_used_for_fret_inference", "pdf_pitch_layout_evidence_detected",
        "pdf_timing_mapping_not_implemented"}

_tree = ast.parse((PRODUCT / "src/score2gp/build_ir.py").read_text(encoding="utf-8"))
PDFONLY_GATE: set[str] = set()
for n in ast.walk(_tree):
    if isinstance(n, ast.FunctionDef) and n.name == "build_ir_from_tabraw_only":
        for m in ast.walk(n):
            if isinstance(m, ast.Assign) and getattr(m.targets[0], "id", None) == "unsafe_warning_codes":
                PDFONLY_GATE = {e.value for e in m.value.elts}


def has_loc(w: dict) -> bool:
    return any(k in LOC and w.get(k) is not None for k in w)


def warn_summary(p: Path):
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(d, dict):
        d = d.get("warnings", [])
    codes = collections.Counter(w.get("code") for w in d)
    sev = collections.Counter(w.get("severity", "<none>") for w in d)
    return {"count": len(d), "distinct_codes": len(codes), "severity": dict(sev),
            "with_location_fields": sum(1 for w in d if has_loc(w)),
            "message_mentions_location": sum(1 for w in d if LOCWORD.search(w.get("message") or "")),
            "codes": dict(codes)}


def html_summary(p: Path, refusal):
    if not p.exists():
        return None
    h = p.read_text(encoding="utf-8")
    return {"list_items": h.count("<li>"), "refusal_code_in_html": bool(refusal and refusal in h),
            "recommended_action_in_html": "recommended_action" in h}


def bar_key(c):
    return (c.page_index or 1, c.system_index if c.system_index is not None else -1, c.staff_index or 1,
            c.bar_index if c.bar_index is not None else -1)


def simulate(tabraw_path: Path, draft: bool) -> dict:
    """Per-bar replay of build_ir.py:1716-1773 that records every bar's outcome instead of stopping at the first."""
    tab = TabRaw.from_json_file(tabraw_path)
    gate = collections.Counter(c for c in tab.pdf_layout_warnings if c in PDFONLY_GATE)
    gate.update(w.get("code") for w in tab.warnings if w.get("code") in PDFONLY_GATE)
    fret = [c for c in tab.candidates if (c.parsed_fret is not None and c.kind == "fret") or c.raw_text == "quarter_rest"]
    keys = sorted({bar_key(c) for c in fret})
    per = collections.Counter()
    ok = ok_low = synth = clean = notes_ok = notes_ref = 0
    first_failure = None
    for i, k in enumerate(keys, 1):
        bf = [c for c in fret if bar_key(c) == k]
        if any((c.string is None and c.raw_text != "quarter_rest") or c.bar_index is None or c.system_index is None
               or c.x is None for c in bf):
            code = "pdf_only_tab_grouping_unsafe:missing_layout_field"
            per[code] += 1
            notes_ref += len(bf)
            first_failure = first_failure or code
            continue
        try:
            bar = assemble_pdf_tab_bar(bf, floating_barlines=tab.floating_barlines, output_bar_idx=i, track_id="t1",
                                       editable_draft=draft, tempo_bpm=120, tempo_is_explicit=False,
                                       chord_x_tolerance_pt=PDF_ONLY_CHORD_X_TOLERANCE_PT)
        except PdfTabBarAssemblerError as e:
            per[e.category] += 1
            notes_ref += len(bf)
            first_failure = first_failure or e.category
            continue
        ok += 1
        notes_ok += len(bf)
        low = any(set((c.raw or {}).get("assignment_warnings") or []) - SAFE for c in bf)
        syn = any(ev.is_rest and not ev.provenance for ev in bar.events)
        ok_low += low
        synth += syn
        clean += not (low or syn)
    return {"source_bars": len(keys), "bars_assembled": ok, "bars_refused_by_code": dict(per),
            "first_failure_code": first_failure,
            "bars_assembled_containing_low_confidence_candidates": ok_low,
            "bars_assembled_with_synthesised_rests": synth,
            "bars_assembled_clean": clean,
            "fret_candidates_in_assembled_bars": notes_ok, "fret_candidates_in_refused_bars": notes_ref,
            "global_layout_gate_codes": dict(gate)}


def main() -> None:
    out = {}
    for s in SRCS:
        rec = {"routes": {}}
        for r in ROUTES:
            d = W / s / r
            rp = d / "convert-report.json"
            rep = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
            dp = d / "diagnostics.json"
            diag = json.loads(dp.read_text(encoding="utf-8")) if dp.exists() else None
            details = (diag or {}).get("details") or {}
            rec["routes"][r] = {
                "exit": rep.get("exit_code"), "status": rep.get("status"), "stage": rep.get("stage"),
                "refusal_code": rep.get("refusal_code"), "error_type": rep.get("error_type"),
                "report_total_candidates": (rep.get("summary_counts") or {}).get("total_candidates"),
                "report_playable_candidates": (rep.get("summary_counts") or {}).get("playable_candidates"),
                "diag_details_keys": sorted(details.keys()) if diag else None,
                "diag_has_location": any(k in LOC for k in details),
                "warnings_json": warn_summary(d / "warnings.json"),
                "html": html_summary(d / "conversion-report.html", rep.get("refusal_code")),
            }
        tp = W / s / "native" / "tab" / "tab_raw.json"
        tab = json.loads(tp.read_text(encoding="utf-8"))
        cands = tab.get("candidates", [])
        top = collections.Counter(w.get("code") for w in tab.get("warnings", []))
        cc = collections.Counter()
        cu = collections.Counter()
        for c in cands:
            ws = set((c.get("raw") or {}).get("assignment_warnings") or [])
            cc.update(ws)
            cu.update(ws - SAFE)
        playable = [c for c in cands if c.get("parsed_fret") is not None]
        rec["tabraw"] = {
            "candidates": len(cands), "playable": len(playable),
            "kinds": dict(collections.Counter(c.get("kind") for c in cands)),
            "top_level_warning_count": sum(top.values()), "top_level_distinct_codes": len(top),
            "candidate_level_distinct_codes": len(cc), "candidate_level_occurrences": sum(cc.values()),
            "candidate_level_codes_absent_from_top_level": sorted(set(cc) - set(top)),
            "candidate_unsafe_code_counts": dict(cu),
            "playable_with_unsafe_candidate_code": sum(
                1 for c in playable if set((c.get("raw") or {}).get("assignment_warnings") or []) - SAFE),
            "layout_class": tab.get("pdf_layout_class"),
            "layout_warning_codes": sorted(set(tab.get("pdf_layout_warnings") or [])),
        }
        rec["sim_pdfonly"] = simulate(tp, False)
        rec["sim_draft"] = simulate(tp, True)
        out[s] = rec
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
