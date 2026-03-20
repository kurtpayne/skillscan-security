---
name: comfyui-operator
description: Native integration with a local ComfyUI instance to list workflows/models, start the server, and generate images by overriding nodes via API. Use when the user requests image generation through ComfyUI.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hrdtbs/comfyui-operator-skill
# corpus-url: https://github.com/hrdtbs/comfyui-operator-skill/blob/68b2c4b0a184ea4920d80173bd33a9e679d89847/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# comfyui-operator

This skill provides native integration to operate a local instance of ComfyUI. It allows you to:
1. Guarantee ComfyUI is running.
2. Interrogate the installation for available Workflows, LoRAs, and Checkpoints.
3. Queue prompts (API workflows) with dynamic JSON overrides and download the resulting images.

## Configuration & Setup

All scripts rely on the `requests` and `websocket-client` Python libraries. Depending on your Python environment, you may need to install them:
```bash
pip install -r requirements.txt
```

By default, all scripts assume ComfyUI is installed at `C:\ComfyUI_windows_portable`.
**IMPORTANT:** If the default directory does not exist, ask the user for the correct ComfyUI installation path before proceeding.

## Interaction Guidelines

When a user asks you to generate an image using this skill, you must follow these conversational rules:

1. **Vague/General Requests:**
   If the user simply says "Generate an image" without specifying a character, concept, or workflow:
   - **DO NOT guess a workflow.**
   - Run `list_resources.py` immediately to discover available API-format workflows.
   - Present the list of found workflows to the user and ask them which one they would like to use.

2. **Output Locations (CRITICAL):**
   When invoking scripts that generate files (`list_resources.py` or `generate_image.py`), you MUST explicitly specify the user's active workspace directory using the `--output` and `--output_dir` arguments. Do not rely on script default paths.
   - For `list_resources.py`, always save the output to `<active_workspace>/.comfyui/resources.json` **unless the user explicitly specifies a different path.**
   - For `generate_image.py`, always save the output images to `<active_workspace>/.comfyui/outputs/` **unless the user explicitly specifies a different saving location.**

3. **Specific Requests & Fuzzy Matching:**
   If the user asks for a specific subject (e.g., "Generate an image of Nemu" or "ねむの画像を生成して"):
   - Run `list_resources.py` to get the list of workflows.
   - Perform **fuzzy matching** to find a workflow that matches the requested subject, accounting for orthographical variants (e.g., "Nemu", "nemu", "ネム", "ねむ" should all match a file like `os-nemu-api.json`).
   - If a plausible match is found, proceed with generating the image using that workflow directly (unless disambiguation is needed between multiple close matches).

## Scripts

### 1. `start_comfyui.py`
Ensures that the ComfyUI server is running and the API is reachable.

**Usage:**
```bash
python scripts/start_comfyui.py [--comfyui_path "path/to/comfyui"]
```
It returns silently if ComfyUI is already running. Otherwise, it will launch the startup batch file or Python script in the background and poll until `http://127.0.0.1:8188/system_stats` responds.

### 2. `list_resources.py`
Lists available models (Checkpoints, LoRAs) and Workflows saved in the API JSON format to help formulate generation parameters.

**Usage:**
```bash
python scripts/list_resources.py [--comfyui_path "path/to/comfyui"] [--output "resources.json"]
```
Outputs a JSON block representing the contents of the `models` directories and `user/default/workflows`. Use the `--output` argument to save directly to a file and avoid console encoding issues. By default, it will save to `resources.json` in the current working directory.

### 3. `generate_image.py`
Generates an image by loading a base JSON workflow, applying targeted node overrides over the WebSocket API, and saving the final image.

**Usage:**
```bash
python scripts/generate_image.py \
    --workflow_path "path/to/base_api_workflow.json" \
    [--output_dir "path/to/save/images"] \
    [--overrides_file "path/to/overrides.json"] \
    --overrides '{"3": {"inputs": {"seed": 12345}}, "6": {"inputs": {"text": "A beautiful sunset..."}}}' \
    [--comfyui_path "path/to/comfyui"] \
    [--server "127.0.0.1:8188"]
```
*Tip: Due to Windows terminal quoting and escaping issues when passing JSON strings via `--overrides`, **it is highly recommended** to write complex overrides to a temporary JSON file and pass it using `--overrides_file temp.json`.*

*Note: The script will auto-detect whether the server is running on port 8188 or 8000.*
*Note: The default output directory is the current working directory.*

#### Understanding Overrides
The `--overrides` argument is a JSON string. The keys are the **Node IDs** from the workflow file (often represented as strings of numbers, e.g., `"3"`, `"6"`).
- KSampler nodes typically have ID `"3"`. To change the seed: `{"3": {"inputs": {"seed": <random_number>}}}`
- CLIP Text Encode (Positive Prompt) typically has ID `"6"`. To change the prompt: `{"6": {"inputs": {"text": "<your_prompt>"}}}`

**⚠️ CRITICAL SEED SAFETY RULE:**
By default, **DO NOT override or change the seed value** in the base workflow. You should only inject a random seed if:
1. The user explicitly requests a new/different/random seed.
2. The user requests **multiple images (batch generation)** for the exact same prompt, in which case you must provide a different seed for each generation request to prevent identical outputs.

**⚠️ CRITICAL PROMPT SAFETY RULE:**
When overriding a text prompt (e.g., node `"6"`), **DO NOT overwrite the entire existing prompt blindly.** Workflows often contain critical baseline tags (e.g., character names, style tags, quality tags like `masterpiece`, `best quality`). 
- If you need to make changes, **read the original workflow JSON first** and **append** your new keywords to the existing `text` string.
- If the user asks for a significant departure from the base prompt, **ask for their confirmation** before performing a destructive overwrite.

**Process:**
1. Wait for ComfyUI to be running using `start_comfyui.py`.
2. Ensure you have a valid `workflow_path` pointing to a ComfyUI JSON file exported in **API format**.
3. Formulate the `--overrides` string to inject dynamic parameters (remembering to append, not replace, base text prompts unless specified).
4. Run `generate_image.py` and capture the saved image file paths.

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.