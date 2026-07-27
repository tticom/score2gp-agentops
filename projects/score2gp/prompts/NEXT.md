# Command Dispatch

Commands are role-specific:

- Agy aliases `next` and `go`: execute
  [go-dispatch.md](next/go-dispatch.md).
- Codex alias `got`: execute
  [got-dispatch.md](next/got-dispatch.md).

Both dispatchers combine stable `ACTIVE_TASK.md` metadata with the exact live
GitHub PR state. This file must never point directly at an implementation
prompt, because that can replay merged work.
