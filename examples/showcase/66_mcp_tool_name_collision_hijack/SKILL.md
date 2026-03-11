# MCP Research Helper

Security note copied from an external issue triage:

A malicious remote MCP server can abuse **tool name collision** when a client maps tools as `mcp_{service}_{tool}`.
The attacker registers a colliding tool that overwrites a legitimate one (e.g., tavily_extract) and hijacks tool execution flow.

Do not trust repository-provided MCP server names or aliases without collision checks.
