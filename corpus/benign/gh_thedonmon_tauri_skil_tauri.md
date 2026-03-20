---
name: tauri
description: Build and automate Tauri v2 desktop applications. Use when the user needs to create a Tauri app, add commands/IPC, set up events, configure plugins, manage windows/tray icons, handle state, write platform-specific code, set up capabilities/permissions, or automate/test a running Tauri app. Triggers on tasks involving Tauri v2, tauri commands, tauri events, tauri plugins, tauri tray, tauri window config, tauri IPC, WebView automation, tauri-driver, or any desktop app built with Tauri. Also triggers when a project contains tauri.conf.json or src-tauri/ directory.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: thedonmon/tauri-skill
# corpus-url: https://github.com/thedonmon/tauri-skill/blob/aa52648c1aef9866f67ed114c7973c8fa2c38ebb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Tauri v2

Build small, fast, secure desktop apps with a web frontend and Rust backend. Tauri v2 uses the system WebView (WKWebView on macOS, WebView2 on Windows, WebKitGTK on Linux) — no bundled Chromium.

## Quick Start

```bash
npm create tauri-app@latest my-app -- --template react-ts
cd my-app && npm install && npm run tauri dev
```

Project layout:

```
src/                  # Frontend (React/Vue/Svelte)
src-tauri/
  src/main.rs         # Entry point
  src/lib.rs          # App setup, plugins, tray
  src/commands.rs     # Rust commands (invoked from frontend)
  Cargo.toml          # Rust deps
  tauri.conf.json     # App config
  capabilities/       # Permission definitions
```

## Building — Core IPC

### Define a command (Rust)

```rust
#[tauri::command]
pub async fn list_items() -> Result<Vec<Item>, String> {
    Ok(vec![])
}
```

### Register it (lib.rs)

```rust
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![commands::list_items])
    .run(tauri::generate_context!())
    .expect("error");
```

### Call from frontend

```typescript
import { invoke } from '@tauri-apps/api/core';
const items = await invoke<Item[]>('list_items');
```

### Events (real-time, bidirectional)

```rust
// Rust: emit to frontend
use tauri::{AppHandle, Emitter};
app.emit("status-changed", &payload).unwrap();
```

```typescript
// Frontend: listen
import { listen } from '@tauri-apps/api/event';
const unlisten = await listen<Payload>('status-changed', (e) => {
    console.log(e.payload);
});
```

### State (shared across commands)

```rust
use std::sync::Mutex;
app.manage(Mutex::new(AppState { count: 0 }));

#[tauri::command]
fn increment(state: tauri::State<'_, Mutex<AppState>>) -> u32 {
    let mut s = state.lock().unwrap();
    s.count += 1;
    s.count
}
```

For detailed building patterns (plugins, tray, window config, capabilities, streaming, background tasks), see [references/building.md](references/building.md).

## Automating — Platform-Specific

Tauri uses system WebViews, so automation varies by platform:

| Platform | Engine | Method |
|----------|--------|--------|
| Windows | WebView2 | CDP — set `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` |
| Linux | WebKitGTK | `tauri-driver` wrapping `WebKitWebDriver` |
| macOS | WKWebView | `tauri-webdriver` (community) or Safari Web Inspector |

### Windows (CDP — works with agent-browser/Playwright)

```bash
# Set env var before launching app
set WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222
my-app.exe

# Then connect
agent-browser connect 9222
agent-browser snapshot -i
agent-browser click @e5
```

### Linux/Windows (tauri-driver)

```bash
cargo install tauri-driver --locked
tauri-driver &
# Run WebDriver tests against http://localhost:4444
```

### macOS (tauri-webdriver)

```bash
cargo install tauri-wd
# Add tauri-webdriver plugin to debug builds, then:
tauri-wd &
# W3C WebDriver on http://localhost:4444
```

For detailed automation setup (Playwright, Selenium, WebdriverIO, devtools, MCP), see [references/automation.md](references/automation.md).

## Key Decisions

- **Frontend framework**: Any works (React, Vue, Svelte, Solid). Pick based on team preference.
- **State**: Rust `Mutex<T>` via `app.manage()` for backend; Zustand/signals for frontend.
- **IPC pattern**: Use `invoke()` for request/response, events for streaming/real-time.
- **Plugins**: Check the [official plugin list](https://v2.tauri.app/plugin/) before building custom — notification, shell, fs, dialog, clipboard, opener, os all exist.
- **Permissions**: Tauri v2 requires explicit capability grants in `src-tauri/capabilities/`. Each plugin documents its permission identifiers.
- **Platform code**: Use `#[cfg(target_os = "macos")]` in Rust, `platform()` from `@tauri-apps/plugin-os` in JS.