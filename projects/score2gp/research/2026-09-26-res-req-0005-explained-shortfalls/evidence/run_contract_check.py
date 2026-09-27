"""Run-bound output contract model for RES-REQ-0005, with negative controls.

Design 03 section 3.3a proposes a run-bound output contract. Its central claim is that file
presence at `--out` is never proof that a run succeeded: a refused rerun without `--overwrite`, or
a run that dies before it writes anything, leaves an earlier run's file in place. Success is
accepted only from the run record (the JSON report) of the caller's own run: matching `run_id`,
`status: success`, exit 0, and the SHA-256 of the file at `--out` equal to the recorded hash.

This module models the proposed contract on a real temporary directory (no product import; the
product has no `run_id`, `--overwrite` or preflight today) and runs three consumers against it:

- `conforming`: the contract's consumer rule (run record bound to the caller's run_id, plus hash);
- `presence_only`: accepts when a file exists at `--out` (forbidden by the contract);
- `status_only`: accepts when the report says `success`, without checking run_id or hash.

The self-test proves:

1. the conforming consumer accepts exactly the successful runs, in every case;
2. in case S2' without `--overwrite` (refused `output_exists`) and in a run that dies before its
   first write, the presence-only consumer is given a false success, so the contract must forbid
   it and cannot be restated as "the file at `--out` is this run's output or absent";
3. with `--overwrite`, a non-success run leaves no file at `--out` (defence in depth), and the
   earlier file is kept under the run's staging directory, not deleted;
4. the status-only consumer is fooled by a stale report, so run_id binding is required;
5. a file replaced at `--out` after a successful run fails the hash check;
6. a caller-supplied `run_id` outside the grammar (traversal, separators, absolute or drive paths)
   is refused with `invalid_run_id` before any path is derived from it, and a run root or staging
   directory that resolves outside `<out-dir>/.score2gp-runs/` (symlink or junction) is refused
   with `run_path_escape` before any mkdir, write or move; in both cases, with `--overwrite`, the
   earlier `--out` stays in place and nothing but the report changes anywhere in the tree;
7. a valid explicit `run_id` with `--overwrite` keeps the earlier file under its own staging
   directory, inside the run root (positive control).

Usage: python run_contract_check.py   (runs the self-test; exit 0 only if every control behaves as stated)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path

EXIT = {"success": 0, "output_exists": 1, "invalid_run_id": 1, "run_path_escape": 1,
        "refused": 2, "partial": 6}
RUN_ROOT = ".score2gp-runs"
# One path component: starts alphanumeric, at most 64 characters, no separator, no drive colon.
RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
WINDOWS_DEVICE = re.compile(r"(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\..*)?", re.IGNORECASE)


class Crash(Exception):
    """Fault injection: the process dies at this point without a handled exit."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _write_report(report: Path, record: dict) -> None:
    _write_atomic(report, json.dumps(record, sort_keys=True).encode())


def valid_run_id(run_id: object) -> bool:
    """The section 3.3a grammar: full match, no '..', no trailing dot, no Windows device name."""
    return (isinstance(run_id, str) and RUN_ID.fullmatch(run_id) is not None
            and ".." not in run_id and not run_id.endswith(".")
            and WINDOWS_DEVICE.fullmatch(run_id) is None)


def _key(path: Path | str) -> str:
    return os.path.normcase(os.path.realpath(path))


def _confined(path: Path, root_real: str, *parts: str) -> bool:
    """True when `path`, with every link resolved, is exactly `root_real` joined with `parts`."""
    return _key(path) == os.path.normcase(os.path.join(root_real, *parts))


