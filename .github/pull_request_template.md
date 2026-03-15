## Summary
- What changed?
- Why this is needed now?

## Pattern Update Checklist (required for rules/default.yaml edits)
- [ ] Worked on a feature branch (not `main`)
- [ ] Added/updated rule IDs in `src/skillscan/data/rules/default.yaml`
- [ ] Bumped rulepack version (`YYYY.MM.DD.N`)
- [ ] Added/updated at least one showcase fixture under `examples/showcase/*`
- [ ] Updated `examples/showcase/INDEX.md`
- [ ] Updated `docs/EXAMPLES.md`
- [ ] Added source-backed rationale in `docs/RULE_UPDATES.md` or `PATTERN_UPDATES.md`
- [ ] Added tests in `tests/test_rules.py`
- [ ] Added showcase assertion(s) in `tests/test_showcase_examples.py`

## Validation
- [ ] `ruff check src tests`
- [ ] `pytest -q`

## Sources
- Link 1
- Link 2
