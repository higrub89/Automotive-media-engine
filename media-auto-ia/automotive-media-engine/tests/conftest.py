"""
Pytest configuration and fixtures for RYA.ai testing.
"""

import pytest
import os
from pathlib import Path

# Set test environment variables
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["DEBUG"] = "true"

# Disable external API calls during tests (unless explicitly enabled)
if "TEST_WITH_REAL_APIS" not in os.environ:
    os.environ["ELEVENLABS_API_KEY"] = ""
    os.environ["GEMINI_API_KEY"] = "test-key"
    os.environ["ANTHROPIC_API_KEY"] = "test-key"

@pytest.fixture
def test_output_dir(tmp_path):
    """Provide a temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

@pytest.fixture
def mock_content_brief():
    """Provide a sample ContentBrief for testing."""
    from core.models import ContentBrief, StyleArchetype, Platform
    
    return ContentBrief(
        topic="Test Topic: Electric Vehicles",
        key_points=[
            "Introduction to EVs",
            "Battery technology",
            "Charging infrastructure",
            "Future outlook"
        ],
        target_duration=30,
        style_archetype=StyleArchetype.TECHNICAL,
        platform=Platform.LINKEDIN
    )

@pytest.fixture
def mock_video_script():
    """Provide a sample VideoScript for testing."""
    from core.models import VideoScript, Scene
    from datetime import datetime
    
    return VideoScript(
        topic="Test Topic",
        total_duration=30,
        scenes=[
            Scene(
                scene_number=1,
                visual_type="title",
                narration_text="This is a test narration.",
                duration=10,
                visual_config={"title": "Test Title", "subtitle": "Test Subtitle"}
            ),
            Scene(
                scene_number=2,
                visual_type="bullet_list",
                narration_text="Here are the key points.",
                duration=10,
                visual_config={"items": ["Point 1", "Point 2", "Point 3"]}
            ),
            Scene(
                scene_number=3,
                visual_type="title",
                narration_text="Thank you for watching.",
                duration=10,
                visual_config={"title": "Conclusion", "subtitle": ""}
            )
        ],
        script_text="This is a test narration. Here are the key points. Thank you for watching.",
        generated_at=datetime.now()
    )
