"""
Test de motores de adquisición visual
Valida que ai_image_generator y broll_manager funcionan correctamente
"""
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
    stream=sys.stdout
)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ai_image_generator import AIBlueprintGenerator
from core.broll_manager import BRollManager


def test_blueprint_generator():
    """Test AI blueprint generation"""
    print("\n" + "="*60)
    print("TEST 1: AI Blueprint Generator")
    print("="*60 + "\n")
    
    generator = AIBlueprintGenerator()
    
    test_topics = [
        "V6 engine",
        "ABS brake system",
        "turbocharger cutaway"
    ]
    
    results = []
    for topic in test_topics:
        print(f"\n→ Testing: {topic}")
        result = generator.generate_blueprint(topic)
        
        if result and result.exists():
            print(f"  ✓ Success: {result}")
            print(f"  Size: {result.stat().st_size / 1024:.1f} KB")
            results.append(True)
        else:
            print(f"  ✗ Failed: {topic}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n{'='*60}")
    print(f"Blueprint Generator: {sum(results)}/{len(results)} successful ({success_rate:.0f}%)")
    print(f"{'='*60}\n")
    
    return all(results)


def test_broll_manager():
    """Test B-Roll acquisition"""
    print("\n" + "="*60)
    print("TEST 2: B-Roll Manager")
    print("="*60 + "\n")
    
    manager = BRollManager()
    
    test_queries = [
        ("car engine running", "landscape"),
        ("mechanic working", "portrait"),
        ("highway driving", "landscape")
    ]
    
    results = []
    for query, orientation in test_queries:
        print(f"\n→ Testing: '{query}' ({orientation})")
        result = manager.get_cinematic_clip(query, orientation)
        
        if result and result.exists():
            print(f"  ✓ Success: {result}")
            print(f"  Size: {result.stat().st_size / 1024 / 1024:.1f} MB")
            results.append(True)
        else:
            print(f"  ✗ Failed: {query}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n{'='*60}")
    print(f"B-Roll Manager: {sum(results)}/{len(results)} successful ({success_rate:.0f}%)")
    print(f"{'='*60}\n")
    
    return all(results)


def test_cache_effectiveness():
    """Test that cache works (second call should be instant)"""
    print("\n" + "="*60)
    print("TEST 3: Cache Effectiveness")
    print("="*60 + "\n")
    
    import time
    
    generator = AIBlueprintGenerator()
    
    # First call (should generate)
    print("→ First call (should generate new):")
    start = time.time()
    result1 = generator.generate_blueprint("V8 engine")
    time1 = time.time() - start
    print(f"  Time: {time1:.2f}s")
    
    # Second call (should use cache)
    print("\n→ Second call (should use cache):")
    start = time.time()
    result2 = generator.generate_blueprint("V8 engine")
    time2 = time.time() - start
    print(f"  Time: {time2:.2f}s")
    
    cache_worked = time2 < (time1 * 0.1)  # Cache should be 10x+ faster
    
    print(f"\n{'='*60}")
    if cache_worked:
        print(f"✓ Cache working: {time1/time2:.1f}x speedup")
    else:
        print(f"✗ Cache may not be working properly")
    print(f"{'='*60}\n")
    
    return cache_worked


if __name__ == "__main__":
    print("\n" + "🚀 " + "="*56)
    print("🚀  VISUAL ACQUISITION ENGINES TEST SUITE")
    print("🚀 " + "="*56 + "\n")
    
    # Run tests
    blueprint_ok = test_blueprint_generator()
    broll_ok = test_broll_manager()
    cache_ok = test_cache_effectiveness()
    
    # Summary
    print("\n" + "📊 " + "="*56)
    print("📊  TEST SUMMARY")
    print("📊 " + "="*56)
    print(f"  Blueprint Generator: {'✓ PASS' if blueprint_ok else '✗ FAIL'}")
    print(f"  B-Roll Manager:      {'✓ PASS' if broll_ok else '✗ FAIL'}")
    print(f"  Cache System:        {'✓ PASS' if cache_ok else '✗ FAIL'}")
    print("="*60 + "\n")
    
    if blueprint_ok and broll_ok and cache_ok:
        print("🎉 ALL TESTS PASSED - Ready for integration!\n")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed - check logs above\n")
        sys.exit(1)