def contract_run(root: Path, run_id: str, outcome: str, overwrite: bool = False,
                 crash_at: str | None = None) -> int | None:
    """Model one `convert` run under the proposed contract. Returns the exit code, None on crash.

    outcome: "success", "partial" or "refused" (what the stages would produce).
    crash_at: None, "start" (before any write) or "stages" (after the report-first write).
    """
    out, partial, report = root / "out.gp", root / "out.partial.gp", root / "report.json"
    if crash_at == "start":
        raise Crash
    # 0. argument validation: no path is derived from a run_id outside the grammar, and the
    #    rejected value is not echoed into the record
    if not valid_run_id(run_id):
        _write_report(report, {"run_id": None, "status": "refused", "code": "invalid_run_id",
                               "output_written": False, "outputs": [],
                               "exit": EXIT["invalid_run_id"]})
        return EXIT["invalid_run_id"]
    # 1. report first: a fresh record for this run before anything else
    record = {"run_id": run_id, "status": "running", "output_written": False, "outputs": []}
    _write_report(report, record)
    # 2. preflight: containment of every derived path first, then existing outputs
    out_dir_real = os.path.realpath(root)
    run_root_real = os.path.join(out_dir_real, RUN_ROOT)
    run_root = root / RUN_ROOT
    staging = run_root / run_id
    if not (_confined(run_root, out_dir_real, RUN_ROOT)
            and _confined(staging, run_root_real, run_id)
            and _confined(staging / "previous", run_root_real, run_id, "previous")
            and not os.path.lexists(staging)):
        record.update(status="refused", code="run_path_escape", exit=EXIT["run_path_escape"])
        _write_report(report, record)
        return EXIT["run_path_escape"]
    existing = [p for p in (out, partial) if p.exists()]
    if existing and not overwrite:
        record.update(status="refused", code="output_exists", exit=EXIT["output_exists"])
        _write_report(report, record)
        return EXIT["output_exists"]
    run_root.mkdir(exist_ok=True)
    staging.mkdir()
    if not _confined(staging, run_root_real, run_id):  # re-checked once created
        raise RuntimeError("staging directory left the run root")
    if existing:
        previous = staging / "previous"
        previous.mkdir()
        for p in existing:
            if not _confined(previous / p.name, run_root_real, run_id, "previous", p.name):
                raise RuntimeError("move target left the run root")
            os.replace(p, previous / p.name)
    # 3. stages
    if crash_at == "stages":
        raise Crash
    # 4. build in the run-unique staging directory, then publish atomically
    if outcome in ("success", "partial"):
        target = out if outcome == "success" else partial
        built = staging / target.name
        if not _confined(built, run_root_real, run_id, target.name):
            raise RuntimeError("staged artifact left the run root")
        built.write_bytes(f"GP {outcome} run_id={run_id}".encode())
        digest = _sha256(built)
        os.replace(built, target)
        record["outputs"].append({"role": "primary" if outcome == "success" else "partial",
                                  "path": target.name, "sha256": digest})
        record["output_written"] = outcome == "success"
    # 5. final record
    record.update(status=outcome, exit=EXIT[outcome])
    _write_report(report, record)
    return EXIT[outcome]


def conforming(root: Path, run_id: str, exit_code: int | None) -> bool:
    out, report = root / "out.gp", root / "report.json"
    if exit_code != 0 or not report.exists():
        return False
    record = json.loads(report.read_text())
    if record.get("run_id") != run_id or record.get("status") != "success":
        return False
    primary = [o for o in record["outputs"] if o["role"] == "primary"]
    return len(primary) == 1 and out.exists() and _sha256(out) == primary[0]["sha256"]


def presence_only(root: Path, run_id: str, exit_code: int | None) -> bool:
    return (root / "out.gp").exists()


def status_only(root: Path, run_id: str, exit_code: int | None) -> bool:
    report = root / "report.json"
    return report.exists() and json.loads(report.read_text()).get("status") == "success"


def _run(root: Path, outcome: str, run_id: str | None = None,
         **kwargs) -> tuple[str, int | None]:
    run_id = str(uuid.uuid4()) if run_id is None else run_id
    try:
        return run_id, contract_run(root, run_id, outcome, **kwargs)
    except Crash:
        return run_id, None


