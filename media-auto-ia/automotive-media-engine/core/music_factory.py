
import os
from pathlib import Path
from typing import Optional, Dict
from .models import StyleArchetype
from .logger import get_logger

log = get_logger("music_factory")

class MusicFactory:
    """
    Selects and processes background music based on style archetypes.
    """
    
    STYLE_MUSIC_MAP = {
        StyleArchetype.TECHNICAL: {
            "search_query": "ambient electronic technical documentary",
            "fallback_file": "technical_bg.mp3",
            "volume_boost": -15 # dB
        },
        StyleArchetype.STORYTELLING: {
            "search_query": "dramatic cinematic emotional narrative",
            "fallback_file": "storytelling_bg.mp3",
            "volume_boost": -12 # dB
        },
        StyleArchetype.DOCUMENTARY: {
            "search_query": "minimalist educational acoustic corporate",
            "fallback_file": "documentary_bg.mp3",
            "volume_boost": -18 # dB
        },
        StyleArchetype.MINIMALIST: {
            "search_query": "lofi chill beat minimalist",
            "fallback_file": "minimalist_bg.mp3",
            "volume_boost": -20 # dB
        }
    }

    def __init__(self, music_dir: str = "./assets/music"):
        self.music_dir = Path(music_dir)
        self.music_dir.mkdir(parents=True, exist_ok=True)

    def get_music_for_style(self, style: StyleArchetype) -> Path:
        """
        Returns the path to a music file appropriate for the style.
        Actually searches in local assets or returns a default.
        """
        config = self.STYLE_MUSIC_MAP.get(style, self.STYLE_MUSIC_MAP[StyleArchetype.TECHNICAL])
        
        # Look for local file in assets/music
        local_path = self.music_dir / config["fallback_file"]
        
        if local_path.exists():
            return local_path
            
        # If not exists, we should ideally download from a royalty-free API
        # For now, return a placeholder or the intended path
        log.warning("Music file not found, using fallback", style=style.value, path=str(local_path))
        return local_path

    def mix_audio(self, narration_path: Path, music_path: Path, output_path: Path, style: StyleArchetype):
        """
        Mixes narration and music using FFmpeg.
        Higher priority for narration, music is ducked.
        """
        import subprocess
        
        config = self.STYLE_MUSIC_MAP.get(style, self.STYLE_MUSIC_MAP[StyleArchetype.TECHNICAL])
        volume = config["volume_boost"]
        
        # FFmpeg command for mixing:
        # 1. Take narration as [0:a]
        # 2. Take music as [1:a], loop it, and adjust volume
        # 3. amix them together
        
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(narration_path),
            "-stream_loop", "-1",
            "-i", str(music_path),
            "-filter_complex", 
            f"[1:a]volume={volume}dB[music];[0:a][music]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "[a]",
            "-c:a", "libmp3lame",
            "-q:a", "2",
            str(output_path)
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            log.info("Audio mixing completed", output=str(output_path))
            return output_path
        except Exception as e:
            log.error("Music mixing failed", error=str(e))

            # Fallback to pure narration if mixing fails
            import shutil
            shutil.copy(narration_path, output_path)
            return output_path
