---
name: kagenti-a2a-adapter
description: Wrap existing agent code with A2A (Agent-to-Agent) protocol support for deployment on Kagenti. This skill should be used when the user has an existing AI agent (CrewAI, LangGraph, OpenAI Agents SDK, or custom Python) and wants to make it A2A-ready, deploy it on Kagenti or any A2A-compatible Kubernetes platform, or containerize an agent with proper protocol endpoints. Triggers include requests like "make my agent A2A ready", "deploy my agent on Kagenti", "wrap my CrewAI agent for Kubernetes", "add A2A support to my agent", "containerize my LangGraph agent", or "generate Kagenti manifests for my agent".
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zanetworker/kagenti-a2a-adapter
# corpus-url: https://github.com/zanetworker/kagenti-a2a-adapter/blob/945ceb4a11af2efaa3465291d7e315684161f430/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Kagenti A2A Adapter

Generate A2A protocol adapters and Kagenti deployment manifests for existing agent code. The agent code stays untouched; the adapter wraps it in a FastAPI server that speaks the A2A protocol.

## What This Skill Produces

| File | Purpose |
|------|---------|
| `a2a_server.py` | FastAPI app with A2A endpoints (`/task`, `/.well-known/agent-card.json`, `/health`) |
| `requirements.txt` | Python dependencies for the adapter |
| `Dockerfile` | Container image build file |
| `k8s/deployment.yaml` | Kubernetes Deployment + Service with `kagenti.io/type: agent` label |
| `k8s/agentruntime.yaml` | Optional AgentRuntime CR for per-workload identity/trace overrides |
| `k8s/agentcard.yaml` | AgentCard CR for Kubernetes-native A2A agent discovery |

## Workflow

### 1. Detect or Ask for Framework

Inspect the user's agent code to determine the framework. Look for these import patterns:

| Framework | Detection Pattern | Template |
|-----------|------------------|----------|
| **CrewAI** | `from crewai import Agent, Crew, Task` | `a2a_server_crewai.py.tmpl` |
| **LangGraph** | `from langgraph.graph import StateGraph` | `a2a_server_langgraph.py.tmpl` |
| **OpenAI Agents SDK** | `from agents import Agent, Runner` | `a2a_server_openai.py.tmpl` |
| **Custom Python** | None of the above | `a2a_server_custom.py.tmpl` |

If the framework cannot be determined from the code, ask the user.

### 2. Identify Agent Entry Point

Find the agent's callable entry point in the user's code:

- **CrewAI**: The `Crew(...)` instance (e.g., `my_crew`). Called via `crew.kickoff(inputs={"query": msg})`
- **LangGraph**: The compiled graph from `graph.compile()` (e.g., `app`). Called via `graph.invoke({"messages": [HumanMessage(content=msg)]})`
- **OpenAI Agents SDK**: The `Agent(...)` instance (e.g., `agent`). Called via `await Runner.run(agent, msg)`
- **Custom**: A callable function or class. Read the code to determine the call pattern.

Determine the module name and entry point variable name. These become `{{AGENT_MODULE}}` and `{{AGENT_ENTRY_POINT}}` in the template.

### 3. Gather Metadata

Collect from the user or infer from the code:

| Variable | Description | Default |
|----------|-------------|---------|
| `{{AGENT_NAME}}` | Kebab-case name for the agent | Infer from filename or ask |
| `{{AGENT_DESCRIPTION}}` | One-line description of what the agent does | Infer from docstrings or ask |
| `{{IMAGE_REGISTRY}}` | Container registry prefix | `quay.io/<username>` or ask |
| `{{AGENT_MODULE}}` | Python module containing the agent | Detected in step 2 |
| `{{AGENT_ENTRY_POINT}}` | Variable name of the agent instance | Detected in step 2 |

### 4. Generate Files

Read the appropriate template from this skill's `assets/templates/` directory and substitute all `{{VARIABLE}}` placeholders with the collected values.

**a2a_server.py**: Select the template matching the detected framework. Substitute all placeholders. For custom agents, adapt the invocation line to match the agent's actual interface by reading the agent code.

**requirements.txt**: Include `fastapi`, `uvicorn[standard]`, `sse-starlette`. Add framework-specific dependencies based on what the agent code imports. If the agent has its own `requirements.txt` or `pyproject.toml`, merge dependencies.

