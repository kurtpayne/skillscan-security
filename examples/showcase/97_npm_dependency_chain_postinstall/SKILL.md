# npm Dependency Chain Attack via Hollow Relay Package
Demonstrates detection of the GlassWorm/ForceMemo three-layer dependency
chain attack where compromised npm packages use hollow relay scoped
packages to deliver Solana blockchain C2 malware via postinstall hooks.
## Attack Overview
The attacker compromises a popular npm package via account takeover and
adds a dependency on a hollow relay scoped package. That relay package
depends on a payload host that runs a postinstall hook executing a
JavaScript loader file.
## Malicious package.json (payload host)
```json
{
  "name": "@usebioerhold8733/s-format",
  "version": "2.0.4",
  "scripts": {
    "postinstall": "node child.js"
  }
}
```
## Loader chain
```json
{
  "name": "react-native-international-phone-number",
  "version": "0.12.1",
  "dependencies": {
    "@agnoliaarisian7180/string-argv": "0.3.0"
  },
  "scripts": {
    "postinstall": "node init.js"
  }
}
```
## Detection Rationale
The postinstall hook executing standalone JavaScript loader files such
as init.js or child.js is a hallmark of the GlassWorm/ForceMemo supply
chain attack documented by StepSecurity and Sonatype in March 2026.
