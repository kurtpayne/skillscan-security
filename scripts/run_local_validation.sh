#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTEST_BIN=".venv/bin/pytest"
RUFF_BIN=".venv/bin/ruff"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-900}"
TARGETED_TIMEOUT_SECONDS="${TARGETED_TIMEOUT_SECONDS:-240}"

if [[ ! -x "$PYTEST_BIN" || ! -x "$RUFF_BIN" ]]; then
  echo "ERROR: missing repo venv tools. Run 'make setup' in $ROOT_DIR" >&2
  exit 2
fi

echo "[validate] root=$ROOT_DIR"
echo "[validate] timeout=${TIMEOUT_SECONDS}s"

echo "[1/3] ruff"
"$RUFF_BIN" check src tests

echo "[2/3] targeted tests"
"$PYTEST_BIN" -q tests/test_rules.py::test_new_patterns_2026_03_15
"$PYTEST_BIN" -q tests/test_showcase_examples.py::test_showcase_detection_rules

echo "[3/3] full suite (timeout)"
set +e
timeout "${TIMEOUT_SECONDS}s" "$PYTEST_BIN" -q
rc=$?
set -e

if [[ $rc -eq 0 ]]; then
  echo "[validate] full suite passed"
  exit 0
fi

if [[ $rc -eq 124 ]]; then
  echo "[validate] full suite timed out after ${TIMEOUT_SECONDS}s" >&2
  exit 124
fi

echo "[validate] full suite failed with exit code $rc" >&2
exit "$rc"
