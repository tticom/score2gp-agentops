"""PLAN-01: the task authority is the single, machine-validated backlog."""
from __future__ import annotations

import copy
from collections import Counter
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
# Separators are optional ("tasklist", "work-list", "to do list"), every inflection of queue counts
# ("queuing", "enqueue"), and a bare "todo" (TODO.md) counts. A bare "to do" is ordinary English and does not.
SEP = "[-‐-― ]"  # ASCII hyphen, Unicode hyphens and dashes, or a space
CONTAINER_WORDS = (r"backlog(?:s|ged|ging)?|(?:en|de|re)?queu(?:e|es|ed|eing|ing)"
                   rf"|(?:task|work|to{SEP}?do|wish|punch|issue){SEP}?lists?"
                   rf"|to[-‐-―]?dos?|kanban|icebox|trackers?|sprints?"
                   rf"|work{SEP}?items?|task{SEP}?boards?|planning{SEP}?(?:files?|documents?|data)")
CONTAINER = re.compile(r"\b(" + CONTAINER_WORDS + r")\b", re.I)
AUTHORITY_REFERENCE = re.compile(r"\bauthority\b|ORCHESTRATION_STATE|next_task_proposal|queued_task_proposals|ready_frontier", re.I)
# Queues that are product features or GitHub mechanisms, not task queues.
NON_TASK_QUEUE = re.compile(r"\b(?:job|cloud|message|merge|conversion job) queue\b", re.I)


# A qualifier naming an alternative container is a claim even when the authority is also mentioned:
# "keep a separate team backlog", "another queue".
ALTERNATIVE_CONTAINER = re.compile(
    r"\b(?:separate|another|second|additional|parallel|private|personal|team|own|extra|shadow|local)\s+(?:[\w-]+\s+){0,2}"
    r"(?:" + CONTAINER_WORDS + r")\b", re.I)
# Layer 1, the grammar. Every container mention must be *bound* to the task authority by a closed
# grammar. Nothing else binds: not proximity, not a conjunction, not free words between the authority and
# the container, and not another authority ("merge authority", "review authority").
#   before:  task authority | the/an authority | unqualified authority | ORCHESTRATION_STATE.json, then ['s [single|non-executable|
#            light|unpromoted]{0,2}] backlog;  authority.get("backlog") | authority['backlog']
#   after:   backlog [`] [field|item|items] in|of|within  the task authority | the authority | ORCHESTRATION_STATE.json
# A line that binds a container but also directs it to another location ("the authority's backlog in
# NOTES.md", "copy it into the wiki") is still a claim.
# A bare "authority" binds only where no word qualifies it: at the start of the line, a quote or a bracket.
AUTHORITY_TERM = r"(?:\btask\s+authority|\b(?:the|an)\s+authority|(?:^|[\"'(])\s*authority|`?\bORCHESTRATION_STATE(?:\.json)?`?)"
MODIFIER = r"(?:single|non-executable|light|unpromoted)"
BOUND_BEFORE = re.compile(AUTHORITY_TERM + r"(?:'s\s+(?:" + MODIFIER + r"\s+){0,2}|\s+)`{0,2}$", re.I)
BOUND_CODE = re.compile(r"(?<![\w.-])authority(?:\.get\(|\[)[\"']$")
BOUND_AFTER = re.compile(
    r"^`{0,2}(?:\s+(?:field|items?))?\s+(?:in|of|within)\s+"
    r"(?:(?:the\s+)?task\s+authority\b|the\s+authority\b|`?(?:projects/score2gp/)?ORCHESTRATION_STATE\.json`?)", re.I)
OTHER_LOCATION = re.compile(
    r"\b(?:in|into|on|at|to|from|onto)\s+(?:the\s+|a\s+|an\s+|your\s+|our\s+|my\s+)?"
    r"(?:`?(?![\w./-]*ORCHESTRATION_STATE\.json)[\w./-]+\.(?:md|txt|json|ya?ml|csv|tsv|xlsx?|docx?|org)`?"
    r"|(?:wiki|notes|notebook|slack|spreadsheet|sheet|board|trello|jira|notion)\b)", re.I)


