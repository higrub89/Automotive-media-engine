import os
import time
from rq import Worker, Queue
from core.queue_manager import queue_manager
from core.pipeline import RYAPipeline
from core.logger import get_logger
from core.models import StyleArchetype

# Pre-load pipeline to avoid loading it on every job
logger = get_logger("worker")
logger.info("🚀 Initializing Worker Pipeline...")
pipeline = RYAPipeline()
logger.info("✅ Worker Pipeline Ready!")

def process_video_job(topic: str, style_archetype: str, duration: int, voice_id: str = None, job_id: str = None):
    """
    Worker function executed by RQ.
    """
    job_log = get_logger(job_id)
    job_log.info(f"👷 Worker started job: {topic} ({style_archetype})")
    
    # Update status to processing
    queue_manager.store.update(job_id, {"status": "processing", "progress": 5})
    
    try:
        # Convert string back to Enum
        style = StyleArchetype(style_archetype)
        
        # Run Pipeline (Sync wrapper around async if needed, or use async worker)
        # Since pipeline.run is async, we need to run it synchronously here
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        
        # Define progress callback
        def update_progress(progress_percent: int, status_message: str):
            """Updates progress in Redis."""
            queue_manager.store.update(job_id, {
                "progress": progress_percent,
                "status": "processing" if progress_percent < 100 else "completed",
                "status_message": status_message
            })

        result = loop.run_until_complete(
            pipeline.run(
                topic=topic,
                style=style,
                duration=duration,
                voice_id=voice_id,
                job_id=job_id,
                progress_callback=update_progress
            )
        )
        loop.close()
        
        # Save final result
        queue_manager.store.update(job_id, result)
        job_log.info("✅ Worker finished job successfully")
        
    except Exception as e:
        logger.exception(f"❌ Worker failed job {job_id}")
        queue_manager.store.update(job_id, {
            "status": "failed", 
            "error": str(e)
        })
        raise e

def start_worker():
    """Starts the RQ worker listening on 'default'."""
    worker = Worker(["default"], connection=queue_manager.redis)
    worker.work()

if __name__ == "__main__":
    start_worker()
