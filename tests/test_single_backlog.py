"""PLAN-01: the task authority is the single, machine-validated backlog."""
from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path

import pytest

from scripts import score2gp_orca_control as orca

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "projects/score2gp/ORCHESTRATION_STATE.json"
REGISTER = ROOT / "projects/score2gp/requirements/README.md"
REQUIREMENT_ORDER = ["PROPOSED", "RESEARCHED", "ACCEPTED", "PLANNED", "IN_DELIVERY", "VERIFIED"]


def authority() -> dict:
    return json.loads(AUTHORITY_PATH.read_text(encoding="utf-8"))


def backlog_item(iid: str, status: str = "READY", depends_on: list[str] | None = None, **extra) -> dict:
    return {"id": iid, "title": iid, "requirements": ["REQ-0001"], "kind": "implementation", "repository": "tticom/x",
            "status": status, "priority": 1, "depends_on": depends_on or [], "notes": "", **extra}


def synthetic(*items: dict) -> dict:
    a = authority()
    a["backlog"] = list(items)
    return a


# --- schema, dependencies and the ready frontier -------------------------------------------------

def test_the_live_authority_backlog_is_valid_and_has_a_ready_frontier() -> None:
    a = authority()
    orca.validate_authority(a)
    assert a["backlog"], "the authority must hold the backlog"
    assert orca.ready_frontier(a), "a planned backlog must have promotable work"


@pytest.mark.parametrize("mutate, message", [
    (lambda i: i.pop("priority"), "fields missing"),
    (lambda i: i.update(kind="chore"), "unsupported kind"),
    (lambda i: i.update(status="SOMEDAY"), "unsupported status"),
    (lambda i: i.update(priority=0), "positive integer"),
    (lambda i: i.update(priority=True), "positive integer"),
    (lambda i: i.update(requirements=[]), "at least one requirement"),
    (lambda i: i.update(depends_on="X"), "must be a list"),
    (lambda i: i.update(depends_on=[7]), "must be a list of IDs"),
    (lambda i: i.update(title=42), "title must be"),              # review 5322160552
    (lambda i: i.update(title="  "), "title must be"),
    (lambda i: i.update(repository=None), "owner/name"),          # review 5322160552
    (lambda i: i.update(repository="score2gp"), "owner/name"),
    (lambda i: i.update(notes=[]), "notes must be"),               # review 5322160552
    (lambda i: i.update(requirements=["REQ-1"]), "unknown requirement reference"),
    (lambda i: i.update(requirements=["REQ-0001:U15"]), "unknown requirement reference"),
    (lambda i: i.update(requirements=["control-plane:anything"]), "unknown requirement reference"),
])
def test_malformed_backlog_items_are_rejected(mutate, message) -> None:
    bad = backlog_item("A")
    mutate(bad)
    with pytest.raises(orca.ControlError, match=message):
        orca.validate_backlog(synthetic(bad))


def test_an_unregistered_requirement_is_rejected_against_the_register() -> None:
    # Review 5322160552: requirements=["REQ-9999"] must not pass.
    known = orca.register_requirement_ids(AUTHORITY_PATH)
    assert known >= {"REQ-0001", "REQ-0005"}
    item = backlog_item("A", requirements=["REQ-9999"])
    orca.validate_backlog(synthetic(item))  # well-formed on its own ...
    with pytest.raises(orca.ControlError, match="unregistered requirement REQ-9999"):
        orca.validate_backlog(synthetic(item), known)  # ... but not a registered requirement


def test_the_live_backlog_cites_only_registered_requirements() -> None:
    orca.validate_backlog(authority(), orca.register_requirement_ids(AUTHORITY_PATH))


def test_duplicate_ids_are_rejected_including_collisions_with_known_tasks() -> None:
    with pytest.raises(orca.ControlError, match="duplicated"):
        orca.validate_backlog(synthetic(backlog_item("A"), backlog_item("A")))
    with pytest.raises(orca.ControlError, match="duplicated"):
        orca.validate_backlog(synthetic(backlog_item(authority()["task"]["id"])))


