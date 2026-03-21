# GlassWorm extensionPack Transitive Dependency Attack
Demonstrates detection of the GlassWorm supply chain technique where
malicious Open VSX extensions use extensionPack and extensionDependencies
to pull in payload extensions transitively, bypassing marketplace checks.
## Attack Overview
The attacker publishes a clean-looking extension that declares malicious
extensions in its extensionPack or extensionDependencies array. When a
user installs the parent extension, the malicious children are silently
installed as transitive dependencies.
## Malicious package.json
```json
{
  "name": "ng-angular-extension",
  "publisher": "angular-studio",
  "version": "1.0.3",
  "extensionPack": ["angular-studio.ng-angular-extension", "gvotcha.claude-code-extension", "crotoapp.vscode-xml-extension"]
}
```
## Additional dependency vector
```json
{
  "extensionDependencies": ["mswincx.antigravity-cockpit", "turbobase.sql-turbo-tool", "vce-brendan-studio-eich.js-debuger-vscode"]
}
```
## Detection Rationale
The extensionPack and extensionDependencies arrays reference suspicious
extension IDs that follow the GlassWorm naming pattern, including
claude-code-extension and other AI-themed extension names used as
delivery vehicles for malicious payloads.
