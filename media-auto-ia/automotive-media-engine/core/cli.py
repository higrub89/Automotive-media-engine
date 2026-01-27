"""
Automotive Media Engine - CLI

Unified command-line interface for F1-grade video production.

Commands:
  generate  - Generate a complete video from topic
  publish   - Upload video to YouTube
  test      - Validate pipeline components
  
Example:
  python -m core.cli generate --topic "Lamborghini Aventador SVJ" --platform youtube
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .models import ContentBrief, Platform, AudienceLevel
from .script_engine import generate_script_from_brief
from .audio_factory import AudioFactory
from .visual_assembly import VisualAssembly
from .video_assembler import VideoAssembler, VideoConfig


class CLI:
    """Command-line interface for video generation pipeline."""
    
    def __init__(self):
        self.parser = self._build_parser()
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser with all commands."""
        parser = argparse.ArgumentParser(
            description="Automotive Media Engine - F1-Grade Video Production CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")
        
        # GENERATE command
        gen_parser = subparsers.add_parser(
            "generate",
            help="Generate a complete video from topic"
        )
        gen_parser.add_argument(
            "--topic",
            required=True,
            help="Video topic (in quotes). Example: 'Ferrari 296 GTB - El V6 Híbrido'"
        )
        gen_parser.add_argument(
            "--platform",
            default="linkedin",
            choices=["linkedin", "youtube", "tiktok", "instagram"],
            help="Target platform (default: linkedin)"
        )
        gen_parser.add_argument(
            "--audience",
            default="intermediate",
            choices=["beginner", "intermediate", "advanced"],
            help="Audience level (default: intermediate)"
        )
        gen_parser.add_argument(
            "--duration",
            type=int,
            default=60,
            help="Target duration in seconds (default: 60)"
        )
        gen_parser.add_argument(
            "--no-research",
            action="store_true",
            help="Disable DuckDuckGo research (faster but less context)"
        )
        gen_parser.add_argument(
            "--auto-upload",
            action="store_true",
            help="Automatically upload to YouTube after generation"
        )
        gen_parser.add_argument(
            "--output",
            help="Custom output filename (without extension)"
        )
        
        # PUBLISH command
        pub_parser = subparsers.add_parser(
            "publish",
            help="Upload video to YouTube"
        )
        pub_parser.add_argument(
            "video_path",
            help="Path to video file"
        )
        pub_parser.add_argument(
            "--title",
            help="Video title (defaults to filename)"
        )
        pub_parser.add_argument(
            "--description",
            help="Video description"
        )
        
        # TEST command
        test_parser = subparsers.add_parser(
            "test",
            help="Test pipeline components"
        )
        test_parser.add_argument(
            "--component",
            choices=["script", "audio", "visual", "all"],
            default="all",
            help="Component to test (default: all)"
        )
        
        return parser
    
    def run(self, args: Optional[list] = None):
        """Execute CLI command."""
        parsed = self.parser.parse_args(args)
        
        if parsed.command == "generate":
            return self._cmd_generate(parsed)
        elif parsed.command == "publish":
            return self._cmd_publish(parsed)
        elif parsed.command == "test":
            return self._cmd_test(parsed)
    
    def _cmd_generate(self, args) -> int:
        """Generate complete video."""
        print("🏎️  AUTOMOTIVE MEDIA ENGINE - CLI")
        print("=" * 70)
        print(f"Topic: {args.topic}")
        print(f"Platform: {args.platform}")
        print(f"Audience: {args.audience}")
        print(f"Duration: {args.duration}s")
        print("=" * 70)
        
        # Create brief
        brief = ContentBrief(
            topic=args.topic,
            key_points=[f"Auto-generated content brief for: {args.topic}"],
            target_duration=args.duration,
            platform=Platform(args.platform),
            audience_level=AudienceLevel(args.audience)
        )
        
        # Step 1: Generate Script
        print("\n🧠 [1/4] Generating script...")
        enable_research = not args.no_research
        
        if enable_research:
            print("   (Research: ENABLED - enriching with real-time data)")
        else:
            print("   (Research: DISABLED - using base knowledge)")
        
        try:
            from .script_engine import ScriptEngine
            engine = ScriptEngine()
            script = engine.generate_script(brief, enable_research=enable_research)
            
            # Soft validation - warn but don't fail
            is_valid, error = engine.validate_script(script)
            if not is_valid:
                print(f"   ⚠️  Validation warning: {error}")
                print(f"   → Continuing anyway (non-critical)")
            
            print(f"   ✓ Script: {len(script.scenes)} scenes, {len(script.script_text)} chars")
            
            # Prosody analysis
            pause_count = script.script_text.count("[PAUSE]")
            short_pause_count = script.script_text.count("[SHORT_PAUSE]")
            total_prosody = pause_count + short_pause_count
            
            if total_prosody > 0:
                print(f"   ✓ Prosody: {total_prosody} tags (authority voice)")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            return 1
        
        # Step 2: Generate Audio
        print("\n🎙️  [2/4] Synthesizing voice...")
        
        try:
            audio_factory = AudioFactory()
            audio_path = audio_factory.generate_audio(script)
            duration = audio_factory.get_audio_duration(audio_path)
            
            print(f"   ✓ Audio: {audio_path}")
            print(f"   ✓ Duration: {duration:.1f}s")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            return 1
        
        # Step 3: Generate Visuals
        print("\n🎨 [3/4] Rendering visuals...")
        
        try:
            visual_assembly = VisualAssembly(platform=brief.platform)
            visual_paths = []
            
            for i, scene in enumerate(script.scenes, 1):
                indicator = "📷" if scene.visual_type == "image" else "🎬"
                print(f"   [{i}/{len(script.scenes)}] {indicator} {scene.visual_type.upper()}")
                
                visual_path = visual_assembly.generate_scene_visual(scene)
                visual_paths.append(visual_path)
            
            print(f"   ✓ Rendered: {len(visual_paths)} scenes")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            return 1
        
        # Step 4: Assemble Video
        print("\n🎬 [4/4] Assembling video...")
        
        try:
            output_filename = args.output if args.output else args.topic.replace(" ", "_").lower()
            if not output_filename.endswith(".mp4"):
                output_filename += ".mp4"
            
            config = VideoConfig(
                project_name=output_filename.replace(".mp4", ""),
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
                output_filename=output_filename
            )
            
            if not result.success:
                print(f"   ❌ Assembly failed: {result.error_message}")
                return 1
            
            print(f"   ✓ Video: {result.video_path}")
            print(f"   ✓ Duration: {result.duration:.1f}s")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            return 1
        
        # Success summary
        print("\n" + "=" * 70)
        print("✅ VIDEO GENERATION COMPLETE")
        print("=" * 70)
        print(f"📹 Output: {result.video_path}")
        print(f"⏱️  Duration: {result.duration:.1f}s")
        print(f"🎯 Quality: F1-Grade Production")
        print("\n🎬 Play: mpv {0}".format(result.video_path))
        
        # Auto-upload if requested
        if args.auto_upload:
            print("\n📤 Auto-uploading to YouTube...")
            return self._upload_video(result.video_path, args.topic)
        
        return 0
    
    def _cmd_publish(self, args) -> int:
        """Publish video to YouTube."""
        print("📺 YOUTUBE PUBLISHER")
        print("=" * 70)
        
        video_path = Path(args.video_path)
        
        if not video_path.exists():
            print(f"❌ Video not found: {video_path}")
            return 1
        
        title = args.title or video_path.stem.replace("_", " ").title()
        description = args.description or f"Technical analysis: {title}"
        
        return self._upload_video(video_path, title, description)
    
    def _upload_video(
        self,
        video_path: Path,
        title: str,
        description: Optional[str] = None
    ) -> int:
        """Upload video to YouTube."""
        try:
            from .youtube_publisher import YouTubePublisher
            
            publisher = YouTubePublisher()
            
            video_id = publisher.upload_video(
                video_path=video_path,
                title=title,
                description=description or f"Technical analysis: {title}",
                tags=["Automotive", "Engineering", "Technical"]
            )
            
            print(f"\n✅ UPLOADED SUCCESSFULLY")
            print(f"🔗 https://youtube.com/watch?v={video_id}")
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Upload failed: {e}")
            return 1
    
    def _cmd_test(self, args) -> int:
        """Test pipeline components."""
        print("🧪 PIPELINE TEST")
        print("=" * 70)
        
        if args.component in ["script", "all"]:
            print("\n[1] Testing Script Engine...")
            try:
                brief = ContentBrief(
                    topic="Test Topic",
                    key_points=["Test point"],
                    target_duration=30,
                    platform=Platform.LINKEDIN,
                    audience_level=AudienceLevel.INTERMEDIATE
                )
                script = generate_script_from_brief(brief, enable_research=False)
                print(f"   ✓ Script engine: OK ({len(script.scenes)} scenes)")
            except Exception as e:
                print(f"   ❌ Script engine: FAILED - {e}")
                return 1
        
        if args.component in ["audio", "all"]:
            print("\n[2] Testing Audio Factory...")
            try:
                factory = AudioFactory()
                test_path = factory.test_voice("Test de audio en español.")
                print(f"   ✓ Audio factory: OK ({test_path})")
            except Exception as e:
                print(f"   ❌ Audio factory: FAILED - {e}")
                return 1
        
        if args.component in ["visual", "all"]:
            print("\n[3] Testing Visual Assembly...")
            print("   ⚠️  Visual test requires full scene render (skipped in quick test)")
            print("   ✓ Visual assembly: SKIPPED")
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        
        return 0


def main():
    """Entry point for CLI."""
    cli = CLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
