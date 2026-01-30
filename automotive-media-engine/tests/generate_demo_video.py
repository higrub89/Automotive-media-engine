#!/usr/bin/env python3
"""
Demo Video Generator - Creates first test video from SF90 content brief.

This script demonstrates the complete pipeline:
1. Parse content brief
2. Generate script with Gemini
3. Generate audio with ElevenLabs
4. Generate visuals
5. Assemble final video

Usage:
    python tests/generate_demo_video.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import ContentBrief, VideoConfig, Platform, AudienceLevel, QualityPreset
from core.script_engine import ScriptEngine, LLMProvider
from core.audio_factory import AudioFactory
from core.visual_assembly import VisualAssembly
from core.video_assembler import VideoAssembler

load_dotenv()


def create_demo_brief() -> ContentBrief:
    """Create demo content brief programmatically."""
    return ContentBrief(
        topic="MV Agusta Brutale 1000 RR - Radial Valve Engineering",
        key_points=[
            "Signature Radial Valve geometry (F1 inspired)",
            "Titanium connecting rods reducing reciprocating mass",
            "208 HP at 13,000 RPM from 998cc inline-four",
            "Carbon fiber winglets for high-speed stability"
        ],
        target_duration=60,
        platform=Platform.LINKEDIN,
        audience_level=AudienceLevel.ADVANCED,
        visual_references=[
            "Radial valve combustion chamber diagram",
            "Titanium rod stress analysis",
            "Power curve showing high-RPM dominance"
        ],
        call_to_action="Is this the most beautiful naked bike ever made?"
    )


def main():
    """Generate demo video."""
    print("=" * 70)
    print("AUTOMOTIVE MEDIA ENGINE - DEMO VIDEO GENERATION")
    print("=" * 70)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Create content brief
        print("📝 Step 1: Creating content brief...")
        brief = create_demo_brief()
        print(f"   Topic: {brief.topic}")
        print(f"   Platform: {brief.platform.value}")
        print(f"   Target duration: {brief.target_duration}s")
        print(f"   ✓ Brief created\n")
        
        # Step 2: Generate script
        print("🤖 Step 2: Generating script with Gemini...")
        engine = ScriptEngine(provider=LLMProvider.GEMINI)
        script = engine.generate_script(brief)
        
        print(f"   Generated {len(script.scenes)} scenes")
        print(f"   Total duration: {script.total_duration}s")
        print(f"   Speaking pace: {script.words_per_minute:.0f} WPM")
        print(f"   ✓ Script generated\n")
        
        # Validate script
        is_valid, error = engine.validate_script(script)
        if not is_valid:
            print(f"   ⚠️  Script validation warning: {error}")
            print("   Continuing anyway for demo purposes...\n")
        
        # Show script preview
        print("   Script preview (first 150 chars):")
        print(f"   \"{script.script_text[:150]}...\"\n")
        
        # Step 3: Generate audio
        print("🎙️  Step 3: Generating audio narration...")
        audio_factory = AudioFactory()
        audio_path = audio_factory.generate_audio(
            script,
            output_filename="sf90_demo_narration.mp3"
        )
        print(f"   Audio saved: {audio_path}")
        
        # Get actual audio duration
        actual_duration = audio_factory.get_audio_duration(audio_path)
        print(f"   Actual audio duration: {actual_duration}s")
        print(f"   ✓ Audio generated\n")
        
        # Step 4: Generate visuals
        print("🎨 Step 4: Rendering technical animations with Manim...")
        print("   (This takes longer than static images - generating precision vectors)")
        visual_assembly = VisualAssembly(platform=brief.platform)
        
        visual_paths = []
        for i, scene in enumerate(script.scenes, 1):
            print(f"   Rendering scene {i}/{len(script.scenes)}...", end="", flush=True)
            path = visual_assembly.generate_scene_visual(scene)
            visual_paths.append(path)
            print(f" ✓ Done ({path.name})")
        
        print(f"   ✓ All animations rendered\n")
        
        # Step 5: Assemble video
        print("🎬 Step 5: Assembling final video...")
        
        config = VideoConfig(
            project_name="porsche_gt3rs_aero",
            script=script,
            quality=QualityPreset.STANDARD,
            voice_id="es-ES-AlvaroNeural"  # Spanish Senior Mentor
        )
        
        assembler = VideoAssembler()
        result = assembler.assemble_video(
            config,
            audio_path,
            visual_paths,
            output_filename="sf90_hybrid_demo.mp4"
        )
        
        if result.success:
            print(f"   ✓ Video assembled successfully!\n")
            print("=" * 70)
            print("✅ DEMO VIDEO GENERATION COMPLETE")
            print("=" * 70)
            print(f"\n📹 Output: {result.video_path}")
            print(f"   Duration: {result.duration}s")
            print(f"   File size: {result.file_size_mb:.2f} MB")
            print(f"   Generation time: {result.generation_time_seconds:.1f}s")
            print(f"   Platform: {config.platform_specs['resolution'][0]}x{config.platform_specs['resolution'][1]} ({brief.platform.value})")
            print(f"\n🎉 Your first automated technical video is ready!")
            print(f"\nNext steps:")
            print(f"  1. Review the video: vlc {result.video_path}")
            print(f"  2. Check audio quality and pacing")
            print(f"  3. Verify visual aesthetic matches your brand")
            print(f"  4. If satisfied, create more content briefs in content/")
            print(f"  5. Scale to daily production!")
            
            # Cleanup temp files
            assembler.cleanup_temp_files()
            
            # AUTOMATED YOUTUBE UPLOAD
            print("\n📺 Step 6: Automated YouTube Distribution...")
            try:
                from core.youtube_publisher import YouTubePublisher
                publisher = YouTubePublisher()
                
                # Dynamic metadata from brief
                pub_title = f"MV Agusta 1000 RR: Ingeniería Radial (AI Explained) #Shorts"
                pub_desc = f"""Technical analysis of the MV Agusta Brutale 1000 RR.
                
                Key Engineering Points:
                - {brief.key_points[0]}
                - {brief.key_points[1]}
                - {brief.key_points[2]}
                
                Generated by AutoMedia Engine (Gemini + Manim + Local AI).
                #MVAgusta #Motorcycle #Engineering #Manim
                """
                
                publisher.upload_video(
                    video_path=result.video_path,
                    title=pub_title,
                    description=pub_desc,
                    tags=["MV Agusta", "Engineering", "Motorcycle", "Tech", "Manim"],
                    privacy_status="private" 
                )
            except Exception as e:
                print(f"   ⚠️ Upload failed: {e}")
            
            return 0
        else:
            print(f"   ❌ Video assembly failed: {result.error_message}\n")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user")
        return 130
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
