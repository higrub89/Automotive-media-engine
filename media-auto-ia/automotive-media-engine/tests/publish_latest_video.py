"""
Script to publish the latest generated video to YouTube.
Uses the core.youtube_publisher module.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.youtube_publisher import YouTubePublisher

def main():
    # 1. Locate video
    # Note: In a real system, we'd pass this as arg, but for demo we use the known path
    # The previous run generated sf90_hybrid_demo.mp4 (content is Porsche)
    video_path = Path("output/sf90_hybrid_demo.mp4")
    
    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        return 1
        
    print(f"📦 Found video: {video_path}")
    
    # 2. Initialize Publisher
    try:
        publisher = YouTubePublisher()
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return 1
        
    # 3. Upload
    print("🚀 Starting upload process...")
    
    # We use hardcoded metadata for this test, normally this comes from ContentBrief
    title = "Porsche 911 GT3 RS: Ingeniería de la Aerodinámica Activa #AutomotiveEngineering"
    description = """
    Análisis técnico del sistema DRS y gestión del flujo de aire en el Porsche 911 GT3 RS (992).
    
    Puntos clave:
    - Downforce: 860kg a 285 km/h
    - Radiador central único
    - Sistema DRS hidráulico
    
    Generado automáticamente por Automotive Media Engine (AI).
    #Porsche #GT3RS #Engineering #Manim #Tech
    """
    
    try:
        video_id = publisher.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=["Porsche", "Engineering", "Automotive", "GT3 RS", "Tech"],
            privacy_status="private"  # Safer for initial test
        )
        
        print("\n✨ SUCCESS! Video uploaded.")
        print(f"➡️  Check it here: https://youtu.be/{video_id}")
        print("   (Note: It is set to PRIVATE. Go to YouTube Studio to publish it.)")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return 1

if __name__ == "__main__":
    main()
