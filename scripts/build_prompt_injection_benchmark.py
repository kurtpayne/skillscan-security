#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _iter_json_records(root: Path):
    for path in root.rglob("*"):
        if path.suffix.lower() not in {".json", ".jsonl"}:
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if path.suffix.lower() == ".jsonl":
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    yield obj
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            yield obj
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    yield item


def _extract_text_label(record: dict) -> tuple[str, bool] | None:
    text = (
        record.get("text")
        or record.get("prompt")
        or record.get("instruction")
        or record.get("content")
        or record.get("input")
    )
    if not isinstance(text, str) or len(text.strip()) < 30:
        return None

    lbl = record.get("label")
    if isinstance(lbl, str):
        label = lbl.lower() in {"1", "true", "attack", "malicious", "injection", "pi"}
    else:
        label = bool(record.get("is_prompt_injection") or record.get("attack") or record.get("malicious"))
    return text.strip(), label


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build prompt-injection benchmark manifest from local datasets"
    )
    parser.add_argument("--pint-root", type=Path, required=True)
    parser.add_argument("--openpi-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("tests/benchmark/generated_prompt_injection"))
    parser.add_argument("--limit-per-dataset", type=int, default=200)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    cases_dir = args.out_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    manifest_cases: list[dict] = []
    ds_specs = [
        ("pint", args.pint_root),
        ("openpi", args.openpi_root),
    ]

    for name, root in ds_specs:
        count = 0
        for record in _iter_json_records(root):
            parsed = _extract_text_label(record)
            if parsed is None:
                continue
            text, is_attack = parsed
            case_name = f"{name}_{count:04d}"
            case_dir = cases_dir / case_name
            case_dir.mkdir(parents=True, exist_ok=True)
            (case_dir / "SKILL.md").write_text(text + "\n", encoding="utf-8")
            manifest_cases.append(
                {
                    "target": str(case_dir),
                    "expected_ids": ["PINJ-SEM-001"] if is_attack else [],
                    "forbidden_ids": ["PINJ-SEM-001"] if not is_attack else [],
                }
            )
            count += 1
            if count >= args.limit_per_dataset:
                break

    manifest = {"cases": manifest_cases}
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(manifest_cases)} cases to {args.out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
