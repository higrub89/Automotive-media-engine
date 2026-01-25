#!/usr/bin/env python3
"""
Quick test script for ElevenLabs integration.
Tests with pre-made voices before cloning.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from core.voice_cloner import ElevenLabsVoiceCloner

def test_with_premade_voice():
    """
    Test ElevenLabs with a pre-made voice.
    
    Popular Spanish voices:
    - "Matias": Spanish male, calm technical
    - "Valentino": Spanish male, energetic
    - "Antoni": Multilingual male, warm
    """
    
    print("=" * 70)
    print("🎙️  ELEVENLABS VOICE TEST - Pre-made Voice")
    print("=" * 70)
    
    # Check API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("\n❌ API key not configured")
        print("\n📝 Steps:")
        print("1. Get API key from: https://elevenlabs.io/app/settings/api-keys")
        print("2. Configure:")
        print("   echo 'ELEVENLABS_API_KEY=sk_xxxxx' >> .env")
        print("   source .env")
        return False
    
    print(f"✅ API key found: {api_key[:8]}...")
    
    # Initialize cloner
    try:
        cloner = ElevenLabsVoiceCloner(api_key)
        print("✅ ElevenLabs client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False
    
    # Test text (Spanish automotive content)
    test_text = """
    El Ferrari 296 GTB representa una revolución en la ingeniería híbrida.
    Con 830 caballos de potencia, este V6 biturbo desafía todas las expectativas.
    De cero a cien kilómetros por hora en apenas dos punto nueve segundos.
    Es violencia pura, convertida en aceleración.
    """
    
    print("\n📝 Test text:")
    print(f"   {test_text.strip()[:80]}...")
    print(f"   ({len(test_text)} characters)")
    
    # List available voices
    print("\n🎭 Available pre-made voices:")
    print("   (Using first available voice for test)")
    
    # For free tier, we'll use a specific voice ID
    # Antoni is a good multilingual option
    premade_voice_id = "ErXwobaYiN019PkySvjV"  # Antoni
    cloner.voice_id = premade_voice_id
    
    print(f"   Voice ID: {premade_voice_id}")
    
    # Generate test audio
    output_path = Path("./assets/audio/elevenlabs_test.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print("\n🎵 Generating audio...")
        result = cloner.generate_narration(
            text=test_text,
            output_path=output_path
        )
        
        print(f"\n✅ SUCCESS!")
        print(f"📁 Audio saved: {result}")
        print(f"\n🎧 Listen to test:")
        print(f"   mpv {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        print(f"\n💡 Common issues:")
        print("   - API key invalid/expired")
        print("   - Free tier quota exceeded")
        print("   - Network connection issue")
        return False


if __name__ == "__main__":
    success = test_with_premade_voice()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ ElevenLabs integration working!")
        print("=" * 70)
        print("\n📋 Next steps:")
        print("1. Listen to test audio to verify quality")
        print("2. If satisfied, proceed to voice cloning")
        print("3. Or integrate directly into AudioFactory with pre-made voice")
        print("\n💰 Free tier limits:")
        print("   - 10,000 characters/month")
        print("   - ~6-7 videos of 60s")
        print("   - Upgrade to Creator ($5/mes) for 30,000 chars")
    else:
        print("\n" + "=" * 70)
        print("❌ Test failed - check errors above")
        print("=" * 70)
    
    sys.exit(0 if success else 1)
