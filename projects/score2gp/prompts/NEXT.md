# Command Dispatch

Commands are role-specific. In Antigravity with the Score2GP `go` skill
installed, the author invokes `/go` (plain `go`/`next` are compatibility
aliases). Codex uses `got` for governance/reviewer work and must not invoke
the author command:

- Agy `/go`, `next`, and `go`: execute
  [go-dispatch.md](next/go-dispatch.md).
- Codex alias `got`: execute
  [got-dispatch.md](next/got-dispatch.md).

Both dispatchers combine stable `ACTIVE_TASK.md` metadata with the exact live
GitHub PR state. This file must never point directly at an implementation
prompt, because that can replay merged work.
