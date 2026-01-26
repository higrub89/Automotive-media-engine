#!/usr/bin/env python3
"""
Generate C Programming Video (Cyberpunk/Hacker Style).
Focus: Code Syntax Highlighting & Technical Depth.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.models import ContentBrief, VideoConfig, Platform, AudienceLevel, QualityPreset
from core.script_engine import ScriptEngine, LLMProvider
from core.audio_factory import AudioFactory
from core.visual_assembly import VisualAssembly
from core.video_assembler import VideoAssembler

load_dotenv()

def create_c_code_brief() -> ContentBrief:
    return ContentBrief(
        topic="Punteros y Memoria en C",
        key_points=[
            "Acceso directo a memoria física",
            "Punteros: Potencia y peligro",
            "Gestión manual con malloc/free"
        ],
        target_duration=45,
        platform=Platform.LINKEDIN,
        audience_level=AudienceLevel.ADVANCED,
        visual_references=["Code terminal", "Memory addresses"],
        call_to_action="¿Controlas tú la memoria o ella a ti?"
    )

def main():
    print("=" * 70)
    print("💻 GENERATING C CODE VIDEO (HACKER MODE)")
    print("=" * 70)
    
    try:
        # Step 1: Brief
        brief = create_c_code_brief()
        
        # Step 2: Script
        print("🤖 Paso 2: Generando guion técnico...")
        engine = ScriptEngine(provider=LLMProvider.GEMINI)
        script = engine.generate_script(brief)
        
        # 🔧 FORCE CODE SCENES
        print("🔧 Inyectando código C real en las escenas...")
        
        code_snippets = [
            # Scene 1: Basics
            {
                "code": "#include <stdio.h>\n\nint main() {\n    int x = 42;\n    int *ptr = &x;\n    printf(\"Addr: %p\", ptr);\n}",
                "filename": "memory_addr.c"
            },
            # Scene 2: Power
            {
                "code": "void kernel_panic() {\n    // Direct hardware access\n    char *video_mem = 0xB8000;\n    *video_mem = 'X';\n}",
                "filename": "kernel.c"
            },
            # Scene 3: Allocation
            {
                "code": "struct Matrix* create_matrix(int n) {\n    // Manual allocation\n    void* mem = malloc(n * n * 4);\n    if (!mem) return NULL;\n    return (struct Matrix*)mem;\n}",
                "filename": "allocator.c"
            },
             # Scene 4: Danger
            {
                "code": "while(1) {\n    fork(); // Fork bomb\n    malloc(1024*1024);\n    // Visualizing memory leak\n}",
                "filename": "danger.c"
            }
        ]
        
        for i, scene in enumerate(script.scenes):
            if i < len(code_snippets):
                # Force visual type to code
                scene.visual_type = "code"
                scene.visual_config.update(code_snippets[i])
                scene.visual_config["language"] = "c"
                print(f"   Scene {i+1}: Code -> {code_snippets[i]['filename']}")
        
        # Step 3: Audio
        print("\n🎙️  Paso 3: Generando narración técnica (Edge-TTS)...")
        audio_factory = AudioFactory(use_elevenlabs=False)
        audio_path = audio_factory.generate_audio(script, output_filename="c_code_narration.mp3")
        
        # Step 4: Visuals
        print("\n🎨 Paso 4: Renderizando Código (Manim CodeScene)...")
        visual_assembly = VisualAssembly(platform=brief.platform)
        visual_paths = []
        
        for i, scene in enumerate(script.scenes, 1):
            print(f"   Escena {i}/{len(script.scenes)}...", end="", flush=True)
            path = visual_assembly.generate_scene_visual(scene)
            visual_paths.append(path)
            print(f" ✓ {path.name}")

        # Step 5: Assemble
        print("\n🎬 Paso 5: Ensamblando video...")
        assembler = VideoAssembler()
        config = VideoConfig(project_name="c_code_demo", script=script, quality=QualityPreset.STANDARD)
        
        result = assembler.assemble_video(config, audio_path, visual_paths, output_filename="c_pointers_demo.mp4")
        
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