def _bound_to_authority(text: str, match: re.Match) -> bool:
    before, after = text[:match.start()], text[match.end():match.end() + 80]
    return bool(BOUND_BEFORE.search(before) or BOUND_CODE.search(before) or BOUND_AFTER.search(after))


def claims_a_queue(line: str) -> bool:
    if LEGACY_QUEUE.search(line):
        return True
    text = NON_TASK_QUEUE.sub("", line)
    if ALTERNATIVE_CONTAINER.search(text):
        return True
    mentions = list(CONTAINER.finditer(text))
    if any(not _bound_to_authority(text, m) for m in mentions):
        return True
    return bool(mentions) and bool(OTHER_LOCATION.search(text))


# Layer 2, the closed world. A pattern cannot enumerate every English sentence that sends work elsewhere,
# so every live line that mentions a container must also appear, verbatim, in REVIEWED_MENTIONS at the end
# of this file. A new or reworded mention fails until its exact text is added there, which a reviewer sees
# in the PR diff. The list lives in this oracle file because PLAN-01 7.4(e) exempts it by name.


def mention_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if CONTAINER.search(line) or LEGACY_QUEUE.search(line)]


def load_ledger() -> Counter:
    """Reviewed mentions as a multiset of (path, line): each occurrence of a line needs its own entry."""
    return Counter(REVIEWED_MENTIONS)


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


def live_files(files: dict[str, str], a: dict) -> dict[str, str]:
    completed = completed_task_prompts(a)  # (b, completed) prompts of tasks in completed_tasks
    return {path: text for path, text in files.items()
            if path not in completed and not any(rx.search(path) for rx in EXEMPT_CLASSES.values())}


def queue_claim_violations(files: dict[str, str], a: dict, ledger=()) -> list[str]:
    """Live paths with a line the grammar calls a claim, or container mentions that the ledger does not
    list exactly as often as they occur."""
    ledger = Counter(ledger)
    return sorted(path for path, text in live_files(files, a).items()
                  if any(claims_a_queue(line) for line in text.splitlines())
                  or any(ledger[(path, line)] != n for line, n in Counter(mention_lines(text)).items()))


# Only these suffixes may be skipped as binary, and only when their bytes are not text. No tracked file has one.
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".pdf", ".zip", ".gz", ".gp", ".gpx", ".woff", ".woff2"}


def decode_text(path: str, data: bytes) -> str | None:
    """The text of a tracked file, or None for an allow-listed binary.

    Text is NUL-free UTF-8, optionally with a UTF-8 byte-order mark. Every other file raises, whatever its
    byte-order mark (UTF-16/32, a BOM in front of UTF-8 bytes, a UTF-16 file with UTF-8 appended), cp1252
    or an unlisted binary, so a claim cannot drop out of the oracle by its encoding. An allow-listed suffix
    is skipped only when its bytes are not text (reviews 5323510443, 5323539979, 5323582757).
    """
    try:
        if b"\0" in data:
            raise UnicodeDecodeError("utf-8", data, data.index(b"\0"), data.index(b"\0") + 1, "NUL byte")
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        if Path(path).suffix.lower() in BINARY_SUFFIXES:
            return None
        raise UnicodeDecodeError(error.encoding, error.object, error.start, error.end,
                                 f"{path} is not UTF-8 text; save it as UTF-8") from error


def read_text_files(root: Path, paths: list[str]) -> dict[str, str]:
    files = {}
    for path in paths:
        try:
            data = (root / path).read_bytes()
        except (FileNotFoundError, IsADirectoryError):
            continue  # deleted in the worktree, or a submodule: no text to judge
        text = decode_text(path, data)
        if text is not None:
            files[path] = text
    return files


