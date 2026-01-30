"""
Universal AI Visual Engine
--------------------------
Handles generation of images using a cascading strategy for cost optimization:
1. Pollinations.ai (Free) - Default.
2. Replicate (Flux Schnell) (Cheap) - Fallback or high quality.
3. OpenAI (DALL-E 3) (Premium) - Complex prompts.

Also handles Style Awareness (Technical, Minimalist, Storytelling).
"""
import os
import requests
import time
import logging
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv

from core.models import StyleArchetype

load_dotenv()
logger = logging.getLogger(__name__)

class AIVisualEngine:
    """
    Tiered AI Image Generator.
    """
    
    def __init__(self, output_dir: str = "./assets/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        # Style Mappings: Add specific keywords to prompts based on archetype
        self.STYLE_PROMPTS = {
            StyleArchetype.TECHNICAL: (
                "technical architectural blueprint, automotive engineering style, "
                "white lines on dark blue grid paper background, schematic, exploded view, "
                "highly detailed, 8k resolution, vector style, cad drawing"
            ),
            StyleArchetype.STORYTELLING: (
                "cinematic shot, photorealistic, dramatic lighting, 8k, unreal engine 5 render, "
                "highly detailed texture, emotional atmosphere, depth of field"
            ),
            StyleArchetype.DOCUMENTARY: (
                "editorial photography, national geographic style, high definition, "
                "realistic lighting, sharp focus, professional journalism"
            ),
            StyleArchetype.MINIMALIST: (
                "minimalist flat vector art, clean lines, solid colors, modern ui design, "
                "abstract simplification, corporate memphis style, high contrast"
            )
        }

    def generate_image(self, topic: str, style: StyleArchetype = StyleArchetype.TECHNICAL, tier: str = "auto") -> Optional[Path]:
        """
        Main entry point for generation.
        """
        # 1. Check Cache
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).lower()[:50]
        style_suffix = style.value.lower()
        save_path = self.output_dir / f"ai_{safe_topic}_{style_suffix}.png"
        
        if save_path.exists():
            logger.info(f"♻️  Visual Cache: {save_path.name}")
            return save_path

        # 2. Prepare Prompt
        base_prompt = f"{topic}, {self.STYLE_PROMPTS.get(style, '')}"
        logger.info(f"🎨 Generating Visual ({style.value}): '{topic}'")

        # 3. Cascading Logic
        if tier == "auto":
            # Tier 1: Pollinations (Free)
            result = self._generate_pollinations(base_prompt, save_path)
            if result: return result
            
            # Tier 2: Replicate (Flux)
            if self.replicate_token:
                result = self._generate_replicate(base_prompt, save_path)
                if result: return result
            
            # Tier 3: OpenAI (DALL-E) - Only if really needed or explicitly requested
            # Keeping it as last resort due to cost.
            if self.openai_key:
                result = self._generate_dalle(base_prompt, save_path)
                if result: return result
                
        # Explicit overrides
        elif tier == "premium":
            return self._generate_dalle(base_prompt, save_path)
        
        elif tier == "flux":
            return self._generate_replicate(base_prompt, save_path)

        logger.error(f"❌ All visual engines failed for '{topic}'")
        return None

    def _generate_pollinations(self, prompt: str, save_path: Path) -> Optional[Path]:
        """Tier 1: Pollinations.ai (Free)"""
        try:
            logger.info("   🌸 Tier 1: Pollinations...")
            import urllib.parse
            encoded_prompt = urllib.parse.quote(prompt)
            # HD Resolution
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true&seed={int(time.time())}"
            
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return save_path
        except Exception as e:
            logger.warning(f"   ⚠️ Pollinations failed: {e}")
        return None

    def _generate_replicate(self, prompt: str, save_path: Path) -> Optional[Path]:
        """Tier 2: Replicate / Flux Schnell ($0.003)"""
        try:
            logger.info("   ⚡ Tier 2: Replicate (Flux)...")
            import replicate
            
            client = replicate.Client(api_token=self.replicate_token)
            output = client.run(
                "black-forest-labs/flux-schnell",
                input={"prompt": prompt, "aspect_ratio": "16:9"}
            )
            # Flux returns a list of URLs
            image_url = output[0] if isinstance(output, list) else output
            
            resp = requests.get(str(image_url))
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return save_path
        except Exception as e:
            logger.warning(f"   ⚠️ Replicate failed: {e}")
        return None

    def _generate_dalle(self, prompt: str, save_path: Path) -> Optional[Path]:
        """Tier 3: DALL-E 3 ($0.04)"""
        try:
            logger.info("   💎 Tier 3: DALL-E 3...")
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            resp = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024", # DALL-E 3 standard
                quality="standard",
                n=1,
            )
            
            image_url = resp.data[0].url
            resp = requests.get(image_url)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return save_path
        except Exception as e:
            logger.warning(f"   ⚠️ DALL-E failed: {e}")
        return None
