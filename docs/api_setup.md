# API Setup Guide

This guide walks you through obtaining and configuring the required API keys for the Automotive Media Engine.

## Cost Overview

| Service | Plan | Monthly Cost | Notes |
|---------|------|--------------|-------|
| **Gemini Pro** | Free (42 Madrid) | **€0** | Primary LLM - 1 year free via 42 Madrid partnership |
| **ElevenLabs** | Starter | **~€22** | Voice synthesis - ~30K characters/month (~20 videos) |
| **Total** | | **~€22/month** | 60% cheaper than Claude-based approach |

---

## 1. Gemini API (Primary LLM - FREE)

### Why Gemini?
- **Free for 1 year** via your 42 Madrid Pro subscription
- Comparable quality to Claude for technical content generation
- Primary provider = maximum cost savings

### Setup Steps

1. **Access Google AI Studio**
   - Visit: https://aistudio.google.com/
   - Sign in with your 42 Madrid Google account

2. **Get API Key**
   - Click "Get API key" in the top right
   - Create a new API key or use existing one
   - Copy the key (starts with `AIza...`)

3. **Configure Environment**
   ```bash
   cd ~/Automatitation/automotive-media-engine
   cp .env.example .env
   nano .env  # or your preferred editor
   ```

4. **Add to .env**
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Test Connection**
   ```bash
   source venv/bin/activate
   python3 << 'EOF'
   import os
   from dotenv import load_dotenv
   import google.generativeai as genai
   
   load_dotenv()
   genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
   model = genai.GenerativeModel('gemini-2.0-flash-exp')
   
   response = model.generate_content("Test: Explain a Ferrari V12 in 10 words.")
   print("✓ Gemini API working!")
   print(f"Response: {response.text}")
   EOF
   ```

### Usage Limits (Free Tier)
- **Requests per minute**: 60
- **Requests per day**: 1,500
- **Tokens per minute**: 1 million

For our use case (3-5 videos/day), this is **more than sufficient**.

---

## 2. ElevenLabs API (Voice Synthesis)

### Why ElevenLabs?
- Industry-leading voice quality
- Professional, authoritative voice models perfect for technical content
- Consistent pronunciation of technical terms

### Setup Steps

1. **Create Account**
   - Visit: https://elevenlabs.io/
   - Sign up with email or Google

2. **Choose Plan**
   -  **Starter Plan** (~$22/month)
     - 30,000 characters/month
     - ~20 videos @ 60-90 seconds each
     - Commercial license included
   - Scale to **Creator Plan** ($99/month) as you grow

3. **Get API Key**
   - Go to Profile Settings → API Keys
   - Click "Create API Key"
   - Copy and securely store the key

4. **Add to .env**
   ```bash
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```

5. **Select Voice Model**
   - Go to Voice Library
   - Recommended voices for technical content:
     - **Adam**: Professional, clear, authoritative (DEFAULT)
     - **Antoni**: Deep, serious, technical
     - **Josh**: Warm but professional
   
   - Copy the Voice ID from your chosen voice
   - Add to .env:
     ```bash
     ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB  # Adam (default)
     ```

6. **Test Voice**
   ```bash
   source venv/bin/activate
   python3 << 'EOF'
   from core.audio_factory import AudioFactory
   
   factory = AudioFactory()
   audio_path = factory.test_voice(
       "The SF90 Stradale combines a twin-turbo V8 with three electric motors, delivering 986 horsepower."
   )
   print(f"✓ Audio generated: {audio_path}")
   print("Listen to verify voice quality!")
   EOF
   ```

---

## 3. Claude API (Optional Fallback)

Only needed if you want to use Claude as a fallback LLM provider. **Skip this if using Gemini exclusively.**

### Setup Steps

1. **Create Anthropic Account**
   - Visit: https://console.anthropic.com/
   - Sign up and verify email

2. **Add Payment Method**
   - Claude is pay-as-you-go
   - Estimated cost: $20-50/month for daily video generation

3. **Get API Key**
   - Go to API Keys section
   - Create a new key
   - Copy the key (starts with `sk-ant-...`)

4. **Add to .env**
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

5. **Test (Optional)**
   ```bash
   python3 << 'EOF'
   from core.script_engine import ScriptEngine, LLMProvider
   from core.models import ContentBrief, Platform, AudienceLevel
   
   brief = ContentBrief(
       topic="Testing Claude API",
       key_points=["Point 1", "Point 2", "Point 3"],
       platform=Platform.LINKEDIN
   )
   
   engine = ScriptEngine(provider=LLMProvider.CLAUDE)
   script = engine.generate_script(brief)
   print("✓ Claude API working!")
   EOF
   ```

---

## 4. FFmpeg (Video Processing)

### Install FFmpeg

```bash
sudo apt update
sudo apt install ffmpeg -y
```

### Verify Installation

```bash
ffmpeg -version
```

Should show version 4.x or higher.

---

## Final Configuration Check

Your `.env` file should look like:

```bash
# API Keys (Priority: Gemini for cost savings)
GEMINI_API_KEY=AIza...your_key_here
ANTHROPIC_API_KEY=sk-ant-...optional  # Optional fallback
ELEVENLABS_API_KEY=your_elevenlabs_key

# ElevenLabs Voice Configuration
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB  # Adam
ELEVENLABS_MODEL_ID=eleven_turbo_v2_5

# Video Generation Settings
DEFAULT_PLATFORM=linkedin
DEFAULT_DURATION=60
DEFAULT_QUALITY=standard

# Content Settings
CONTENT_TONE=professional_technical
AUDIENCE_LEVEL=intermediate

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
```

---

## Security Notes

1. **Never commit .env to Git** (already in .gitignore)
2. **Rotate keys if accidentally exposed**
3. **Set spending limits** in ElevenLabs dashboard
4. **Monitor usage** via respective dashboards:
   - Gemini: https://aistudio.google.com/app/apikey
   - ElevenLabs: https://elevenlabs.io/usage

---

## Cost Monitoring

### Weekly Check
```bash
# Check approximate costs based on generated videos
ls output/*.mp4 | wc -l  # Video count this week
```

### Monthly Budget Targets
- **Month 1-2** (MVP): ~€22-30/month
- **Month 3-4** (Scaling): ~€100-150/month
- **Month 5+** (Revenue generating): Should cover costs from client work

---

## Next Steps

Once all APIs are configured:

1. ✅ Test each component individually
2. ✅ Generate your first complete video (see main README.md)
3. ✅ Monitor API usage and costs
4. ✅ Scale as you gain clients

**Ready to generate your first video? Proceed to the main README for the quickstart guide.**
