---
name: setup-rag-pipeline
version: "0.9"
description: Set up a basic RAG pipeline with a local vector store.
tags: [ai, rag, embeddings]
allowed-tools: [Read, Write, Bash]
---
## Overview
Sets up a retrieval-augmented generation pipeline using a local
ChromaDB vector store and sentence-transformers embeddings.

## Usage
1. Read documents from the specified directory.
2. Chunk documents into 512-token segments with 64-token overlap.
3. Generate embeddings and store in a local ChromaDB collection.
4. Test the pipeline with a sample query.

## Notes
Uses local models and storage only. Does not call external APIs.
