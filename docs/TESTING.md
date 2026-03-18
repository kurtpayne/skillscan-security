# Testing

Run local checks:

```bash
pytest -q
ruff check src tests
mypy src
```

Recommended CI gates:

1. Unit tests and fixture regression tests
2. Lint and typing checks
3. Minimum coverage threshold for scanner core

The malicious fixtures include OpenClaw-style compromised plugin patterns reproduced in safe test data.

## Regression fixtures

1. `tests/fixtures/benign/basic_skill`: low-risk baseline.
2. `tests/fixtures/malicious/openclaw_compromised_like`: strict profile should block.
3. `tests/fixtures/dependencies`: vulnerable and unpinned dependency coverage.
4. `tests/fixtures/policy`: policy domain-block behavior.
5. `examples/showcase/20_social_engineering_credential_harvest`: social engineering credential harvest example (SE-001 + SE-SEM-001).

## Adversarial regression corpus

SkillScan includes a red-team style adversarial suite with expected verdicts and finding IDs:

1. Cases: `tests/adversarial/cases/`
2. Manifest: `tests/adversarial/expectations.json`
3. Test runner: `tests/test_adversarial_suite.py`

Run all tests:

```bash
pytest -q
```
