---
name: voice-assistant-platform
description: Multi-tenant, callable voice assistant platform for company-specific information.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: papdawin/customer-service-assistant
# corpus-url: https://github.com/papdawin/customer-service-assistant/blob/b7c0112453f61640bd53a0664e985e433ea73039/skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Voice Assistant Platform

## Purpose
Build and operate a callable, company-facing voice assistant that answers questions about a business (location, opening hours, contact methods, reachability, services, and policies). The platform is designed for multi-tenant deployments: each company maintains its own knowledge base, while core speech and language services are shared to keep operations efficient.

## What This System Does
- Accepts live or recorded audio from callers.
- Detects speech segments to avoid sending silence and noise downstream.
- Transcribes speech into text with STT.
- Retrieves company-specific knowledge with RAG.
- Generates a concise, accurate answer with the shared LLM.
- Synthesizes spoken replies with TTS.
- Returns audio and text results with timing data for monitoring and UX feedback.

## Multi-Tenant Model
- Each company is a tenant with its own data and retrieval index.
- The RAG service is instantiated per tenant and points at tenant data sources.
- STT, TTS, VAD, and the LLM are shared services across all tenants.
- The backend gateway routes requests to the correct tenant RAG based on deployment config.

## Core Services
- **RAG**: Per-tenant retrieval service. Companies can update their own information without changing core services.
- **STT**: Shared speech-to-text service (Whisper). Converts audio to text.
- **TTS**: Shared text-to-speech service (Piper). Converts responses into audio.
- **VAD**: Shared voice activity detection. Identifies speech segments to improve accuracy and efficiency.
- **Backend**: Orchestrates the pipeline and exposes HTTP + WebSocket APIs.
- **Frontend**: Serves the UI for testing or operational use.

## Typical Data Sources Per Company
- Location and address details
- Opening hours and holiday schedules
- Contact and reachability information
- Services offered and pricing/availability
- FAQ and policy documents

## Operational Goals
- Consistent responses across multiple companies with tenant-specific accuracy.
- Low-latency speech pipeline with observable timings.
- Easy onboarding of new companies by providing their data to RAG.
- Shared infrastructure for compute-heavy services to reduce cost.

## Main Components
- End-to-end audio pipeline: VAD -> STT -> RAG -> LLM -> TTS.
- Tenant-specific indices and retrieval settings.
- Standardized APIs for health, config, and inference.
- Streaming support for live voice interactions.