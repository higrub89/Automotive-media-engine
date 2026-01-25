"""
ElevenLabs Voice Cloning Module

Replaces Edge-TTS with user's cloned voice for authentic narration.
Requires ElevenLabs Creator subscription ($5/mes).
"""

import os
from pathlib import Path
from typing import Optional, Dict
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

class ElevenLabsVoiceCloner:
    """
    Production-grade voice cloning with ElevenLabs.
    
    Features:
    - Clone voice from sample audio
    - Generate narration with cloned voice
    - SSML tag conversion
    - Prosody control (stability, similarity, style)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with API key.
        
        Args:
            api_key: ElevenLabs API key (or set ELEVENLABS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ElevenLabs API key required. Set ELEVENLABS_API_KEY env var "
                "or pass api_key parameter."
            )
        
        # Initialize client
        self.client = ElevenLabs(api_key=self.api_key)
        
        # Load voice_id from env or set to None (will clone first time)
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        
        # Default voice settings (can be tuned)
        self.default_settings = VoiceSettings(
            stability=0.5,        # 0-1: Higher = more consistent, lower = more expressive
            similarity_boost=0.8, # 0-1: How similar to original sample
            style=0.6,            # 0-1: Exaggeration of speaking style
            use_speaker_boost=True # Enhances similarity
        )
    
    def clone_voice_from_sample(
        self, 
        sample_audio_path: Path, 
        voice_name: str = "Ruben",
        description: str = "Energetic automotive technical narrator"
    ) -> str:
        """
        Clone voice from audio sample.
        
        Requirements:
        - Audio: 5-10 minutes minimum
        - Format: MP3, WAV, M4A
        - Quality: 44.1kHz, clear audio, no background noise
        - Content: Varied emotion and pacing
        
        Args:
            sample_audio_path: Path to voice sample file
            voice_name: Name for cloned voice
            description: Description for reference
            
        Returns:
            voice_id: ID to use for generation
        """
        if not sample_audio_path.exists():
            raise FileNotFoundError(f"Voice sample not found: {sample_audio_path}")
        
        print(f"🎙️  Cloning voice from {sample_audio_path}...")
        print("   This may take 30-60 seconds...")
        
        # Clone voice
        voice = clone(
            name=voice_name,
            description=description,
            files=[str(sample_audio_path)]
        )
        
        self.voice_id = voice.voice_id
        
        print(f"✅ Voice cloned successfully!")
        print(f"   Voice ID: {voice.voice_id}")
        print(f"   Name: {voice_name}")
        print(f"\n💡 Save this to .env:")
        print(f"   ELEVENLABS_VOICE_ID={voice.voice_id}")
        
        return voice.voice_id
    
    def generate_narration(
        self,
        text: str,
        output_path: Path,
        voice_settings: Optional[VoiceSettings] = None,
        model: str = "eleven_multilingual_v2"
    ) -> Path:
        """
        Generate narration audio with cloned voice.
        
        Args:
            text: Script text with SSML tags ([PAUSE], [SHORT_PAUSE])
            output_path: Where to save MP3
            voice_settings: Custom voice settings (uses defaults if None)
            model: ElevenLabs model (multilingual_v2 for Spanish)
            
        Returns:
            Path to generated audio file
        """
        if not self.voice_id:
            raise ValueError(
                "No voice_id set. Either:\n"
                "1. Clone voice first with clone_voice_from_sample()\n"
                "2. Set ELEVENLABS_VOICE_ID environment variable"
            )
        
        # Convert SSML tags to natural pauses
        processed_text = self._convert_ssml_tags(text)
        
        # Use provided settings or defaults
        settings = voice_settings or self.default_settings
        
        print(f"🎙️  Generating narration ({len(processed_text)} chars)...")
        
        # Generate audio using client (v2.31 API)
        audio = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            text=processed_text,
            model_id=model,
            voice_settings=settings
        )
        
        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # The audio is a generator, we need to collect all chunks
        audio_bytes = b"".join(audio)
        
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        
        print(f"✅ Audio saved: {output_path}")
        
        return output_path
    
    def _convert_ssml_tags(self, text: str) -> str:
        """
        Convert SSML tags to natural pause markers.
        
        ElevenLabs doesn't use SSML but interprets natural punctuation:
        - [PAUSE] → ... (ellipsis = dramatic pause)
        - [SHORT_PAUSE] → , (comma = brief pause)
        
        Args:
            text: Text with [PAUSE] and [SHORT_PAUSE] tags
            
        Returns:
            Text with converted pause markers
        """
        # Replace SSML tags with natural punctuation
        text = text.replace("[PAUSE]", "...")
        text = text.replace("[SHORT_PAUSE]", ",")
        
        # Clean up consecutive commas/ellipsis
        text = text.replace(",,", ",")
        text = text.replace("....", "...")
        
        return text
    
    def test_voice(self, test_text: str = None) -> Path:
        """
        Quick test generation to validate voice quality.
        
        Args:
            test_text: Custom test text (or uses default)
            
        Returns:
            Path to test audio file
        """
        if not test_text:
            test_text = (
                "El Ferrari 296 GTB representa una revolución en la ingeniería híbrida... "
                "Con 830 caballos de potencia, este V6 biturbo desafía todas las expectativas."
            )
        
        test_path = Path("./assets/audio/voice_test.mp3")
        
        return self.generate_narration(test_text, test_path)


# Utility function for easy testing
def test_elevenlabs_setup():
    """
    Test script to validate ElevenLabs configuration.
    Run this after setting up API key.
    """
    try:
        cloner = ElevenLabsVoiceCloner()
        
        print("✅ ElevenLabs API key configured correctly")
        
        if cloner.voice_id:
            print(f"✅ Voice ID found: {cloner.voice_id}")
            
            # Test generation
            test_audio = cloner.test_voice()
            print(f"\n🎵 Test audio generated: {test_audio}")
            print("   Listen to verify voice quality.")
        else:
            print("\n⚠️  No voice_id configured yet.")
            print("   Next step: Clone voice with clone_voice_from_sample()")
        
        return True
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📝 Setup steps:")
        print("1. Get API key from https://elevenlabs.io/app/settings/api-keys")
        print("2. Set environment variable: export ELEVENLABS_API_KEY='your_key'")
        print("3. (Optional) Set voice ID if already cloned: export ELEVENLABS_VOICE_ID='your_id'")
        return False


if __name__ == "__main__":
    # Run test when executed directly
    test_elevenlabs_setup()
