from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

from core.pipeline import RYAPipeline
from core.models import StyleArchetype
from core.logger import get_logger

router = APIRouter(
    prefix="/video",
    tags=["video"],
)

# Initialize Pipeline
pipeline = RYAPipeline()

# System logger for API
log = get_logger("api")

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
    output_url: Optional[str] = None
    metadata: Optional[dict] = None

# Mock database
jobs = {}

async def process_video_generation(job_id: str, request: VideoRequest):
    """Background task to run the RYA.ai pipeline."""
    job_log = get_logger(job_id)
    
    try:
        jobs[job_id]["status"] = "processing"
        job_log.info("Background task started", topic=request.topic)
        
        result = await pipeline.run(
            topic=request.topic,
            style=request.style_archetype,
            duration=request.duration,
            voice_id=request.voice_id
        )
        jobs[job_id].update(result)
        job_log.info("Background task completed", status=result["status"])
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        job_log.exception("Background task failed", error=str(e))

@router.post("/generate", response_model=VideoStatus)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    
    log.info("Video generation requested", 
             job_id=job_id, 
             topic=request.topic, 
             style=request.style_archetype.value,
             duration=request.duration)
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "output_url": None
    }
    
    background_tasks.add_task(process_video_generation, job_id, request)
    
    log.info("Job queued successfully", job_id=job_id)
    return jobs[job_id]

@router.get("/status/{job_id}", response_model=VideoStatus)
async def get_status(job_id: str):
    if job_id not in jobs:
        log.warning("Job not found", job_id=job_id)
        raise HTTPException(status_code=404, detail="Job not found")
    
    log.debug("Status requested", job_id=job_id, status=jobs[job_id]["status"])
    return jobs[job_id]
