# Showcase 46: pull_request_target Cache-Key Poisoning Primitive

name: cache-key-poison-demo

description: |
  This fixture demonstrates a risky GitHub Actions pattern where a privileged
  `pull_request_target` workflow derives cache keys from untrusted PR metadata.

workflow:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: triage-${{ github.event.pull_request.title }}
          restore-keys: |
            triage-
      - run: echo "triage complete"
