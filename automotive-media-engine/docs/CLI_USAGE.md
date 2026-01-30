# CLI Usage Guide

## Automotive Media Engine - Command Line Interface

### Quick Start

```bash
# Activate environment
cd ~/Automatitation/automotive-media-engine
source venv/bin/activate

# Generate a video
python -m core.cli generate --topic "Lamborghini Aventador SVJ" --platform youtube
```

---

## Commands

### 1. `generate` - Create Complete Video

Generate a video from topic to final output.

**Basic usage:**
```bash
python -m core.cli generate --topic "Your Topic Here"
```

**Full options:**
```bash
python -m core.cli generate \
  --topic "Ferrari 296 GTB - El V6 Híbrido" \
  --platform youtube \
  --audience intermediate \
  --duration 90 \
  --auto-upload
```

**Arguments:**
- `--topic` (required): Video topic in quotes
- `--platform`: Target platform (linkedin, youtube, tiktok, instagram) [default: linkedin]
- `--audience`: Audience level (beginner, intermediate, advanced) [default: intermediate]
- `--duration`: Target duration in seconds [default: 60]
- `--no-research`: Disable DuckDuckGo research for faster generation
- `--auto-upload`: Automatically upload to YouTube after generation
- `--output`: Custom filename (without .mp4 extension)

**Examples:**
```bash
# Quick LinkedIn video (60s)
python -m core.cli generate --topic "Porsche 911 GT3 RS Aero"

# Long-form YouTube video with research
python -m core.cli generate \
  --topic "MV Agusta Brutale 1000 RR - 208 CV" \
  --platform youtube \
  --duration 120

# Fast generation without research
python -m core.cli generate \
  --topic "Bugatti Chiron - El W16" \
  --no-research
```

---

### 2. `publish` - Upload to YouTube

Upload an existing video to YouTube.

**Usage:**
```bash
python -m core.cli publish output/my_video.mp4 \
  --title "Ferrari 296 GTB Analysis" \
  --description "Technical deep-dive into hybrid supercar technology"
```

**Arguments:**
- `video_path` (required): Path to video file
- `--title`: Video title (defaults to filename)
- `--description`: Video description

**Example:**
```bash
python -m core.cli publish output/ferrari_296_gtb_hyperluxury_demo.mp4
```

---

### 3. `test` - Validate Components

Test individual pipeline components.

**Usage:**
```bash
python -m core.cli test --component all
```

**Arguments:**
- `--component`: Component to test (script, audio, visual, all) [default: all]

**Examples:**
```bash
# Test everything
python -m core.cli test

# Test only script generation
python -m core.cli test --component script

# Test audio synthesis
python -m core.cli test --component audio
```

---

## Workflows

### Production Workflow

1. **Generate video:**
   ```bash
   python -m core.cli generate \
     --topic "Lamborghini Huracán Sterrato" \
     --platform youtube \
     --duration 90
   ```

2. **Review output:**
   ```bash
   mpv output/lamborghini_huracán_sterrato.mp4
   ```

3. **Publish if satisfied:**
   ```bash
   python -m core.cli publish output/lamborghini_huracán_sterrato.mp4
   ```

### Batch Production

```bash
# Generate multiple videos in sequence
for topic in \
  "Ferrari SF90 - Hybrid Hypercar" \
  "Porsche 911 Turbo S - AWD Mastery" \
  "McLaren P1 - Formula 1 Tech"
do
  python -m core.cli generate --topic "$topic" --platform youtube
done
```

### Fast Iteration

```bash
# Quick generation without research (faster)
python -m core.cli generate \
  --topic "Aston Martin Valkyrie" \
  --no-research \
  --duration 60
```

---

## Tips

1. **Topic Naming:**
   - Use Spanish for best results (voice is Spanish)
   - Include brand + model for clarity
   - Example: "Ferrari 296 GTB - El V6 Híbrido"

2. **Platform Selection:**
   - LinkedIn: 60-90s, technical depth
   - YouTube: 90-180s, comprehensive analysis
   - TikTok/Instagram: 30-60s, quick hooks

3. **Duration:**
   - Keep under 120s for best pacing
   - LLM may generate slightly longer scripts
   - Audio synthesis adds ~10% to estimated time

4. **Research:**
   - Enable for unfamiliar topics (more accurate)
   - Disable for speed or known content

---

## Troubleshooting

**Script validation fails:**
- Duration mismatch: LLM generated too long → reduce --duration
- Try --no-research for simpler scripts

**Audio generation slow:**
- Edge-TTS can take 1-2 min for long scripts
- Normal behavior, be patient

**Visual rendering:**
- Each scene takes ~10-30s to render
- 5 scenes = ~2-3 minutes total

**Upload fails:**
- Check YouTube credentials in `client_secret.json`
- Verify token.pickle exists and is valid
- Re-authenticate if needed

---

## Output Locations

- **Videos**: `output/*.mp4`
- **Audio**: `assets/audio/*.mp3`
- **Visuals**: `assets/video/scene_*.mp4`

---

## Next: Automation Scripts

For even more control, create bash aliases:

```bash
# Add to ~/.bashrc
alias ame-gen='cd ~/Automatitation/automotive-media-engine && source venv/bin/activate && python -m core.cli generate'

# Usage
ame-gen --topic "Your Topic" --platform youtube
```
