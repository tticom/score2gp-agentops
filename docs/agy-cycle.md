# AGY Cycle Runner

`scripts/agy_cycle.py` is a deterministic, one-task/one-PR controller. It does
not ask AGY or another model to select work or infer lifecycle state.

## Operator loop

From the repository root:

```bash
python -m pip install -r requirements-agy-cycle.txt
python scripts/agy_cycle.py claim
```

The claim command prints a cycle ID. The orchestrator then asks for the next
bounded operation:

```bash
python scripts/agy_cycle.py next CYCLE-ID
python scripts/agy_cycle.py prompt CYCLE-ID > agy-cycle-prompt.txt
```

Or launch the configured interactive AGY binary directly through a PTY. The
prompt is injected once and the rest of the session remains interactive:

```bash
python scripts/agy_cycle.py run CYCLE-ID
```

Set `AGY_CLI` when the executable needs arguments, for example
`AGY_CLI='agy --profile automation'`. The worker reports facts; the controller
performs transitions explicitly:

```bash
python scripts/agy_cycle.py transition CYCLE-ID IMPLEMENTING
python scripts/agy_cycle.py transition CYCLE-ID VERIFYING
python scripts/agy_cycle.py transition CYCLE-ID PR_OPEN
python scripts/agy_cycle.py attach-pr CYCLE-ID https://github.com/ORG/REPO/pull/123
```

There can be only one attached PR per cycle. A human can repair a stuck cycle
without reconstructing history through an AI:

```bash
python scripts/agy_cycle.py reset CYCLE-ID FAILED
python scripts/agy_cycle.py reset CYCLE-ID READY
```

Resetting to `READY` archives the old runtime record and releases its claim;
the task can then be claimed as a new cycle.

## Source of truth

- `.agy/flow.yaml` defines the state transitions and hard limits.
- `plan/backlog.yaml` defines sprints, ordering, dependencies, and task scope.
- `.agy/cycles/` contains ignored runtime records and atomic claim locks.

Each task must have `cardinality: 1`. Larger work must be split before it can
be claimed. `ordinality` provides deterministic implementation order within a
sprint; `priority` breaks ties.
