# Automotive Media Engine 🏎️

> **Precision engineering applied to content generation.** An automated pipeline for creating technical automotive videos with the exactitude of aerospace systems and the aesthetics of Italian supercars.

## Mission Statement

Transform technical expertise into scalable content revenue through systematic automation. This is not an "influencer tool"—it's a **production system** built to industrial standards.

## System Architecture

```
┌─────────────────┐
│  Content Brief  │  (Markdown input)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Script Engine   │  (Claude API + Templating)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Audio Factory   │  (ElevenLabs TTS)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Visual Assembly │  (Matplotlib/Pillow/Stock)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Assembler │  (FFmpeg Automation)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Platform QC    │  (Format validation)
└────────┬────────┘
         │
         ▼
     [OUTPUT]  → LinkedIn/TikTok/YouTube
```

## Quick Start

### 1. Environment Setup

```bash
cd ~/Automatitation/automotive-media-engine
source venv/bin/activate
pip install -r requirements.txt
```

### 2. API Configuration

Create `.env` file:

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- **Anthropic Claude**: For script generation
- **ElevenLabs**: For voice synthesis

See [docs/api_setup.md](docs/api_setup.md) for detailed instructions.

### 3. Generate Your First Video

```bash
# Create a content brief
cp templates/content_brief_template.md content/my_first_video.md
# Edit with your technical content

# Generate video
python -m core.cli generate content/my_first_video.md --output my_first_video

# Output will be in: output/my_first_video.mp4
```

## Project Structure

```
automotive-media-engine/
├── core/                   # Pipeline components
│   ├── models.py          # Data structures
│   ├── script_engine.py   # Script generation
│   ├── audio_factory.py   # TTS integration
│   ├── visual_assembly.py # Visual generation
│   ├── video_assembler.py # FFmpeg automation
│   └── cli.py             # Command-line interface
├── mcp-servers/           # Model Context Protocol servers
│   ├── content_research_server.py
│   └── local_knowledge_server.py
├── assets/                # Generated assets
│   ├── audio/
│   ├── video/
│   └── diagrams/
├── content/               # Your content briefs (input)
├── templates/             # Content templates
├── output/                # Final videos (export)
├── docs/                  # Documentation
└── tests/                 # Test suite
```

## Development Roadmap

- **Week 1-2**: MVP - First video generation
- **Week 3-4**: Content production & testing
- **Week 5-6**: Monetization setup
- **Week 7-10**: Scaling & automation
- **Week 11-16**: Revenue optimization

**Target**: €3000/month recurring revenue by Week 16 (May 2026)

See [task.md](../../.gemini/antigravity/brain/22c8b31f-080e-4df6-b5a9-81d08a379fb3/task.md) for detailed breakdown.

## Technical Specifications

### Supported Platforms
- **LinkedIn**: 1080x1080 (square), 60-120 seconds
- **TikTok/Reels**: 1080x1920 (vertical), 15-90 seconds
- **YouTube Shorts**: 1080x1920 (vertical), 15-60 seconds

### Quality Presets
- **Ultra**: CRF 18, slow (archival quality)
- **Standard**: CRF 23, medium (social media)
- **Fast**: CRF 28, fast (testing)

### Content Philosophy

1. **Technical Precision**: Every claim must be verifiable
2. **Aesthetic Minimalism**: Clean, distraction-free visuals
3. **Mentorship Value**: Each video teaches something concrete

## Cost Structure

- **ElevenLabs**: ~$22/month (Starter)
- **Claude API**: ~$20-50/month (usage-based)
- **Total**: ~$50-75/month operational cost

## Contributing

This is a personal production system. However, if you're building similar tools, feel free to reference the architecture.

## License

Proprietary - All rights reserved

---

**Built with engineering discipline. Optimized for revenue generation.**
