# CI triage workflow (intentionally unsafe showcase)

```yaml
name: triage
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@main
        with:
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: echo "triage done"
```
