# Architecture: Orca Multi-WSL Agent Orchestration

**Date:** 2026-09-10  
**Status:** Approved Reference / Architectural Blueprint  
**Repository:** `score2gp-agentops`  
**Target Project:** `score2gp`  
**Purpose:** Define architecture, range of strategies, and operational protocols for orchestrating autonomous agents across multiple WSL Linux distributions using Orca.

---

## 1. Context & Motivation

Score2GP governance requires strict role separation between identities:
- **`tticom-automation`**: Author / implementation worker (creates PRs, edits code, pushes branches).
- **`tticom-codex`**: Architectural auditor / Devil's Advocate reviewer (runs adversarial disconfirmation probes).
- **`tticom-gov`**: Formal governance reviewer (submits formal verdicts, `CHANGES_REQUESTED` or `GO`).
- **`tticom-orca`**: Orchestration supervisor (coordinates DAGs, worktree lifecycles, and handoffs).

### The Self-Review Deadlock Problem
When all worker terminals run in a single shared environment or under a shared user without credential scoping, agents inherit the ambient `gh` CLI authentication of `tticom-automation` (the PR author). Under GitHub rulesets, authors cannot submit formal reviews or request changes on their own pull requests (failing with: `GitHub forbids requesting changes on your own PR`).

To resolve this deterministically, distinct WSL instances (`ubuntu-automation`, `ubuntu-gov`, `ubuntu-codex`, `Ubuntu-Orca`) isolate the filesystem, user environment, and credential stores. Orca serves as the coordinator across these instances.

---

## 2. Architecture & Strategy Spectrum

Orca supports heterogeneous **Execution Hosts** and **Federated Runtimes** (`out/shared/execution-host.js`). The coordinator can target workers through three primary strategies:

```
                                  +-------------------------------------------------+
                                  |         Orca Coordinator Runtime                |
                                  |         (Host / Windows Desktop / WSL)          |
                                  |                                                 |
                                  |  Run: run_<id>                                  |
                                  |  Inbox: worker_done, ask/reply, heartbeats      |
                                  +-----------------------+-------------------------+
                                                          |
                 +----------------------------------------+----------------------------------------+
                 |                                                                                 |
                 | [Strategy 1: WebSocket RPC Federation]                                          | [Strategy 2: Scoped SSH Targets]
                 v                                                                                 v
+------------------------------------+                                           +------------------------------------+
|   WSL: ubuntu-automation           |                                           |   WSL: ubuntu-gov / ubuntu-codex   |
|   Server: orca serve :6771         |                                           |   Server: orca serve :6772 (or SSH)|
|   Identity: tticom-automation      |                                           |   Identity: tticom-gov / codex     |
|   Role: Implementation Worker      |                                           |   Role: Governance / DA Reviewer   |
+------------------------------------+                                           +------------------------------------+
```

### Strategy Comparison

| Strategy | Isolation Boundary | Setup Overhead | Notes |
| :--- | :--- | :--- | :--- |
| **Method 1: Orca Federation (`orca serve` + `--on <env>`)** | Process, Host, Network RPC | Medium | **Recommended**: First-class Orca design for multi-agent DAGs; preserves native task preambles, streaming output, `worker_done`, and blocking `ask`/`reply`. |
| **Method 2: Per-Distro SSH Targets (`--host ssh:<id>`)** | OpenSSH / User Boundary | Low–Medium | Daemonless worker distros; leverages standard OpenSSH keys or WSL proxy commands. |
| **Method 3: Path-Based UNC Distro Routing (`\\wsl.localhost\<distro>`)** | Windows WSL Interop | Lowest | Native Windows Orca detects the distro from the worktree root path and invokes `wsl.exe -d <distro>`. |
| **Method 4: Scoped Credential Profiles (`GH_CONFIG_DIR`)** | Single OS, Token Isolation | Lowest | Resource-conserving fallback within a single WSL instance without spinning up multiple distros. |

---

## 3. Method 1: The Federated Orca Server Model (Recommended Architecture)

### 3.1 Headless Worker Servers

Inside each worker WSL instance, start an Orca headless runtime server:

**In `ubuntu-automation`:**
```bash
orca serve --port 6771 --pairing-address 127.0.0.1
```

**In `ubuntu-gov`:**
```bash
orca serve --port 6772 --pairing-address 127.0.0.1
```

**In `ubuntu-codex`:**
```bash
orca serve --port 6773 --pairing-address 127.0.0.1
```

*(Note: For in-repo development builds, use `pnpm exec orca-dev serve` or the built binary path).*

### 3.2 Coordinator Pairing

