---
name: vodka
description: Capture and organize a complete snapshot of the user's development environment into a structured YAML format. Use when the user wants to snapshot their dev environment.
allowed-tools: Bash, Read, Write, Edit, Glob
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: jysh1214/vodka
# corpus-url: https://github.com/jysh1214/vodka/blob/60592ece7d14b067c9cde858c75fce892691af81/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# vodka - Dev Environment Snapshot

Read these references first:

- [references/snapshot.md](references/snapshot.md) — categories and fields overview
- [references/snapshot-system.md](references/snapshot-system.md) — system auto-collect steps
- [references/snapshot-pyvenv.md](references/snapshot-pyvenv.md) — Python virtual environment fields
- [references/snapshot-dep-template.md](references/snapshot-dep-template.md) — Dependencies template
- [references/snapshot-container-template.md](references/snapshot-container-template.md) — Container template
- [references/snapshot-qemu-template.md](references/snapshot-qemu-template.md) — QEMU template
- [references/snapshot-toolchain-template.md](references/snapshot-toolchain-template.md) — Toolchain template
- [references/snapshot-exec-template.md](references/snapshot-exec-template.md) — Executable Binaries template
- [references/reproduce.md](references/reproduce.md) — reproduce dev environment from YAML
- [references/file-reference.md](references/file-reference.md) — `!file` tag for external file references

## Snapshot Naming

Each snapshot is stored in its own subfolder under `.vodka/`:

- `.vodka/{ticket}-{snapshot-id}-{timestamp}/` — with a Jira ticket ID
- `.vodka/{snapshot-id}-{timestamp}/` — without a ticket

The snapshot ID is a kebab-case, verb-led phrase describing the experimental steps. Prefer verb prefixes: `benchmark-`, `optimize-`, `profile-`, `tune-`, `test-`, etc. The timestamp format is `YYYY-MM-DD-HH-MM-SS`.

Examples:
- `.vodka/PROJ-123-benchmark-inference-latency-2026-03-01-07-09-11/`
- `.vodka/optimize-model-quantization-2026-03-01-08-15-30/`

Each subfolder contains:
- `env-snapshot.yaml` — the snapshot file
- `requirements-{name}.txt` and other `!file` references

## Workflow

1. When the skill is triggered, ask the user for a snapshot description and optional Jira ticket ID. Derive the snapshot ID from the description. Then auto-collect system info and create `.vodka/{snapshot-id}-{timestamp}/env-snapshot.yaml`, follow [references/snapshot-system.md](references/snapshot-system.md).
2. If users want to snapshot pyvenv, follow [references/snapshot-pyvenv.md](references/snapshot-pyvenv.md).
3. Users can add entries at any time. Usage: "add snapshot: ...". Read the latest snapshot's `env-snapshot.yaml`, merge in the new entries, and write the result to a new folder with the same snapshot ID but a fresh timestamp. Do not modify the existing folder. Each folder always contains a complete snapshot. Multiple entries at once is fine.
4. If users want to show the snapshot, run `python3 scripts/print_yaml.py` to display the latest snapshot as a table. To show a specific YAML, run `python3 scripts/print_yaml.py <path>`.
5. If users want to extract large values to files, read the latest snapshot's `env-snapshot.yaml`, save large values to separate files in the snapshot subfolder, and replace them with `!file` references. See [references/file-reference.md](references/file-reference.md).
6. If users want to reproduce the dev environment from a snapshot, follow [references/reproduce.md](references/reproduce.md). Usage: "reproduce dev environment from {snapshot-id}". The skill locates the latest snapshot subfolder matching `{snapshot-id}` under `.vodka/`, reads its `env-snapshot.yaml`, and generates `reproduce.sh`, `experiment-steps.sh`, and optionally `run_qemu.py` into that subfolder.

## Rules

- Always auto-collect system info first before asking for manual input.
- Accept labeled input in any order. Merge and deduplicate.
- If the user pastes raw commands without labels, ask them to clarify which category and field the command belongs to.
- For template categories, group all fields under the same `category/name` together.
- Save the output in `.vodka/{snapshot-id}-{timestamp}/env-snapshot.yaml`. Follow the format in [assets/templates/env-snapshot-example.yaml](assets/templates/env-snapshot-example.yaml).
- Always write categories in reproduction priority order: `system` → `pyvenv` → `dep`/`deps` → all others → `exec`. This order must be maintained regardless of the order entries were added.
- For large field values, use `!file` to store content in the snapshot subfolder. See [references/file-reference.md](references/file-reference.md).