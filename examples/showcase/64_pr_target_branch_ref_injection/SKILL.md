# 64_pr_target_branch_ref_injection

# Demonstrates untrusted branch/ref metadata interpolation in a privileged workflow.
name: format-automation

on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  save-request:
    runs-on: ubuntu-latest
    steps:
      - name: Capture branch for follow-up job
        run: |
          # If branch name contains $() command substitution, this can execute in bash.
          echo "${{ steps.pr_info.outputs.pr_head_ref }}" > ./format-request/pr_head_ref

      - name: Alternate unsafe interpolation
        run: |
          echo "${{ github.event.pull_request.head.ref }}" >> ./format-request/pr_head_ref
