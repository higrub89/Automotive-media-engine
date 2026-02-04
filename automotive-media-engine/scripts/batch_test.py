import os
import asyncio
from dotenv import load_dotenv
from core.pipeline import RYAPipeline
from core.models import StyleArchetype

load_dotenv()

# Force Edge-TTS for testing
os.environ["ELEVENLABS_API_KEY"] = ""

async def run_single_test(topic, style, duration=15):
    print(f"\n🚀 [TEST] Topic: '{topic}' | Style: {style.value}")
    pipeline = RYAPipeline()
    
    def print_progress(progress: int, message: str):
        # Print only major steps to avoid noise in batch test
        if progress % 25 == 0 or progress == 100 or "Progress" not in message:
             print(f"  [{topic[:15]}...] {progress}% - {message}")

    try:
        result = await pipeline.run(
            topic=topic,
            style=style,
            duration=duration,
            progress_callback=print_progress
        )
        print(f"  ✅ SUCCESS: {result['status']}")
        print(f"  💰 Cost: {result.get('metadata', {}).get('cost_report', {})}")
        return True
    except Exception as e:
        print(f"  ❌ FAILED: {topic} - {e}")
        return False

async def main():
    print("🧪 Starting Batch Pipeline Generation Test...")
    
    tests = [
        ("Sistemas de Propulsión de Hidrógeno", StyleArchetype.TECHNICAL),
        ("La Leyenda del Lancia Stratos", StyleArchetype.STORYTELLING),
        ("Evolución de la Aerodinámica en F1", StyleArchetype.DOCUMENTARY),
        ("Interiores Minimalistas en EVs", StyleArchetype.MINIMALIST)
    ]
    
    results = []
    for topic, style in tests:
        success = await run_single_test(topic, style)
        results.append((topic, success))
        # Small delay between tests to be kind to APIs
        await asyncio.sleep(2)

    print("\n--- BATCH TEST SUMMARY ---")
    for topic, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {topic}")

if __name__ == "__main__":
    asyncio.run(main())
