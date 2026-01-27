#!/usr/bin/env python3
"""
API Test Suite - Verify all services are configured correctly.

Run this after setting up your .env file to validate:
- Gemini API connectivity
- ElevenLabs API connectivity  
- FFmpeg installation

Usage:
    python tests/test_apis.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

def test_gemini():
    """Test Gemini API connection."""
    print("\n🔍 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Test with automotive content
        response = model.generate_content(
            "In exactly 15 words, explain what makes a Ferrari V12 engine special."
        )
        
        print(f"✅ Gemini API working!")
        print(f"   Model: gemini-2.0-flash-exp")
        print(f"   Test response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False


def test_edge_tts():
    """Test Edge-TTS (Zero Cost Audio) installation."""
    print("\n🔍 Testing Edge-TTS...")
    
    try:
        import edge_tts
        print(f"✅ Edge-TTS installed!")
        
        # We can't easily test async function here without event loop, 
        # but importing verifies installation
        return True
        
    except ImportError:
        print("❌ Edge-TTS not installed. Run: pip install edge-tts")
        return False
    except Exception as e:
        print(f"❌ Edge-TTS test failed: {e}")
        return False


def test_manim():
    """Test Manim (Zero Cost Visuals) installation."""
    print("\n🔍 Testing Manim...")
    
    try:
        import manim
        
        # Check system dependencies
        import subprocess
        result = subprocess.run(["latex", "--version"], capture_output=True)
        if result.returncode != 0:
            print("⚠️  LaTeX not found (required for Manim text). Install texlive-base.")
        
        print(f"✅ Manim installed! Version: {manim.__version__}")
        return True
        
    except ImportError:
        print("❌ Manim not installed. Run: pip install manim")
        return False
    except Exception as e:
        print(f"❌ Manim test failed: {e}")
        return False
        

def test_ffmpeg():
    """Test FFmpeg installation."""
    print("\n🔍 Testing FFmpeg...")
    
    try:
        import subprocess
        
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract version
        version_line = result.stdout.split('\n')[0]
        
        print(f"✅ FFmpeg installed!")
        print(f"   {version_line}")
        return True
        
    except FileNotFoundError:
        print("❌ FFmpeg not found. Install with: sudo apt install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test failed: {e}")
        return False


def test_pipeline_imports():
    """Test that all pipeline components can be imported."""
    print("\n🔍 Testing pipeline imports...")
    
    try:
        from core.models import ContentBrief, VideoScript, VideoConfig
        from core.script_engine import ScriptEngine, LLMProvider
        from core.audio_factory import AudioFactory
        from core.visual_assembly import VisualAssembly
        from core.video_assembler import VideoAssembler
        
        print("✅ All pipeline components imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AUTOMOTIVE MEDIA ENGINE - ZERO COST STACK TEST")
    print("=" * 60)
    
    results = {
        "Gemini API (LLM)": test_gemini(),
        "Edge-TTS (Audio)": test_edge_tts(),
        "Manim (Visuals)": test_manim(),
        "FFmpeg (Assembly)": test_ffmpeg(),
        "Pipeline Imports": test_pipeline_imports(),
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Zero-Cost System Ready!")
        print("\nNext step: Run the demo video generation:")
        print("  python tests/generate_demo_video.py")
    else:
        print("⚠️  SOME TESTS FAILED - Fix errors before generating videos")
        print("   If Manim fails, ensure system dependencies are installed:")
        print("   sudo apt install libcairo2-dev libpango1.0-dev ffmpeg texlive-base")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
