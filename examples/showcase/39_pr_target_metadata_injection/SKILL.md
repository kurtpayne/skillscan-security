# Example: pull_request_target metadata interpolation injection

name: PR Notify

on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Unsafe shell interpolation of PR metadata
        run: |
          echo "Preparing notification"
          payload='${{ github.event.pull_request.title }}'
          bash -lc "$payload"
