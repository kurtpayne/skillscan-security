---
name: semantic-search
version: "1.0"
description: Perform semantic search over a document collection using embeddings.
tags: [ai, embeddings, search]
allowed-tools: [Read, Bash]
---
## Overview
Builds a simple semantic search index from a document collection
and returns the most relevant documents for a query.

## Usage
1. Read documents from the specified directory.
2. Generate embeddings using sentence-transformers.
3. Compute cosine similarity between the query and all documents.
4. Return the top-k most similar documents with similarity scores.

## Notes
Uses local sentence-transformers model. Does not call external APIs.
