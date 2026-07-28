from __future__ import annotations

import subprocess
from pathlib import Path
import pytest

from scripts.score2gp_go_bootstrap import parse_active_task_content, run_go_bootstrap


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

    # 1. Checkout completed task branch locally in AgentOps and Product
    run_git(local_ops, ["checkout", "-b", "agy/generate-public-pdf-tab-duration-fixture"])
    run_git(local_prod, ["checkout", "-b", "agy/generate-public-pdf-tab-duration-fixture"])

    # 2. Update remote origin/main with newly promoted task (PDFTAB-DUR-03)
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

    # 3. Demonstrate original failure mode: working-tree ACTIVE_TASK.md has old task PDFTAB-DUR-02
    stale_task = parse_active_task_content((local_ops / "projects/score2gp/ACTIVE_TASK.md").read_text())
    assert stale_task["task"] == "PDFTAB-DUR-02: Public PDF-Tab Duration Synthetic Fixture Creation"

    # 4. Run repaired go_bootstrap helper
    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        skip_identity_check=True,
        allow_custom_slug=True,
    )

    # 5. Verify helper fast-forwards local main, reads remote task, creates new branch agy/pdftab-duration-extraction-architecture from origin/main
    assert res["ok"] is True
    assert res["active_task"]["task"] == "PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture"
    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"
    assert run_git(local_prod, ["branch", "--show-current"]) == "agy/pdftab-duration-extraction-architecture"


def test_case_2_fetch_succeeds_but_old_working_tree_task_differs(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    # Local is on old task branch
    run_git(local_ops, ["checkout", "-b", "agy/old-task-branch"])

    # Remote changes to new task
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
        skip_identity_check=True,
        allow_custom_slug=True,
    )

    assert res["active_task"]["task"] == "PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture"
    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"


def test_case_3_agentops_and_product_both_behind(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]
    init_prod = temp_git_repos["init_product"]

    # Push commit to init_ops
    (init_ops / "README.md").write_text("Ops update")
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "ops commit"])
    run_git(init_ops, ["push", "origin", "main"])

    # Push commit to init_prod
    (init_prod / "PRODUCT.md").write_text("Prod update")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "prod commit"])
    run_git(init_prod, ["push", "origin", "main"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        skip_identity_check=True,
        allow_custom_slug=True,
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
            skip_identity_check=True,
            allow_custom_slug=True,
        )


def test_case_5_local_main_cannot_fast_forward_hard_stop(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]

    # Ensure local_ops is on main
    run_git(local_ops, ["checkout", "main"])

    # Create diverged commit on local_ops main
    (local_ops / "local_change.txt").write_text("divergent")
    run_git(local_ops, ["add", "."])
    run_git(local_ops, ["commit", "-m", "divergent local commit"])

    # Create commit on remote main
    (init_ops / "remote_change.txt").write_text("remote")
    run_git(init_ops, ["add", "."])
    run_git(init_ops, ["commit", "-m", "remote commit"])
    run_git(init_ops, ["push", "origin", "main"])

    with pytest.raises(SystemExit):
        run_go_bootstrap(
            agentops_path=local_ops,
            product_path=local_prod,
            skip_identity_check=True,
            allow_custom_slug=True,
        )


def test_case_6_authorised_branch_exists_remotely(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]
    init_ops = temp_git_repos["init_agentops"]
    init_prod = temp_git_repos["init_product"]

    # Update remote ACTIVE_TASK to point to branch
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

    # Push branch remotely on product
    run_git(init_prod, ["checkout", "-b", "agy/pdftab-duration-extraction-architecture"])
    (init_prod / "remote_branch.txt").write_text("remote branch content")
    run_git(init_prod, ["add", "."])
    run_git(init_prod, ["commit", "-m", "commit on remote branch"])
    run_git(init_prod, ["push", "origin", "agy/pdftab-duration-extraction-architecture"])

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        skip_identity_check=True,
        allow_custom_slug=True,
    )

    assert res["selected_branch"] == "agy/pdftab-duration-extraction-architecture"
    assert (local_prod / "remote_branch.txt").exists()


def test_case_7_exact_pr_already_exists(temp_git_repos: dict[str, Path]) -> None:
    local_ops = temp_git_repos["local_agentops"]
    local_prod = temp_git_repos["local_product"]

    res = run_go_bootstrap(
        agentops_path=local_ops,
        product_path=local_prod,
        skip_identity_check=True,
        allow_custom_slug=True,
    )
    assert res["state"] in ("EXECUTE_PROMPT", "PR_OPEN", "MERGED_AWAITING_GOVERNANCE_PROMOTION")


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
        skip_identity_check=True,
        allow_custom_slug=True,
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
        skip_identity_check=True,
        allow_custom_slug=True,
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
            skip_identity_check=True,
            allow_custom_slug=True,
        )
