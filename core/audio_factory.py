"""
Audio Factory: Text-to-Speech generation using ElevenLabs API.

Converts VideoScript narration into high-quality audio with precise timing metadata.
"""

import os
from pathlib import Path
from typing import Optional
from elevenlabs import ElevenLabs, VoiceSettings
from dotenv import load_dotenv

from .models import VideoScript, Scene

load_dotenv()


class AudioFactory:
    """
    Generates professional voice narration for video scripts.
    
    Optimized for technical content with clear enunciation and authority.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: Optional[str] = None,
        output_dir: str = "./assets/audio"
    ):
        """
        Initialize the audio factory.
        
        Args:
            api_key: ElevenLabs API key (defaults to ELEVENLABS_API_KEY env var)
            voice_id: Voice model ID (defaults to ELEVENLABS_VOICE_ID env var or 'adam')
            output_dir: Directory to save audio files
        """
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment or provided")
        
        self.client = ElevenLabs(api_key=self.api_key)
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Adam voice
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Voice settings optimized for technical narration
        self.voice_settings = VoiceSettings(
            stability=0.6,  # Balanced - not too robotic, not too expressive
            similarity_boost=0.8,  # High similarity to original voice
            style=0.3,  # Moderate style for professional tone
            use_speaker_boost=True  # Enhance clarity
        )
    
    def generate_audio(
        self,
        script: VideoScript,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate audio narration for entire script.
        
        Args:
            script: VideoScript with narration text
            output_filename: Custom output filename (defaults to timestamp-based)
            
        Returns:
            Path to generated audio file
        """
        if not output_filename:
            timestamp = script.generated_at.strftime("%Y%m%d_%H%M%S")
            output_filename = f"narration_{timestamp}.mp3"
        
        output_path = self.output_dir / output_filename
        
        # Generate audio using ElevenLabs TTS
        audio_generator = self.client.text_to_speech.convert(
            text=script.script_text,
            voice_id=self.voice_id,
            model_id="eleven_turbo_v2_5",  # Latest fast model with high quality
            voice_settings=self.voice_settings,
            output_format="mp3_44100_128"  # High quality MP3
        )
        
        # Write audio to file
        with open(output_path, "wb") as audio_file:
            for chunk in audio_generator:
                audio_file.write(chunk)
        
        return output_path
    
    def generate_scene_audio(
        self,
        scene: Scene,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate audio for a single scene (useful for testing/previews).
        
        Args:
            scene: Scene object with narration text
            output_filename: Custom output filename
            
        Returns:
            Path to generated audio file
        """
        if not output_filename:
            output_filename = f"scene_{scene.scene_number}.mp3"
        
        output_path = self.output_dir / output_filename
        
        audio_generator = self.client.text_to_speech.convert(
            text=scene.narration_text,
            voice_id=self.voice_id,
            model_id="eleven_turbo_v2_5",
            voice_settings=self.voice_settings,
            output_format="mp3_44100_128"
        )
        
        with open(output_path, "wb") as audio_file:
            for chunk in audio_generator:
                audio_file.write(chunk)
        
        return output_path
    
    def test_voice(self, test_text: str = "This is a test of the audio generation system.") -> Path:
        """
        Generate a test audio clip to verify voice quality.
        
        Args:
            test_text: Text to narrate for testing
            
        Returns:
            Path to test audio file
        """
        output_path = self.output_dir / "voice_test.mp3"
        
        audio_generator = self.client.text_to_speech.convert(
            text=test_text,
            voice_id=self.voice_id,
            model_id="eleven_turbo_v2_5",
            voice_settings=self.voice_settings,
            output_format="mp3_44100_128"
        )
        
        with open(output_path, "wb") as audio_file:
            for chunk in audio_generator:
                audio_file.write(chunk)
        
        print(f"✓ Test audio generated: {output_path}")
        print(f"  Voice ID: {self.voice_id}")
        print(f"  Settings: Stability={self.voice_settings.stability}, "
              f"Similarity={self.voice_settings.similarity_boost}")
        
        return output_path
    
    def list_available_voices(self) -> list[dict]:
        """
        List all available voices in your ElevenLabs account.
        
        Returns:
            List of voice dictionaries with id, name, and metadata
        """
        voices = self.client.voices.get_all()
        
        voice_list = []
        for voice in voices.voices:
            voice_list.append({
                "id": voice.voice_id,
                "name": voice.name,
                "category": voice.category,
                "description": voice.description
            })
        
        return voice_list
    
    def get_audio_duration(self, audio_path: Path) -> float:
        """
        Get duration of audio file in seconds.
        
        Note: Requires ffmpeg/ffprobe to be installed.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        import subprocess
        import json
        
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    str(audio_path)
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            data = json.loads(result.stdout)
            duration = float(data["format"]["duration"])
            return round(duration, 2)
            
        except (subprocess.CalledProcessError, KeyError, ValueError) as e:
            raise RuntimeError(f"Failed to get audio duration: {e}")


# Convenience function for quick audio generation
def generate_audio_from_script(script: VideoScript, output_filename: Optional[str] = None) -> Path:
    """
    Quick helper to generate audio without instantiating factory.
    
    Args:
        script: VideoScript object
        output_filename: Optional custom filename
        
    Returns:
        Path to generated audio file
    """
    factory = AudioFactory()
    return factory.generate_audio(script, output_filename)