def self_test() -> list[str]:
    failures = []

    def expect(name, root, run_id, code, want, extra=()):
        got = {c.__name__: c(root, run_id, code) for c in (conforming, presence_only, status_only)}
        ok = got == want and all(cond for _, cond in extra)
        if not ok:
            failures.append(f"{name}: consumers={got} expected={want} extra={[n for n, c in extra if not c]}")
        print(f"{name}: {'PASS' if ok else 'FAIL'} (exit={code}, conforming={got['conforming']}, "
              f"presence_only={got['presence_only']}, status_only={got['status_only']})")

    def case(fn):
        with tempfile.TemporaryDirectory() as d:
            fn(Path(d))

    def fresh_success(root):
        rid, code = _run(root, "success")
        expect("control-1 fresh success", root, rid, code,
               {"conforming": True, "presence_only": True, "status_only": True})

    def s2_no_overwrite(root):
        _, _ = _run(root, "success")
        before = _sha256(root / "out.gp")
        rid, code = _run(root, "partial")
        expect("control-2 S2' partial rerun, no --overwrite (output_exists)", root, rid, code,
               {"conforming": False, "presence_only": True, "status_only": False},
               [("exit 1", code == EXIT["output_exists"]),
                ("old file untouched", _sha256(root / "out.gp") == before),
                ("no partial written", not (root / "out.partial.gp").exists())])

    def s2_overwrite_partial(root):
        _, _ = _run(root, "success")
        before = _sha256(root / "out.gp")
        rid, code = _run(root, "partial", overwrite=True)
        kept = root / ".score2gp-runs" / rid / "previous" / "out.gp"
        expect("control-3 S2' partial rerun, --overwrite", root, rid, code,
               {"conforming": False, "presence_only": False, "status_only": False},
               [("exit 6", code == EXIT["partial"]),
                ("partial from this run", rid in (root / "out.partial.gp").read_text()),
                ("earlier file kept, not deleted", kept.exists() and _sha256(kept) == before)])

    def s2_overwrite_refused(root):
        _, _ = _run(root, "success")
        rid, code = _run(root, "refused", overwrite=True)
        expect("control-3 S2' refused rerun, --overwrite", root, rid, code,
               {"conforming": False, "presence_only": False, "status_only": False},
               [("exit 2", code == EXIT["refused"]),
                ("no partial", not (root / "out.partial.gp").exists())])

    def s2_crash_start(root):
        _, _ = _run(root, "success")
        rid, code = _run(root, "success", overwrite=True, crash_at="start")
        expect("control-2 S2' run dies before its first write", root, rid, code,
               {"conforming": False, "presence_only": True, "status_only": True})

    def s3_stale_partial(root):
        _, _ = _run(root, "partial")
        rid, code = _run(root, "success", overwrite=True)
        expect("control-1 S3' stale partial, complete rerun, --overwrite", root, rid, code,
               {"conforming": True, "presence_only": True, "status_only": True},
               [("no partial left", not (root / "out.partial.gp").exists())])

    def s4_crash_stages(root):
        _, _ = _run(root, "success")
        rid, code = _run(root, "success", overwrite=True, crash_at="stages")
        record = json.loads((root / "report.json").read_text())
        expect("control-4 S4' crash after report-first write", root, rid, code,
               {"conforming": False, "presence_only": False, "status_only": False},
               [("report running", record["status"] == "running" and record["run_id"] == rid)])

    def s6_replaced_after_success(root):
        rid, code = _run(root, "success")
        (root / "out.gp").write_bytes(b"GP from another process")
        expect("control-5 S6' file replaced after success", root, rid, code,
               {"conforming": False, "presence_only": True, "status_only": True})

    def tree(base: Path) -> dict[str, str]:
        return {p.relative_to(base).as_posix(): (_sha256(p) if p.is_file() else "dir")
                for p in base.rglob("*")}

    def escape_layout(base: Path) -> tuple[Path, Path]:
        """<base>/out-dir holds an earlier output; <base>/outside is a sibling directory."""
        root, outside = base / "out-dir", base / "outside"
        root.mkdir()
        outside.mkdir()
        (root / "out.gp").write_bytes(b"GP from an earlier run")
        return root, outside

    def refused_escape(name, base, root, before, rid, code, want_code, links=()):
        """A refusal with no side effect: only out-dir/report.json changed anywhere under base."""
        after = tree(base)
        changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
        record = json.loads((root / "report.json").read_text())
        expect(name, root, rid, code,
               {"conforming": False, "presence_only": True, "status_only": False},
               [(f"exit 1 {want_code}", code == 1 and record.get("code") == want_code),
                ("earlier --out untouched in place",
                 _sha256(root / "out.gp") == before["out-dir/out.gp"]),
                ("only report.json changed", changed <= {"out-dir/report.json"}),
                ("links unchanged", all(_key(link) == target for link, target in links))])

    def traversal_ids(base):
        for rid in ("../../outside/leak", "../outside", "..", ".", "a/../b", "a\\..\\b",
                    "run..1", "leak/", "", "x" * 65, "run\n", "NUL", "run."):
            with tempfile.TemporaryDirectory(dir=base) as d:
                sub = Path(d)
                root, _ = escape_layout(sub)
                before = tree(sub)
                _, code = _run(root, "success", run_id=rid, overwrite=True)
                refused_escape(f"control-6 traversal/invalid run_id {rid!r}, --overwrite", sub,
                               root, before, rid, code, "invalid_run_id")

    def absolute_ids(base):
        root, outside = escape_layout(base)
        for rid in (str(outside / "leak"), outside.as_posix() + "/leak", "/tmp/leak", "C:\\leak",
                    "C:leak", "C:/leak", "\\\\server\\share\\leak", "//server/share/leak"):
            before = tree(base)
            _, code = _run(root, "success", run_id=rid, overwrite=True)
            refused_escape(f"control-6 absolute run_id {rid!r}, --overwrite", base, root, before,
                           rid, code, "invalid_run_id")

    def link_escape(which):
        def check(base):
            root, outside = escape_layout(base)
            rid = "run-escape-1"
            link = root / RUN_ROOT if which == "run root" else root / RUN_ROOT / rid
            link.parent.mkdir(exist_ok=True)
            _dir_link(link, outside)
            before = tree(base)
            _, code = _run(root, "success", run_id=rid, overwrite=True)
            refused_escape(f"control-6 {which} is a symlink/junction to a sibling, --overwrite",
                           base, root, before, rid, code, "run_path_escape",
                           [(link, _key(outside))])
        check.__name__ = f"link_escape_{which.replace(' ', '_')}"
        return check

    def valid_explicit_id(base):
        root, outside = escape_layout(base)
        before = _sha256(root / "out.gp")
        rid = "run-2026.09.27_A1"
        _, code = _run(root, "success", run_id=rid, overwrite=True)
        kept = root / RUN_ROOT / rid / "previous" / "out.gp"
        run_root_real = os.path.join(os.path.realpath(root), RUN_ROOT)
        expect("control-7 valid explicit run_id, --overwrite (positive)", root, rid, code,
               {"conforming": True, "presence_only": True, "status_only": True},
               [("run_id accepted by grammar", valid_run_id(rid)),
                ("generated uuid4 accepted by grammar", valid_run_id(str(uuid.uuid4()))),
                ("earlier file kept inside the run root",
                 kept.exists() and _sha256(kept) == before
                 and _confined(kept, run_root_real, rid, "previous", "out.gp")),
                ("nothing written outside out-dir", not any(outside.iterdir()))])

    for fn in (fresh_success, s2_no_overwrite, s2_overwrite_partial, s2_overwrite_refused,
               s2_crash_start, s3_stale_partial, s4_crash_stages, s6_replaced_after_success,
               traversal_ids, absolute_ids, link_escape("run root"),
               link_escape("staging directory"), valid_explicit_id):
        case(fn)
    return failures


def _dir_link(link: Path, target: Path) -> None:
    """A directory symlink, or an NTFS junction where a symlink needs a privilege."""
    try:
        os.symlink(target, link, target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        import _winapi
        _winapi.CreateJunction(str(target), str(link))


if __name__ == "__main__":
    bad = self_test()
    print("self-test:", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)
