import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from core.ai_visual_engine import AIVisualEngine
from core.models import StyleArchetype

@pytest.fixture
def engine():
    return AIVisualEngine(output_dir="./tests/output")

def test_pollinations_integration(engine):
    """
    Live test for Tier 1 (Pollinations).
    Should actually generate a file since it's free.
    """
    # Use a simple prompt to ensure speed
    result = engine.generate_image("red cube", style=StyleArchetype.MINIMALIST, tier="auto")
    
    assert result is not None
    assert result.exists()
    assert result.stat().st_size > 0
    # Clean up
    result.unlink()

@patch("replicate.Client")
def test_replicate_mock(mock_client_cls, engine):
    """
    Mock test for Tier 2 (Replicate).
    """
    # Setup mock
    engine.replicate_token = "fake-token"
    mock_client = mock_client_cls.return_value
    mock_client.run.return_value = ["http://fake-url.com/image.png"]
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake-image-content"
        
        result = engine.generate_image("test topic", tier="flux")
        
        assert result is not None
        assert result.exists()
        result.unlink()

@patch("openai.OpenAI")
def test_dalle_mock(mock_openai_cls, engine):
    """
    Mock test for Tier 3 (DALL-E).
    """
    engine.openai_key = "fake-key"
    mock_client = mock_openai_cls.return_value
    mock_response = MagicMock()
    mock_response.data[0].url = "http://fake-dalle.com"
    mock_client.images.generate.return_value = mock_response
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake-dalle-content"
        
        # Force premium tier
        result = engine.generate_image("test topic", tier="premium")
        
        assert result is not None
        assert result.exists()
        result.unlink()
