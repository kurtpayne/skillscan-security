# Workflow helper

A dangerous GitHub Actions pattern appears when untrusted issue/comment text is interpolated directly in `run` or script blocks.

```yaml
name: issue-command
on:
  issues:
    types: [opened, edited]
  issue_comment:
    types: [created]
jobs:
  repro:
    runs-on: ubuntu-latest
    steps:
      - name: vulnerable issue title use
        run: echo "${{ github.event.issue.title }}"
      - name: vulnerable comment body use
        run: |
          payload='${{ github.event.comment.body }}'
          bash -lc "$payload"
```
