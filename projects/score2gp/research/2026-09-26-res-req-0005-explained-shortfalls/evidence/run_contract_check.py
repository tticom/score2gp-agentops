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
5. a file replaced at `--out` after a successful run fails the hash check.

Usage: python run_contract_check.py   (runs the self-test; exit 0 only if every control behaves as stated)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

EXIT = {"success": 0, "output_exists": 1, "refused": 2, "partial": 6}


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


def contract_run(root: Path, run_id: str, outcome: str, overwrite: bool = False,
                 crash_at: str | None = None) -> int | None:
    """Model one `convert` run under the proposed contract. Returns the exit code, None on crash.

    outcome: "success", "partial" or "refused" (what the stages would produce).
    crash_at: None, "start" (before any write) or "stages" (after the report-first write).
    """
    out, partial, report = root / "out.gp", root / "out.partial.gp", root / "report.json"
    staging = root / ".score2gp-runs" / run_id
    if crash_at == "start":
        raise Crash
    # 1. report first: a fresh record for this run before anything else
    record = {"run_id": run_id, "status": "running", "output_written": False, "outputs": []}
    _write_report(report, record)
    # 2. preflight
    existing = [p for p in (out, partial) if p.exists()]
    if existing and not overwrite:
        record.update(status="refused", code="output_exists", exit=EXIT["output_exists"])
        _write_report(report, record)
        return EXIT["output_exists"]
    staging.mkdir(parents=True)
    if existing:
        (staging / "previous").mkdir()
        for p in existing:
            os.replace(p, staging / "previous" / p.name)
    # 3. stages
    if crash_at == "stages":
        raise Crash
    # 4. build in the run-unique staging directory, then publish atomically
    if outcome in ("success", "partial"):
        target = out if outcome == "success" else partial
        built = staging / target.name
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


def _run(root: Path, outcome: str, **kwargs) -> tuple[str, int | None]:
    run_id = str(uuid.uuid4())
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

    for fn in (fresh_success, s2_no_overwrite, s2_overwrite_partial, s2_overwrite_refused,
               s2_crash_start, s3_stale_partial, s4_crash_stages, s6_replaced_after_success):
        case(fn)
    return failures


if __name__ == "__main__":
    bad = self_test()
    print("self-test:", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)
