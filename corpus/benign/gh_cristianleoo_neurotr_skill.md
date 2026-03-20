---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: cristianleoo/NeuroTrace
# corpus-url: https://github.com/cristianleoo/NeuroTrace/blob/b2aea458145d111cd3b0d7c0dd46da7183601351/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# neurotrace — Agent Skill

You are an AI agent that can run **neurotrace**, an activation-patching framework for encoder-only transformer models. Use this skill when a user wants to understand where factual knowledge is stored inside a HuggingFace MLM, or to compare how two models encode domain-specific facts.

## When to use this skill

- User asks "does [model] actually know [domain] facts?"
- User wants to compare a fine-tuned model against its base model
- User wants to locate knowledge neurons or test factual recall
- User asks about activation patching, causal tracing, or knowledge localisation

## Prerequisites

The repo must be installed:

```bash
cd /path/to/neurotrace
uv venv && uv pip install -e .
source .venv/bin/activate
```

### Option A: Use the built-in Strands orchestrator agent

If you have a Strands-compatible LLM provider configured, you can delegate to the built-in orchestrator:

```python
from neurotrace.providers import get_model
from neurotrace.agents import create_orchestrator

model = get_model("anthropic", client_args={"api_key": "sk-..."})
# Also available: "openai", "bedrock", "gemini"

agent = create_orchestrator(model=model)
agent("Compare SecureBERT vs ModernBERT on cybersecurity knowledge")
```

The orchestrator has tools for dataset generation, tracing, charting, and interpretation.
It will drive the full pipeline autonomously.

### Option B: Drive the pipeline yourself (step-by-step below)

## Step-by-step protocol

### Step 1: Gather information from the user

Ask the following questions (skip any the user has already answered):

1. **Domain**: What knowledge domain? (e.g. cybersecurity, medicine, law, finance, programming)
2. **Goal**: What do you want to find out? (e.g. "Does BioBERT store drug-disease associations differently from BERT?")
3. **Models**: Which models to compare? Need display name + HuggingFace ID for each. At least one model, ideally two for comparison.
4. **Facts**: What factual associations to test? For each fact, you need:
   - A sentence template with `{}` where the subject goes (e.g. "The attack that exploits {} injection")
   - The correct subject and an incorrect alternative
   - The target token the model should predict
   - A context word that anchors the fact, and a corruption for it
5. **Variants** (optional): Custom prompt phrasing variants, or use defaults.

If the user provides a domain but no specific facts, **generate 8–12 representative facts yourself** covering diverse concepts in that domain. Ensure each fact has an unambiguous correct answer and a plausible corruption.

### Step 2: Build the DatasetSpec

Create a JSON spec and save it:

```python
from neurotrace.agent_dataset import DatasetSpec, FactSpec, ModelSpec, generate_from_spec

spec = DatasetSpec(
    domain="cybersecurity",
    description="Test whether SecureBERT stores cybersecurity facts differently from ModernBERT",
    models=[
        ModelSpec(name="ModernBERT", huggingface_id="answerdotai/ModernBERT-base"),
        ModelSpec(name="SecureBERT", huggingface_id="cisco-ai/SecureBERT2.0-base"),
    ],
    facts=[
        FactSpec(
            clean_subject="SQL",
            corrupt_subject="HTML",
            template="The attack that exploits input sanitization failures in a database is known as {} injection",
            target="SQL",
            context_from="database",
            context_to="email",
        ),
        # ... more facts ...
    ],
    output_dir="output",
)

dataset, config = generate_from_spec(spec, save_path="output/dataset.json")
```

### Step 3: Run the trace

```python
from neurotrace import CausalTracer
from neurotrace.tracer import save_results

results = []
results_dict = {}

for model_spec in spec.models:
    tracer = CausalTracer(model_spec.name, model_spec.huggingface_id)
    result = tracer.trace(dataset)
    results.append(result)
    results_dict[model_spec.name] = result.to_dict()
    tracer.release()

save_results(results, f"{spec.output_dir}/trace_results.json")
```

