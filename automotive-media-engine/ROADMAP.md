# RYA.ai - Production Roadmap

> **Last Updated:** 2026-01-27  
> **Status:** Multi-Style Engine Operational ✅  
> **Next Phase:** Production Hardening 🔧

---

## 🎯 Current State (v1.0 - MVP Complete)

### ✅ What's Working
- ✅ Multi-style content engine (4 archetypes: Technical, Storytelling, Documentary, Minimalist)
- ✅ Script generation with LLM (Gemini/Claude) + Research integration
- ✅ Audio narration (ElevenLabs + Edge-TTS fallback)
- ✅ Manim visual generation with style-aware scenes
- ✅ Background music mixing (FFmpeg)
- ✅ FastAPI backend with async job processing
- ✅ GCP Storage integration
- ✅ Manual end-to-end pipeline verification

### ⚠️ Known Limitations
- Logging via `print()` statements (not production-grade)
- No automated testing (fragile codebase)
- No job persistence (lost on server restart)
- No monitoring/observability
- Not containerized (manual deployment)

---

## 📋 Roadmap Phases

### **Phase 1: Production Hardening** (Week 1-2) 🔥 **PRIORITY**

**Goal:** Make the system reliable and debuggable for production use.

#### 1.1 Structured Logging ✅
- [x] Install `loguru` dependency
- [x] Create `core/logger.py` with centralized config
- [x] Replace all `print()` in:
  - [x] `core/pipeline.py`
  - [x] `core/script_engine.py` (verified via pipeline tests)
  - [x] `core/audio_factory.py`
  - [x] `core/visual_assembly.py` (verified via pipeline tests)
  - [x] `core/music_factory.py`
  - [x] `api/router.py`
- [x] Configure log levels (DEBUG, INFO, WARNING, ERROR)
- [x] Add JSON logging for GCP Cloud Logging compatibility
- [x] Include job_id correlation in all logs

**Success Criteria:** Can trace any job failure through structured logs.

---

#### 1.2 Automated Testing ✅
- [x] Install `pytest` + `pytest-asyncio`
- [x] Create `tests/integration/` directory
- [x] Write integration tests:
  - [x] `test_pipeline.py` - End-to-end storytelling & technical video
  - [x] `test_api.py` - API endpoint & status validation
- [x] Mock external APIs (Gemini, ElevenLabs, DuckDuckGo)
- [x] Configure GitHub Actions CI workflow
- [x] Add badge to README.md showing test status

**Success Criteria:** All tests pass on every push. CI fails if tests break.

---

### **Phase 2: Scalability & Resilience** (Week 3-4)

#### 2.1 Job Queue with Persistence
- [ ] Evaluate: Redis vs Google Cloud Tasks
- [ ] Implement job state machine (`queued` → `processing` → `completed`/`failed`)
- [ ] Add retry logic for transient failures
- [ ] Implement job TTL (auto-cleanup after 24h)
- [ ] Update API to return job progress percentage
- [ ] Add `/video/retry/{job_id}` endpoint

**Success Criteria:** Jobs survive server restarts. Failed jobs can be retried.

---

#### 2.2 Containerization
- [ ] Create `Dockerfile` with multi-stage build
- [ ] Create `docker-compose.yml` for local development
- [ ] Configure `.dockerignore`
- [ ] Test container locally
- [ ] Push to Google Artifact Registry
- [ ] Deploy to Cloud Run (GCP)

**Success Criteria:** Can deploy the entire app with a single `docker run` command.

---

### **Phase 4: Monitoring & Observability** (Week 5-6)

#### 4.1 Performance Metrics
- [ ] Implement video generation duration tracking
- [ ] Track API credit usage (Gemini, ElevenLabs, Anthropic)
- [ ] Monitor FFmpeg rendering times
- [ ] Configure Google Cloud Monitoring dashboards
- [ ] Set up alerting for:
  - [ ] High error rate (>10% failed jobs)
  - [ ] API quota near limit
  - [ ] Slow generation times (>5 min for 60s video)

**Success Criteria:** Real-time visibility into system health.

---

### **Phase 5: Frontend & User Experience** (Coordinated with Alex)

#### 5.1 Web Interface (Alex's Task)
- [ ] Design mockups for video generation form
- [ ] Implement React/Vue frontend
- [ ] Connect to FastAPI backend
- [ ] Add job status polling UI
- [ ] Implement video preview & download

#### 4.2 Backend Enhancements for Frontend
- [ ] Add user authentication (Firebase Auth / OAuth)
- [ ] Implement rate limiting per user
- [ ] Add video history endpoint (`/video/history`)
- [ ] Generate video thumbnails
- [ ] Add download endpoint with signed URLs

**Success Criteria:** Non-technical users can generate videos through the web UI.

---

### **Phase 6: Advanced Features** (Post-MVP)

#### 6.1 Multi-Platform Publishing
- [ ] Implement `linkedin_publisher.py`
- [ ] Implement `tiktok_publisher.py`
- [ ] Implement `instagram_publisher.py`
- [ ] Auto-format videos for each platform (aspect ratio, duration limits)

#### 5.2 Analytics & Feedback Loop
- [ ] Collect YouTube video metrics (views, retention)
- [ ] Analyze top-performing topics
- [ ] Feed insights back to `researcher.py`

#### 5.3 Enhanced Customization
- [ ] Allow users to specify visual style (blueprint, photorealistic)
- [ ] Add music genre selection
- [ ] Support custom voice uploads (ElevenLabs cloning)

---

## 🚀 Immediate Next Steps (Phase 2)

1. **Job Queue (Scalability):** Implement Redis / Google Cloud Tasks to persist jobs.
2. **Containerization:** Dockerize the application for Cloud Run deployment.
3. **Frontend Handoff:** Finalize API documentation for Alex.

---

## 📊 Success Metrics

| Metric | Current | Target (Phase 1) | Target (Phase 3) |
|--------|---------|------------------|------------------|
| Test Coverage (Integration) | 100% | 60% | 80% |
| Mean Time to Debug | <1 min | <15 min | <5 min |
| Job Success Rate | 100% (Test) | >90% | >95% |
| Deployment Time | Manual | <10 min | <2 min (automated) |

---

## 🤝 Team Responsibilities

- **Ruben:** Backend, core pipeline, testing, infrastructure
- **Alex:** Frontend, UI/UX, API integration
- **Shared:** Documentation, deployment, monitoring

---

*Last manual pipeline test: 2026-01-27 - PASSED ✅*
