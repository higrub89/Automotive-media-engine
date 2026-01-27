"""
Integration test for RYA.ai Pipeline end-to-end flow.

Tests the complete video generation pipeline with mocked external APIs.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from core.pipeline import RYAPipeline
from core.models import StyleArchetype


@pytest.mark.integration
@pytest.mark.asyncio
class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    async def test_pipeline_storytelling_style(self, test_output_dir, mock_video_script):
        """Test complete pipeline execution with STORYTELLING style."""
        
        with patch('core.script_engine.ScriptEngine.generate_script') as mock_script, \
             patch('core.audio_factory.AudioFactory.generate_audio') as mock_audio, \
             patch('core.visual_assembly.VisualAssembly.generate_scene_visual') as mock_visual, \
             patch('core.music_factory.MusicFactory.get_music_for_style') as mock_music, \
             patch('core.music_factory.MusicFactory.mix_audio') as mock_mix, \
             patch('core.video_assembler.VideoAssembler.assemble_video') as mock_assembler, \
             patch('core.gcp_storage.GCPStorage.upload_video') as mock_upload:
            
            # Mock script generation
            mock_script.return_value = mock_video_script
            
            # Mock audio generation
            mock_audio_path = test_output_dir / "test_narration.mp3"
            mock_audio_path.touch()
            mock_audio.return_value = mock_audio_path
            
            # Mock visual generation
            mock_visual_path = test_output_dir / "scene_1.mp4"
            mock_visual_path.touch()
            mock_visual.return_value = mock_visual_path
            
            # Mock music
            mock_music_path = test_output_dir / "music.mp3"
            mock_music_path.touch()
            mock_music.return_value = mock_music_path
            
            # Mock video assembly
            from core.models import GenerationResult
            mock_result = GenerationResult(
                success=True,
                video_path=str(test_output_dir / "final_video.mp4"),
                file_size_mb=15.5,
                duration=30.0,
                generation_time_seconds=10.0,
                metadata={"scenes": 3, "platform": "linkedin"}
            )
            mock_assembler.return_value = mock_result
            
            # Mock GCP upload
            mock_upload.return_value = "https://storage.googleapis.com/test-bucket/video.mp4"
            
            # Run pipeline
            pipeline = RYAPipeline()
            result = await pipeline.run(
                topic="Future of Electric Vehicles",
                style=StyleArchetype.STORYTELLING,
                duration=30
            )
            
            # Assertions
            assert result["status"] == "completed"
            assert result["job_id"] is not None
            assert "output_url" in result
            assert result["metadata"]["scenes"] == 3
            
            # Verify all steps were called
            mock_script.assert_called_once()
            mock_audio.assert_called_once()
            assert mock_visual.call_count == len(mock_video_script.scenes)
            mock_music.assert_called_once()
            mock_assembler.assert_called_once()
    
    async def test_pipeline_technical_style(self, test_output_dir, mock_video_script):
        """Test complete pipeline execution with TECHNICAL style."""
        
        with patch('core.script_engine.ScriptEngine.generate_script') as mock_script, \
             patch('core.audio_factory.AudioFactory.generate_audio') as mock_audio, \
             patch('core.visual_assembly.VisualAssembly.generate_scene_visual') as mock_visual, \
             patch('core.music_factory.MusicFactory.get_music_for_style') as mock_music, \
             patch('core.music_factory.MusicFactory.mix_audio') as mock_mix, \
             patch('core.video_assembler.VideoAssembler.assemble_video') as mock_assembler, \
             patch('core.gcp_storage.GCPStorage.upload_video') as mock_upload:
            
            # Setup mocks
            mock_script.return_value = mock_video_script
            
            mock_audio_path = test_output_dir / "test_narration.mp3"
            mock_audio_path.touch()
            mock_audio.return_value = mock_audio_path
            
            mock_visual_path = test_output_dir / "scene_1.mp4"
            mock_visual_path.touch()
            mock_visual.return_value = mock_visual_path
            
            mock_music_path = test_output_dir / "music.mp3"
            mock_music_path.touch()
            mock_music.return_value = mock_music_path
            
            from core.models import GenerationResult
            mock_result = GenerationResult(
                success=True,
                video_path=str(test_output_dir / "final_video.mp4"),
                file_size_mb=12.3,
                duration=30.0,
                generation_time_seconds=8.5,
                metadata={"scenes": 3, "platform": "linkedin"}
            )
            mock_assembler.return_value = mock_result
            
            mock_upload.return_value = None  # Simulate no GCP credentials
            
            # Run pipeline
            pipeline = RYAPipeline()
            result = await pipeline.run(
                topic="Advanced Battery Technology",
                style=StyleArchetype.TECHNICAL,
                duration=30
            )
            
            # Assertions
            assert result["status"] == "completed"
            assert result["job_id"] is not None
            # Should fall back to local path when GCP is not available
            assert "output" in result["output_url"].lower() or "video" in result["output_url"].lower()
    
    async def test_pipeline_handles_errors_gracefully(self, test_output_dir):
        """Test that pipeline handles errors without crashing."""
        
        with patch('core.script_engine.ScriptEngine.generate_script') as mock_script:
            # Simulate script generation failure
            mock_script.side_effect = Exception("LLM API failure")
            
            pipeline = RYAPipeline()
            result = await pipeline.run(
                topic="Test Topic",
                style=StyleArchetype.DOCUMENTARY,
                duration=30
            )
            
            # Should return failed status instead of crashing
            assert result["status"] == "failed"
            assert "error" in result
            assert "LLM API failure" in result["error"]
