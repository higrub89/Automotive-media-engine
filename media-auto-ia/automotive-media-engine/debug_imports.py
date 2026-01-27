
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())
print("Path:", sys.path)

try:
    print("Importing loguru...")
    import loguru
    print("✅ loguru")
except ImportError as e:
    print(f"❌ loguru: {e}")

try:
    print("Importing fastapi...")
    import fastapi
    print("✅ fastapi")
except ImportError as e:
    print(f"❌ fastapi: {e}")

try:
    print("Importing core.pipeline...")
    from core.pipeline import RYAPipeline
    print("✅ core.pipeline")
except ImportError as e:
    print(f"❌ core.pipeline: {e}")
except Exception as e:
    print(f"❌ core.pipeline (other error): {e}")

try:
    print("Importing api.main...")
    from api.main import app
    print("✅ api.main")
except ImportError as e:
    print(f"❌ api.main: {e}")
except Exception as e:
    print(f"❌ api.main (other error): {e}")
