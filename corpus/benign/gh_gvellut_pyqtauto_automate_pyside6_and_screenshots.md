---
name: automate-pyside6-and-screenshots
description: Use PyQtAuto to automate and test PySide6 applications. PyQtAuto works like Playwright for web browsers, but for Qt/PySide6 desktop applications. Screenshots can be grabbed to see what is going on.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: gvellut/pyqtauto
# corpus-url: https://github.com/gvellut/pyqtauto/blob/86046d13513a594e401f1a85beda2d3fd2f71205/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

This document describes how to use PyQtAuto to automate and test PySide6 applications. PyQtAuto works like Playwright for web browsers, but for Qt/PySide6 desktop applications.

## Quick Start

### 1. Add PyQtAuto as a Development Dependency

In your project's `pyproject.toml`, add pyqtauto as a local source dependency:

```toml
[project]
dependencies = [
    "pyside6>=6.5.0",
]

[tool.uv.sources]
pyqtauto = { path = "/Users/guilhem/Documents/projects/github/pyqtauto" }

[project.optional-dependencies]
dev = [
    "pyqtauto",
]
```

Then install the dev dependencies:

```bash
uv sync --extra dev
```

### 2. Enable the Server in Your Application

Add the server import with a try/except to make it optional (recommended for production code):

```python
# Optional import - pyqtauto may not be installed in production
try:
    from pyqtauto.server import start_server
except ImportError:
    start_server = None

# Later, after QApplication is created:
if start_server is not None:
    server = start_server()  # Checks PYQTAUTO_ENABLED env var
    if server:
        print(f"PyQtAuto server on port {server.port}")
```

Or for forced development mode:
```python
from pyqtauto.server import start_server
start_server(force=True)  # Always starts, ignores env var
```

Complete example:

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from pyqtauto.server import start_server

def main():
    app = QApplication(sys.argv)

    # Start automation server
    server = start_server(force=True)
    if server:
        print(f"PyQtAuto server on port {server.port}")

    window = QMainWindow()
    window.setObjectName("main_window")  # Important for selectors!
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### 3. Write Automation Scripts

Create a Python script to automate your application:

```python
from pyqtauto import PyQtAutoClient

with PyQtAutoClient(port=9876) as client:
    # Wait for app to be ready
    client.wait_idle()

    # Click a button
    client.click("@name:submit_button")

    # Type text into an input
    client.type("@name:email_input", "test@example.com")

    # Take a screenshot
    client.screenshot_to_file("result.png")

    # Get widget text
    result = client.get_text("@name:status_label")
    print(f"Status: {result}")
```

#### Location of temporary files

Do not write automation scripts and save screenshots in the project folder (so does not pollute the workspace). Use a temp folder or pass the string as the script directly (instead of file).

However output in clear the path to the folder where the screenshots are stored, for inspection.

## Widget Selectors

PyQtAuto uses selectors to find widgets. Always set `objectName` on your widgets:

```python
button = QPushButton("Click Me")
button.setObjectName("submit_btn")  # Now use "@name:submit_btn"
```

### Selector Types

| Selector | Example | Description |
|----------|---------|-------------|
| `@name:` | `@name:submit_btn` | Find by objectName (recommended) |
| `@class:` | `@class:QPushButton` | Find first widget of class |
| `@text:` | `@text:Submit` | Find by text content |
| Path | `main_window/form/button` | Hierarchical path |

## Common Actions

### Clicking

```python
client.click("@name:button")           # Left click
client.double_click("@name:item")      # Double click
client.right_click("@name:widget")     # Right click
```

### Typing

```python
client.type("@name:input", "Hello World")
client.type("@name:input", "text", clear_first=False)  # Append
```

### Keyboard

```python
client.key("@name:input", "Return")                    # Press Enter
client.key("@name:input", "A", modifiers=["ctrl"])     # Ctrl+A
client.key_sequence("@name:input", "Ctrl+S")           # Key sequence
```

### Setting Values (Smart Setter)

```python
client.set_value("@name:checkbox", True)      # Check/uncheck
client.set_value("@name:spinbox", 42)         # Set number
client.set_value("@name:combo", "Option 2")   # Select text
client.set_value("@name:combo", 1)            # Select index
client.set_value("@name:slider", 75)          # Set slider
```

### Reading Values

```python
text = client.get_text("@name:label")
value = client.get_property("@name:spinbox", "value")
props = client.list_properties("@name:widget")
```

