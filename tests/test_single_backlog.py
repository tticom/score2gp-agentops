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


def test_the_authority_record_of_registered_requirements_matches_the_register() -> None:
    assert orca.registered_requirements(authority()) == orca.register_requirement_ids(AUTHORITY_PATH)


def test_the_normal_authority_path_rejects_an_unregistered_requirement() -> None:
    # Review 5322962856: validate_authority itself, not only the frontier command, must refuse REQ-9999.
    a = authority()
    a["backlog"].append(backlog_item("NEW-1", requirements=["REQ-9999"]))
    with pytest.raises(orca.ControlError, match="unregistered requirement REQ-9999"):
        orca.validate_authority(a)


def _paired_mutation_copy(tmp_path: Path, register_row: bool) -> Path:
    """A copy of the authority whose backlog and registered_requirements both gain REQ-9999."""
    a = authority()
    a["registered_requirements"].append("REQ-9999")
    a["backlog"].append(backlog_item("NEW-1", requirements=["REQ-9999"]))
    path = tmp_path / "ORCHESTRATION_STATE.json"
    path.write_text(json.dumps(a), encoding="utf-8")
    (tmp_path / "requirements").mkdir()
    register = (AUTHORITY_PATH.parent / "requirements" / "README.md").read_text(encoding="utf-8")
    if register_row:
        register += "\n| REQ-9999 | Test requirement | `PROPOSED` | test | none |\n"
    (tmp_path / "requirements" / "README.md").write_text(register, encoding="utf-8")
    return path


def test_the_loading_boundary_rejects_a_snapshot_edited_without_the_register(tmp_path: Path) -> None:
    # Review 5323059011: editing registered_requirements alongside the citation must not legitimise it.
    from scripts import score2gp_orchestrator as orchestrator

    path = _paired_mutation_copy(tmp_path, register_row=False)
    orca.validate_authority(json.loads(path.read_text(encoding="utf-8")))  # the snapshot alone is self-consistent
    with pytest.raises(orca.ControlError, match="differs from the requirements register"):
        orca.load_json(path)
    with pytest.raises(orchestrator.OrchestrationError, match="differs from the requirements register"):
        orchestrator.load_authority(path)


def test_the_loading_boundary_accepts_a_requirement_added_to_the_register(tmp_path: Path) -> None:
    from scripts import score2gp_orchestrator as orchestrator

    path = _paired_mutation_copy(tmp_path, register_row=True)
    assert orca.load_json(path)["registered_requirements"][-1] == "REQ-9999"
    assert orchestrator.load_authority(path)["backlog"][-1]["id"] == "NEW-1"


def test_the_normal_authority_path_refuses_a_backlog_without_its_register_record() -> None:
    a = authority()
    a.pop("registered_requirements")
    with pytest.raises(orca.ControlError, match="registered_requirements"):
        orca.validate_authority(a)


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
CONTAINER = re.compile(r"\b(backlogs?|queues?|queued|queueing|task[- ]lists?|to-?do[- ]lists?|work[- ]lists?|planning (?:files?|documents?|data))\b", re.I)
AUTHORITY_REFERENCE = re.compile(r"\bauthority\b|ORCHESTRATION_STATE|next_task_proposal|queued_task_proposals|ready_frontier", re.I)
# Queues that are product features or GitHub mechanisms, not task queues.
NON_TASK_QUEUE = re.compile(r"\b(?:job|cloud|message|merge|conversion job) queue\b", re.I)


# A qualifier naming an alternative container is a claim even when the authority is also mentioned:
# "keep a separate team backlog", "another queue".
ALTERNATIVE_CONTAINER = re.compile(
    r"\b(?:separate|another|second|additional|parallel|private|personal|team|own|extra|shadow|local)\s+(?:[\w-]+\s+){0,2}"
    r"(?:backlogs?|queues?|task[- ]lists?|to-?do[- ]lists?|work[- ]lists?)\b", re.I)
