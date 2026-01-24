"""
Video Assembler: FFmpeg automation for final video production.

Combines audio narration with visual scenes into platform-optimized videos.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import ffmpeg

from .models import VideoScript, VideoConfig, GenerationResult, QualityPreset, Platform


class VideoAssembler:
    """
    Assembles final video from audio and visual components using FFmpeg.
    
    Handles platform-specific encoding, timing synchronization, and quality optimization.
    """
    
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize video assembler.
        
        Args:
            output_dir: Directory for final video exports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verify FFmpeg is installed
        self._verify_ffmpeg()
    
    def _verify_ffmpeg(self):
        """Verify FFmpeg is installed and accessible."""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg not found. Install with: sudo apt install ffmpeg"
            )
    
    def assemble_video(
        self,
        config: VideoConfig,
        audio_path: Path,
        visual_paths: List[Path],
        output_filename: Optional[str] = None
    ) -> GenerationResult:
        """
        Assemble complete video from components.
        
        Args:
            config: VideoConfig with all project settings
            audio_path: Path to audio narration file
            visual_paths: List of paths to scene visuals (in order)
            output_filename: Custom output filename
            
        Returns:
            GenerationResult with success status and metadata
        """
        start_time = datetime.now()
        
        try:
            # Generate output filename if not provided
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{config.project_name}_{timestamp}.mp4"
            
            output_path = self.output_dir / output_filename
            
            # Build video timeline from scenes
            video_timeline_path = self._create_video_timeline(
                config.script,
                visual_paths
            )
            
            # Encode final video
            self._encode_video(
                video_timeline_path,
                audio_path,
                output_path,
                config
            )
            
            # Get file size
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            
            # Calculate generation time
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return GenerationResult(
                success=True,
                video_path=str(output_path),
                thumbnail_path=None,  # Will be added in Phase 2
                duration=config.script.total_duration,
                file_size_mb=round(file_size_mb, 2),
                generation_time_seconds=round(generation_time, 2),
                metadata={
                    "platform": config.script.brief.platform.value,
                    "quality": config.quality.value,
                    "scenes": len(config.script.scenes),
                    "resolution": f"{config.platform_specs['resolution'][0]}x{config.platform_specs['resolution'][1]}"
                }
            )
            
        except Exception as e:
            generation_time = (datetime.now() - start_time).total_seconds()
            return GenerationResult(
                success=False,
                duration=0.0,
                generation_time_seconds=round(generation_time, 2),
                error_message=str(e)
            )
    
    def _create_video_timeline(
        self,
        script: VideoScript,
        visual_paths: List[Path]
    ) -> Path:
        """
        Create video timeline by concatenating scene visuals with proper timing.
        
        Args:
            script: VideoScript with scene timing
            visual_paths: List of visual image paths
            
        Returns:
            Path to concatenated video file
        """
        if len(visual_paths) != len(script.scenes):
            raise ValueError(
                f"Visual count ({len(visual_paths)}) doesn't match scene count ({len(script.scenes)})"
            )
        
        # Create temp directory for scene videos
        temp_dir = Path("./temp")
        temp_dir.mkdir(exist_ok=True)
        
        scene_videos = []
        
        # Convert each static image to video with scene duration
        for i, (scene, visual_path) in enumerate(zip(script.scenes, visual_paths)):
            scene_video_path = temp_dir / f"scene_{i:02d}.mp4"
            
            # Get platform resolution
            resolution = self._get_platform_resolution(script.brief.platform)
            
            # Create video from static image with scene duration
            (
                ffmpeg
                .input(str(visual_path), loop=1, t=scene.duration)
                .filter('scale', resolution[0], resolution[1])
                .output(
                    str(scene_video_path),
                    vcodec='libx264',
                    pix_fmt='yuv420p',
                    r=30,  # 30 fps
                    **{'b:v': '5M'}  # Bitrate
                )
                .overwrite_output()
                .run(quiet=True)
            )
            
            scene_videos.append(scene_video_path)
        
        # Concatenate all scene videos
        concat_list_path = temp_dir / "concat_list.txt"
        with open(concat_list_path, 'w') as f:
            for video in scene_videos:
                f.write(f"file '{video.absolute()}'\n")
        
        timeline_path = temp_dir / "timeline.mp4"
        
        # Concatenate using concat demuxer (lossless)
        subprocess.run(
            [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_path),
                "-c", "copy",
                "-y",
                str(timeline_path)
            ],
            check=True,
            capture_output=True
        )
        
        return timeline_path
    
    def _encode_video(
        self,
        video_timeline_path: Path,
        audio_path: Path,
        output_path: Path,
        config: VideoConfig
    ):
        """
        Encode final video with audio, optimized for platform and quality preset.
        
        Args:
            video_timeline_path: Path to concatenated video timeline
            audio_path: Path to audio narration
            output_path: Final output path
            config: VideoConfig with encoding settings
        """
        # Quality preset settings
        quality_settings = {
            QualityPreset.ULTRA: {
                'crf': 18,
                'preset': 'slow',
                'profile': 'high'
            },
            QualityPreset.STANDARD: {
                'crf': 23,
                'preset': 'medium',
                'profile': 'main'
            },
            QualityPreset.FAST: {
                'crf': 28,
                'preset': 'fast',
                'profile': 'baseline'
            }
        }
        
        settings = quality_settings[config.quality]
        
        # Platform-specific encoding parameters
        resolution = config.platform_specs['resolution']
        
        # Combine video and audio
        video_input = ffmpeg.input(str(video_timeline_path))
        audio_input = ffmpeg.input(str(audio_path))
        
        (
            ffmpeg
            .output(
                video_input,
                audio_input,
                str(output_path),
                vcodec='libx264',
                acodec='aac',
                **{
                    'crf': settings['crf'],
                    'preset': settings['preset'],
                    'profile:v': settings['profile'],
                    'b:a': '192k',
                    'ar': 44100,
                    'movflags': '+faststart',  # Web optimization
                }
            )
            .overwrite_output()
            .run(capture_output=True, quiet=True)
        )
    
    def _get_platform_resolution(self, platform: Platform) -> tuple:
        """Get resolution tuple for platform."""
        resolutions = {
            Platform.LINKEDIN: (1080, 1080),
            Platform.TIKTOK: (1080, 1920),
            Platform.INSTAGRAM: (1080, 1920),
            Platform.YOUTUBE: (1080, 1920),
        }
        return resolutions[platform]
    
    def get_video_metadata(self, video_path: Path) -> dict:
        """
        Extract metadata from video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)
    
    def cleanup_temp_files(self):
        """Clean up temporary files from video assembly."""
        temp_dir = Path("./temp")
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
            temp_dir.mkdir(exist_ok=True)


# Convenience function
def assemble_video_from_components(
    config: VideoConfig,
    audio_path: Path,
    visual_paths: List[Path],
    output_filename: Optional[str] = None
) -> GenerationResult:
    """
    Quick helper to assemble video without instantiating assembler.
    
    Args:
        config: VideoConfig object
        audio_path: Path to audio file
        visual_paths: List of visual paths
        output_filename: Optional custom filename
        
    Returns:
        GenerationResult with success status
    """
    assembler = VideoAssembler()
    result = assembler.assemble_video(config, audio_path, visual_paths, output_filename)
    
    # Cleanup temp files after assembly
    if result.success:
        assembler.cleanup_temp_files()
    
    return result
