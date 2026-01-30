import os
import asyncio
from dotenv import load_dotenv
from typing import Optional

# Load environment logic
load_dotenv()

# Force Edge-TTS for testing (avoid quota limits)
os.environ["ELEVENLABS_API_KEY"] = ""

# Import Pipeline
from core.pipeline import RYAPipeline
from core.models import StyleArchetype

async def main():
    print("🧪 Starting Manual Pipeline Test...")
    
    # Initialize Pipeline
    pipeline = RYAPipeline()
    
    # Force mock mode for GCP if no credentials
    print("⚠️ Cloud Credentials not checked (using generic storage).")
    # pipeline.storage.client checks credentials internally
        
    # Define test callback
    def print_progress(progress: int, message: str):
        print(f"🔄 Progress: {progress}% - {message}")

    # Run test job
    try:
        topic = "El Futuro de la IA Generativa"
        result = await pipeline.run(
            topic=topic,
            style=StyleArchetype.STORYTELLING,
            duration=15,  # Short duration for quick test
            progress_callback=print_progress
        )
        
        print("\n🎉 Test Finished!")
        print(f"Status: {result['status']}")
        print(f"Output: {result.get('output_url')}")
        print(f"Metadata: {result.get('metadata')}")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
