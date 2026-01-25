"""
Test SSML Prosody Implementation

Generates a short video to validate [PAUSE] and [SHORT_PAUSE] tag functionality.
This will verify the "authority voice" enhancement before full integration.
"""

import sys
from pathlib import Path

# Add core to path
sys.path.append(str(Path(__file__).parent.parent))

from core.models import ContentBrief, Platform, AudienceLevel
from core.script_engine import generate_script_from_brief
from core.audio_factory import AudioFactory
from core.visual_assembly import VisualAssembly
from core.video_assembler import VideoAssembler, VideoConfig


def main():
    print("🎙️  SSML Prosody Control - Validation Test")
    print("=" * 60)
    
    # Create brief focused on dramatic technical narrative
    brief = ContentBrief(
        topic="MV Agusta Brutale 1000 RR - El Motor de 208 CV",
        key_points=[
            "Motor 4 cilindros en línea derivado de MotoGP",
            "208 CV a 13,450 RPM - densidad de potencia extrema",
            "Sistema de contrarotación del cigüeñal para estabilidad",
            "Electrónica de última generación con IMU de 6 ejes"
        ],
        target_duration=60,
        platform=Platform.LINKEDIN,
        audience_level=AudienceLevel.ADVANCED,
        visual_references=["Motor naked bike", "Curva de potencia", "Electrónica racing"]
    )
    
    print(f"\n📋 Brief: {brief.topic}")
    print(f"   Platform: {brief.platform.value} | Duration: {brief.target_duration}s")
    
    # Generate script with prosody tags
    print("\n🧠 Generating script with SSML prosody tags...")
    script = generate_script_from_brief(brief, enable_research=False)
    
    print(f"\n✅ Script generated:")
    print(f"   Scenes: {len(script.scenes)}")
    print(f"   Total narration length: {len(script.script_text)} characters")
    
    # Check if prosody tags were inserted
    pause_count = script.script_text.count("[PAUSE]")
    short_pause_count = script.script_text.count("[SHORT_PAUSE]")
    print(f"\n🎯 Prosody Tag Analysis:")
    print(f"   [PAUSE]: {pause_count}")
    print(f"   [SHORT_PAUSE]: {short_pause_count}")
    
    if pause_count == 0 and short_pause_count == 0:
        print("   ⚠️  WARNING: No prosody tags detected. LLM may need additional training.")
    
    # Generate audio with SSML processing
    print("\n🎙️  Synthesizing voice with SSML...")
    audio_factory = AudioFactory()
    audio_path = audio_factory.generate_audio(script, output_filename="ssml_prosody_test.mp3")
    
    print(f"   ✓ Audio generated: {audio_path}")
    
    # Get audio duration
    duration = audio_factory.get_audio_duration(audio_path)
    print(f"   Duration: {duration:.2f}s (Target: {brief.target_duration}s)")
    
    # Generate visuals
    print("\n🎨 Rendering visuals...")
    visual_assembly = VisualAssembly(platform=brief.platform)
    visual_paths = []
    
    for scene in script.scenes:
        print(f"   Rendering scene {scene.scene_number}: {scene.visual_type}")
        visual_path = visual_assembly.generate_scene_visual(scene)
        visual_paths.append(visual_path)
    
    print(f"   ✓ {len(visual_paths)} scenes rendered")
    
    # Assemble video
    print("\n🎬 Assembling final video...")
    config = VideoConfig(
        resolution=(1920, 1080),
        fps=30,
        output_quality="high"
    )
    
    assembler = VideoAssembler()
    result = assembler.assemble_video(
        config=config,
        audio_path=audio_path,
        visual_paths=visual_paths,
        output_filename="ssml_prosody_validation.mp4"
    )
    
    if result.success:
        print(f"\n✅ SUCCESS!")
        print(f"   Video: {result.video_path}")
        print(f"   Duration: {result.duration}s")
        print("\n🎧 NEXT STEP: Listen to the audio and verify:")
        print("   1. Pauses are audible and natural")
        print("   2. Voice sounds authoritative, not robotic")
        print("   3. Pacing matches a senior technical mentor")
    else:
        print(f"\n❌ ASSEMBLY FAILED: {result.error_message}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
