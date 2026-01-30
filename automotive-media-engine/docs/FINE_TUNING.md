# Hyperluxury Fine-Tuning - Implementation Notes

## Adjustments Applied

### A. ✅ 60 FPS Visual Fluidity
**File:** `core/visual_assembly.py:18`
**Change:** `config.frame_rate = 30` → `config.frame_rate = 60`

**Impact:**
- Buttery smooth animations (luxury standard)
- Render time: 2x longer per scene
- Visual quality: Premium social media grade

**Trade-off:** Acceptable - quality over speed for F1-grade production.

---

### B. ✅ SSML Number Emphasis
**File:** `core/script_engine.py:170-187`
**Enhancement:** Added "CRITICAL NUMBERS RULE" to prosody instructions

**New Behavior:**
- LLM now adds `[SHORT_PAUSE]` before performance figures
- Examples: "830 [SHORT_PAUSE] caballos", "0 a 100 en [SHORT_PAUSE] 2.9 segundos"
- Numbers get dramatic weight and respect

**Impact:** Technical figures sound authoritative, not rushed.

---

### C. 🔄 Dynamic Image Download (Planned)
**Status:** Documented for Phase 2 implementation

**Current State:**
- Images manually placed in `assets/images/`
- `ImageTechnicalScene` has fallback placeholder

**Next Implementation:**
```python
# In core/researcher.py (future enhancement)
class ImageDownloader:
    def fetch_technical_image(self, query: str) -> Path:
        """
        Download technical image from web based on query.
        
        Sources:
        1. Unsplash API (free, high-quality)
        2. Pexels API (free, automotive focus)
        3. Google Custom Search (fallback)
        
        Returns: Path to downloaded image in assets/images/
        """
        pass
```

**Integration Point:**
- `ScriptEngine` detects `[VISUAL: image]` tag
- Calls `ImageDownloader.fetch_technical_image(topic)`
- Saves to `assets/images/` before `VisualAssembly` renders

**Priority:** Medium (manual workflow acceptable for now)

---

## Performance Impact

### Before Fine-Tuning:
- Frame rate: 30 FPS
- Render time: ~10-30s per scene
- Numbers: Rushed delivery
- Images: Manual only

### After Fine-Tuning:
- Frame rate: 60 FPS ✨
- Render time: ~20-60s per scene (2x)
- Numbers: Dramatic pauses ✨
- Images: Manual (auto-download planned)

**Total video generation time:**
- 60s video: ~3-5 min → ~5-8 min
- Still acceptable for F1-grade quality

---

## Validation Needed

**Next Test:**
```bash
python -m core.cli generate \
  --topic "Bugatti Chiron - 1500 CV de Ingeniería Francesa" \
  --duration 60 \
  --no-research
```

**Expected Results:**
1. Visuals render at 60 FPS (check with `ffmpeg -i output.mp4`)
2. Audio contains pauses before "1500 CV" and other figures
3. Smooth, premium visual quality

---

## Future Enhancements (Phase 2)

1. **Auto Image Download:**
   - Integrate Unsplash/Pexels API
   - Cache downloaded images
   - Fallback to AI-generated images (like we did with Ferrari V12)

2. **Variable Frame Rate:**
   - 60 FPS for title/image scenes (premium)
   - 30 FPS for concept scenes (efficiency)
   - Smart allocation based on scene importance

3. **SSML Advanced:**
   - Speed control: `<prosody rate="slow">830 caballos</prosody>`
   - Pitch variation for emphasis
   - Multiple voice actors for dialogue

---

## Commit Message

```
feat: Hyperluxury Fine-Tuning - 60 FPS + Number Emphasis

- Upgraded visual frame rate to 60 FPS for luxury fluidity
- Enhanced SSML prompt with CRITICAL NUMBERS RULE
- Numbers now get dramatic pauses for authority
- Documented dynamic image download for future implementation

Render time impact: 2x (acceptable for F1-grade quality)
```
