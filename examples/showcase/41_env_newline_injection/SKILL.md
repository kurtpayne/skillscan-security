# OAuth Token Sync Helper (Unsafe Example)

This sample demonstrates a vulnerable token update flow where user-provided token text is written into `.env`.

```json
{
  "tool": "ebay_set_user_tokens",
  "accessToken": "ok-token\nNODE_OPTIONS=--require /tmp/evil.js",
  "refreshToken": "refresh-ok"
}
```

Any workflow that accepts newline characters in token fields can inject arbitrary environment variables.
