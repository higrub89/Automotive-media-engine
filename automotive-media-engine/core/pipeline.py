import os
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import uuid
import asyncio

from .models import ContentBrief, VideoConfig, StyleArchetype, Platform, QualityPreset
from .script_engine import ScriptEngine
from .audio_factory import AudioFactory
from .visual_assembly import VisualAssembly
from .video_assembler import VideoAssembler
from .music_factory import MusicFactory
from .s3_storage import S3Storage
from .logger import get_logger
from .billing import CostEstimator, UsageMetrics

class RYAPipeline:
    """
    The orchestrator for the RYA.ai multi-style video generation engine.
    """
    
    def __init__(self):
        self.script_engine = ScriptEngine()
        self.audio_factory = AudioFactory()
        self.visual_assembly = VisualAssembly()
        self.video_assembler = VideoAssembler()
        self.music_factory = MusicFactory()
        self.storage = S3Storage()
        
        self.temp_dir = Path("./temp/pipeline")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def run(self, topic: str, style: StyleArchetype, duration: int = 60, voice_id: Optional[str] = None, job_id: Optional[str] = None, progress_callback: Optional[Callable[[int, str], None]] = None) -> Dict[str, Any]:
        """
        Runs the full end-to-end video generation flow.
        """
        if not job_id:
            job_id = str(uuid.uuid4())
            
        job_dir = self.temp_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Get logger with job_id context
        log = get_logger(job_id)
        
        log.info("Pipeline started", topic=topic, style=style.value, duration=duration)
        
        # Initialize usage tracking
        usage_metrics = UsageMetrics()
        
        if progress_callback:
            progress_callback(5, "Generating script...")
        
        try:
            # 1. Generate Script
            brief = ContentBrief(
                topic=topic,
                key_points=[
                    f"Introduction to {topic}",
                    "Key technological advancements",
                    "Impact on the automotive industry",
                    "Future outlook"
                ],
                target_duration=duration,
                style_archetype=style,
                platform=Platform.LINKEDIN # Default to LinkedIn for now
            )
            script = self.script_engine.generate_script(brief)
            log.info("Script generated", scenes=len(script.scenes), total_duration=script.total_duration)
            
            # Track LLM Usage
            if script.usage_metadata:
                usage_metrics.llm_input_tokens += script.usage_metadata.get("input_tokens", 0)
                usage_metrics.llm_output_tokens += script.usage_metadata.get("output_tokens", 0)
            
            # Track TTS Usage
            usage_metrics.tts_characters += len(script.script_text)
            usage_metrics.tts_provider = "elevenlabs" if self.audio_factory.use_elevenlabs else "edge_tts"

            if progress_callback:
                progress_callback(15, "Generating narration...")
            
            # 2. Generate Narration
            narration_path = await self.audio_factory.generate_audio(script, output_filename=f"job_{job_id}_narration.mp3")
            log.info("Narration generated", audio_file=narration_path.name)
            if progress_callback:
                progress_callback(30, "Generating visuals...")
            
            # 3. Generate Visuals (each scene)
            visual_paths = []
            total_scenes = len(script.scenes)
            for i, scene in enumerate(script.scenes):
                scene_filename = f"scene_{scene.scene_number}.mp4"
                
                # Update progress for individual scenes (30% to 70%)
                if progress_callback:
                    current_percent = 30 + int((i / total_scenes) * 40)
                    progress_callback(current_percent, f"Visualizing scene {i+1}/{total_scenes}...")
                
                scene_path = self.visual_assembly.generate_scene_visual(scene, style=style, output_filename=scene_filename)
                visual_paths.append(scene_path)
                
                # Track Image Gen (simplification: 1 image per scene assumed for cost model)
                # In reality, visual_assembly might use 0 or 1 AI image. 
                # For now we assume if it's not a blacklist type, it uses AI.
                if scene.visual_type not in ["title", "list", "code"]:
                    usage_metrics.image_count_pollinations += 1
                    
            log.info("Visuals generated", scene_count=len(visual_paths))
            if progress_callback:
                progress_callback(75, "Mixing audio...")
            
            # 4. Generate & Mix Music
            music_path = self.music_factory.get_music_for_style(style)
            final_audio_path = job_dir / "final_audio.mp3"
            self.music_factory.mix_audio(narration_path, music_path, final_audio_path, style)
            log.info("Music mixed", output_audio=final_audio_path.name)
            if progress_callback:
                progress_callback(85, "Assembling final video...")
            
            # 5. Assemble Video
            config = VideoConfig(
                project_name=f"job_{job_id}",
                script=script,
                quality=QualityPreset.STANDARD
            )
            generation_result = self.video_assembler.assemble_video(
                config=config,
                audio_path=final_audio_path,
                visual_paths=visual_paths,
                output_filename=f"video_{job_id}.mp4"
            )
            
            if not generation_result.success:
                log.error("Video assembly failed", error=generation_result.error_message)
                return {"job_id": job_id, "status": "failed", "error": generation_result.error_message}
                
            log.info("Video assembled", video_path=generation_result.video_path, file_size_mb=generation_result.file_size_mb)
            if progress_callback:
                progress_callback(95, "Uploading to cloud...")
            
            # 6. Upload to Cloud (S3/R2)
            video_path = Path(generation_result.video_path)
            cloud_url = self.storage.upload_video(video_path)
            
            if cloud_url:
                log.info("Video uploaded to Cloud", url=cloud_url)
            else:
                log.warning("Cloud upload skipped (no credentials)", local_path=str(video_path.absolute()))
            
            # Calculate final costs
            cost_report = CostEstimator.calculate_cost(usage_metrics)
            log.info("Cost Report", cost=cost_report)
            
            # Merge cost report into metadata
            final_metadata = generation_result.metadata
            final_metadata["cost_report"] = cost_report
            
            result = {
                "job_id": job_id,
                "status": "completed",
                "output_url": cloud_url or str(video_path.absolute()),
                "metadata": final_metadata
            }
            
            log.info("Pipeline completed successfully", duration_seconds=generation_result.generation_time_seconds)
            if progress_callback:
                progress_callback(100, "Completed")
                
            return result
            
        except Exception as e:
            log.exception("Pipeline failed with exception", error=str(e))
            return {"job_id": job_id, "status": "failed", "error": str(e)}
