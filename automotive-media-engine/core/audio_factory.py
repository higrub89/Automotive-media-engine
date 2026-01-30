"""
Audio Factory: Text-to-Speech generation using Edge-TTS (Free Neural Voices).

Converts VideoScript narration into high-quality audio without API costs.
"""

import os
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List
import edge_tts
from dotenv import load_dotenv

from .models import VideoScript, Scene
from .logger import get_logger

load_dotenv()

log = get_logger("audio_factory")


class AudioFactory:
    """
    Generates professional voice narration.
    
    Supports:
    - ElevenLabs (premium, cloned voice)
    - Edge-TTS (free fallback)
    """
    
    def __init__(
        self,
        voice_id: str = "es-ES-AlvaroNeural",
        output_dir: str = "./assets/audio",
        use_elevenlabs: bool = None
    ):
        """
        Initialize the audio factory.
        
        Args:
            voice_id: Voice identifier (Edge-TTS or ElevenLabs)
            output_dir: Directory to save audio files
            use_elevenlabs: Force ElevenLabs (auto-detect if None)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Auto-detect ElevenLabs from environment
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        
        if use_elevenlabs is None:
            use_elevenlabs = bool(elevenlabs_key)
        
        self.use_elevenlabs = use_elevenlabs
        
        if self.use_elevenlabs:
            # ElevenLabs configuration
            from .voice_cloner import ElevenLabsVoiceCloner
            from elevenlabs import VoiceSettings
            
            self.voice_cloner = ElevenLabsVoiceCloner()
            
            # Load voice settings from environment or use defaults
            self.voice_settings = VoiceSettings(
                stability=float(os.getenv("ELEVENLABS_STABILITY", "0.2")),
                similarity_boost=float(os.getenv("ELEVENLABS_SIMILARITY", "0.75")),
                style=float(os.getenv("ELEVENLABS_STYLE", "0.9")),
                use_speaker_boost=True
            )
            
            log.info("Audio engine initialized", engine="ElevenLabs", voice_id=self.voice_cloner.voice_id)
        else:
            # Edge-TTS fallback
            self.voice_id = voice_id
            log.info("Audio engine initialized", engine="Edge-TTS", voice_id=voice_id)
    
    async def generate_audio(
        self,
        script: VideoScript,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate audio narration for entire script.
        Routes to ElevenLabs or Edge-TTS based on configuration.
        """
        if not output_filename:
            timestamp = script.generated_at.strftime("%Y%m%d_%H%M%S")
            output_filename = f"narration_{timestamp}.mp3"
        
        output_path = self.output_dir / output_filename
        
        if self.use_elevenlabs:
            return self._generate_elevenlabs(script, output_path)
        else:
            return await self._generate_edge_tts(script, output_path)
    
    def _generate_elevenlabs(self, script: VideoScript, output_path: Path) -> Path:
        """Generate audio using ElevenLabs."""
        return self.voice_cloner.generate_narration(
            text=script.script_text,
            output_path=output_path,
            voice_settings=self.voice_settings
        )
    
    async def _generate_edge_tts(self, script: VideoScript, output_path: Path) -> Path:
        """Generate audio using Edge-TTS."""
        await self._generate_file(script.script_text, output_path)
        
        return output_path
    
    async def generate_scene_audio(
        self,
        scene: Scene,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate audio for a single scene.
        """
        if not output_filename:
            output_filename = f"scene_{scene.scene_number}.mp3"
        
        output_path = self.output_dir / output_filename
        
        await self._generate_file(scene.narration_text, output_path)
        
        return output_path
    
    async def _generate_file(self, text: str, output_path: Path):
        """
        Internal async generator with SSML support for dramatic prosody control.
        
        Processes [PAUSE] and [SHORT_PAUSE] tags for authority voice pacing.
        """
        # Convert script tags to SSML timing directives
        ssml_text = text.replace("[PAUSE]", '\u003cbreak time="800ms"/\u003e')
        ssml_text = ssml_text.replace("[SHORT_PAUSE]", '\u003cbreak time="400ms"/\u003e')
        
        # Wrap in SSML structure for Edge-TTS interpretation
        full_ssml = f"""
        \u003cspeak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='es-ES'\u003e
            \u003cvoice name='{self.voice_id}'\u003e
                {ssml_text}
            \u003c/voice\u003e
        \u003c/speak\u003e
        """
        
        communicate = edge_tts.Communicate(full_ssml, self.voice_id)
        await communicate.save(str(output_path))
    
    def test_voice(self, test_text: str = "This is a test of the zero-cost audio system.") -> Path:
        """Generate test audio."""
        output_path = self.output_dir / "voice_test.mp3"
        asyncio.run(self._generate_file(test_text, output_path))
        return output_path
    
    def list_available_voices(self) -> List[dict]:
        """List recommended technical voices."""
        return [
            {"id": "en-US-ChristopherNeural", "name": "Christopher", "gender": "Male", "style": "Professional"},
            {"id": "en-US-EricNeural", "name": "Eric", "gender": "Male", "style": "Assertive"},
            {"id": "en-GB-RyanNeural", "name": "Ryan", "gender": "Male", "style": "British Tech"},
        ]
    
    def get_audio_duration(self, audio_path: Path) -> float:
        """Get duration using FFprobe."""
        import subprocess
        import json
        
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(audio_path)],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return float(data["format"]["duration"])
        except Exception as e:
            log.warning("Could not get audio duration", error=str(e))
            return 0.0


def generate_audio_from_script(script: VideoScript, output_name: Optional[str] = None) -> Path:
    factory = AudioFactory()
    return factory.generate_audio(script, output_name)
