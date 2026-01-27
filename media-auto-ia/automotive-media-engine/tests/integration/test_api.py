"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from api.main import app
from core.models import StyleArchetype


@pytest.mark.api
class TestVideoAPI:
    """Test video generation API endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)
    
    def test_generate_video_endpoint(self):
        """Test POST /video/generate endpoint."""
        
        request_data = {
            "topic": "Future of Autonomous Vehicles",
            "duration": 60,
            "platforms": ["linkedin"],
            "style_archetype": "technical"
        }
        
        response = self.client.post("/video/generate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "job_id" in data
        assert data["status"] == "queued"
        assert data["progress"] == 0
        assert data["output_url"] is None
    
    def test_get_status_endpoint_existing_job(self):
        """Test GET /video/status/{job_id} for existing job."""
        
        # First create a job
        request_data = {
            "topic": "Electric Vehicle Charging",
            "duration": 45,
            "style_archetype": "storytelling"
        }
        
        create_response = self.client.post("/video/generate", json=request_data)
        job_id = create_response.json()["job_id"]
        
        # Then check its status
        status_response = self.client.get(f"/video/status/{job_id}")
        
        assert status_response.status_code == 200
        data = status_response.json()
        
        assert data["job_id"] == job_id
        assert "status" in data
        assert data["status"] in ["queued", "processing", "completed", "failed"]
    
    def test_get_status_endpoint_nonexistent_job(self):
        """Test GET /video/status/{job_id} for non-existent job."""
        
        fake_job_id = "00000000-0000-0000-0000-000000000000"
        
        response = self.client.get(f"/video/status/{fake_job_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_api_validates_style_archetype(self):
        """Test that API validates style_archetype enum."""
        
        request_data = {
            "topic": "Test Topic",
            "duration": 30,
            "style_archetype": "INVALID_STYLE"  # Invalid
        }
        
        response = self.client.post("/video/generate", json=request_data)
        
        # Should return 422 Unprocessable Entity
        assert response.status_code == 422
    
    def test_api_uses_default_values(self):
        """Test that API uses default values for optional fields."""
        
        # Minimal request with only required field
        request_data = {
            "topic": "Minimal Test Topic"
        }
        
        response = self.client.post("/video/generate", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "queued"
        # Defaults should be applied by the model