Register the environments with the coordinator:
```bash
orca environment add --name automation --pairing-code "<pairing-url-from-port-6771>"
orca environment add --name gov --pairing-code "<pairing-url-from-port-6772>"
orca environment add --name codex --pairing-code "<pairing-url-from-port-6773>"
```

Confirm presence in the host registry:
```bash
orca host list
orca environment list
```

### 3.3 Supervised Dispatch Loop

The coordinator manages the DAG and delegates tasks to specific environments:

```bash
# 1. Bind an orchestration Run
orca orchestration run-create --objective "Score2GP remediation and review loop" --json

# 2. Dispatch Implementation Task to Automation Environment
orca orchestration task-create --spec "Implement PR bug fix" --json
orca orchestration worker-start \
  --task <task_id> \
  --on automation \
  --agent codex \
  --json

# 3. Reactive Wait (No busy polling)
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json

# 4. Settle & Release Completed Worker
orca orchestration worker-release --dispatch <author_dispatch_id> --json

# 5. Dispatch Independent Review to Governance Environment
orca orchestration task-create --spec "Perform adversarial disconfirmation review on PR head" --json
orca orchestration worker-start \
  --task <review_task_id> \
  --on gov \
  --agent codex \
  --json

# 6. Wait for Review Settlement
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
orca orchestration worker-release --dispatch <review_dispatch_id> --json
```

---

## 4. Method 2: Per-Distro SSH Targets (`--host ssh:<id>`)

Each WSL instance can be registered as an independent SSH target in Orca.

### 4.1 Proxy Configuration (Windows `~/.ssh/config`)

Using OpenSSH `ProxyCommand`, no separate network ports or listening daemons are strictly required:

```ssh-config
Host wsl-automation
  User tticom-automation
  ProxyCommand wsl.exe -d ubuntu-automation -u tticom-automation exec /bin/nc -q0 %h %p

Host wsl-gov
  User tticom-gov
  ProxyCommand wsl.exe -d ubuntu-gov -u tticom-gov exec /bin/nc -q0 %h %p

Host wsl-codex
  User tticom-codex
  ProxyCommand wsl.exe -d ubuntu-codex -u tticom-codex exec /bin/nc -q0 %h %p
```

### 4.2 Worktree and Terminal Binding

Register the hosts in Orca, then create worktrees or terminals explicitly targeting them:
```bash
orca worktree create --project <project_id> --host ssh:wsl-gov --name review-tree --agent codex --json
```

The terminal process executes in `ubuntu-gov` under user `tticom-gov`.

---

## 5. Method 3: Path-Based UNC Distro Routing (`\\wsl.localhost\<distro>`)

Orca's path resolution (`out/shared/wsl-paths.js`) extracts WSL distributions from UNC file paths:
`\\wsl.localhost\<distro>\<linuxPath>`

When a repository or worktree is registered via its UNC path:
```bash
orca repo add --path "\\\\wsl.localhost\\ubuntu-automation\\home\\tticom-automation\\work\\score2gp"
orca repo add --path "\\\\wsl.localhost\\ubuntu-gov\\home\\tticom-gov\\work\\score2gp"
```
Any agent launched in that repository will execute directly inside that specific distribution via `wsl.exe -d <distro>`.

---

## 6. Method 4: Single-Distro Scoped Credential Profiles (`GH_CONFIG_DIR`)

When host memory constraints make multiple running WSL instances impractical, role separation can be achieved inside a single distribution (`Ubuntu-Orca`) by scoping the GitHub CLI configuration directory:

```bash
# Automation profile
export GH_CONFIG_DIR="$HOME/.config/gh-automation"
gh auth status  # Authenticated as tticom-automation

# Governance profile
export GH_CONFIG_DIR="$HOME/.config/gh-gov"
gh auth status  # Authenticated as tticom-gov

# Reviewer profile
export GH_CONFIG_DIR="$HOME/.config/gh-codex"
gh auth status  # Authenticated as tticom-codex
```

In Orca, spawn the worker with the scoped profile:
```bash
orca terminal create \
  --worktree active \
  --title "governance-reviewer" \
  --command "env GH_CONFIG_DIR=$HOME/.config/gh-gov codex" \
  --json
```

---

## 7. Operational Invariants for Score2GP

1. **Deterministic Halting:** A coordinator must never loop or poll `status`. Always use `orca orchestration check --wait`.
2. **Terminal Accountability:** Every settled worker terminal must be cleanly recycled via `worker-start --terminal <handle>`, retained for debugging via `worker-retain`, or closed via `worker-release`.
3. **Identity Firewall:** Author agents (`tticom-automation`) must never execute review or governance tasks. Reviewer agents (`tticom-gov` / `tticom-codex`) must never write product code or request reviews on their own changes.
