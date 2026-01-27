#!/usr/bin/env python3
"""
Debug script to check what text is being sent to ElevenLabs.
Shows before/after SSML conversion.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.script_engine import ScriptEngine
from core.voice_cloner import ElevenLabsVoiceCloner

# Generate a quick script
engine = ScriptEngine()
script = engine.generate_script(
    topic="Lamborghini Aventador SVJ Test",
    platform="linkedin",
    duration=45,
    skip_research=True
)

print("=" * 70)
print("📝 ORIGINAL SCRIPT TEXT (with SSML tags)")
print("=" * 70)
print(script.script_text)
print("\n")

# Show what gets converted
cloner = ElevenLabsVoiceCloner()
converted = cloner._convert_ssml_tags(script.script_text)

print("=" * 70)
print("🔄 CONVERTED TEXT (sent to ElevenLabs)")
print("=" * 70)
print(converted)
print("\n")

print("=" * 70)
print("📊 COMPARISON")
print("=" * 70)
print(f"Original length: {len(script.script_text)} chars")
print(f"Converted length: {len(converted)} chars")
print(f"Tags replaced: {script.script_text.count('[PAUSE]') + script.script_text.count('[SHORT_PAUSE]')}")
