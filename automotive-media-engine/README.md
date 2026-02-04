# Automotive Media Engine 🏎️

> **Precision engineering applied to content generation.** An automated pipeline for creating technical automotive videos at **zero marginal cost**, optimized for LinkedIn, TikTok, and YouTube.

## 🎯 Project Mission
Transform technical automotive expertise into a high-frequency content machine. Built for **scalability**, **observability**, and **maximum cost efficiency**.

---

## 🏗️ System Architecture

```
┌─────────────────┐
│  Next.js UI     │  (Alex's Dashboard)
└────────┬────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐
│ FastAPI Engine  │ ──▶ │ Redis Queue(RQ) │
└────────┬────────┘     └────────┬────────┘
         │                       ▼
         │              ┌─────────────────┐
         └────────────▶ │ Pipeline Worker │
                        └────────┬────────┘
                                 ▼
           ┌─────────────────────┴─────────────────────┐
           │                                           │
  ┌────────▼────────┐                         ┌────────▼────────┐
  │ Script (LLM)    │                         │ Audio (TTS)     │
  │ Gemini 2.0 Flash│                         │ Edge-TTS (Free) │
  └────────┬────────┘                         └────────┬────────┘
           │                                           │
  ┌────────▼────────┐                         ┌────────▼────────┐
  │ Visuals (Manim) │                         │ Cloud Storage   │
  │ Style-Aware Gen │                         │ Cloudflare R2   │
  └────────┬────────┘                         └────────┬────────┘
           │                                           │
           ▼                 [SOCIALS]                 ▼
      [OUTPUT]  ──────▶  LinkedIn / TikTok  ◀────── [URL]
```

## ✨ Key Features

*   🚀 **Zero Marginal Cost**: Using Edge-TTS and Gemini 2.0 Flash to achieve ~$0.0001 per video generation.
*   📊 **Real-time Observability**: Granular progress tracking (0-100%) and live status messages via API.
*   💰 **Billing System**: Automatic cost tracking for every job.
*   🎥 **Multi-Style Engine**: 4 distinct visual archetypes (Technical, Storytelling, Documentary, Minimalist).
*   🌐 **Cloud Native**: S3-compatible storage adapter ready for Cloudflare R2 (zero egress fees).

---

## ⚙️ Quick Start

### 1. Environment Setup
```bash
cd automotive-media-engine
/usr/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. API Configuration
Required in `.env`:
*   `GEMINI_API_KEY`: For script generation (Primary).
*   `ELEVENLABS_API_KEY`: (Optional) For premium voice cloning.
*   `S3_ENDPOINT_URL`: For R2/S3 storage.

### 3. Run the Pipeline
```bash
# Start Redis
docker run -p 6379:6379 -d redis

# Start Worker (Terminal 1)
export PYTHONPATH=$PYTHONPATH:. && ./venv/bin/python core/worker.py

# Start API (Terminal 2)
uvicorn api.main:app --reload

# Test via CLI (Terminal 3)
./venv/bin/python scripts/test_pipeline.py
```

---

## 📉 Cost Comparison

| Component | Premium (v1.0) | Zero-Cost (Current) | Savings |
|-----------|----------------|---------------------|---------|
| Script | Claude ($0.02) | **Gemini (Free/Low)** | 100% |
| Audio | ElevenLabs ($0.09) | **Edge-TTS ($0.00)** | 100% |
| Storage | GCP (Egress fees) | **Cloudflare R2 ($0.00)**| 100% |
| **Total** | **~$0.15/video** | **~$0.0001/video** | **99.9%** |

---

## 🤝 Project Structure
*   `api/`: FastAPI routes and request/response models.
*   `core/`: The heart of the engine (Pipeline, Scripting, Audio, Visuals).
*   `docs/`: Architecture Decision Records (ADR) and handoff guides.
*   `scripts/`: Testing and maintenance utilities.
*   `assets/`: Local static files (music, fonts, temporary files).

---
**Built with engineering discipline. Optimized for zero-cost scalability.**
