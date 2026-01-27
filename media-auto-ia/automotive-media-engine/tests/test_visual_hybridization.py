"""
Test Visual Hybridization - Image Scene Integration

Validates the new ImageTechnicalScene with real technical photos.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.models import ContentBrief, Platform, AudienceLevel, Scene as DataScene
from core.visual_assembly import VisualAssembly


def main():
    print("🖼️  Visual Hybridization - Image Integration Test")
    print("=" * 60)
    
    # Create test scene with image
    test_scene = DataScene(
        scene_number=1,
        visual_type="image",
        narration_text="El motor V12 de Ferrari representa la cúspide de la ingeniería atmosférica. Cada componente es una obra de arte funcional.",
        duration=8.0,
        start_time=0.0,
        visual_config={
            "image_path": "ferrari_v12_engine.png",
            "caption": "Ferrari V12 - Anatomía de la Potencia"
        }
    )
    
    print(f"\n📋 Test Scene:")
    print(f"   Type: {test_scene.visual_type}")
    print(f"   Image: {test_scene.visual_config['image_path']}")
    print(f"   Caption: {test_scene.visual_config['caption']}")
    
    # Generate visual
    print("\n🎨 Rendering hybrid visual (Manim + Photo)...")
    
    visual_assembly = VisualAssembly(platform=Platform.LINKEDIN)
    
    try:
        output_path = visual_assembly.generate_scene_visual(
            test_scene, 
            output_filename="test_image_scene.mp4"
        )
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path}")
        print(f"\n🎯 Validation:")
        print(f"   1. Video should show Ferrari V12 engine photo")
        print(f"   2. Red technical border around image")
        print(f"   3. Caption: 'Ferrari V12 - Anatomía de la Potencia'")
        print(f"   4. Metadata bar at bottom")
        print(f"\n   View with: mpv {output_path}")
        
    except Exception as e:
        print(f"\n❌ RENDER FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Test 2: Fallback placeholder (non-existent image)
    print("\n" + "=" * 60)
    print("🔧 Testing fallback placeholder...")
    
    fallback_scene = DataScene(
        scene_number=2,
        visual_type="image",
        narration_text="Test de fallback cuando la imagen no existe.",
        duration=5.0,
        start_time=0.0,
        visual_config={
            "image_path": "nonexistent_image.jpg",
            "caption": "FALLBACK TEST"
        }
    )
    
    try:
        fallback_path = visual_assembly.generate_scene_visual(
            fallback_scene,
            output_filename="test_fallback_scene.mp4"
        )
        
        print(f"   ✓ Fallback rendered: {fallback_path}")
        print(f"   Should show: 'IMAGE NOT AVAILABLE' placeholder")
        
    except Exception as e:
        print(f"   ⚠️  Fallback test failed: {e}")
    
    return 0


if __name__ == "__main__":
    exit(main())
