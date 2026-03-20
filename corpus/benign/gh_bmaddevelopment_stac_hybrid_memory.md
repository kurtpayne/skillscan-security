---
name: hybrid_memory
description: >
  Hybrid RAG memory skill combining vector embeddings (ChromaDB) and a
  directed knowledge graph (NetworkX). Runs both retrieval modes in a single
  call or independently. Best for coding agents that need both semantic
  similarity search AND structural relationship traversal over a codebase.

tools:
  - name: hybrid_ingest
    description: Ingests a codebase into both the vector index and the knowledge graph.
    parameters:
      type: object
      required: [path]
      properties:
        path:
          type: string
          description: Absolute or relative path to the codebase root.

  - name: hybrid_retrieve
    description: >
      Runs vector search and/or graph traversal. Both modes are optional but
      at least one must be provided.
    parameters:
      type: object
      properties:
        query:
          type: string
          description: Natural language query for semantic vector search.
        graph_query:
          type: string
          description: >
            Graph traversal query. Patterns:
            "X calls" | "functions called by X" | "class X" | "file X"
        n_results:
          type: integer
          description: Number of vector results to return. Default 5.
        filter_kind:
          type: string
          description: "Filter vector results by chunk type: function | class | method | module_chunk"
        filter_file:
          type: string
          description: Filter vector results by partial file path.
        filter_lang:
          type: string
          description: "Filter vector results by language: python | ts | js | tsx | jsx"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: bmaddevelopment-stack/openclaw-skill-hybrid-memory
# corpus-url: https://github.com/bmaddevelopment-stack/openclaw-skill-hybrid-memory/blob/05c5a518288a25a9362595fcdd3cc940482f7c04/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Hybrid Memory Skill

This skill combines **vector semantic search** and **graph structural traversal**
into a single unified retrieval interface. Use it when the agent needs both
*"what looks like this?"* (vector) and *"what connects to this?"* (graph).

## When to Use This Skill

Use `hybrid_memory` for complex coding tasks that require both modes:

- *"Find authentication code and show what it calls"*
- *"What functions handle retries, and what do they depend on?"*
- *"Explain the data pipeline and trace its call graph"*

## Component Skills

This skill is the composition of two standalone skills:

| Skill | Repo | Use When |
|---|---|---|
| `vector_memory` | `openclaw-skill-vector-memory` | Semantic search only, resource-constrained |
| `graph_memory` | `openclaw-skill-graph-memory` | Structural traversal only, no embedding needed |
| `hybrid_memory` | `openclaw-skill-hybrid-memory` | Both modes needed simultaneously |

## Vector Search

Returns ranked chunks by cosine similarity with full metadata:
`score`, `chunk_kind`, `name`, `qualified_name`, `file_path`,
`line_start`, `line_end`, `token_estimate`, `docstring`, `language`, `code`.

Optional filters: `--kind`, `--file`, `--lang`.

## Graph Traversal Patterns

| Pattern | Returns |
|---|---|
| `"X calls"` | All functions/methods directly called by X |
| `"functions called by X"` | All callers of X (reverse lookup) |
| `"class X"` | All methods defined on class X |
| `"file X"` | All entities defined in file X (partial match) |

## Dependencies

```
chromadb
sentence-transformers
networkx
```