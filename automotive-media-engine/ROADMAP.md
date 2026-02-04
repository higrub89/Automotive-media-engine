# RYA.ai - Production Roadmap

> **Last Updated:** 2026-01-30  
> **Status:** Low-Cost Infrastructure Pivot & Observability Implemented ✅  
> **Next Phase:** Cloud Deployment & Social Media Automation 🚀

---

## 🎯 Current State (v1.1 - Low-Cost Production Ready)

### ✅ What's Working
- ✅ **Zero-Cost Audio**: Edge-TTS is now the default provider (99.9% cost reduction).
- ✅ **Observability**: Real-time progress updates (0-100%) and granular status messages.
- ✅ **Billing System**: Automated cost estimation (USD) per generation job.
- ✅ **S3-Compatible Storage**: Adapter ready for Cloudflare R2 (zero egress fees).
- ✅ **Modern Brain**: Gemini 2.0 Flash integrated for fast, low-cost script generation.
- ✅ **Multi-style Engine**: 4 archetypes (Technical, Storytelling, Documentary, Minimalist) with style-aware Manim visuals.
- ✅ **Structured Logging**: Loguru integration with job_id correlation.
- ✅ **Automated Testing**: Integration tests for pipeline and API.

### ⚠️ Known Blockers / Pending Issues
- **Music Mixing**: Music library needs more variety; fallback is generic.
- **Research Ratelimits**: DuckDuckGo search occasionally hits ratelimits in high volume.
- **Docker Networking**: Redis/Worker communication needs stabilization for cloud environments.

---

## 📋 Roadmap Phases

### **Phase 1: Production Hardening** (DONE ✅)
*Goal: Reliability and Debuggability.*
- [x] Structured Logging (Loguru).
- [x] Automated Integration Tests (Pytest).
- [x] Job ID Correlation across all modules.

### **Phase 2: Zero-Cost Economy** (DONE ✅)
*Goal: Marginal cost < $0.01 per video.*
- [x] **Edge-TTS** Integration (Free Neural Voices).
- [x] **Billing Tracker** (Real-time cost calculation).
- [x] **Gemini 2.0 Flash** migration.
- [x] **S3 Storage Adapter** (Ready for Cloudflare R2).

### **Phase 3: Scalability & Cloud Ops** (Week 4 - IN PROGRESS 🏗️)
- [ ] **Hetzner Cloud Deployment**: Move from local to CPX21 VPS.
- [ ] **Job Persistence**: Ensure Redis jobs survive server restarts.
- [ ] **Retry Logic**: Implement automated retries for transient failures (e.g., image gen 404s).
- [ ] **Docker Swarm/Compose**: Finalize production-ready stack orchestration.

### **Phase 4: Monitoring & Advanced Visuals** (Week 5)
- [ ] **UI Performance Dashboard**: Visualize cost trends and render times.
- [ ] **Cascading Visual Engine**: Implement Pollinations -> Flux -> DALL-E 3 fallback logic.
- [ ] **B-Roll Auto-Search**: Higher precision style-adjectives for Pexels search.

### **Phase 5: Frontend & User Experience** (Alex's Current Task 🎨)
- [ ] Create **Next.js Dashboard**.
- [ ] Implement **Progress Polling UI** with real-time status messages.
- [ ] Video History & Download Gallery.
- [ ] **Handoff Documentation**: Completed in `docs/frontend_handoff.md`.

### **Phase 6: Distribution & Revenue** (Next Priority 💰)
- [ ] **LinkedIn Autopublish**: One-click upload with AI-generated captions.
- [ ] **Analytics loop**: Feed view metrics back into the Research engine.
- [ ] **Multi-platform formatting**: Auto-crop videos for TikTok/Shorts (9:16).

---

## 🚀 Immediate Next Steps

1. **Frontend Support**: Assist Alex in connecting the Next.js UI to the `/generate` and `/status` endpoints.
2. **Infrastructure**: Deploy the Redis + Worker + API stack to a Hetzner trial instance.
3. **LinkedIn Integration**: Research and implement the LinkedIn Video API for automated posting.

---

## 📊 Success Metrics

| Metric | Start (v1.0) | Current (v1.1) | Target (Phase 6) |
|--------|---------|------------------|------------------|
| Marginal Cost/Video | ~$0.15 | **<$0.001** | <$0.001 |
| Job Feedback | None (Static) | **Live (Granular)** | Live (Visual) |
| Render Time (60s) | ~2 min | ~90 sec | <60 sec |
| Automation Level | Manual CLI | **Queue Based** | **Autopublish** |

---

*Last Pipeline Verification: 2026-01-30 - PASSED (Cost: $0.0001) ✅*
