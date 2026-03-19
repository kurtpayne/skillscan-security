---
name: webauthn-setup
version: "1.0"
description: Guide users through setting up WebAuthn/FIDO2 passkeys.
tags: [auth, webauthn, security]
---
## WebAuthn Setup
This skill guides users through registering a passkey using WebAuthn.
No passwords or secrets are collected. The browser handles all
cryptographic operations locally. The server only receives a public key.

## Steps
1. The user clicks "Register passkey" in their browser.
2. The browser prompts for biometric or PIN verification.
3. A public/private key pair is generated locally.
4. Only the public key is sent to the server.
