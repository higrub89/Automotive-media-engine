import os
from pathlib import Path
from typing import Optional
from google.cloud import storage
from datetime import datetime, timedelta
from logger import get_logger

log = get_logger("gcp_storage")

class GCPStorage:
    """
    Wrapper for Google Cloud Storage for professional asset management.
    """
    
    def __init__(self, bucket_name: Optional[str] = None):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.bucket_name = bucket_name or os.getenv("GCP_STORAGE_BUCKET", "rya-assets-prod")
        
        # Initialize client (requires GOOGLE_APPLICATION_CREDENTIALS)
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.client = storage.Client()
            self.bucket = self.client.bucket(self.bucket_name)
        else:
            self.client = None
            self.bucket = None
            log.warning("GCP credentials not found, GCS operations disabled")

    def upload_video(self, local_path: Path, destination_blob_name: Optional[str] = None) -> Optional[str]:
        """
        Uploads a video to GCS and returns its public or signed URL.
        """
        if not self.bucket:
            return None
            
        if not destination_blob_name:
            destination_blob_name = f"videos/{local_path.name}"
            
        blob = self.bucket.blob(destination_blob_name)
        
        log.info("Uploading video to GCS", filename=local_path.name, bucket=self.bucket_name)
        blob.upload_from_filename(str(local_path))
        log.info("Upload completed", blob_name=destination_blob_name)
        
        return self.get_signed_url(destination_blob_name)

    def get_signed_url(self, blob_name: str, expiration_minutes: int = 60) -> str:
        """
        Generates a v4 signed URL for a specific blob.
        """
        if not self.bucket:
            return ""
            
        blob = self.bucket.blob(blob_name)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
        )
        
        return url
