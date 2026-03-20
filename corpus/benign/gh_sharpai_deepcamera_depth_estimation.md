---
name: depth-estimation
description: "Real-time depth map privacy transforms using Depth Anything v2 (CoreML + PyTorch)"
version: 1.2.0
category: privacy

parameters:
  - name: model
    label: "Depth Model"
    type: select
    options: ["depth-anything-v2-small", "depth-anything-v2-base", "depth-anything-v2-large"]
    default: "depth-anything-v2-small"
    group: Model

  - name: variant
    label: "CoreML Variant (macOS)"
    type: select
    options: ["DepthAnythingV2SmallF16", "DepthAnythingV2SmallF16INT8", "DepthAnythingV2SmallF32"]
    default: "DepthAnythingV2SmallF16"
    group: Model

  - name: blend_mode
    label: "Display Mode"
    type: select
    options: ["depth_only", "overlay", "side_by_side"]
    default: "depth_only"
    group: Display

  - name: opacity
    label: "Overlay Opacity"
    type: number
    min: 0.0
    max: 1.0
    default: 0.5
    group: Display

  - name: colormap
    label: "Depth Colormap"
    type: select
    options: ["inferno", "viridis", "plasma", "magma", "jet", "turbo", "hot", "cool"]
    default: "viridis"
    group: Display

  - name: device
    label: "Device"
    type: select
    options: ["auto", "cpu", "cuda", "mps"]
    default: "auto"
    group: Performance

capabilities:
  live_transform:
    script: scripts/transform.py
    description: "Real-time depth estimation overlay on live feed"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: SharpAI/DeepCamera
# corpus-url: https://github.com/SharpAI/DeepCamera/blob/c7e9ddda012ad3f8e9e5a95e2d2776bcf7442224/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Depth Estimation (Privacy)

Real-time monocular depth estimation using Depth Anything v2. Transforms camera feeds with colorized depth maps — near objects appear warm, far objects appear cool.

When used for **privacy mode**, the `depth_only` blend mode fully anonymizes the scene while preserving spatial layout and activity, enabling security monitoring without revealing identities.

## Hardware Backends

| Platform | Backend | Runtime | Model |
|----------|---------|---------|-------|
| **macOS** | CoreML | Apple Neural Engine | `apple/coreml-depth-anything-v2-small` (.mlpackage) |
| Linux/Windows | PyTorch | CUDA / CPU | `depth-anything/Depth-Anything-V2-Small` (.pth) |

On macOS, CoreML runs on the Neural Engine, leaving the GPU free for other tasks. The model is auto-downloaded from HuggingFace and stored at `~/.aegis-ai/models/feature-extraction/`.

## What You Get

- **Privacy anonymization** — depth-only mode hides all visual identity
- **Depth overlays** on live camera feeds
- **3D scene understanding** — spatial layout of the scene
- **CoreML acceleration** — Neural Engine on Apple Silicon (3-5x faster than MPS)

## Interface: TransformSkillBase

This skill implements the `TransformSkillBase` interface. Any new privacy skill can be created by subclassing `TransformSkillBase` and implementing two methods:

```python
from transform_base import TransformSkillBase

class MyPrivacySkill(TransformSkillBase):
    def load_model(self, config):
        # Load your model, return {"model": "...", "device": "..."}
        ...

    def transform_frame(self, image, metadata):
        # Transform BGR image, return BGR image
        ...
```

## Protocol

### Aegis → Skill (stdin)
```jsonl
{"event": "frame", "frame_id": "cam1_1710001", "camera_id": "front_door", "frame_path": "/tmp/frame.jpg", "timestamp": "..."}
{"command": "config-update", "config": {"opacity": 0.8, "blend_mode": "overlay"}}
{"command": "stop"}
```

### Skill → Aegis (stdout)
```jsonl
{"event": "ready", "model": "coreml-DepthAnythingV2SmallF16", "device": "neural_engine", "backend": "coreml"}
{"event": "transform", "frame_id": "cam1_1710001", "camera_id": "front_door", "transform_data": "<base64 JPEG>"}
{"event": "perf_stats", "total_frames": 50, "timings_ms": {"transform": {"avg": 12.5, ...}}}
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```