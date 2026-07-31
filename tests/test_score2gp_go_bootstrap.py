from __future__ import annotations

import subprocess
from pathlib import Path
import pytest

from scripts.score2gp_go_bootstrap import parse_active_task_content, run_go_bootstrap, query_github_pr_state


def run_git(cwd: str | Path, args: list[str], check: bool = True) -> str:
    res = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )
    return res.stdout.strip()


@pytest.fixture
def temp_git_repos(tmp_path: Path) -> dict[str, Path]:
    bare_agentops = tmp_path / "remote_agentops.git"
    bare_product = tmp_path / "remote_product.git"

    run_git(tmp_path, ["init", "--bare", str(bare_agentops)])
    run_git(tmp_path, ["init", "--bare", str(bare_product)])

    run_git(bare_agentops, ["symbolic-ref", "HEAD", "refs/heads/main"])
    run_git(bare_product, ["symbolic-ref", "HEAD", "refs/heads/main"])

    init_agentops = tmp_path / "init_agentops"
    init_product = tmp_path / "init_product"

    run_git(tmp_path, ["clone", str(bare_agentops), str(init_agentops)])
    run_git(tmp_path, ["clone", str(bare_product), str(init_product)])

    for repo in [init_agentops, init_product]:
        run_git(repo, ["config", "user.name", "Test User"])
        run_git(repo, ["config", "user.email", "test@example.com"])

    active_task_dir = init_agentops / "projects/score2gp"
    active_task_dir.mkdir(parents=True, exist_ok=True)

    task_v1 = """# Active Task

**Task**: PDFTAB-DUR-02: Public PDF-Tab Duration Synthetic Fixture Creation
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Fixture Author
**Repository**: tticom/score2gp
**PR Branch**: `agy/generate-public-pdf-tab-duration-fixture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0019-generate-public-pdf-tab-duration-fixture.md`
"""
    (active_task_dir / "ACTIVE_TASK.md").write_text(task_v1)
    (init_product / "README.md").write_text("# Score2GP Product")

    run_git(init_agentops, ["add", "."])
    run_git(init_agentops, ["commit", "-m", "Initial commit task 1"])
    run_git(init_agentops, ["branch", "-M", "main"])
    run_git(init_agentops, ["push", "origin", "main"])

    run_git(init_product, ["add", "."])
    run_git(init_product, ["commit", "-m", "Initial product commit"])
    run_git(init_product, ["branch", "-M", "main"])
    run_git(init_product, ["push", "origin", "main"])

    local_agentops = tmp_path / "local_agentops"
    local_product = tmp_path / "local_product"

    run_git(tmp_path, ["clone", str(bare_agentops), str(local_agentops)])
    run_git(tmp_path, ["clone", str(bare_product), str(local_product)])

    for repo in [local_agentops, local_product]:
        run_git(repo, ["config", "user.name", "Test User"])
        run_git(repo, ["config", "user.email", "test@example.com"])

    return {
        "bare_agentops": bare_agentops,
        "bare_product": bare_product,
        "init_agentops": init_agentops,
        "init_product": init_product,
        "local_agentops": local_agentops,
        "local_product": local_product,
    }


def test_case_1_completed_task_branch_stale_main_remote_task_changed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    run_git(local_ops, ["checkout", "-b", "agy/generate-public-pdf-tab-duration-fixture"])
    run_git(local_prod, ["checkout", "-b", "agy/generate-public-pdf-tab-duration-fixture"])

    task_v2 = """# Active Task

**Task**: PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-extraction-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_v2)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Promote task 2"])
    run_git(init_ops, ["push", "origin", "main"])

    stale_task = parse_active_task_content((local_ops / "projects/score2gp/ACTIVE_TASK.md").read_text())
    assert stale_task["task"] == "PDFTAB-DUR-02: Public PDF-Tab Duration Synthetic Fixture Creation"

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    assert res["ok"] is True
    assert res["active_task"]["task"] == "PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture"
    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"
    assert run_git(local_prod, ["branch", "--show-current"]) == "agy/pdftab-duration-extraction-architecture"


def test_case_2_fetch_succeeds_but_old_working_tree_task_differs(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    run_git(local_ops, ["checkout", "-b", "agy/old-task-branch"])

    task_v2 = """# Active Task