def tracked_text_files() -> dict[str, str]:
    # -z gives raw paths: with core.quotePath a non-ASCII path would be quoted, not found, and skipped.
    listing = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return read_text_files(ROOT, [p for p in listing.decode("utf-8").split("\0") if p])


RIVAL = "Keep the backlog in NOTES.md – new work goes there."


@pytest.mark.parametrize("data", [
    RIVAL.encode("cp1252"),
    RIVAL.encode("utf-16-le"), RIVAL.encode("utf-16-be"), RIVAL.encode("utf-32-le"),   # no byte-order mark
    RIVAL.encode("utf-16"), RIVAL.encode("utf-32"),                                     # with one
    b"\xff\xfe" + b"Keep the backlog in NOTES.md.\n",                                   # review 5323582757: BOM on UTF-8
    RIVAL.encode("utf-16") + "\nKeep the backlog in NOTES.md.\n".encode("utf-8"),        # UTF-16 with UTF-8 appended
    b"\x89PNG\r\n\x1a\n\0\0\0",                                                         # a binary without a listed suffix
], ids=["cp1252", "utf16le", "utf16be", "utf32le", "utf16-bom", "utf32-bom", "bom-on-utf8", "mixed", "unlisted-binary"])
def test_negative_control_a_file_that_is_not_utf8_text_fails_rather_than_being_skipped(tmp_path: Path, data) -> None:
    (tmp_path / "new-plan.md").write_bytes(data)
    with pytest.raises(UnicodeDecodeError, match="not UTF-8 text"):
        read_text_files(tmp_path, ["new-plan.md"])


def test_utf8_with_a_byte_order_mark_is_read_and_judged(tmp_path: Path) -> None:
    (tmp_path / "new-plan.md").write_bytes(RIVAL.encode("utf-8-sig"))
    files = {f"projects/score2gp/{k}": v for k, v in read_text_files(tmp_path, ["new-plan.md"]).items()}
    assert queue_claim_violations(files, authority(), load_ledger()) == ["projects/score2gp/new-plan.md"]


def test_an_allow_listed_suffix_is_skipped_only_when_its_bytes_are_not_text(tmp_path: Path) -> None:
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\0\0\0")
    (tmp_path / "f.PDF").write_bytes(RIVAL.encode("utf-8"))  # review 5323582757 (non-blocking): text named .pdf
    assert read_text_files(tmp_path, ["image.png"]) == {}
    assert read_text_files(tmp_path, ["f.PDF"]) == {"f.PDF": RIVAL}


def test_no_live_file_directs_work_into_a_queue_other_than_the_authority() -> None:
    assert queue_claim_violations(tracked_text_files(), authority(), load_ledger()) == []


def test_every_ledger_entry_is_still_present_verbatim() -> None:
    # A stale entry could later excuse a different line with the same text, so each entry's count must
    # match the tree (exempt files included, so completing a task's prompt does not strand its entries).
    files = tracked_text_files()
    stale = sorted(e for e, n in load_ledger().items() if Counter(mention_lines(files.get(e[0], "")))[e[1]] != n)
    assert stale == []


def test_negative_control_a_listed_line_repeated_in_the_same_file_fails() -> None:
    # Review 5323468082: a listed line copied under a rival heading must need its own entry.
    line = "Promote the next item from the task authority's backlog."
    path = "projects/score2gp/new-plan.md"
    assert queue_claim_violations({path: f"{line}\n## Rival\n{line}\n"}, authority(), {(path, line): 1}) == [path]
    assert queue_claim_violations({path: f"{line}\n## Rival\n{line}\n"}, authority(), {(path, line): 2}) == []