### Verification

```python
client.exists("@name:widget")           # Returns True/False
client.is_visible("@name:widget")
client.is_enabled("@name:widget")

# Assert properties
assert client.assert_property("@name:label", "text", "==", "Success")
```

### Waiting

```python
client.wait("@name:button", "visible", timeout_ms=5000)
client.wait("@name:spinner", "not_visible")
client.wait("@name:checkbox", "property:checked=true")
client.wait_idle()
client.sleep(1000)  # Use sparingly
```

### Screenshots

```python
# Save to file
client.screenshot_to_file("screenshot.png")
client.screenshot_to_file("widget.png", target="@name:specific_widget")

# Get as bytes
image_bytes = client.screenshot_to_bytes()
```

### Widget Tree Exploration

```python
tree = client.get_tree()
# IMPORTANT: get_tree() returns a dict, not a string!
# To save to file, use json.dumps():
import json
with open("widget_tree.json", "w") as f:
    f.write(json.dumps(tree, indent=2))

# Find multiple widgets - returns list of dicts with widget info
widgets = client.find("@class:QPushButton", max_results=10)
# Each widget dict contains: objectName, class, visible, enabled, geometry
# Example: {"objectName": "", "class": "QPushButton", "visible": true, "geometry": {...}}
```

**IMPORTANT**: `find()` returns widget info dicts, NOT selectors. You cannot pass these directly to `click()`. Use them for inspection only:

```python
# WRONG - will raise an error:
widgets = client.find("@class:PhotoCell", max_results=5)
client.click(widgets[0])  # Error! widgets[0] is a dict, not a selector

# CORRECT - use class selector directly:
client.click("@class:PhotoCell")  # Clicks the first matching widget

# Or use find() for inspection, then construct a selector:
widgets = client.find("@class:QPushButton", max_results=10)
for w in widgets:
    print(f"Found button: {w.get('objectName')} - text: {w.get('text')}")
# Then click by name if objectName is set:
client.click("@name:submit_btn")
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYQTAUTO_ENABLED` | - | Set to `1`, `true`, or `yes` to enable server |
| `PYQTAUTO_PORT` | `9876` | Server port |

## CLI Tool

PyQtAuto also provides a command-line tool:

```bash
# Get widget tree
pyqtauto tree

# Click a button
pyqtauto click "@name:submit_btn"

# Type text
pyqtauto type "@name:input" "Hello World"

# Take screenshot
pyqtauto screenshot output.png

# Interactive shell
pyqtauto shell
```

## Best Practices for Testable Applications

1. **Always set objectName**: Every widget you want to automate should have a unique `objectName`:
   ```python
   widget.setObjectName("unique_name")
   ```

2. **Use meaningful names**: Choose descriptive names like `login_button`, `email_input`, `status_label`.

3. **Wait for conditions**: Use `wait()` instead of `sleep()`:
   ```python
   # Good
   client.wait("@name:result", "visible")

   # Avoid
   client.sleep(1000)
   ```

4. **Take screenshots for verification**: Especially useful for AI agents:
   ```python
   client.click("@name:submit")
   client.wait_idle()
   client.screenshot_to_file("after_submit.png")
   ```

5. **Handle async operations**: Use `wait_idle()` after actions that trigger processing:
   ```python
   client.click("@name:load_data")
   client.wait_idle()  # Wait for event queue to empty
   ```

## Example: Full Test Script

```python
#!/usr/bin/env python3
"""Test script for MyApp."""

from pathlib import Path
from pyqtauto import PyQtAutoClient

def test_login():
    screenshots = Path("test_screenshots")
    screenshots.mkdir(exist_ok=True)

    with PyQtAutoClient() as client:
        # Initial state
        client.wait_idle()
        client.screenshot_to_file(screenshots / "01_initial.png")

        # Fill login form
        client.type("@name:username_input", "testuser")
        client.type("@name:password_input", "password123")
        client.screenshot_to_file(screenshots / "02_filled.png")

        # Submit
        client.click("@name:login_button")

        # Wait for result
        client.wait("@name:dashboard", "visible", timeout_ms=5000)
        client.screenshot_to_file(screenshots / "03_logged_in.png")

        # Verify
        welcome = client.get_text("@name:welcome_label")
        assert "testuser" in welcome

        print("Login test passed!")

if __name__ == "__main__":
    test_login()
```

## Error Handling

