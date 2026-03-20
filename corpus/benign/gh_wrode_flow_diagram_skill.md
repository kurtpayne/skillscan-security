---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: wrode/flow-diagram
# corpus-url: https://github.com/wrode/flow-diagram/blob/654b83350db72f0b495d1bc85db35c61fc3911f1/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Flow Diagram

Trace data flow through a codebase and produce an interactive HTML diagram.

Trigger: `/flow-diagram`

## Usage

```
/flow-diagram src/api/handler.ts
/flow-diagram "what happens when a user submits a form"
/flow-diagram src/routes/index.ts -> service -> database
```

The argument is either:
- A file path (entry point to trace from)
- A natural language description of the flow to diagram
- A path with `->` arrows describing the flow to trace

## Process

### 1. Investigate

Read the actual source code. Do NOT guess or hallucinate connections. Every node and edge in the diagram must come from real imports, function calls, API routes, database queries, or event dispatches found in the code.

Trace strategy:
- Start from the entry point file/function
- Follow imports and function calls
- Track data shape transformations (what goes in, what comes out)
- Note async boundaries (API calls, database queries, queue jobs, webhooks)
- Stop at external service boundaries -- show them as terminal nodes

For each step, record:
- File path and line number of the key call
- Function/method name
- Data shape entering and leaving (brief: e.g., "txHash: string" -> "TraceResult")
- Whether it's sync, async, or a separate job/request
- A short description of what the function does (1-2 sentences)

### 2. Build the node metadata

For every node in the diagram, prepare a JSON metadata object with:
- `id`: unique node ID used in Mermaid
- `label`: display name (function or file name)
- `file`: relative file path
- `line`: line number
- `layer`: one of "api", "service", "database", "async"
- `description`: what this step does (1-2 sentences)
- `dataIn`: data shape entering (e.g., "{ txHash: string, chainId: number }")
- `dataOut`: data shape leaving (e.g., "TraceResult | null")
- `code`: the key line(s) of code showing the call (2-5 lines max)

This metadata powers the interactive detail panel.

### 3. Build the Mermaid diagram

Use `flowchart TD` (top-down) for linear flows, `flowchart LR` (left-right) for branching.