def test_negative_control_a_bound_but_unreviewed_mention_fails() -> None:
    # The grammar accepts this line; only the ledger stops a new, unreviewed mention.
    line = "Promote the next item from the task authority's backlog."
    assert not claims_a_queue(line)
    assert queue_claim_violations({"projects/score2gp/new-plan.md": line}, authority(), load_ledger()) == ["projects/score2gp/new-plan.md"]
    assert queue_claim_violations({"projects/score2gp/new-plan.md": line}, authority(), {("projects/score2gp/new-plan.md", line)}) == []


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
    # Review 5323410769: another authority is not the task authority, and a bound container sent elsewhere is a claim.
    "Keep the merge authority backlog in NOTES.md.",
    "Add new tasks to the review authority's backlog in NOTES.md.",
    "The design authority's backlog in NOTES.md is where new work goes.",
    "Maintain an authority backlog in NOTES.md.",
    "Keep the authority's backlog in NOTES.md from now on.",
    "Copy the task authority's backlog into NOTES.md and work from the copy.",
    "Mirror the backlog of the task authority in NOTES.md and pick tasks from there.",
    "Mirror the task authority's backlog in the wiki.",
    # Review 5323468082: closed-compound spellings, and the other common planning-container words.
    "Add new tasks to the worklist in NOTES.md and work from it.",
    "Keep the tasklist in NOTES.md; it is where new work goes.",
    "Keep a running todolist in NOTES.md and work from it.",
    "Track upcoming work in TODO.md.",
    "New work goes on the kanban.",
    "Park ideas in the icebox.",
    "Use the issue tracker for planned work.",
    "Plan the next sprint here.",
    "Work items are listed below.",
    # Review 5323510443: every inflection of queue, and the open spelling of to-do list.
    "Keep queuing new tasks in NOTES.md and work from them.",
    "Enqueue new tasks in NOTES.md.",
    "Keep a running to do list in NOTES.md and work from it.",
    "Requeue unfinished tasks in NOTES.md.",
    "Anything backlogged goes in NOTES.md.",
    # Review 5323539979 (non-blocking): the remaining inflections and Unicode hyphens.
    "Keep backlogging ideas in NOTES.md.",
    "Dequeue the next task from NOTES.md.",
    "Keep a running to‑do list in NOTES.md.",
    "Track it on the task‐board in NOTES.md.",
])
def test_negative_control_differently_worded_queue_claims_fail(text) -> None:
    # The grammar alone rejects each one, so the ledger is a second layer rather than the only one.
    assert claims_a_queue(text)
    assert queue_claim_violations({"projects/score2gp/new-plan.md": text}, authority(), {("projects/score2gp/new-plan.md", text)}) == [
        "projects/score2gp/new-plan.md"]


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
    assert not claims_a_queue(text)


# --- the dispatcher's resolution is unchanged by the backlog --------------------------------------

def test_dispatcher_resolution_of_the_current_task_is_unchanged_by_the_backlog() -> None:
    with_backlog = authority()
    without = copy.deepcopy(with_backlog)
    without.pop("backlog")
    assert orca.resolve_state(with_backlog, {}) == orca.resolve_state(without, {})


