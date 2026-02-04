import os
import asyncio
from dotenv import load_dotenv
from core.pipeline import RYAPipeline
from core.models import StyleArchetype

load_dotenv()

# Force Edge-TTS for cost control
os.environ["ELEVENLABS_API_KEY"] = ""

async def main():
    topic = "El motor Raxial Flux 'Dark Matter' de Koenigsegg: La mayor densidad de potencia del mundo"
    print(f"🚀 [COMPLEX TEST] Topic: {topic}")
    
    pipeline = RYAPipeline()
    
    def print_progress(progress: int, message: str):
        print(f"  [Progress] {progress}% - {message}")

    try:
        # 60 seconds is enough for a deep technical dive
        result = await pipeline.run(
            topic=topic,
            style=StyleArchetype.TECHNICAL,
            duration=60,
            progress_callback=print_progress
        )
        
        print("\n🏆 COMPLEX GENERATION COMPLETE!")
        print(f"  Status: {result['status']}")
        print(f"  Final Output: {result.get('output_url')}")
        print(f"  Cost: {result.get('metadata', {}).get('cost_report', {})}")
        print(f"  Scenes Generated: {len(result.get('metadata', {}).get('scenes_metadata', []))}")
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
