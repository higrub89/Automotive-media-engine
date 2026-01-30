from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

# Remove direct pipeline import, use queue_manager
from core.models import StyleArchetype
from core.logger import get_logger
from core.queue_manager import queue_manager
from core.worker import process_video_job # Import function reference for RQ

router = APIRouter(
    prefix="/video",
    tags=["video"],
)

# System logger for API
log = get_logger("api")

# Health Check Endpoint
@router.get("/health")
async def health_check():
    """
    Health check for Docker/K8s.
    Checks:
    1. API is up.
    2. REDIS connection (optional but recommended).
    """
    # The queue_manager is already imported at the top of the file.
    # from core.queue_manager import queue_manager # This line is redundant here.
    redis_status = "ok"
    try:
        if not queue_manager.redis.ping():
            redis_status = "error"
    except Exception:
        redis_status = "disconnected"

    return {
        "status": "healthy",
        "service": "rya-api",
        "redis": redis_status
    }

class VideoRequest(BaseModel):
    topic: str
    duration: int = 60
    platforms: List[str] = ["linkedin"]
    style_archetype: StyleArchetype = StyleArchetype.TECHNICAL
    voice_id: Optional[str] = None

class VideoStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    status_message: Optional[str] = None
    output_url: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None

@router.post("/generate", response_model=VideoStatus)
async def generate_video(request: VideoRequest):
    job_id = str(uuid.uuid4())
    
    log.info("Video generation requested", 
             job_id=job_id, 
             topic=request.topic, 
             style=request.style_archetype.value)
    
    # 1. Initialize Job State in Redis
    initial_state = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "output_url": None,
        "input": request.model_dump()
    }
    queue_manager.store.save_job(job_id, initial_state)
    
    # 2. Enqueue Job
    queue_manager.enqueue_job(
        job_id=job_id, 
        func=process_video_job,
        topic=request.topic,
        style_archetype=request.style_archetype.value, # Pass as string
        duration=request.duration,
        voice_id=request.voice_id
    )
    
    log.info("Job queued successfully via Redis", job_id=job_id)
    return initial_state

@router.get("/status/{job_id}", response_model=VideoStatus)
async def get_status(job_id: str):
    job = queue_manager.store.get_job(job_id)
    
    if not job:
        log.warning("Job not found in Redis", job_id=job_id)
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job
