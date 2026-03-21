---
name: mcp-server-command-injection
description: Demonstrates MCP server command injection via unsanitized Git parameters
---

# MCP Server Command Injection

This skill demonstrates the CVE-2026-4198 and CVE-2026-4496 vulnerabilities in MCP
server packages that allow command injection through unsanitized Git parameters.

## Vulnerable Package: mcp-server-auto-commit

The `mcp-server-auto-commit` package passes user input directly to shell commands
without sanitization in the getGitChanges function:

```javascript
// Vulnerable getGitChanges function in mcp-server-auto-commit
async function getGitChanges(repoPath) {
  // CVE-2026-4198: repoPath is not sanitized before exec
  const { stdout } = await exec(`git -C ${repoPath} diff --cached`);
  return stdout;
}
```

## Vulnerable Package: Git-MCP-Server

The sigmade/Git-MCP-Server uses child_process.exec with unsanitized input in
the show_merge_diff, quick_merge_summary, and show_file_diff tools:

```javascript
// CVE-2026-4496: OS command injection in gitUtils.ts
const { stdout } = child_process.exec(
  `git show_merge_diff ${userInput}`
);
```
