"""Run CP-18 tests against wrong implementations, outside the source checkout.

Exit zero only when every named mutant produces an assertion failure. Receipts
contain counts and codes; failing raw test transcripts are never published.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

# Name, original text, replacement, tests that independently reject the error.
MUTANTS = [
    ("ignore_status_warning", 'and result.stderr.strip():', 'and False:',
     "test_status_warning_is_not_clean"),
    ("never_remove", 'git(repo, "worktree", "remove", str(path.absolute()))',
     'None', "test_lifecycle"),
    ("remove_dirty", 'return "dirty"', 'return "remove_closed_author"', "test_lifecycle and dirty"),
    ("ignore_lock", 'return "locked"', 'return "remove_closed_author"', "test_lifecycle"),
    ("remove_open_pr_worktree", 'return "open_pr_author"',
     'return "remove_closed_author"', "test_lifecycle"),
    ("remove_unclassified", 'return "unclassified"', 'return "remove_closed_author"', "test_lifecycle"),
    ("lose_deliverables", 'return "requested_deliverables"',
     'return "remove_closed_author"', "test_lifecycle"),
    ("ignore_pr_binding", 'return "pr_mismatch"', 'return "remove_closed_author"', "test_lifecycle"),
    ("ignore_remote", 'return "repository_mismatch"', 'return "remove_closed_author"', "test_lifecycle"),
    ("review_without_summary", 'comments = pages(f"repos/{repository}/issues/{pr}/comments")',
     'return True', "test_publication or test_lifecycle"),
    ("accept_wrong_summary_actor", 'if (comment.get("user") or {}).get("login") != actor:',
     'if False:', "test_publication"),
    ("accept_wrong_review_head", ' or review.get("commit_id") != head', '', "test_publication"),
    ("accept_self_review", ' or actor == author', '', "test_publication"),
    ("accept_pending_review", '{"APPROVED": "APPROVE",',
     '{"PENDING": "APPROVE", "APPROVED": "APPROVE",', "test_publication"),
    ("accept_wrong_verdict", ' and f"Verdict: {verdict}" in body', '', "test_publication"),
    ("delete_in_dry_run", 'if not dry_run:', 'if True:', "test_dry_run_and_removal_failure"),
    ("suppress_removal_error", 'row.update(action="preserved", reason="evidence_or_removal_failed")',
     'row.update(action="removed", reason="remove_closed_author")',
     "test_dry_run_and_removal_failure or test_bounds_and_api_failure"),
    ("ignore_bounds", 'return "unsafe_path"', 'return "unclassified"', "test_bounds_and_api_failure"),
    ("leak_owned_temp", 'shutil.rmtree(path, onerror=retry_readonly)', 'None', "test_owned_temp"),
    ("sweep_peer_temp", 'shutil.rmtree(path, onerror=retry_readonly)',
     'shutil.rmtree(temp_root)', "test_owned_temp"),
    ("ignore_temp_keep", 'if keep:\n            row.update', 'if False:\n            row.update', "test_owned_temp"),
    ("hide_child_failure", 'return subprocess.run([arg.replace',
     'return 0 * subprocess.run([arg.replace', "test_owned_temp"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--temp-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    source = (repo / "scripts/score2gp_lifecycle_cleanup.py").read_text(encoding="utf-8")
    rows = []
    args.temp_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cp18-mutants-", dir=args.temp_root) as scratch:
        scratch = Path(scratch)
        for name, before, after, selected in MUTANTS:
            if before not in source:
                raise RuntimeError(f"mutation_anchor_missing:{name}")
            mutant = scratch / "mutant.py"
            mutant.write_text(source.replace(before, after), encoding="utf-8")
            env = dict(os.environ, CP18_CLEANUP_MODULE=str(mutant))
            result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                     "tests/test_cp_18_lifecycle_cleanup.py", "-k", selected,
                                     "--basetemp", str(scratch / "tests")],
                                    cwd=repo, env=env, capture_output=True, text=True,
                                    encoding="utf-8", errors="strict")
            rejected = result.returncode == 1 and "AssertionError" in result.stdout
            rows.append({"mutant": name, "rejected": rejected, "exit_code": result.returncode})
            print(f"{name}: {'REJECTED' if rejected else 'NOT_REJECTED'}", flush=True)
        # The compatibility skill entrypoint must also reach the bounded CLI.
        legacy = scratch / "legacy.py"
        legacy.write_text((repo / "scripts/score2gp_agent_workspace_cleanup.py").read_text().replace(
            "return lifecycle_main()", "return 0"), encoding="utf-8")
        env = dict(os.environ, CP18_LEGACY_MODULE=str(legacy), PYTHONPATH=str(repo))
        result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                                 "tests/test_cp_18_lifecycle_cleanup.py", "-k", "test_legacy_entrypoint"],
                                cwd=repo, env=env, capture_output=True, text=True,
                                encoding="utf-8", errors="strict")
        rows.append({"mutant": "legacy_unbounded_entrypoint",
                     "rejected": result.returncode == 1 and "AssertionError" in result.stdout,
                     "exit_code": result.returncode})
    args.receipt.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return int(not all(row["rejected"] for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