**Task**: PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-extraction-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_v2)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Promote task 2"])
    run_git(init_ops, ["push", "origin", "main"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    assert res["active_task"]["task"] == "PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture"
    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"


def test_case_3_agentops_and_product_both_behind(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]
    init_prod = temp_git_repos["init_product"]

    (init_ops / "README.md").write_text("Ops update")
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "ops commit"])
    run_git(init_ops, ["push", "origin", "main"])

    (init_prod / "PRODUCT.md").write_text("Prod update")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "prod commit"])
    run_git(init_prod, ["push", "origin", "main"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    ops_sha = run_git(local_ops, ["rev-parse", "main"])
    prod_sha = run_git(local_prod, ["rev-parse", "main"])

    assert ops_sha == run_git(temp_git_repos["bare_agentops"], ["rev-parse", "main"])
    assert prod_sha == run_git(temp_git_repos["bare_product"], ["rev-parse", "main"])


def test_case_4_dirty_worktree_hard_stop(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]

    (local_ops / "dirty.txt").write_text("uncommitted")

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_5_local_main_cannot_fast_forward_hard_stop(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    run_git(local_ops, ["checkout", "main"])

    (local_ops / "local_change.txt").write_text("divergent")
    run_git(local_ops, ["add", "."])
    run_git(local_ops, ["commit", "-m", "divergent local commit"])

    (init_ops / "remote_change.txt").write_text("remote")
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "remote commit"])
    run_git(init_ops, ["push", "origin", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_6_authorised_branch_exists_remotely(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]
    init_prod = temp_git_repos["init_product"]

    task_v2 = """# Active Task

**Task**: PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-extraction-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_v2)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Promote task 2"])
    run_git(init_ops, ["push", "origin", "main"])

    run_git(init_prod, ["checkout", "-b", "agy/pdftab-duration-extraction-architecture"])
    (init_prod / "remote_branch.txt").write_text("remote branch content")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "commit on remote branch"])
    run_git(init_prod, ["push", "origin", "agy/pdftab-duration-extraction-architecture"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"
    assert (local_prod / "remote_branch.txt").exists()


def test_case_7_exact_pr_already_exists_mocked(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]

    pr_branch = "agy/generate-public-pdf-tab-duration-fixture"
    run_git(local_prod, ["checkout", "-b", pr_branch])
    (local_prod / "pr_change.txt").write_text("PR content")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "PR commit"])
    pr_head_sha = run_git(local_prod, ["rev-parse", "HEAD"])
    run_git(local_prod, ["checkout", "main"])

    def mock_gh_runner(repo: str, branch: str) -> dict[str, Any]:
        return {
            "number": 391,
            "state": "OPEN",
            "headRefOid": pr_head_sha,
        }

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
        _gh_runner=mock_gh_runner,
    )
    assert res["state"] == "AWAITING_GOVERNANCE_REVIEW"
    assert res["pr_number"] == 391
    assert res["output_sha"] == pr_head_sha


def test_case_8_merged_old_task_plus_merged_new_governance_promotion(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    task_v2 = """# Active Task

**Task**: PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-extraction-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_v2)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Promote task 2"])
    run_git(init_ops, ["push", "origin", "main"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    assert res["active_task"]["task"] == "PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture"
    assert res["state"] == "EXECUTE_PROMPT"


def test_case_9_repository_field_selects_agentops(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    task_ops = """# Active Task

**Task**: GOV-01: Governance Task
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/gov-01`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0001-gov-task.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_ops)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Gov task"])
    run_git(init_ops, ["push", "origin", "main"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
    )

    assert res["output_repo"] == "tticom/score2gp-agentops"
    assert res["selected_branch"] == "agy/gov-01"


def test_case_10_missing_or_malformed_required_fields_fail_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    task_bad = """# Active Task

**Task**: Broken Task
**Status**: APPROVED
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_bad)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Bad task"])
    run_git(init_ops, ["push", "origin", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_11_wrong_user_identity_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=False,
            _allow_custom_slug=True,
        )


def test_case_12_wrong_assigned_identity_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    task_codex = """# Active Task

**Task**: CODEX-TASK-01: Review Task
**Status**: APPROVED
**Assigned Identity**: tticom-codex
**Authorised Role**: Reviewer
**Repository**: tticom/score2gp
**PR Branch**: `codex/review-01`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0001-review.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_codex)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Codex assigned task"])
    run_git(init_ops, ["push", "origin", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_13_wrong_repository_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    task_unknown_repo = """# Active Task

**Task**: UNKNOWN-REPO-01: Unknown Repo Task
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/unknown-repository
**PR Branch**: `agy/unknown-01`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0001-unknown.md`
"""
    (init_ops / "projects/score2gp/ACTIVE_TASK.md").write_text(task_unknown_repo)
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "Unknown repo task"])
    run_git(init_ops, ["push", "origin", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=False,
        )


def test_case_14_divergent_existing_local_branch_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_prod = temp_git_repos["init_product"]

    (init_prod / "remote_file.txt").write_text("remote main commit")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "Remote main commit"])
    run_git(init_prod, ["push", "origin", "main"])

    run_git(local_prod, ["checkout", "-b", "agy/generate-public-pdf-tab-duration-fixture"])
    (local_prod / "divergent_file.txt").write_text("divergent branch content")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "Divergent branch commit"])

    run_git(local_prod, ["checkout", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_15_local_branch_ahead_of_open_pr_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]

    pr_branch = "agy/generate-public-pdf-tab-duration-fixture"
    run_git(local_prod, ["checkout", "-b", pr_branch])
    (local_prod / "base_change.txt").write_text("Base commit")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "Base commit"])
    base_sha = run_git(local_prod, ["rev-parse", "HEAD"])

    # Create unpushed local commit ahead of PR head
    (local_prod / "unpushed_change.txt").write_text("Unpushed commit")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "Unpushed commit"])
    run_git(local_prod, ["checkout", "main"])

    def mock_gh_runner(repo: str, branch: str) -> dict[str, Any]:
        return {
            "number": 391,
            "state": "OPEN",
            "headRefOid": base_sha, # PR head is at base_sha, but local branch is 1 commit ahead
        }

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
            _gh_runner=mock_gh_runner,
        )


def test_case_16_local_branch_ahead_of_remote_branch_no_pr_fails_closed(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_prod = temp_git_repos["init_product"]

    pr_branch = "agy/generate-public-pdf-tab-duration-fixture"
    run_git(init_prod, ["checkout", "-b", pr_branch])
    (init_prod / "remote_change.txt").write_text("Remote commit")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "Remote commit"])
    run_git(init_prod, ["push", "origin", pr_branch])

    run_git(local_prod, ["fetch", "origin"])
    run_git(local_prod, ["checkout", "-b", pr_branch, f"origin/{pr_branch}"])
    (local_prod / "unpushed_change.txt").write_text("Unpushed commit")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "Unpushed local commit"])
    run_git(local_prod, ["checkout", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            _skip_identity_check=True,
            _allow_custom_slug=True,
        )


def test_case_17_github_permission_error_fails_closed(monkeypatch: pytest.MonkeyPatch, temp_git_repos: dict[str, Path]) -> None:
    # Test query_github_pr_state with permission/auth error stderr
    class MockCompletedProcess:
        def __init__(self, returncode: int, stderr: str):
            self.returncode = returncode
            self.stderr = stderr
            self.stdout = ""

    def mock_run(args: list[str], **kwargs: Any) -> MockCompletedProcess:
        if "gh" in args:
            return MockCompletedProcess(1, "gh: Could not resolve to a repository: tticom/score2gp. Not found or permission denied.")
        return subprocess.run(args, **kwargs)

    monkeypatch.setattr(subprocess, "run", mock_run)

    with pytest.raises(SystemExit):
        query_github_pr_state("tticom/score2gp", "agy/test-branch")


def test_case_18_exact_recognised_no_pr_returns_none() -> None:
    # gh pr list represents the expected no-PR state as an empty JSON list.
    class MockCompletedProcess:
        def __init__(self, returncode: int, stderr: str, stdout: str = ""):
            self.returncode = returncode
            self.stderr = stderr
            self.stdout = stdout

    def mock_run(args: list[str], **kwargs: Any) -> MockCompletedProcess:
        if "gh" in args:
            return MockCompletedProcess(0, "", "[]")
        return subprocess.run(args, **kwargs)

    import pytest
    import scripts.score2gp_go_bootstrap as helper
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(subprocess, "run", mock_run)

    res = helper.query_github_pr_state("tticom/score2gp", "agy/test-branch")
    assert res is None
    monkeypatch.undo()


def test_no_pr_lookup_uses_exact_head_and_all_states(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []

    class MockCompletedProcess:
        returncode = 0
        stderr = ""
        stdout = "[]"

    def mock_run(args: list[str], **kwargs: Any) -> MockCompletedProcess:
        captured.extend(args)
        return MockCompletedProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert query_github_pr_state("tticom/score2gp", "agy/new-task") is None
    assert captured[:3] == ["gh", "pr", "list"]
    assert captured[captured.index("--head") + 1] == "agy/new-task"
    assert captured[captured.index("--state") + 1] == "all"


def test_reused_branch_selects_unique_open_pr(monkeypatch: pytest.MonkeyPatch) -> None:
    class MockCompletedProcess:
        returncode = 0
        stderr = ""
        stdout = (
            '[{"number":1,"state":"CLOSED","headRefOid":"a"},'
            '{"number":2,"state":"OPEN","headRefOid":"b"}]'
        )

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockCompletedProcess())
    result = query_github_pr_state("tticom/score2gp", "agy/reused-task")

    assert result == {"number": 2, "state": "OPEN", "headRefOid": "b"}


def test_case_19_latest_current_head_changes_requested_governs(
    temp_git_repos: dict[str, Path],
) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    branch = "agy/generate-public-pdf-tab-duration-fixture"
    run_git(local_prod, ["checkout", "-b", branch])
    (local_prod / "reviewed.txt").write_text("reviewed")
    run_git(local_prod, ["add", "."])
    run_git(local_prod, ["commit", "-m", "reviewed"])
    head = run_git(local_prod, ["rev-parse", "HEAD"])
    run_git(local_prod, ["checkout", "main"])

    def runner(repo: str, selected_branch: str) -> dict[str, Any]:
        assert selected_branch == branch
        return {
            "number": 393,
            "state": "OPEN",
            "headRefOid": head,
            "reviews": [
                {
                    "id": 10,
                    "state": "APPROVED",
                    "commit_id": head,
                    "submitted_at": "2026-07-28T18:40:00Z",
                    "user": {"login": "tticomgov-code"},
                },
                {
                    "id": 11,
                    "state": "CHANGES_REQUESTED",
                    "commit_id": head,
                    "submitted_at": "2026-07-28T18:45:00Z",
                    "user": {"login": "tticomgov-code"},
                },
            ],
        }

    result = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        _skip_identity_check=True,
        _allow_custom_slug=True,
        _gh_runner=runner,
    )
    assert result["state"] == "ADDRESS_CURRENT_PR_REVIEW"
    assert result["current_review"]["id"] == 11
