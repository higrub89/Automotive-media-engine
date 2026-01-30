"""
AI Blueprint Generator: Motor de generación de planos técnicos.
Soporta múltiples backends:
  - Hugging Face Inference API (GRATIS, default)
  - Replicate (de pago, mejor calidad)
"""
import os
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging
import time

load_dotenv()
logger = logging.getLogger(__name__)


class AIBlueprintGenerator:
    """Genera blueprints técnicos estilo ingeniería automotriz usando IA"""
    
    # Hugging Face models (gratuitos) - Actualizados a versiones activas
    HF_MODELS = [
        "black-forest-labs/FLUX.1-schnell",  # Mismo que Replicate, gratis en HF
        "stabilityai/stable-diffusion-3-medium-diffusers",
        "stabilityai/sdxl-turbo",  # Rápido
    ]
    
    def __init__(self, backend: str = "auto"):
        """
        Args:
            backend: 'huggingface', 'replicate', or 'auto' (tries HF first)
        """
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        self.hf_token = os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACE_API_TOKEN")
        self.output_dir = Path("./assets/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine backend
        if backend == "auto":
            # Prefer Hugging Face (free), fallback to Replicate
            if self.hf_token:
                self.backend = "huggingface"
            elif self.replicate_token:
                self.backend = "replicate"
            else:
                self.backend = "huggingface"  # HF works without token too (slower)
        else:
            self.backend = backend
            
        logger.info(f"🎨 AI Generator initialized: backend={self.backend}")
            
    def generate_blueprint(self, topic: str) -> Optional[Path]:
        """
        Genera un blueprint técnico azul/blanco para el tema dado.
        
        Args:
            topic: Tema del blueprint (e.g., "V6 engine", "ABS brake system")
        
        Returns:
            Path al archivo generado, o None si falla
        """
        # Sanitize filename
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:50]
        save_path = self.output_dir / f"ai_{safe_topic}.png"
        
        # Sistema de Caché Básico (Ahorro de Costes)
        if save_path.exists():
            logger.info(f"♻️  Cache Hit: Usando imagen existente para '{topic}'")
            return save_path

        logger.info(f"🎨 Generating AI Blueprint: '{topic}' (backend: {self.backend})...")
        
        # Prompt optimizado para blueprints técnicos
        prompt = (
            f"technical architectural blueprint of {topic}, "
            "automotive engineering style, white lines on dark blue grid paper background, "
            "schematic, exploded view, highly detailed, 8k resolution, vector style, "
            "cad drawing, industrial design, text labels, professional, white on blue"
        )
        
        # Try Pollinations first (100% free, no auth)
        result = self._generate_with_pollinations(prompt, save_path)
        if result:
            return result
        
        # Fallback to original backends
        if self.backend == "huggingface":
            return self._generate_with_huggingface(prompt, save_path, topic)
        elif self.backend == "replicate":
            return self._generate_with_replicate(prompt, save_path)
        else:
            logger.error(f"❌ Unknown backend: {self.backend}")
            return None
    
    def _generate_with_pollinations(self, prompt: str, save_path: Path) -> Optional[Path]:
        """Genera imagen usando Pollinations.AI (100% GRATIS, sin API key)"""
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    logger.info(f"   🔄 Retry {attempt}/{max_retries-1}...")
                else:
                    logger.info(f"   🌸 Using Pollinations.AI (free, no limits)...")
                
                # Pollinations usa URLs directas para generar imágenes
                # Encode prompt para URL
                import urllib.parse
                encoded_prompt = urllib.parse.quote(prompt)
                
                # La API de Pollinations es simplemente una URL
                api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true"
                
                response = requests.get(api_url, timeout=150)  # Aumentado de 90 a 150s
                response.raise_for_status()
                
                # Guardar imagen
                with open(save_path, "wb") as f:
                    f.write(response.content)
                
                size_kb = save_path.stat().st_size / 1024
                logger.info(f"   ✨ Generated: {save_path.name} ({size_kb:.1f} KB)")
                return save_path
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    logger.warning(f"   ⏳ Timeout, retrying...")
                    continue
                else:
                    logger.warning(f"   ⚠️  Pollinations timeout after {max_retries} attempts")
                    return None
            except Exception as e:
                logger.warning(f"   ⚠️  Pollinations failed: {e}")
                return None
        
        return None
    
    def _generate_with_huggingface(self, prompt: str, save_path: Path, topic: str) -> Optional[Path]:
        """Genera imagen usando Hugging Face Inference API (GRATIS)"""
        
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
        # Try each model until one works
        for model in self.HF_MODELS:
            api_url = f"https://api-inference.huggingface.co/models/{model}"
            
            try:
                logger.info(f"   🤗 Trying HuggingFace model: {model}...")
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=120  # HF can be slow without token
                )
                
                if response.status_code == 200:
                    # Success - save image
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    
                    size_kb = save_path.stat().st_size / 1024
                    logger.info(f"   ✨ Generated: {save_path.name} ({size_kb:.1f} KB)")
                    return save_path
                    
                elif response.status_code == 503:
                    # Model loading - wait and retry
                    data = response.json()
                    wait_time = data.get("estimated_time", 30)
                    logger.info(f"   ⏳ Model loading, waiting {wait_time:.0f}s...")
                    time.sleep(min(wait_time, 60))
                    
                    # Retry
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json={"inputs": prompt},
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        size_kb = save_path.stat().st_size / 1024
                        logger.info(f"   ✨ Generated: {save_path.name} ({size_kb:.1f} KB)")
                        return save_path
                else:
                    logger.warning(f"   ⚠️  Model {model} failed: {response.status_code}")
                    continue
                    
            except requests.exceptions.Timeout:
                logger.warning(f"   ⚠️  Timeout for model {model}")
                continue
            except Exception as e:
                logger.warning(f"   ⚠️  Error with {model}: {e}")
                continue
        
        logger.error(f"❌ All HuggingFace models failed for '{topic}'")
        return None
    
    def _generate_with_replicate(self, prompt: str, save_path: Path) -> Optional[Path]:
        """Genera imagen usando Replicate (de pago)"""
        
        if not self.replicate_token:
            logger.warning("⚠️  Replicate disabled: No REPLICATE_API_TOKEN")
            return None
        
        try:
            import replicate
            client = replicate.Client(api_token=self.replicate_token)
            
            output = client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                    "output_quality": 90,
                    "disable_safety_checker": True
                }
            )
            
            image_url = output[0] if isinstance(output, list) else output
            
            logger.info(f"   📥 Downloading from Replicate...")
            response = requests.get(str(image_url))
            response.raise_for_status()
            
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            size_kb = save_path.stat().st_size / 1024
            logger.info(f"   ✨ Generated: {save_path.name} ({size_kb:.1f} KB)")
            return save_path
            
        except Exception as e:
            logger.error(f"❌ Replicate Error: {e}")
            return None
    
    def has_cached(self, topic: str) -> bool:
        """Verifica si ya existe un blueprint cacheado para el topic"""
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:50]
        save_path = self.output_dir / f"ai_{safe_topic}.png"
        return save_path.exists()


if __name__ == "__main__":
    # Test básico
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    
    generator = AIBlueprintGenerator(backend="huggingface")
    
    test_topics = [
        "ABS brake system",
    ]
    
    for topic in test_topics:
        result = generator.generate_blueprint(topic)
        if result:
            print(f"✓ Success: {result}")
        else:
            print(f"✗ Failed: {topic}")