### Step 4: Generate charts

```python
from neurotrace import plot_comparison, plot_patching_flow, plot_heatmap, plot_peak_bars

out = spec.output_dir

# Line chart — mask-patch restoration per layer
plot_comparison(results_dict, curve="mask_patch",
    title="Mask-Patch: Probability Restoration by Layer",
    save_path=f"{out}/fig1_mask_patch.png")

# Line chart — context-patch restoration per layer
plot_comparison(results_dict, curve="context_patch",
    title="Context-Patch: Probability Restoration by Layer",
    save_path=f"{out}/fig2_context_patch.png")

# Patching flow diagram
peak = results[0].peak_layer()[0]
plot_patching_flow(num_layers=results[0].num_layers,
    highlighted_layer=peak, save_path=f"{out}/fig3_flow.png")

# Heatmap
plot_heatmap(results_dict, save_path=f"{out}/fig4_heatmap.png")

# Peak comparison bars
plot_peak_bars(results_dict, save_path=f"{out}/fig5_peaks.png")
```

### Step 5: Interpret the results

Report to the user:

1. **Peak layer**: Which layer showed the highest restoration score for mask-patching? This is where the model stores the domain knowledge.
2. **Peak magnitude**: How strong was the signal? Larger = the model relies more on context to retrieve the fact.
3. **Context-patch vs mask-patch**: If context-patch is flat (near zero), the model stores facts directly at the prediction position, not via context tokens.
4. **Clean-minus-corrupt baseline** (`clean_minus_corrupt` in the results): If positive, clean context helps. If negative, the model's knowledge is robust enough that corruption doesn't hurt — a sign of strong factual entrenchment.
5. **Cross-model comparison**: If two models peak at the same layer but with different magnitudes, the one with the *smaller* peak may actually have *stronger* knowledge (less to restore because corruption matters less).

## DatasetSpec JSON schema

```json
{
  "domain": "string (required)",
  "description": "string (required)",
  "models": [
    {
      "name": "string",
      "huggingface_id": "string"
    }
  ],
  "facts": [
    {
      "clean_subject": "string",
      "corrupt_subject": "string",
      "template": "string with {} placeholder",
      "target": "string",
      "context_from": "string",
      "context_to": "string"
    }
  ],
  "variants": [["prefix", "suffix"], ...],
  "output_dir": "string (default: 'output')"
}
```

## Fact design guidelines

When generating facts for the user:

- The template MUST contain `{}` where the subject goes
- `clean_subject` should be the unambiguously correct answer
- `corrupt_subject` should be a plausible but wrong alternative from the same category
- `target` is the token the model predicts (usually same as `clean_subject`)
- `context_from` is a word in the template that supports the correct answer
- `context_to` replaces it with something that shifts meaning but keeps the sentence grammatical
- Aim for 8–12 diverse facts per domain, covering different sub-topics
- Each fact should be testable as a fill-in-the-blank: "...is known as [MASK]..."

## Output files

After a run, the output directory will contain:

| File | Contents |
|------|----------|
| `dataset.json` | The generated prompt pairs |
| `run_config.json` | Models, domain, metadata |
| `trace_results.json` | Per-layer restoration scores |
| `fig1_mask_patch.png` | Mask-patch line chart |
| `fig2_context_patch.png` | Context-patch line chart |
| `fig3_flow.png` | Patching flow diagram |
| `fig4_heatmap.png` | Layer × model heatmap |
| `fig5_peaks.png` | Peak layer bar chart |

## Error handling

- If a model fails to load, `CausalTracer.__init__` will raise an exception. Catch it and report the HuggingFace ID to the user — they may need to `pip install` a specific tokenizer or use `trust_remote_code=True`.
- If the `[MASK]` token is not found, the tracer falls back to finding the subject token position. This works but is less precise for MLMs.
- Running on CPU is fine for base-size models (~120M params). For large models, suggest the user use a GPU.