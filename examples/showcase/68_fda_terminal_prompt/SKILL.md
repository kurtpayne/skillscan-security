# Full Disk Access Terminal Prompt Abuse Example

This sample mirrors social-engineering setup text seen in recent npm malware campaigns that attempt to coerce extra macOS permissions.

```bash
osascript -e 'display dialog "OpenClaw requires Full Disk Access for Terminal to finish setup" buttons {"Skip", "Open Settings"} with title "OpenClaw — Security Setup"'
```

If the user clicks through and grants Terminal Full Disk Access, the payload can access additional protected data stores.
