import os
import redis
import json
from rq import Queue
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class JobStore:
    """
    Persists job metadata in Redis separately from the RQ queue.
    This allows us to track detailed progress and results even after RQ finishes.
    """
    def __init__(self, redis_conn):
        self.redis = redis_conn
        self.prefix = "rya:job:"
        self.ttl = 86400  # 24 hours retention

    def _key(self, job_id: str) -> str:
        return f"{self.prefix}{job_id}"

    def save_job(self, job_id: str, data: Dict[str, Any]):
        """Creates or overwrites a job record."""
        self.redis.setex(
            self._key(job_id),
            self.ttl,
            json.dumps(data)
        )

    def update(self, job_id: str, updates: Dict[str, Any]):
        """Updates specific fields of a job."""
        key = self._key(job_id)
        current_data = self.redis.get(key)
        
        if current_data:
            data = json.loads(current_data)
            data.update(updates)
            self.redis.setex(key, self.ttl, json.dumps(data))
        else:
            # Job disappeared? Re-create it
            self.save_job(job_id, updates)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves job data."""
        data = self.redis.get(self._key(job_id))
        return json.loads(data) if data else None


class QueueManager:
    """
    Central access point for Redis and RQ.
    """
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.from_url(redis_url)
        self.queue = Queue("default", connection=self.redis)
        self.store = JobStore(self.redis)

    def enqueue_job(self, job_id: str, func, **kwargs):
        """
        Enqueues a job in RQ and creates the initial record in JobStore.
        """
        # 1. Add to RQ
        self.queue.enqueue_call(
            func=func,
            args=[],
            kwargs={**kwargs, "job_id": job_id},
            job_id=job_id,
            result_ttl=86400
        )
        
        # 2. Key is already created by API before calling this, 
        # but we ensure connection is alive.
        return job_id

# Global instance
queue_manager = QueueManager()
