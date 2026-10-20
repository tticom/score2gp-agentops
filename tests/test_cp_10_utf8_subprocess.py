"""Byte-level control-plane regressions; gh is a local byte-emitting process.

No GitHub credentials, remote writes, or musical fixtures are used. The shim
changes only executable discovery so Windows needs no compiled fake gh.exe.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

import pytest


ROOT = Path(__file__).resolve().parents[1]
TEXT = "review \u201d \u009d \u96ea"


def encoding_violations(source: str) -> list[int]:
    """Grep-style AST scan also covers multiline calls and injected runners."""
    violations = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not (
            (isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "check_output", "check_call", "Popen", "call"})
            or (isinstance(node.func, ast.Name) and node.func.id == "runner")
        ):
            continue
        keywords = {item.arg: item.value for item in node.keywords}
        # encoding/errors themselves enable subprocess text mode, too.
        text_mode = any(
            key in keywords and not (
                isinstance(keywords[key], ast.Constant)
                and keywords[key].value in (False, None)
            )
            for key in ("text", "universal_newlines", "encoding", "errors")
        )
        if text_mode and any(
            not isinstance(keywords.get(key), ast.Constant)
            or keywords[key].value != value
            for key, value in (("encoding", "utf-8"), ("errors", "strict"))
        ):
            violations.append(node.lineno)
    return violations


def test_scripts_declare_utf8_strict_for_text_subprocesses():
    """Reject reintroduced locale decoding, including indirect runner calls."""
    failures = {
        str(path.relative_to(ROOT)): lines
        for path in sorted((ROOT / "scripts").rglob("*.py"))
        if (lines := encoding_violations(path.read_text(encoding="utf-8")))
    }
    assert failures == {}


STUB = r'''
import json, pathlib, sys
directory = pathlib.Path(sys.argv[1])
args = sys.argv[2:]
text = "review \u201d \u009d \u96ea"
head = "a" * 40
merge_commit = "b" * 40
scenario = (directory / "scenario").read_text()
if args[:2] == ["pr", "view"]:
    merged = (directory / "merged").exists()
    value = dict(number=441, state="MERGED" if merged else "OPEN", title=text,
                 headRefName="feat/task-108", headRefOid=head, baseRefName="main",
                 author={"login":"worker"},
                 reviews=[] if scenario == "deny" else [dict(author={"login":"reviewer-a"}, state="APPROVED", commit={"oid":head})],
                 statusCheckRollup=[dict(name="test", conclusion="SUCCESS")],
                 mergeCommit={"oid":merge_commit} if merged else None,
                 mergedBy={"login":"merge-app"} if merged else None)
elif args[:2] == ["api", "graphql"]:
    value = {"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[],"pageInfo":{"hasNextPage":False}}}}}}
elif args[:2] == ["pr", "merge"]:
    assert args == ["pr", "merge", "441", "--repo", "tticom/score2gp", "--merge", "--match-head-commit", head]
    (directory / "merged").write_text("1")
    sys.stdout.buffer.write(text.encode("utf-8"))
    sys.exit(0)
elif args[:2] == ["pr", "comment"]:
    (directory / "comment").write_text(args[args.index("--body") + 1] + "\n" + text, encoding="utf-8")
    sys.stderr.buffer.write(text.encode("utf-8"))
    sys.exit(0)
elif args[:2] == ["pr", "list"]:
    value = [dict(number=441, mergedBy={"login":"merge-app"}, headRefOid=head, mergeCommit={"oid":merge_commit})]
elif args[-1].endswith("/comments"):
    value = [] if scenario == "missing_receipt" else [[dict(user={"login":"merge-app"}, body=(directory / "comment").read_text(encoding="utf-8"))]]
elif args[-1].endswith("/rulesets"):
    value = [dict(id=1, enforcement="active")]
elif args[-1].endswith("/rulesets/1"):
    value = dict(current_user_can_bypass="never", name=text)
elif args == ["probe"]:
    value = {"text":text}
else:
    raise AssertionError(args)
sys.stdout.buffer.write(json.dumps(value, ensure_ascii=False).encode("utf-8"))
'''


def probe(directory: Path, action: str, scenario: str):
    sys.path.insert(0, str(ROOT))
    from scripts import score2gp_orca_control as control
    from scripts import score2gp_governance_audit as audit

    stub = directory / "gh.py"
    stub.write_text(STUB, encoding="utf-8")
    (directory / "scenario").write_text(scenario, encoding="utf-8")
    real_run = subprocess.run

    def gh_run(command, *args, **kwargs):
        assert command[0] == "gh", command
        return real_run([sys.executable, str(stub), str(directory), *command[1:]], *args, **kwargs)

    with patch.object(subprocess, "run", gh_run):
        if action == "run_json":
            assert control.run_json(["gh", "probe"]) == {"text": TEXT}
            return {"decode": "PASS"}
        if action == "capture_live_state":
            live = control.capture_live_state("tticom/score2gp", 441)
            assert live["pull_request"]["title"] == TEXT
            assert live["protection"]["active_rulesets"] == 1
            return {"decode": "PASS"}

        fixtures = runpy.run_path(str(ROOT / "tests/test_score2gp_orca_control.py"))
        authority = fixtures["executor_authority"]()
        authority["merge_policy"]["executor_audit_since"] = "2026-09-24"
        if scenario == "deny":
            with pytest.raises(control.ControlError, match="insufficient_independent_approvals"):
                control.execute_merge(authority, "tticom/score2gp", 441, "merge-app")
            assert not (directory / "merged").exists()
            return {"merge": "DENY", "mutations": 0}
        receipt = control.execute_merge(authority, "tticom/score2gp", 441, "merge-app")
        assert receipt["head_sha"] == "a" * 40
        assert receipt["gate"] == {"decision": "ALLOW", "failures": []}
        findings = audit.audit_delegated_merges(authority)
        expected = [] if scenario == "allow" else [
            f"{repo}#441 merged by delegated login merge-app without a matching merge-executor receipt"
            for repo in audit.MERGE_AUDIT_REPOSITORIES
        ]
        assert findings == expected, findings
        return {"merge": "ALLOW", "audit_findings": len(findings)}


def run_probe(tmp_path, action, scenario, utf8):
    directory = tmp_path / f"{scenario}-{utf8}"
    directory.mkdir()
    env = dict(os.environ)
    env.pop("PYTHONUTF8", None)
    if utf8 is not None:
        env["PYTHONUTF8"] = utf8
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--probe", str(directory), action, scenario],
        cwd=ROOT, env=env, capture_output=True, encoding="utf-8", errors="strict",
    )


@pytest.mark.parametrize("operation", ["run_json", "capture_live_state"])
def test_run_json_and_capture_decode_real_utf8_bytes(tmp_path, operation):
    """Reject drop-encoding, latin-1, and swallow-error/empty-output mutants."""
    result = run_probe(tmp_path, operation, "allow", None)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert json.loads(result.stdout) == {"decode": "PASS"}


@pytest.mark.parametrize("scenario", ["allow", "deny", "missing_receipt"])
def test_audit_and_executor_independent_of_pythonutf8(tmp_path, scenario):
    """Reject locale reads or false audit findings; retain ALLOW and DENY gates."""
    unset = run_probe(tmp_path, "gates", scenario, None)
    enabled = run_probe(tmp_path, "gates", scenario, "1")
    assert unset.returncode == 0, unset.stderr
    assert enabled.returncode == 0, enabled.stderr
    assert unset.stderr == enabled.stderr == ""
    assert json.loads(unset.stdout) == json.loads(enabled.stdout)


if __name__ == "__main__":
    assert sys.argv[1] == "--probe"
    print(json.dumps(probe(Path(sys.argv[2]), sys.argv[3], sys.argv[4])))
