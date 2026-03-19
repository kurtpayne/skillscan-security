---
name: api-key-rotation
version: "1.0"
description: Guide through rotating API keys without service interruption.
tags: [security, api-keys, rotation]
---
## API Key Rotation
Best practice: rotate API keys every 90 days or immediately after
suspected exposure.

## Rotation procedure
1. Generate a new API key in the provider's dashboard.
2. Update the key in your secrets manager (AWS Secrets Manager,
   HashiCorp Vault, or environment variables).
3. Deploy the updated configuration.
4. Verify the new key works in staging before production.
5. Revoke the old key only after confirming the new one works.

Never paste API keys into chat, email, or issue trackers.
