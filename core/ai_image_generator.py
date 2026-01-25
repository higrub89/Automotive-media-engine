"""
AI Blueprint Generator: Motor de generación de planos técnicos.
Usa Replicate (Flux-Schnell) para crear arte vectorial técnico bajo demanda.
"""
import os
import requests
from pathlib import Path
from typing import Optional
import replicate
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class AIBlueprintGenerator:
    """Genera blueprints técnicos estilo ingeniería automotriz usando IA"""
    
    def __init__(self):
        self.token = os.getenv("REPLICATE_API_TOKEN")
        self.client = replicate.Client(api_token=self.token) if self.token else None
        self.output_dir = Path("./assets/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
            
    def generate_blueprint(self, topic: str) -> Optional[Path]:
        """
        Genera un blueprint técnico azul/blanco para el tema dado.
        
        Args:
            topic: Tema del blueprint (e.g., "V6 engine", "ABS brake system")
        
        Returns:
            Path al archivo generado, o None si falla
        """
        if not self.client:
            logger.warning("⚠️  AI Generator Disabled: No REPLICATE_API_TOKEN in .env")
            return None
            
        # Sanitize filename
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:50]
        save_path = self.output_dir / f"ai_{safe_topic}.png"
        
        # Sistema de Caché Básico (Ahorro de Costes)
        if save_path.exists():
            logger.info(f"♻️  Cache Hit: Usando imagen existente para '{topic}'")
            return save_path

        logger.info(f"🎨 Generating AI Blueprint: '{topic}'...")
        
        # Prompt engineering para blueprints técnicos automotrices
        prompt = (
            f"technical architectural blueprint of {topic}, "
            "automotive engineering style, white lines on dark blue grid paper background, "
            "schematic, exploded view, highly detailed, 8k resolution, vector style, "
            "cad drawing, industrial design, text labels, professional, white on blue"
        )
        
        try:
            output = self.client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                    "output_quality": 90,
                    "disable_safety_checker": True
                }
            )
            
            # Output puede ser lista o string
            image_url = output[0] if isinstance(output, list) else output
            
            # Descargar imagen
            logger.info(f"   📥 Downloading from Replicate...")
            response = requests.get(str(image_url))
            response.raise_for_status()
            
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            size_kb = save_path.stat().st_size / 1024
            logger.info(f"   ✨ Generated: {save_path.name} ({size_kb:.1f} KB)")
            return save_path
            
        except Exception as e:
            logger.error(f"❌ AI Generation Error: {e}", exc_info=True)
            return None
    
    def has_cached(self, topic: str) -> bool:
        """Verifica si ya existe un blueprint cacheado para el topic"""
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:50]
        save_path = self.output_dir / f"ai_{safe_topic}.png"
        return save_path.exists()


if __name__ == "__main__":
    # Test básico
    generator = AIBlueprintGenerator()
    
    test_topics = [
        "V6 engine",
        "ABS brake system",
        "turbocharger cutaway"
    ]
    
    for topic in test_topics:
        result = generator.generate_blueprint(topic)
        if result:
            print(f"✓ Success: {result}")
        else:
            print(f"✗ Failed: {topic}")
