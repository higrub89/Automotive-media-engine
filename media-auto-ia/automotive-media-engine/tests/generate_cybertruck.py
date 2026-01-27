#!/usr/bin/env python3
"""
Generate Cybertruck video with Real Footage (B-Roll).
Focus: Visual aesthetics, no charts/graphs.
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import ContentBrief, VideoConfig, Platform, AudienceLevel, QualityPreset
from core.script_engine import ScriptEngine, LLMProvider
from core.audio_factory import AudioFactory
from core.visual_assembly import VisualAssembly
from core.video_assembler import VideoAssembler

load_dotenv()

def create_cybertruck_brief() -> ContentBrief:
    """
    Create brief focused on Visuals/Cinematics.
    Uses 'broll_query' to force B-Roll Usage.
    """
    return ContentBrief(
        topic="Tesla Cybertruck Design Analysis",
        key_points=[
            "Exoskeleton stainless steel design",
            "Future-forward cyberpunk aesthetic",
            "Off-road commanding presence"
        ],
        target_duration=45,
        platform=Platform.LINKEDIN,
        audience_level=AudienceLevel.INTERMEDIATE,
        # TRICK: Using 'broll_query' in visual_references hints forces the engine to use B-Roll
        # But we will inject specific logic in the script generation to use broll_query
        visual_references=[
            "Tesla Cybertruck driving",
            "Cybertruck stainless steel",
            "futuristic car design"
        ],
        call_to_action="Is this the future of trucks?"
    )

def main():
    print("=" * 70)
    print("📐 GENERATING CYBERTRUCK VIDEO (CINEMATIC MODE)")
    print("=" * 70)
    
    try:
        # Step 1: Brief
        brief = create_cybertruck_brief()
        
        # Step 2: Script (Manual Override to ensure B-Roll)
        print("🤖 Paso 2: Generando guion...")
        engine = ScriptEngine(provider=LLMProvider.GEMINI)
        script = engine.generate_script(brief)
        
        # 🔧 FORCE B-ROLL INJECTION
        # We manually update scene configs to ensure they use B-Roll visual_type
        print("🔧 Forzando modo 'Cinematográfico' (B-Roll Real)...")
        broll_queries = [
            "tesla cybertruck",
            "futuristic car",
            "stainless steel texture",
            "electric truck driving",
            "cyberpunk city"
        ]
        
        for i, scene in enumerate(script.scenes):
            # Assign a cinematic query to each scene
            query = broll_queries[i % len(broll_queries)]
            
            # Configure scene to use B-Roll
            scene.visual_config["broll_query"] = query
            scene.visual_type = "cinematic" # Logical type, though Dispatch checks config first
            
            print(f"   Scene {i+1}: B-Roll Query -> '{query}'")
            
        
        # Step 3: Audio
        print("\n🎙️  Paso 3: Generando narración...")
        audio_factory = AudioFactory()
        audio_path = audio_factory.generate_audio(script, output_filename="cybertruck_narration.mp3")
        
        # Step 4: Visuals (Will use Pexels now)
        print("\n🎨 Paso 4: Adquiriendo B-Roll (Pexels)...")
        visual_assembly = VisualAssembly(platform=brief.platform)
        visual_paths = []
        
        for i, scene in enumerate(script.scenes, 1):
            print(f"   Escena {i}/{len(script.scenes)}...", end="", flush=True)
            path = visual_assembly.generate_scene_visual(scene)
            
            # Fallback if B-Roll fails (use ConceptScene)
            if not path or not path.exists():
                print(" ⚠️ B-Roll missing, trying fallback...", end="")
                scene.visual_config.pop("broll_query", None) # Remove query to trigger fallback
                path = visual_assembly.generate_scene_visual(scene)
                
            visual_paths.append(path)
            print(f" ✓ {path.name}")

        # Step 5: Assemble
        print("\n🎬 Paso 5: Ensamblando video...")
        assembler = VideoAssembler()
        config = VideoConfig(project_name="cybertruck_cinematic", script=script, quality=QualityPreset.STANDARD)
        
        result = assembler.assemble_video(config, audio_path, visual_paths, output_filename="cybertruck_cinematic.mp4")
        
        if result.success:
            print(f"\n✅ VIDEO GENERADO: {result.video_path}")
            print(f"   Duración: {result.duration}s")
        else:
            print(f"\n❌ Error: {result.error_message}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
