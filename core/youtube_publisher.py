"""
YouTube Publisher Module.
Handles OAuth2 authentication and video uploading to YouTube channel.
"""

import os
import pickle
import datetime
from pathlib import Path
from typing import Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube scope required for uploading
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class YouTubePublisher:
    """
    Automated YouTube uploader.
    """
    
    def __init__(self, client_secret_file: str = "client_secret.json"):
        self.client_secret_file = Path(client_secret_file)
        self.credentials = None
        self.service = None
        self._authenticate()
        
    def _authenticate(self):
        """Handle OAuth2 flow."""
        token_file = Path("token.pickle")
        
        # Load existing token
        if token_file.exists():
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
                
        # Refresh or Create new token
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not self.client_secret_file.exists():
                    raise FileNotFoundError(f"Missing {self.client_secret_file}. Please download from Google Cloud Console.")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secret_file), SCOPES)
                
                # Manual Console Flow (since run_console is deprecated/removed)
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print("Please visit this URL to authorize this application:")
                print(auth_url)
                print("Enter the authorization code: ")
                
                code = input().strip()
                flow.fetch_token(code=code)
                self.credentials = flow.credentials
                
            # Save token for next time
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        # Build service
        self.service = build('youtube', 'v3', credentials=self.credentials)
        print("✓ YouTube authentication successful")

    def upload_video(
        self, 
        video_path: Path, 
        title: str, 
        description: str, 
        tags: list[str] = [],
        privacy_status: str = "private" # Start as private for safety
    ) -> str:
        """
        Uploads a video to YouTube.
        Returns: Video ID
        """
        body = {
            'snippet': {
                'title': title[:100], # Max 100 chars
                'description': description[:5000],
                'tags': tags,
                'categoryId': '28' # Science & Technology
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False,
            }
        }

        print(f"🚀 Uploading to YouTube: {title}...")
        
        media = MediaFileUpload(
            str(video_path), 
            chunksize=-1, 
            resumable=True
        )
        
        request = self.service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Upload progress: {int(status.progress() * 100)}%")
                
        video_id = response['id']
        print(f"✅ Upload Complete! Video ID: {video_id}")
        print(f"🔗 Link: https://youtu.be/{video_id}")
        
        return video_id

# Test block
if __name__ == "__main__":
    # Simple test
    try:
        publisher = YouTubePublisher()
        # To test upload, uncomment:
        # publisher.upload_video(Path("output/test.mp4"), "Test Video", "Description")
    except Exception as e:
        print(f"Error: {e}")
