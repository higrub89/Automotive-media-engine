import pytest
import time
import uuid
import json
from core.queue_manager import queue_manager
from core.worker import process_video_job
from core.models import StyleArchetype

# Mock the pipeline run to avoid actual heavy processing during queue test
import core.worker
from unittest.mock import MagicMock

async def mock_run(**kwargs):
    return {
        "status": "completed",
        "output_url": "http://test-bucket/video.mp4",
        "metadata": {"duration": kwargs.get("duration")}
    }

# Patch the pipeline in the worker module
core.worker.pipeline.run = MagicMock(side_effect=mock_run)

def test_redis_connection():
    """Verify we can talk to Redis"""
    assert queue_manager.redis.ping() is True

def test_job_persistence():
    """Verify JobStore saves and retrieves data"""
    job_id = str(uuid.uuid4())
    data = {"status": "queued", "test_val": 123}
    
    queue_manager.store.save_job(job_id, data)
    
    retrieved = queue_manager.store.get_job(job_id)
    assert retrieved is not None
    assert retrieved["status"] == "queued"
    assert retrieved["test_val"] == 123
    
    # Update
    queue_manager.store.update(job_id, {"status": "processing"})
    updated = queue_manager.store.get_job(job_id)
    assert updated["status"] == "processing"
    assert updated["test_val"] == 123

def test_manual_worker_execution():
    """Verify the worker function updates state correctly"""
    job_id = str(uuid.uuid4())
    
    # Initial state
    queue_manager.store.save_job(job_id, {"status": "queued"})
    
    # Run worker function directly (bypass RQ for logic test)
    process_video_job(
        topic="Test Topic",
        style_archetype=StyleArchetype.MINIMALIST.value, # Pass as string as RQ does
        duration=30,
        job_id=job_id
    )
    
    # Check final state
    final = queue_manager.store.get_job(job_id)
    assert final["status"] == "completed"
    assert final["output_url"] == "http://test-bucket/video.mp4"