def test_unknown_dependencies_and_cycles_are_rejected() -> None:
    with pytest.raises(orca.ControlError, match="unknown item"):
        orca.validate_backlog(synthetic(backlog_item("A", depends_on=["NOPE"])))
    with pytest.raises(orca.ControlError, match="cycle"):
        orca.validate_backlog(synthetic(backlog_item("A", depends_on=["B"]), backlog_item("B", depends_on=["C"]),
                                        backlog_item("C", depends_on=["A"])))


def test_the_ready_frontier_is_ready_items_whose_dependencies_are_terminal_in_priority_order() -> None:
    done_task = authority()["completed_tasks"][0]["id"]
    items = [
        backlog_item("DONE-1", status="DONE"),
        backlog_item("R-LATE", depends_on=["DONE-1"], priority=5),
        backlog_item("R-EARLY", depends_on=[done_task], priority=2),
        backlog_item("R-BLOCKED", depends_on=["WAIT"]),
        backlog_item("WAIT", status="NEEDS_DETAIL"),
        backlog_item("IDEA-1", status="IDEA"),
    ]
    assert [i["id"] for i in orca.ready_frontier(synthetic(*items))] == ["R-EARLY", "R-LATE"]


# --- requirement traceability -----------------------------------------------------------------------

def register() -> dict[str, str]:
    rows = re.findall(r"^\| (REQ-\d{4}) \| [^|]+ \| `([A-Z_]+)` \|", REGISTER.read_text(encoding="utf-8"), re.M)
    assert rows, "the requirements register must list requirements"
    return dict(rows)


def cited_requirements(a: dict) -> set[str]:
    cited: set[str] = set()
    for item in [*a.get("backlog", []), a.get("task") or {}, *a.get("queued_task_proposals", [])]:
        for ref in item.get("requirements", []):
            cited.add(str(ref).split(":")[0])
    return cited


def test_every_requirement_below_verified_is_delivered_by_at_least_one_item() -> None:
    cited = cited_requirements(authority())
    open_reqs = [r for r, status in register().items() if status != "VERIFIED"]
    assert [r for r in open_reqs if r not in cited] == []


def test_every_requirement_below_accepted_has_a_research_task_with_a_prompt() -> None:
    a = authority()
    by_id = {i["id"]: i for i in a["backlog"]}
    for req, status in register().items():
        if REQUIREMENT_ORDER.index(status) >= REQUIREMENT_ORDER.index("ACCEPTED"):
            continue
        research = by_id.get(f"RES-{req}")
        assert research and research["kind"] == "research", f"{req} ({status}) needs RES-{req}"
        prompt = re.search(r"prompts/next/res-[\w.-]+\.md", research["notes"])
        assert prompt and (ROOT / "projects/score2gp" / prompt.group(0)).is_file(), f"RES-{req} needs a prompt file"


def test_negative_control_a_requirement_without_items_is_detected() -> None:
    a = authority()
    a["backlog"] = [i for i in a["backlog"] if "REQ-0004" not in i["requirements"]]
    assert "REQ-0004" not in cited_requirements(a)


# --- one backlog: the search oracle ---------------------------------------------------------------

# Known alternative backlog files and headings from earlier methods: always a violation outside the exempt classes.
LEGACY_QUEUE = re.compile(r"PLANNING_DATA|backlog\.yaml|Approved Task Queue")
# Any planning-container wording. A line that uses it must also refer to the task authority, so that a
# new, differently worded queue claim ("this document is the product backlog", "add the next task to a
# separate planning queue") fails however it is phrased.
CONTAINER = re.compile(r"\b(backlogs?|queues?|queued|queueing|task[- ]lists?|to-?do[- ]lists?|work[- ]lists?|planning (?:file|document|data))\b", re.I)
AUTHORITY_REFERENCE = re.compile(r"\bauthority\b|ORCHESTRATION_STATE|next_task_proposal|queued_task_proposals|ready_frontier", re.I)
# Queues that are product features or GitHub mechanisms, not task queues.
NON_TASK_QUEUE = re.compile(r"\b(?:job|cloud|message|merge|conversion job) queue\b", re.I)