# Every container mention must be *bound* to the task authority by a closed grammar. Nothing else
# binds: not proximity, not a conjunction, not free words between the authority and the container.
#   before:  the authority's [single|non-executable|light|unpromoted]{0,2} backlog | authority backlog
#            authority.get("backlog") | authority['backlog']
#   after:   backlog [`] [field|item|items] in|of|within [the] task authority | ORCHESTRATION_STATE.json
AUTHORITY_TERM = r"(?:task\s+)?authority|`?ORCHESTRATION_STATE(?:\.json)?`?"
MODIFIER = r"(?:single|non-executable|light|unpromoted)"
BOUND_BEFORE = re.compile(r"(?<![\w-])(?:" + AUTHORITY_TERM + r")(?:'s\s+(?:" + MODIFIER + r"\s+){0,2}|\s+)`{0,2}$", re.I)
BOUND_CODE = re.compile(r"\bauthority(?:\.get\(|\[)[\"']$")
BOUND_AFTER = re.compile(
    r"^`{0,2}(?:\s+(?:field|items?))?\s+(?:in|of|within)\s+(?:the\s+)?"
    r"(?:(?:task\s+)?authority\b|`?(?:projects/score2gp/)?ORCHESTRATION_STATE\.json`?)", re.I)


def _bound_to_authority(text: str, match: re.Match) -> bool:
    before, after = text[max(0, match.start() - 80):match.start()], text[match.end():match.end() + 80]
    return bool(BOUND_BEFORE.search(before) or BOUND_CODE.search(before) or BOUND_AFTER.search(after))


def claims_a_queue(line: str) -> bool:
    if LEGACY_QUEUE.search(line):
        return True
    text = NON_TASK_QUEUE.sub("", line)
    if ALTERNATIVE_CONTAINER.search(text):
        return True
    return any(not _bound_to_authority(text, m) for m in CONTAINER.finditer(text))


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
    # Review 5322962856: an authority mention elsewhere on the line must not excuse a second backlog.
    "Keep a separate team backlog in NOTES.md; task authority stays in ORCHESTRATION_STATE.json.",
    "Track fixes in our own queue beside the task authority.",
    "The task authority is canonical - but log ideas in the planning document too.",
    # Review 5323059011: a conjunction instead of a separator must not help.
    "Keep a backlog for urgent tasks in NOTES.md while the task authority tracks routine work.",
    "Use a backlog beside the task authority for quick fixes.",
    # A field name is not bound by its backticks alone, and a plural planning file is still one.
    "Keep a `backlog` in NOTES.md.",
    "Record ideas in the planning files as well as the authority.",
    # Review 5323357360: free words between the authority and the container must not bind it.
    "Keep the task authority and a backlog for urgent tasks in NOTES.md.",
    "Use ORCHESTRATION_STATE.json plus a queue in NOTES.md.",
    "The authority's rival backlog lives in NOTES.md.",
    "The backlog is separate from the task authority.",
    "Keep a backlog outside of the authority.",
    "Keep a backlog in the authority and a queue in NOTES.md.",
    "notes.get(\"backlog\")",
    "The authority holds routine items and a queue in SLACK.md holds the rest.",
])
def test_negative_control_differently_worded_queue_claims_fail(text) -> None:
    assert queue_claim_violations({"projects/score2gp/new-plan.md": text}, authority()) == ["projects/score2gp/new-plan.md"]


@pytest.mark.parametrize("text", [
    "Promote the next item from the task authority's backlog.",
    "The backlog in ORCHESTRATION_STATE.json is the only planned-work record.",
    "Record it as an authority backlog item.",
    "The task authority's non-executable `backlog` holds unpromoted work.",
    "Backlog items in `ORCHESTRATION_STATE.json` are not executable.",
    "Items not yet detailed live in the authority's `backlog` field.",
    "items = authority.get(\"backlog\", [])",
    "print(authority['backlog'])",
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
