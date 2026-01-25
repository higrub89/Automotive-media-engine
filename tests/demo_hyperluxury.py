"""
Hyperluxury Enhancement Demo

Generates a complete video demonstrating:
1. SSML Prosody Control (authority voice with strategic pauses)
2. Visual Hybridization (real technical photos + Manim)
3. Strategic Monetization hints
4. Auto-upload to YouTube (optional)
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.models import ContentBrief, Platform, AudienceLevel
from core.script_engine import generate_script_from_brief
from core.audio_factory import AudioFactory
from core.visual_assembly import VisualAssembly
from core.video_assembler import VideoAssembler, VideoConfig


def main():
    print("🏎️  HYPERLUXURY ENHANCEMENT - Full Pipeline Demo")
    print("=" * 70)
    print("Testing: SSML Prosody + Visual Hybridization + Monetization Layer")
    print("=" * 70)
    
    # Create brief for technical automotive content
    brief = ContentBrief(
        topic="Ferrari 296 GTB - El V6 Híbrido que Redefine lo Imposible",
        key_points=[
            "Motor V6 biturbo de 120° con 663 CV + motor eléctrico de 167 CV",
            "830 CV totales con distribución de potencia inteligente",
            "0-100 km/h en 2.9 segundos, velocidad máxima 330 km/h",
            "Arquitectura híbrida plug-in con 25 km de autonomía eléctrica pura",
            "Telemetría en tiempo real y modos de conducción adaptativos"
        ],
        target_duration=90,
        platform=Platform.YOUTUBE,
        audience_level=AudienceLevel.INTERMEDIATE,
        visual_references=[
            "Motor V6 híbrido en detalle",
            "Gráfica de distribución de potencia",
            "Especificaciones técnicas del sistema"
        ],
        call_to_action="¿Qué opinas del futuro híbrido de las superdeportivas?"
    )
    
    print(f"\n📋 Content Brief:")
    print(f"   Topic: {brief.topic}")
    print(f"   Platform: {brief.platform.value}")
    print(f"   Target Duration: {brief.target_duration}s")
    print(f"   Audience: {brief.audience_level.value}")
    
    # Step 1: Generate Script with SSML Prosody
    print("\n🧠 [1/4] Generating script with SSML prosody tags...")
    print("   (Expecting [PAUSE] and [SHORT_PAUSE] tags from LLM)")
    
    script = generate_script_from_brief(brief, enable_research=False)
    
    print(f"   ✓ Script generated: {len(script.scenes)} scenes")
    print(f"   ✓ Total narration: {len(script.script_text)} chars")
    
    # Analyze prosody usage
    pause_count = script.script_text.count("[PAUSE]")
    short_pause_count = script.script_text.count("[SHORT_PAUSE]")
    
    print(f"\n   📊 Prosody Analysis:")
    print(f"      [PAUSE]:       {pause_count}")
    print(f"      [SHORT_PAUSE]: {short_pause_count}")
    
    if pause_count + short_pause_count > 0:
        print(f"      ✅ Prosody tags detected - voice will have authority")
    else:
        print(f"      ⚠️  No prosody tags - LLM may need more training")
    
    # Step 2: Generate Audio with SSML
    print("\n🎙️  [2/4] Synthesizing voice with SSML processing...")
    
    audio_factory = AudioFactory()
    audio_path = audio_factory.generate_audio(script, output_filename="hyperluxury_demo.mp3")
    
    duration = audio_factory.get_audio_duration(audio_path)
    print(f"   ✓ Audio: {audio_path}")
    print(f"   ✓ Duration: {duration:.1f}s (Target: {brief.target_duration}s)")
    
    # Step 3: Generate Visuals (including images)
    print("\n🎨 [3/4] Rendering hybrid visuals...")
    print("   (Combining Manim animations + real technical photos)")
    
    visual_assembly = VisualAssembly(platform=brief.platform)
    visual_paths = []
    
    for i, scene in enumerate(script.scenes, 1):
        visual_indicator = "📷 IMAGE" if scene.visual_type == "image" else f"🎬 {scene.visual_type.upper()}"
        print(f"   [{i}/{len(script.scenes)}] {visual_indicator}: {scene.narration_text[:50]}...")
        
        visual_path = visual_assembly.generate_scene_visual(scene)
        visual_paths.append(visual_path)
    
    print(f"   ✓ All {len(visual_paths)} scenes rendered")
    
    # Step 4: Assemble Final Video
    print("\n🎬 [4/4] Assembling final video...")
    
    config = VideoConfig(
        project_name="hyperluxury_demo",
        script=script,
        resolution=(1920, 1080),
        fps=30,
        output_quality="high"
    )
    
    assembler = VideoAssembler()
    result = assembler.assemble_video(
        config=config,
        audio_path=audio_path,
        visual_paths=visual_paths,
        output_filename="ferrari_296_gtb_hyperluxury_demo.mp4"
    )
    
    if result.success:
        print(f"\n{'=' * 70}")
        print(f"✅ SUCCESS - F1-GRADE VIDEO READY")
        print(f"{'=' * 70}")
        print(f"📹 Video: {result.video_path}")
        print(f"⏱️  Duration: {result.duration:.1f}s")
        print(f"\n🎯 Quality Checkpoints:")
        print(f"   [{'✓' if pause_count > 0 else ' '}] SSML Prosody (Authority Voice)")
        print(f"   [{'✓' if any(s.visual_type == 'image' for s in script.scenes) else ' '}] Visual Hybridization (Real Photos)")
        print(f"   [ ] Strategic Monetization (Check script for tool mentions)")
        print(f"\n🎬 Play video: mpv {result.video_path}")
        
        # Optional: Auto-upload to YouTube
        print(f"\n{'=' * 70}")
        upload = input("📺 Upload to YouTube? (y/n): ").strip().lower()
        
        if upload == 'y':
            print("\n📤 Uploading to YouTube...")
            try:
                from core.youtube_publisher import YouTubePublisher
                
                publisher = YouTubePublisher()
                video_id = publisher.upload_video(
                    video_path=result.video_path,
                    title=brief.topic,
                    description=f"Análisis técnico completo del {brief.topic}.\n\n"
                                f"Puntos clave:\n" + "\n".join(f"- {p}" for p in brief.key_points),
                    tags=["Ferrari", "296 GTB", "Híbrido", "Superdeportivo", "Motor V6"]
                )
                
                print(f"\n✅ VIDEO PUBLICADO")
                print(f"🔗 https://youtube.com/watch?v={video_id}")
                
            except Exception as e:
                print(f"\n⚠️  Upload error: {e}")
                print(f"   (Manual upload available)")
        
        return 0
        
    else:
        print(f"\n❌ ASSEMBLY FAILED: {result.error_message}")
        return 1


if __name__ == "__main__":
    exit(main())