def claims_a_queue(line: str) -> bool:
    if LEGACY_QUEUE.search(line):
        return True
    return bool(CONTAINER.search(NON_TASK_QUEUE.sub("", line))) and not AUTHORITY_REFERENCE.search(line)


EXEMPT_CLASSES = {
    # (a) dated record directories: they describe past state and never instruct.
    "a": re.compile(r"^projects/score2gp/(runs|reviews|research|reports|decisions|handoffs|archive|audits)/"),
    # (b, numbered) legacy prompts from before the authority existed.
    "b": re.compile(r"^projects/score2gp/prompts/next/[0-9]{4}-[^/]*\.md$"),
    # (c) dated cycle-preparation history.
    "c": re.compile(r"^docs/cycle-preparation-history/"),
    # (d) by name: prompts that name the superseded sources in order to retire them.
    "d": re.compile(r"^projects/score2gp/prompts/next/(plan-01-single-coherent-backlog|gov-03-active-task-pr-discovery)\.md$"),
    # (e) by name: the authority, its generated view and this oracle (it must contain the patterns).
    "e": re.compile(r"^(projects/score2gp/ORCHESTRATION_STATE\.json|projects/score2gp/ACTIVE_TASK\.md|tests/test_single_backlog\.py)$"),
}


def completed_task_prompts(a: dict) -> set[str]:
    return {t["prompt"] for t in a.get("completed_tasks", []) if t.get("prompt")}


def queue_claim_violations(files: dict[str, str], a: dict) -> list[str]:
    completed = completed_task_prompts(a)  # (b, completed) prompts of tasks in completed_tasks
    return sorted(path for path, text in files.items()
                  if path not in completed and not any(rx.search(path) for rx in EXEMPT_CLASSES.values())
                  and any(claims_a_queue(line) for line in text.splitlines()))


def tracked_text_files() -> dict[str, str]:
    paths = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    files = {}
    for path in paths:
        try:
            files[path] = (ROOT / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
    return files


def test_no_live_file_directs_work_into_a_queue_other_than_the_authority() -> None:
    assert queue_claim_violations(tracked_text_files(), authority()) == []


@pytest.mark.parametrize("path", [
    "projects/score2gp/new-plan.md",                 # a new live file
    "projects/score2gp/runs-summary.md",             # beside class (a), not inside it
    "projects/score2gp/prompts/next/l3-02-first-system.md",  # a live prompt that is not exempt
    "docs/cycle-preparation.md",                     # parent of class (c), not inside it
])
def test_negative_control_a_new_queue_claim_outside_the_exempt_classes_fails(path) -> None:
    assert queue_claim_violations({path: "Tasks are queued in PLANNING_DATA.md."}, authority()) == [path]


@pytest.mark.parametrize("text", [
    "This document is the product backlog.",                       # review 5322160552
    "Add the next task to a separate planning queue.",             # review 5322160552
    "Keep a running to-do list in NOTES.md and work from it.",
    "Work items are tracked in the sprint task list below.",
    "Our work-list lives in the wiki.",
    "Record new ideas in this planning document.",
    "Pending tasks are queued here until someone picks them up.",
])
def test_negative_control_differently_worded_queue_claims_fail(text) -> None:
    assert queue_claim_violations({"projects/score2gp/new-plan.md": text}, authority()) == ["projects/score2gp/new-plan.md"]


@pytest.mark.parametrize("text", [
    "Promote the next item from the task authority's backlog.",
    "The backlog in ORCHESTRATION_STATE.json is the only planned-work record.",
    "Implement an async conversion job queue for the cloud service.",
])
def test_references_to_the_authority_and_product_queues_are_not_claims(text) -> None:
    assert queue_claim_violations({"projects/score2gp/new-plan.md": text}, authority()) == []


# --- the dispatcher's resolution is unchanged by the backlog --------------------------------------

def test_dispatcher_resolution_of_the_current_task_is_unchanged_by_the_backlog() -> None:
    with_backlog = authority()
    without = copy.deepcopy(with_backlog)
    without.pop("backlog")
    assert orca.resolve_state(with_backlog, {}) == orca.resolve_state(without, {})
