# macOS Setup Guide for Automotive Media Engine 🍎

This guide provides instructions to get the project running on macOS, specifically addressing common issues with Manim, FFmpeg, and Python dependencies on Apple Silicon (M1/M2/M3) and Intel Macs.

---

## Option 1: Docker (Fastest & Recommended) 🐳

Avoid all dependency headaches by running the entire stack in Linux containers.

1.  **Install Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop/).
2.  **Clone & Configure**:
    ```bash
    cp .env.example .env
    # Add your GEMINI_API_KEY
    ```
3.  **Launch**:
    ```bash
    docker-compose up --build
    ```
    *The API will be available at `http://localhost:8000`.*

---

## Option 2: Native Setup (Homebrew) 🛠️

If you prefer to run the project natively for faster rendering or local debugging.

### 1. System Dependencies
macOS requires several system-level libraries for Manim and FFmpeg.

```bash
# Install Homebrew if you don't have it
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install core dependencies
brew install ffmpeg
brew install cairo pango
brew install pkg-config
brew install python@3.12
```

### 2. Python Environment
Use Python 3.12 to ensure compatibility with all project features.

```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip setuptools wheel
```

### 3. Install Requirements
On Apple Silicon (M1/M2/M3), use `ARCHFLAGS` if you encounter architecture-related errors during installation.

```bash
# General installation
pip install -r requirements.txt

# IF YOU HAVE ERRORS on Mac M1/M2/M3:
# ARCHFLAGS="-arch arm64" pip install -r requirements.txt
```

---

## Common macOS Issues & Fixes 💡

### 1. SSL Certificate Errors
If you see errors like `[SSL: CERTIFICATE_VERIFY_FAILED]` when the LLM or Researcher tries to connect to the internet:

```bash
# Run the built-in Python certificate installer
open "/Applications/Python 3.12/Install Certificates.command"
```

### 2. Manim Rendering Issues
If Manim fails to find the libraries, you might need to add them to your path in `.zshrc` or `.bash_profile`:

```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/libffi/lib/pkgconfig"
export LDFLAGS="-L/opt/homebrew/opt/libffi/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libffi/include"
```

### 3. Missing LaTeX (Optional)
If scenes require mathematical formulas (not common for this project yet), install MacTeX:
```bash
brew install --cask mactex
```

---

## Verification
Run a quick test to ensure everything is working:
```bash
export PYTHONPATH=$PYTHONPATH:.
python scripts/test_pipeline.py
```
