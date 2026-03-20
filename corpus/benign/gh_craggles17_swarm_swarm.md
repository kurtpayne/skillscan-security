---
name: swarm
description: "Orchestrates a swarm of parallel agents to complete a list of independent sub-tasks with state tracking, error handling, and atomic result aggregation."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: craggles17/swarm
# corpus-url: https://github.com/craggles17/swarm/blob/b902bcf896847233aa12d2854f8691b30dd6b79e/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Dynamic Worker Swarm

This skill implements a safe Orchestrator-Worker pattern for parallel task execution
with explicit state management, failure recovery, and result synthesis.

## Usage

1. **Define tasks:** Break your goal into discrete, independent sub-tasks. Each task
   must be completable in isolation — no shared mutable state between workers.
2. **Invoke the swarm:** Call this skill with the task list and an aggregation strategy.

## Concepts

### Task Contract

Every sub-task is a structured object with:

| Field | Required | Description |
|---|---|---|
| `id` | yes | Unique slug (e.g., `task-01-parse-config`). Used for file naming and state tracking. |
| `description` | yes | Plain-language description of what the worker must do. |
| `input_files` | no | List of absolute paths the worker may read (read-only). |
| `output_file` | yes | Path where the worker writes its result (must be unique per task). |
| `timeout_s` | no | Per-task timeout in seconds. Default: 120. |
| `retries` | no | Max retry attempts on failure. Default: 1. |

### Task States

Each task moves through a strict state machine:

```
PENDING → DISPATCHED → RUNNING → { SUCCEEDED | FAILED }
                                       ↓
                                   RETRYING → RUNNING → ...
```

- **PENDING**: Queued, not yet assigned to a worker.
- **DISPATCHED**: Agent spawned, awaiting first output signal.
- **RUNNING**: Worker confirmed alive (heartbeat or partial output detected).
- **SUCCEEDED**: Output file exists and passes validation.
- **FAILED**: Worker exited with error, timed out, or exhausted retries.
- **RETRYING**: Failed task re-queued for another attempt.

### State File

The orchestrator maintains a single state file at `.swarm/state.json`:

```json
{
  "swarm_id": "abc123",
  "created_at": "2026-03-16T12:00:00Z",
  "concurrency_limit": 5,
  "tasks": {
    "task-01-parse-config": {
      "state": "SUCCEEDED",
      "attempts": 1,
      "dispatched_at": "...",
      "completed_at": "...",
      "output_file": ".swarm/results/task-01-parse-config.md",
      "error": null
    }
  }
}
```

This file is the single source of truth. Workers never modify it — only the
orchestrator does.

## The Process

### Phase 1: Validation

1. Parse the task list. Reject if:
   - Any `id` is duplicated.
   - Any `output_file` path collides with another task's.
   - Any `input_files` reference doesn't exist.
2. Create `.swarm/` directory and initialize `state.json` with all tasks in `PENDING`.
3. Create `.swarm/results/` directory for output files.

### Phase 2: Dispatch Loop

The orchestrator runs a dispatch loop:

```
while any task is PENDING or RETRYING:
    active_count = count tasks in {DISPATCHED, RUNNING}
    if active_count < concurrency_limit:
        next_task = pick oldest PENDING or RETRYING task
        spawn worker agent for next_task
        set next_task.state = DISPATCHED
        set next_task.dispatched_at = now()
        increment next_task.attempts
    
    for each DISPATCHED or RUNNING task:
        if elapsed > task.timeout_s:
            kill worker
            if task.attempts < task.retries + 1:
                set task.state = RETRYING
            else:
                set task.state = FAILED
                set task.error = "Timeout after {timeout_s}s"
    
    update state.json
    wait 2s before next iteration
```

### Phase 3: Worker Execution

Each worker agent receives a **sealed instruction envelope**:

```
You are a worker in a swarm. Your constraints:
- You MUST NOT use the Agent tool (no spawning sub-agents).
- You MUST NOT modify any file outside your designated output_file.
- You MUST write your complete result to: {output_file}
- You MUST use atomic writes (write to {output_file}.tmp, then rename).

Your task:
  ID: {id}
  Description: {description}
  Input files (read-only): {input_files}

Write your result to {output_file} when done.
```

**Atomic write protocol:** Workers write to `{output_file}.tmp` first, then
rename to `{output_file}`. This prevents the orchestrator from reading
partial results. The orchestrator only considers a task SUCCEEDED when the
final `{output_file}` (not `.tmp`) exists and is non-empty.

### Phase 4: Completion Check

After the dispatch loop exits (no PENDING or RETRYING tasks remain):

1. Read `state.json` for final task states.
2. Classify outcome:
   - **All SUCCEEDED**: Proceed to aggregation.
   - **Some FAILED**: Report failures, proceed to aggregation with available results
     (unless `fail_fast: true` was set, in which case abort).
   - **All FAILED**: Report error, do not aggregate.

### Phase 5: Result Aggregation

The orchestrator reads all successful result files and synthesizes a response.

Aggregation strategies (specified at invocation):

| Strategy | Behavior |
|---|---|
| `concatenate` | Append results in task-id order. Default. |
| `merge` | Orchestrator reads all results and produces a unified synthesis. |
| `structured` | Each result is a JSON object; orchestrator merges into a single JSON document. |

The orchestrator presents the aggregated result to the user, noting any failed
tasks and their errors.

## Safety Guardrails

| Rule | Enforcement |
|---|---|
| **No self-replication** | Worker prompt explicitly forbids Agent tool use. Workers are spawned with `model: "haiku"` which cannot override this. |
| **Concurrency limit** | Hard cap from session config (default: 5). Dispatch loop enforces. |
| **Flat hierarchy** | Only the orchestrator spawns agents. Workers have no Agent tool access. |
| **File isolation** | Each worker has exactly one writable path. Orchestrator validates no overlaps in Phase 1. |
| **Timeout enforcement** | Per-task timeouts with kill + retry semantics. No indefinite hangs. |
| **Idempotency** | If `state.json` already exists, the orchestrator resumes from last known state, skipping SUCCEEDED tasks. |
| **Cost scoping** | Workers use the cheapest viable model (currently `haiku`). |

## Failure Modes & Mitigations

| Failure | Mitigation |
|---|---|
| Worker writes partial output then crashes | Atomic write protocol — `.tmp` files are ignored by orchestrator. |
| Worker hangs forever | Per-task timeout with automatic kill. |
| Worker attempts to spawn sub-agents | Agent tool excluded from worker tool set. |
| Orchestrator crashes mid-swarm | `state.json` persists state. Re-invoking the skill resumes from last checkpoint. |
| Two tasks accidentally share an output path | Caught in Phase 1 validation. |
| Result file is empty or malformed | Orchestrator validates non-empty output before marking SUCCEEDED. |
| All workers fail | Orchestrator reports all errors, does not attempt aggregation. |

## Limitations

- Tasks must be **truly independent** — no task can depend on another task's output.
  The orchestrator does not validate this; it is the caller's responsibility.
- Workers operate in the **same filesystem** — file isolation is by convention
  (enforced output paths), not by sandboxing.
- The state file is not locked — do not run two swarm instances concurrently in
  the same `.swarm/` directory.