# --- the reviewed mentions (layer 2) ---------------------------------------------------------------------
# Every live line that uses a planning-container word, verbatim, one entry per occurrence. Add an entry only
# after reviewing that the line refers to the task authority (ORCHESTRATION_STATE.json) or to a product or
# GitHub queue, and never to another place for planned work.
REVIEWED_MENTIONS = [
    ('.agents/agents/project-director/agent.json',
     '"content": "At the start of every run, verify live state. Do not trust previous agent summaries unless the repositories confirm them.\\n\\nRun the equivalent of:\\nFrom your governance checkout, on any OS:\\npython scripts/verify_identity.py\\ngit status --short --branch\\ngit fetch --all --prune\\nread projects/score2gp/ACTIVE_TASK.md in full\\nprint the backlog in projects/score2gp/ORCHESTRATION_STATE.json (the task authority)\\npython scripts/score2gp_governance_audit.py\\n\\nThen from the sibling ../score2gp checkout:\\ngit status --short --branch\\ngit fetch --all --prune\\ngit log --oneline --decorate --max-count=8"'),
    ('.agents/agents/project-director/agent.json',
     '"content": "Before ending after a successful task, inspect ACTIVE_TASK.md, the backlog in ORCHESTRATION_STATE.json, recent reports, recent reviews, and current blockers. If an approved next task exists and prerequisites are satisfied, execute it. If no approved next task exists, identify the smallest credible continuation still inside the current product direction. Prefer diagnostic, schema, fixture, reporting, smoke-test, fail-closed, or corpus-audit work over stopping. Create a governance PR to record the continuation and make it active when safe.\\n\\nWhen a task hits a blocker, do not default to stopping. Identify the blocker precisely, decide whether a credible unblocker exists, convert that unblocker into the smallest research, fixture, test, reporting, or feature task, and continue on the appropriate branch. Stop only if every credible pivot would require a new product direction, destructive action, unapproved data source, or speculative musical inference."'),
    ('.agents/skills/score2gp-remediation-governance/SKILL.md',
     "description: Governing E2E PDF-to-GP conversion-failure remediation, whose tasks live in the task authority's backlog. Enforces the ban on synthetic tests, mandates real-world in-situ testing on private fixtures, and governs task promotions for barline inheritance, page indexing, and digit over-merging."),
    ('.agents/skills/score2gp-remediation-governance/SKILL.md',
     "* Load the task authority's backlog (`ORCHESTRATION_STATE.json`, which replaced the retired conversion-recovery programme and M6 planning records) and the director skill."),
    ('.agents/skills/score2gp-report-consolidation/SKILL.md',
     '- Commit and push the consolidated report; record follow-up work as task authority backlog items.'),
    ('AGENT-RULES.md',
     "- Must maintain the task authority's backlog state and dependency graph (`ORCHESTRATION_STATE.json`)."),
    ('README.md',
     "### Single task authority (and the authority's backlog)"),
    ('README.md',
     "- the authority's `backlog` of items not yet detailed enough to promote."),
    ('README.md',
     "Every item cites the requirement it delivers (`projects/score2gp/requirements/`). `scripts/score2gp_orca_control.py` validates the authority's backlog and computes the ready frontier (`ready_frontier`). Governance promotes from that frontier, and `ACTIVE_TASK.md` is the generated view. `tests/test_single_backlog.py` enforces that planned work is recorded only in the task authority."),
    ('projects/prompts/05-project-director.md',
     "projects/score2gp/ORCHESTRATION_STATE.json (the task authority, including the authority's single backlog)"),
    ('projects/prompts/05-project-director.md',
     'python -c "import json; authority = json.load(open(\'projects/score2gp/ORCHESTRATION_STATE.json\', encoding=\'utf-8\')); print(json.dumps(authority[\'backlog\'], indent=1))"'),
    ('projects/score2gp/AGENT_CONTROL.md',
     "Agents must not treat `ACTIVE_TASK.md`, `NEXT.md`, the authority's backlog items,"),
    ('projects/score2gp/AGENT_CONTROL.md',
     "5. `projects/score2gp/ORCHESTRATION_STATE.json` (the task authority; the authority's `backlog` holds planned work)"),
    ('projects/score2gp/AGENT_CONTROL.md',
     "## Unpromoted Work (the task authority's backlog)"),
    ('projects/score2gp/AGENT_CONTROL.md',
     "The task authority's `backlog` is non-executable. The JSON task/incident model is the only authored authority. Agents must not execute an authority backlog item or automatically promote one without Orca Control Plane dispatch."),
    ('projects/score2gp/ORCA_WORKFLOW.md',
     '`ACTIVE_TASK.md`, the `backlog` in `ORCHESTRATION_STATE.json`, and `go/got` prompts.'),
    ('projects/score2gp/ORCA_WORKFLOW.md',
     "the task authority's non-executable `backlog` (done by PLAN-01). Make `go/got` thin compatibility wrappers around this CLI."),
    ('projects/score2gp/README.md',
     "- **Task authority (including the authority's single backlog):** [`ORCHESTRATION_STATE.json`](ORCHESTRATION_STATE.json), with the generated view [`ACTIVE_TASK.md`](ACTIVE_TASK.md)."),
    ('projects/score2gp/TASK_RECORDING_CONVENTION.md',
     "| the authority's `backlog` | Items not yet detailed enough to promote, in the light schema (`id`, `title`, `requirements`, `kind`, `repository`, `status`, `priority`, `depends_on`, `notes`) |"),
    ('projects/score2gp/TASK_RECORDING_CONVENTION.md',
     "`scripts/score2gp_orca_control.py` validates the authority's backlog: schema, unique IDs, known dependencies and no cycles. It also computes the **ready frontier**: items with status `READY` whose dependencies are all terminal, in priority order. Governance promotes from the frontier by converting an item to the full proposal schema. `ACTIVE_TASK.md` is generated from the authority and never edited by hand."),
    ('projects/score2gp/TASK_RECORDING_CONVENTION.md',
     "2. **What to do:** `ORCHESTRATION_STATE.json` (the task, proposals and the authority's backlog)"),
    ('projects/score2gp/plans/2026-08-04-multimodal-audio-score-platform-roadmap.md',
     'Phase 6 : Cloud SaaS Gateway : REST API, URL Processing & Cloud Queue'),
    ('projects/score2gp/plans/2026-08-04-multimodal-audio-score-platform-roadmap.md',
     '- [ ] **TSK-603**: Implement async conversion job queue (`ConversionJob`) and user API key authentication (`ApiKey`).'),
    ('projects/score2gp/plans/2026-08-04-multimodal-audio-score-platform-roadmap.md',
     "Each task is recorded in the task authority's `backlog` (`projects/score2gp/ORCHESTRATION_STATE.json`) and promoted by governance; `ACTIVE_TASK.md` is its generated view. Governance worker (`tticom-gov`) will dispatch tasks through the established identity-aware router:"),
    ('projects/score2gp/plans/2026-09-05-lesson3-native-working-slice.md',
     "(The task authority's `backlog` has since replaced that record.) No feature-branch remote"),
    ('projects/score2gp/prompts/2026-07-19-teamwork-runtime-provenance-functional-stabilisation.md',
     "`ACTIVE_TASK.md`, `ORCHESTRATION_STATE.json` (the task authority and the authority's backlog), and"),
    ('projects/score2gp/prompts/next/res-req-0002-pluggable-gp-output-targets.md',
     '- **Kind:** research (authority backlog item `RES-REQ-0002`; promote to a task before execution)'),
    ('projects/score2gp/prompts/next/res-req-0003-dependency-licence-compatibility.md',
     '- **Kind:** research (authority backlog item `RES-REQ-0003`; promote to a task before execution)'),
    ('projects/score2gp/prompts/next/res-req-0003-dependency-licence-compatibility.md',
     '4. **Status proposal.** Recommend `ACCEPTED`, with the chosen direction left to the maintainer as a decision (authority backlog item DEC-04).'),
    ('projects/score2gp/prompts/next/res-req-0005-explained-shortfall-reporting.md',
     '- **Kind:** research (authority backlog item `RES-REQ-0005`; promote to a task before execution)'),
    ('projects/score2gp/requirements/README.md',
     "| `PLANNED` | The task authority's backlog (`ORCHESTRATION_STATE.json`) holds its tasks, with dependencies | Task IDs listed in the record |"),
    ('projects/score2gp/requirements/REQ-0002-pluggable-gp-output-targets.md',
     "## 11. Proposed tasks (recorded in the task authority's backlog; not promoted)"),
    ('projects/score2gp/requirements/REQ-0004-conversion-runtime-provenance.md',
     '- **Task authority backlog item:** PROV-01'),
    ('projects/score2gp/requirements/REQ-0005-explained-shortfall-reporting.md',
     "4. **Learning over time.** Shortfall records are kept and aggregated across runs and sources, so the most frequent and most costly reasons become visible and drive the task authority's backlog."),
    ('projects/score2gp/skills/conversion-recovery-director/SKILL.md',
     "3. the task authority's `backlog` in ORCHESTRATION_STATE.json (it replaced the recovery file retired by PLAN-01);"),
    ('projects/score2gp/skills/developer/SKILL.md',
     'not read the authority backlog to select work, promote a successor, reinterpret an incident,'),
    ('projects/score2gp/skills/project-director/SKILL.md',
     'python -c "import json; authority = json.load(open(\'projects/score2gp/ORCHESTRATION_STATE.json\', encoding=\'utf-8\')); print(json.dumps(authority[\'backlog\'], indent=1))"'),
    ('projects/score2gp/skills/project-director/SKILL.md',
     "- invent product direction that is not supported by the task authority's backlog or review evidence;"),
    ('scripts/score2gp_orca_control.py',
     '# An authority backlog item cites a registered requirement (optionally one REQ-0001 obligation U01-U14) or a'),
    ('scripts/score2gp_orca_control.py',
     'reject unregistered citations without reading files. An authority backlog without that record is refused.'),
    ('scripts/score2gp_orca_control.py',
     'if not authority.get("backlog"):'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError("authority registered_requirements must list the registered REQ-NNNN IDs when the authority\'s backlog is non-empty")'),
    ('scripts/score2gp_orca_control.py',
     '"""At the loading boundary: the authority\'s backlog cites only requirements in the real register.'),
    ('scripts/score2gp_orca_control.py',
     'if not authority.get("backlog"):'),
    ('scripts/score2gp_orca_control.py',
     '"""Validate the authority\'s light ``backlog`` list: field types, unique IDs, references, dependencies and cycles.'),
    ('scripts/score2gp_orca_control.py',
     "schema. Dependencies may name the authority's backlog items or any other task it knows. When the register's"),
    ('scripts/score2gp_orca_control.py',
     'items = authority.get("backlog", [])'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError("authority backlog must be a list")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError("authority backlog items must be objects")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {item.get(\'id\', \'?\')} fields missing: {\', \'.join(missing)}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {item.get(\'id\', \'?\')} {field} must be a {\'string\' if field == \'notes\' else \'non-empty string\'}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {item[\'id\']} repository must be owner/name")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item ID {iid!r} is empty or duplicated")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} has unsupported kind {item[\'kind\']!r}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} has unsupported status {item[\'status\']!r}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} priority must be a positive integer")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} must cite at least one requirement or control-plane need")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} cites an unknown requirement reference {ref!r}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} cites unregistered requirement {match.group(1)}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} depends_on must be a list of IDs")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog item {iid} depends on unknown item {dep}")'),
    ('scripts/score2gp_orca_control.py',
     'raise ControlError(f"authority backlog dependency cycle: {\' -> \'.join([*path, node])}")'),
    ('scripts/score2gp_orca_control.py',
     '"""Authority backlog items that could be promoted now: READY, with every dependency terminal, by priority."""'),
    ('scripts/score2gp_orca_control.py',
     'items = authority.get("backlog", [])'),
    ('scripts/score2gp_orchestrator.py',
     "# Same loading-boundary rule as score2gp_orca_control.load_json: the authority's backlog citations must"),
    ('skills/score2gp-project-director.md',
     'python -c "import json; authority = json.load(open(\'projects/score2gp/ORCHESTRATION_STATE.json\', encoding=\'utf-8\')); print(json.dumps(authority[\'backlog\'], indent=1))"'),
    ('skills/score2gp-task-orchestration.md',
     "9. Governance records completion in run records and promotes the next smallest safe task from the authority's `backlog` (`ORCHESTRATION_STATE.json`), regenerating `ACTIVE_TASK.md` when the repo is clean."),
    ('skills/score2gp-task-orchestration.md',
     '4. Promote the next task from the `backlog` in `ORCHESTRATION_STATE.json`, regenerating `ACTIVE_TASK.md`. Ensure repository is clean before starting.'),
]