```python
from pyqtauto import PyQtAutoClient, CommandError, ConnectionError

try:
    with PyQtAutoClient() as client:
        client.click("@name:nonexistent")
except ConnectionError as e:
    print(f"Could not connect: {e.message}")
except CommandError as e:
    print(f"Command failed [{e.code}]: {e.message}")
```

## Common Gotchas and Troubleshooting

### 1. `get_tree()` returns a dict, not a string
```python
# WRONG:
tree = client.get_tree()
with open("tree.txt", "w") as f:
    f.write(tree)  # TypeError: write() argument must be str, not dict

# CORRECT:
import json
tree = client.get_tree()
with open("tree.json", "w") as f:
    f.write(json.dumps(tree, indent=2))
```

### 2. `find()` returns dicts, not selectors
The `find()` method returns widget info for inspection, not selectors for actions:
```python
# WRONG:
cells = client.find("@class:PhotoCell", max_results=5)
client.click(cells[0])  # Error: 'dict' object has no attribute 'startswith'

# CORRECT:
client.click("@class:PhotoCell")  # Clicks first matching widget
```

### 3. `@class:` selector clicks only the FIRST match
When using `@class:WidgetClass`, it will only interact with the first widget found. If widgets don't have unique `objectName` values, you may need to click the same selector multiple times or use other identifying features.

### 4. Allow time for initial UI rendering
Even after `wait_idle()`, the UI may not be fully rendered (especially thumbnails, images, etc.):
```python
client.wait_idle()
time.sleep(1)  # Give UI time to fully render before first screenshot
client.screenshot_to_file("initial.png")
```

### 5. Starting the application
Run the app in background with `PYQTAUTO_ENABLED=1`:
```bash
PYQTAUTO_ENABLED=1 uv run your_app &
sleep 3  # Wait for app to start
uv run python automation_script.py
```

### 6. Widgets without objectName
Many widgets don't have `objectName` set (shows as empty string `""`). The widget tree from `get_tree()` helps identify:
- Widget class names (use `@class:ClassName`)
- Widget hierarchy paths
- Text content (use `@text:ButtonLabel`)
- Geometry for understanding layout

## Typical AI Agent Workflow

For AI agents testing applications:

1. **Explore**: Get the widget tree to understand the UI structure
2. **Plan**: Identify widget classes and selectors to use
3. **Act**: Perform actions (click, type, etc.) using selectors
4. **Verify**: Take screenshots and check widget states
5. **Iterate**: Repeat based on screenshot analysis

```python
# AI agent example - complete workflow
import json
import time
from pathlib import Path
from pyqtauto import PyQtAutoClient

SCREENSHOT_DIR = Path("/tmp/screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

with PyQtAutoClient() as client:
    # 1. Wait for app and take initial screenshot
    client.wait_idle()
    time.sleep(1)  # Allow UI to fully render
    client.screenshot_to_file(str(SCREENSHOT_DIR / "01_initial.png"))

    # 2. Explore - save widget tree for analysis
    tree = client.get_tree()
    with open(SCREENSHOT_DIR / "widget_tree.json", "w") as f:
        f.write(json.dumps(tree, indent=2))

    # 3. Find widgets to understand what's available
    buttons = client.find("@class:QPushButton", max_results=10)
    print(f"Found {len(buttons)} buttons")
    for btn in buttons:
        print(f"  - {btn.get('objectName') or '(no name)'}: {btn.get('text', '')}")

    # 4. Act using selectors (NOT the find() results)
    client.click("@class:PhotoCell")  # Click first photo
    client.wait_idle()
    time.sleep(0.5)
    client.screenshot_to_file(str(SCREENSHOT_DIR / "02_after_click.png"))

    # 5. Verify with screenshot - AI can analyze the image
    # The screenshot shows the current state of the application

    # 6. Continue based on what AI sees in screenshots
    client.double_click("@class:PhotoCell")
    client.wait_idle()
    client.screenshot_to_file(str(SCREENSHOT_DIR / "03_after_doubleclick.png"))
```

### Recommended Workflow for AI Agents

1. **Always save the widget tree first** - It's essential for understanding the UI structure
2. **Use screenshots liberally** - They help verify actions worked correctly
3. **Use class selectors when objectName is not set** - Many apps don't set objectName
4. **Add delays after wait_idle()** - Especially for initial rendering and image loading
5. **Use find() for inspection, selectors for actions** - Don't mix them up
6. **Store files in a temp directory** - Don't pollute the project folder