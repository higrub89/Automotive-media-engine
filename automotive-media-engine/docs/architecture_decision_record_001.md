# Architecture Decision Record (ADR) 001: Cloud-Native Low-Cost Infrastructure

## Status
Accepted

## Context
The project needs to scale from a local prototype to a production-ready system capable of generating hundreds of videos per month. The initial reliance on premium APIs (ElevenLabs, Claude) and potentially expensive cloud providers (AWS/GCP) poses a financial risk. The target infrastructure must be extremely cost-efficient while maintaining quality. We do not have high-end local hardware (GPU) for self-hosting large models.

## Decision
We will adopt a **"Cloud-Native Low-Cost"** strategy, prioritizing managed services with generous free tiers or low fixed costs over expensive pay-as-you-go GPU instances or premium AI APIs.

### 1. Audio Synthesis (TTS)
*   **From:** ElevenLabs (Default)
*   **To:** **Edge-TTS (Default)**
*   **Rationale:** ElevenLabs costs ~$0.30 per minute of audio. For high volume, this is unsustainable. Edge-TTS is free, runs on CPU, and offers high-quality neural voices (e.g., `es-ES-AlvaroNeural`). ElevenLabs will be kept as a "Premium Tier" option.

### 2. Compute Infrastructure
*   **From:** Local / Google Cloud Run (Potential)
*   **To:** **Hetzner Cloud (CPX Series)**
*   **Rationale:** Hetzner limits bandwidth costs and offers high-performance CPUs (AMD EPYC) at a fraction of the cost of AWS/GCP (approx. €5-10/month vs €50+).

### 3. Object Storage
*   **From:** Google Cloud Storage
*   **To:** **Cloudflare R2**
*   **Rationale:** Zero egress fees. Essential for a video platform where serving content consumes massive bandwidth. 100% S3 compatible API.

### 4. Language Models (LLM)
*   **Decision:** Stick with **Google Gemini 2.0 Flash**.
*   **Rationale:** It is currently faster and significantly cheaper (essentially free for our volume) than self-hosting Llama 3 on a GPU server or using GPT-4/Claude Opus.

## Consequences

### Pros
*   **Dramatic Cost Reduction:** Cost per video drops from ~$0.15 to <$0.01.
*   **Scalability:** R2 and Hetzner handle bandwidth/compute scaling without linear cost explosions.
*   **Simplicity:** Avoiding self-hosted LLMs/SD removes the need for complex GPU cluster management (Kubernetes/vGPU).

### Cons
*   **Voice Emotionality:** Edge-TTS is less expressive than ElevenLabs. We accept this trade-off for the MVP/Scale phase.
*   **Vendor Lock-In (Minor):** Moving to Hetzner requires managing a VPS (Docker), slightly more ops work than serverless Cloud Run.

## Roadmap Updates
*   Prioritize `audio_factory.py` refactor to make Edge-TTS default.
*   Implement `S3Storage` class to replace `GCPStorage`, supporting Cloudflare R2.
