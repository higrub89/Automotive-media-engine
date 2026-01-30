"""
S3 Storage Adapter: Compatible with Cloudflare R2, AWS S3, and MinIO.
Uses boto3 to handle object storage operations cost-effectively.
"""

import os
import boto3
from pathlib import Path
from typing import Optional
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from .logger import get_logger

load_dotenv()

log = get_logger("s3_storage")

class S3Storage:
    """
    Handles video uploads to S3-compatible storage (R2/AWS).
    """
    
    def __init__(self):
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL") # e.g. https://<accountid>.r2.cloudflarestorage.com
        self.access_key = os.getenv("S3_ACCESS_KEY_ID")
        self.secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "rya-videos")
        self.public_url_base = os.getenv("S3_PUBLIC_URL", None) # Optional custom domain
        
        self.client = None
        
        if self.endpoint_url and self.access_key and self.secret_key:
            try:
                self.client = boto3.client(
                    's3',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key
                )
                log.info("S3 Storage initialized", endpoint=self.endpoint_url, bucket=self.bucket_name)
            except Exception as e:
                log.error(f"Failed to initialize S3 client: {e}")
        else:
            log.warning("S3 credentials not found. Cloud upload disabled.")

    def upload_video(self, file_path: Path, destination_blob_name: Optional[str] = None) -> Optional[str]:
        """
        Uploads a video to S3 bucket and returns the public URL.
        """
        if not self.client:
            log.warning("S3 Client not initialized, skipping upload.")
            return None
            
        if not file_path.exists():
            log.error(f"File not found: {file_path}")
            return None

        if not destination_blob_name:
            destination_blob_name = file_path.name

        try:
            log.info(f"Uploading {file_path.name} to {self.bucket_name}/{destination_blob_name}...")
            
            # Upload file
            self.client.upload_file(
                str(file_path), 
                self.bucket_name, 
                destination_blob_name,
                ExtraArgs={'ContentType': 'video/mp4'}
            )
            
            # Generate URL
            if self.public_url_base:
                # Custom domain (e.g. static.ryamedia.com/video.mp4) needs configuration in Cloudflare
                url = f"{self.public_url_base}/{destination_blob_name}"
            else:
                # Fallback to presigned URL if no custom domain (valid for 1 hour)
                # Note: R2 allows public buckets, but signed URLs are safer default
                url = self.client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': destination_blob_name},
                    ExpiresIn=3600
                )
                
            return url
            
        except ClientError as e:
            log.error(f"S3 Upload failed: {e}")
            return None
        except Exception as e:
            log.error(f"Unexpected error during upload: {e}")
            return None
