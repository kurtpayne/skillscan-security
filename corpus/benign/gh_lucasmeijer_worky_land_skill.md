---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: lucasmeijer/worky
# corpus-url: https://github.com/lucasmeijer/worky/blob/59c722a668cc132b0c28ca3b1227dc769a28a2ca/land.skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Land Skill

This skill automates the process of landing code changes to the main branch.

## Workflow

When the user initiates the land skill, you should:

1. **Commit all work**: Create a commit with all staged and unstaged changes
   - Run `git status` to see what needs to be committed
   - Add relevant files with `git add`
   - Create a commit with an appropriate message
   - Include "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>" in the commit message

2. **Rebase onto origin/main**: Sync with the latest main branch
   - Run `git fetch origin`
   - Run `git rebase origin/main`
   - If there are conflicts, notify the user and stop

3. **Run Swift tests**: Verify the code works
   - Run `swift test`
   - If tests fail, notify the user and stop

4. **Push to origin/main**: Land the changes
   - Run `git push origin HEAD:main`

## Important Notes

- Follow the git safety protocol: never use destructive commands without user consent
- If any step fails, stop and report the error to the user
- Provide clear status updates at each step