Node naming rules:
- Use the actual function or file name as the node label
- Color-code by layer using classDef:
  - API endpoints: blue (#4a9eff)
  - Services/business logic: green (#4ade80)
  - Database/external: orange (#fbbf24)
  - Queue/async boundaries: purple (#c084fc)

Edge labels show what data moves between nodes (keep brief).

Use subgraphs for logical groupings when the flow crosses boundaries.

### 4. Output

Write a single self-contained HTML file to `~/.agent/diagrams/flow-<name>.html`.

The HTML file must include:

**Diagram area (left/top):**
- Mermaid diagram with zoom controls (+/-, scroll-to-zoom, reset)
- Nodes are clickable -- clicking a node opens the detail panel for that node

**Detail panel (right side or bottom):**
- Shows when a node is clicked
- Displays: node name, file:line, description, data in/out shapes, code snippet
- Has a close button
- Slides in smoothly
- Highlights the selected node in the diagram

**Legend** below the diagram mapping colors to layers.

Use this template (fill in the placeholders):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flow: {name}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #111; color: #ccc; font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace; }

  .layout { display: grid; grid-template-columns: 1fr 360px; height: 100vh; }
  .layout.panel-closed { grid-template-columns: 1fr 0; }

  /* Diagram side */
  .diagram-side { overflow: hidden; display: flex; flex-direction: column; }
  .header { padding: 16px 20px 0; }
  .header h1 { font-size: 16px; font-weight: 500; color: #eee; }
  .header p { font-size: 11px; color: #555; margin-top: 2px; }

  .diagram-wrap {
    flex: 1; overflow: auto; position: relative; padding: 16px;
  }
  .diagram-wrap .mermaid {
    transition: transform 0.15s ease;
    transform-origin: top left;
    cursor: default;
  }
  .diagram-wrap.is-zoomed { cursor: grab; }
  .diagram-wrap.is-panning { cursor: grabbing; user-select: none; }

  .zoom-controls {
    position: absolute; top: 8px; right: 8px; display: flex; gap: 2px;
    background: #1a1a1a; border: 1px solid #333; border-radius: 4px; padding: 2px; z-index: 10;
  }
  .zoom-controls button {
    width: 28px; height: 28px; border: none; background: transparent;
    color: #666; font-size: 14px; cursor: pointer; border-radius: 3px;
  }
  .zoom-controls button:hover { background: #252525; color: #ccc; }

  .legend {
    display: flex; gap: 14px; padding: 8px 20px; border-top: 1px solid #222;
    font-size: 10px; color: #555;
  }
  .legend-item { display: flex; align-items: center; gap: 5px; }
  .legend-dot { width: 8px; height: 8px; border-radius: 2px; }

  /* Detail panel */
  .panel {
    background: #161616; border-left: 1px solid #222;
    overflow-y: auto; transition: width 0.2s, opacity 0.2s;
    padding: 20px;
  }
  .panel-closed .panel { width: 0; padding: 0; opacity: 0; overflow: hidden; }

  .panel-close {
    float: right; background: none; border: 1px solid #333;
    color: #666; font-size: 11px; padding: 2px 8px; border-radius: 3px; cursor: pointer;
  }
  .panel-close:hover { color: #ccc; border-color: #555; }

  .panel-label {
    font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px;
    color: #555; margin-top: 16px; margin-bottom: 4px;
  }
  .panel-label:first-of-type { margin-top: 8px; }

  .panel-title { font-size: 15px; color: #eee; font-weight: 500; }

  .panel-file {
    font-size: 11px; color: #4a9eff; margin-top: 2px;
    text-decoration: none; cursor: default;
  }

  .panel-desc { font-size: 12px; color: #999; line-height: 1.5; }

  .panel-data {
    font-size: 11px; color: #aaa; background: #1c1c1c;
    border: 1px solid #282828; border-radius: 4px; padding: 8px 10px;
    white-space: pre-wrap; line-height: 1.5;
  }

  .panel-code {
    font-size: 11px; color: #bbb; background: #0d0d0d;
    border: 1px solid #222; border-radius: 4px; padding: 10px 12px;
    overflow-x: auto; line-height: 1.6; white-space: pre;
  }
  .panel-code .line-num { color: #444; margin-right: 12px; user-select: none; }

  .panel-empty {
    text-align: center; color: #444; font-size: 12px;
    margin-top: 40vh; transform: translateY(-50%);
  }

  /* Mermaid node click targets */
  .mermaid .node { cursor: pointer; }
  .mermaid .node:hover rect,
  .mermaid .node:hover polygon,
  .mermaid .node:hover circle { filter: brightness(1.3); }
  .mermaid .node.selected rect,
  .mermaid .node.selected polygon,
  .mermaid .node.selected circle { stroke: #fff; stroke-width: 2px; }

  @media (max-width: 900px) {
    .layout { grid-template-columns: 1fr; grid-template-rows: 1fr auto; }
    .panel { border-left: none; border-top: 1px solid #222; max-height: 45vh; }
    .panel-closed .panel { max-height: 0; }
  }
</style>
</head>
<body>

<div class="layout panel-closed" id="layout">
  <div class="diagram-side">
    <div class="header">
      <h1>{title}</h1>
      <p>{description}</p>
    </div>
    <div class="diagram-wrap" id="diagramWrap">
      <div class="zoom-controls">
        <button onclick="zoomDiagram(1.2)" title="Zoom in">+</button>
        <button onclick="zoomDiagram(0.8)" title="Zoom out">&minus;</button>
        <button onclick="resetZoom()" title="Reset">&#8634;</button>
      </div>
      <pre class="mermaid" id="diagram">
{mermaid_content}
      </pre>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#4a9eff"></div> API</div>
      <div class="legend-item"><div class="legend-dot" style="background:#4ade80"></div> Service</div>
      <div class="legend-item"><div class="legend-dot" style="background:#fbbf24"></div> External</div>
      <div class="legend-item"><div class="legend-dot" style="background:#c084fc"></div> Async</div>
    </div>
  </div>

  <div class="panel" id="panel">
    <div id="panelContent">
      <p class="panel-empty">Click a node to inspect</p>
    </div>
  </div>
</div>

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'basis' },
    securityLevel: 'loose'
  });

  // After render, attach click handlers to nodes
  setTimeout(() => {
    document.querySelectorAll('.mermaid .node').forEach(node => {
      node.style.cursor = 'pointer';
      node.addEventListener('click', () => {
        const nodeId = node.id?.replace(/^flowchart-/, '').replace(/-\d+$/, '') || '';
        selectNode(nodeId);
      });
    });
  }, 500);
</script>

<script>
  // -- Node metadata (filled by the agent) --
  const NODE_DATA = {node_data_json};

  // -- Zoom --
  let scale = 1;
  const wrap = document.getElementById('diagramWrap');
  const dia = () => document.querySelector('.mermaid');

  function zoomDiagram(factor) {
    scale = Math.min(Math.max(scale * factor, 0.3), 5);
    dia().style.transform = 'scale(' + scale + ')';
    wrap.classList.toggle('is-zoomed', scale > 1);
  }
  function resetZoom() {
    scale = 1;
    dia().style.transform = 'scale(1)';
    wrap.classList.remove('is-zoomed');
  }
  wrap.addEventListener('wheel', e => {
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    zoomDiagram(e.deltaY < 0 ? 1.1 : 0.9);
  }, { passive: false });

  // Pan
  let panStart = null;
  wrap.addEventListener('mousedown', e => {
    if (e.target.closest('.zoom-controls')) return;
    if (scale <= 1) return;
    panStart = { x: e.clientX, y: e.clientY, sl: wrap.scrollLeft, st: wrap.scrollTop };
    wrap.classList.add('is-panning');
  });
  window.addEventListener('mousemove', e => {
    if (!panStart) return;
    wrap.scrollLeft = panStart.sl - (e.clientX - panStart.x);
    wrap.scrollTop = panStart.st - (e.clientY - panStart.y);
  });
  window.addEventListener('mouseup', () => { panStart = null; wrap.classList.remove('is-panning'); });

  // -- Node selection --
  function selectNode(nodeId) {
    const data = NODE_DATA[nodeId];
    if (!data) return;

    const layout = document.getElementById('layout');
    layout.classList.remove('panel-closed');

    // Highlight
    document.querySelectorAll('.mermaid .node').forEach(n => n.classList.remove('selected'));
    const el = document.getElementById('flowchart-' + nodeId + '-0')
             || document.querySelector('[id^="flowchart-' + nodeId + '"]');
    if (el) el.classList.add('selected');

    const p = document.getElementById('panelContent');
    const layerColors = { api: '#4a9eff', service: '#4ade80', database: '#fbbf24', async: '#c084fc' };
    const layerColor = layerColors[data.layer] || '#888';

    let codeHtml = '';
    if (data.code) {
      const lines = data.code.split('\n');
      const startLine = data.line || 1;
      codeHtml = lines.map((l, i) =>
        '<span class="line-num">' + (startLine + i) + '</span>' + escHtml(l)
      ).join('\n');
    }

    p.innerHTML = `
      <button class="panel-close" onclick="closePanel()">close</button>
      <div class="panel-label">Node</div>
      <div class="panel-title" style="color:${layerColor}">${escHtml(data.label)}</div>
      <div class="panel-file">${escHtml(data.file)}:${data.line || '?'}</div>

      <div class="panel-label">Description</div>
      <div class="panel-desc">${escHtml(data.description || 'No description')}</div>

      <div class="panel-label">Data In</div>
      <div class="panel-data">${escHtml(data.dataIn || 'N/A')}</div>

      <div class="panel-label">Data Out</div>
      <div class="panel-data">${escHtml(data.dataOut || 'N/A')}</div>

      ${data.code ? `<div class="panel-label">Code</div><pre class="panel-code">${codeHtml}</pre>` : ''}
    `;
  }

  function closePanel() {
    document.getElementById('layout').classList.add('panel-closed');
    document.querySelectorAll('.mermaid .node').forEach(n => n.classList.remove('selected'));
  }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
</script>
</body>
</html>
```

### 5. Report

After opening the file, print a brief summary in chat:
- The flow path in one line (A -> B -> C -> D)
- File path of the diagram
- Any notable findings (circular deps, dead code paths, missing error handling)

## Rules

- NEVER fabricate connections. Every edge must be traceable to an import, function call, or API route in the code.
- Keep diagrams focused. If a flow touches 20+ files, group related files into subgraph clusters.
- Use subgraphs for logical boundaries (e.g., "API Layer", "Service Layer", "Database").
- Show data shape at key transformation points as edge labels.
- External services (databases, third-party APIs, message queues) are always terminal leaf nodes colored orange.
- When the entry point is ambiguous, ask the user to clarify rather than guessing.
- Node IDs in Mermaid must match the keys in NODE_DATA exactly so click handlers work.
- The `code` field in NODE_DATA should show the most relevant 2-5 lines from that step (the actual function call or key logic), not the entire file.
- Always use `securityLevel: 'loose'` in Mermaid config so click handlers work.