**Dockerfile**: Use the `Dockerfile.tmpl` template. Verify the agent code structure matches the COPY expectations.

**k8s/deployment.yaml**: Substitute `{{AGENT_NAME}}` and `{{IMAGE_REGISTRY}}`. Add any environment variables the agent needs (API keys as secretKeyRef).

**k8s/agentruntime.yaml**: Generate only if the user requests custom identity or tracing config. Otherwise, inform the user that Kagenti platform defaults handle identity and tracing automatically, and this file is not required.

**k8s/agentcard.yaml**: Always generate. Use the `agentcard.yaml.tmpl` template. The AgentCard CR enables Kubernetes-native A2A agent discovery. The controller periodically fetches the agent card from the running pod's `/.well-known/agent-card.json` endpoint and caches it in the CR status. It also handles SPIRE x5c signature verification for zero-trust agent identity.

Key AgentCard fields:
- `spec.targetRef` -- points to the Deployment (same as AgentRuntime). Uses `apiVersion: apps/v1`, `kind: Deployment`, `name: <agent-name>`.
- `spec.syncPeriod` -- how often to re-fetch the card (default: `"30s"`).
- `spec.identityBinding.trustDomain` -- override SPIFFE trust domain for this agent (optional).
- `spec.identityBinding.strict` -- when `true`, binding failures trigger network isolation. When `false` (default), failures are audit-only.

The controller populates `status.card` with the fetched A2A card data (name, description, skills, capabilities), `status.validSignature` with signature verification result, and `status.bindingStatus` with identity binding evaluation.

### 5. Verify Structure

After generation, confirm the output directory contains:

```
<agent-dir>/
  a2a_server.py          # Generated A2A adapter
  requirements.txt       # Dependencies
  Dockerfile             # Container build
  <agent source files>   # User's original code (untouched)
  k8s/
    deployment.yaml      # K8s Deployment + Service
    agentcard.yaml       # AgentCard CR for A2A discovery
    agentruntime.yaml    # Optional AgentRuntime CR
```

### 6. Provide Next Steps

After generating all files, display build, test, and deploy instructions:

**Build and push:**
```bash
docker build -t <registry>/<agent-name>:latest .
docker push <registry>/<agent-name>:latest
```

**Test locally:**
```bash
pip install -r requirements.txt
python a2a_server.py
# Verify agent card:
curl http://localhost:8081/.well-known/agent-card.json
# Send a test task:
curl -N -X POST http://localhost:8081/task \
  -H "Content-Type: application/json" \
  -d '{"id":"test-1","messages":[{"role":"user","parts":[{"type":"text","text":"Hello"}]}]}'
```

**Deploy to Kagenti:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/agentcard.yaml
# Only if per-workload overrides are needed:
kubectl apply -f k8s/agentruntime.yaml
```

## A2A Protocol Reference

The adapter implements the minimum viable A2A server:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/.well-known/agent-card.json` | GET | Agent capability discovery |
| `/task` | POST | Task execution (returns SSE stream) |
| `/task/{id}` | GET | Task status polling |
| `/health` | GET | K8s readiness/liveness probe |

Task lifecycle: `submitted` -> `working` -> `completed` | `failed`

SSE events:
- `status` -- task state transition: `{"id": "...", "status": {"state": "working"}}`
- `artifact` -- task output: `{"id": "...", "artifact": {"parts": [{"type": "text", "text": "..."}]}}`

## Framework-Specific Notes

**CrewAI**: Synchronous framework. Wrap `crew.kickoff()` in `asyncio.to_thread()`. `CrewOutput` converts to string via `str(result)`.

**LangGraph**: Extract last message from returned state dict: `result["messages"][-1].content`. Requires `langchain-core` for `HumanMessage`. If the graph is async-native, use `await graph.ainvoke(...)` directly.

**OpenAI Agents SDK**: Already async. Use `await Runner.run(agent, msg)` directly. Result has `.final_output` property.

**Custom**: Read the agent code to determine the call interface. Common patterns: `agent.run(msg)`, `agent.invoke(msg)`, `agent(msg)`, `await agent.arun(msg)`. Adapt the invocation line accordingly.