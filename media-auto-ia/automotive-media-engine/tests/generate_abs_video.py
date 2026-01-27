#!/usr/bin/env python3
"""
Generate ABS video from demo brief.
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


def create_abs_brief() -> ContentBrief:
    """Create ABS content brief."""
    return ContentBrief(
        topic="Cómo Funciona el Sistema ABS",
        key_points=[
            "Detecta bloqueo de ruedas en frenado de emergencia",
            "Modula presión 15 veces por segundo",
            "Mantiene control direccional del vehículo",
            "Ahora estándar en todos los vehículos modernos"
        ],
        target_duration=45,
        platform=Platform.LINKEDIN,
        audience_level=AudienceLevel.INTERMEDIATE,
        visual_references=[
            "ABS brake system",
            "car braking emergency"
        ],
        call_to_action="¿Sabías que el ABS salva vidas cada día?"
    )


def main():
    """Generate ABS demo video."""
    print("=" * 70)
    print("🚗 GENERANDO VIDEO: Sistema ABS")
    print("=" * 70)
    print(f"\nIniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Step 1: Brief
        print("📝 Paso 1: Creando brief...")
        brief = create_abs_brief()
        print(f"   Tema: {brief.topic}")
        print(f"   Duración: {brief.target_duration}s")
        print(f"   ✓ Brief listo\n")
        
        # Step 2: Script
        print("🤖 Paso 2: Generando guion con Gemini...")
        engine = ScriptEngine(provider=LLMProvider.GEMINI)
        script = engine.generate_script(brief)
        print(f"   Escenas: {len(script.scenes)}")
        print(f"   Duración total: {script.total_duration}s")
        print(f"   ✓ Guion generado\n")
        
        # Step 3: Audio
        print("🎙️  Paso 3: Generando narración...")
        audio_factory = AudioFactory()
        audio_path = audio_factory.generate_audio(
            script,
            output_filename="abs_demo_narration.mp3"
        )
        actual_duration = audio_factory.get_audio_duration(audio_path)
        print(f"   Audio: {audio_path}")
        print(f"   Duración real: {actual_duration}s")
        print(f"   ✓ Audio generado\n")
        
        # Step 4: Visuals
        print("🎨 Paso 4: Renderizando animaciones Manim...")
        visual_assembly = VisualAssembly(platform=brief.platform)
        
        visual_paths = []
        for i, scene in enumerate(script.scenes, 1):
            print(f"   Escena {i}/{len(script.scenes)}...", end="", flush=True)
            path = visual_assembly.generate_scene_visual(scene)
            visual_paths.append(path)
            print(f" ✓ {path.name}")
        
        print(f"   ✓ Animaciones completas\n")
        
        # Step 5: Assemble
        print("🎬 Paso 5: Ensamblando video final...")
        config = VideoConfig(
            project_name="abs_system_demo",
            script=script,
            quality=QualityPreset.STANDARD,
            voice_id="es-ES-AlvaroNeural"
        )
        
        assembler = VideoAssembler()
        result = assembler.assemble_video(
            config,
            audio_path,
            visual_paths,
            output_filename="abs_brake_system.mp4"
        )
        
        if result.success:
            print(f"   ✓ Video ensamblado!\n")
            print("=" * 70)
            print("✅ VIDEO GENERADO EXITOSAMENTE")
            print("=" * 70)
            print(f"\n📹 Archivo: {result.video_path}")
            print(f"   Duración: {result.duration}s")
            print(f"   Tamaño: {result.file_size_mb:.2f} MB")
            print(f"   Tiempo de generación: {result.generation_time_seconds:.1f}s")
            print(f"\n🎉 Tu video del Sistema ABS está listo!")
            
            assembler.cleanup_temp_files()
            return 0
        else:
            print(f"   ❌ Error: {result.error_message}\n")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
