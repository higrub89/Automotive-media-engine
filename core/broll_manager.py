"""
B-Roll Manager: Adquisición de video cinematográfico HD.
Usa Pexels API para rellenar huecos narrativos con metraje real.
"""
import os
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class BRollManager:
    """Gestor de B-Roll cinematográfico usando Pexels API"""
    
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        self.output_dir = Path("./assets/video")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://api.pexels.com/videos/search"

    def get_cinematic_clip(self, query: str, orientation: str = 'landscape') -> Optional[Path]:
        """
        Descarga un clip HD vertical/horizontal según necesidad.
        
        Args:
            query: Término de búsqueda (e.g., "car engine running")
            orientation: 'landscape' para LinkedIn, 'portrait' para TikTok/Reels
        
        Returns:
            Path al archivo descargado, o None si falla
        """
        if not self.api_key:
            logger.warning("⚠️  B-Roll Disabled: No PEXELS_API_KEY in .env")
            return None
        
        # Sanitize filename
        safe_query = query.replace(" ", "_").lower()[:50]
        save_path = self.output_dir / f"broll_{safe_query}_{orientation}.mp4"
        
        # Cache check
        if save_path.exists():
            logger.info(f"♻️  Cache Hit: Usando B-Roll existente para '{query}'")
            return save_path
            
        logger.info(f"🎬 Searching Pexels B-Roll: '{query}' ({orientation})...")
        
        try:
            headers = {"Authorization": self.api_key}
            params = {
                "query": query,
                "orientation": orientation,
                "size": "medium",
                "per_page": 5
            }
            
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            
            results = response.json()
            
            if not results.get('videos'):
                logger.warning(f"   ⚠️  No videos found for '{query}'")
                return None
            
            # Filtrar por calidad HD (mínimo 1280px de ancho)
            best_video = None
            best_file = None
            
            for video in results['videos']:
                for file in video['video_files']:
                    width = file.get('width', 0)
                    quality = file.get('quality', '')
                    
                    # Buscar HD con ancho >= 1280
                    if width >= 1280 and quality == 'hd':
                        best_video = video
                        best_file = file
                        break
                
                if best_file:
                    break
            
            if not best_file:
                logger.warning(f"   ⚠️  No HD quality videos found for '{query}'")
                return None
            
            # Descargar
            logger.info(f"   📥 Downloading {best_file['width']}x{best_file['height']} HD clip...")
            video_response = requests.get(best_file['link'])
            video_response.raise_for_status()
            
            with open(save_path, "wb") as f:
                f.write(video_response.content)
            
            size_mb = save_path.stat().st_size / 1024 / 1024
            logger.info(f"   ✨ Downloaded: {save_path.name} ({size_mb:.1f} MB)")
            return save_path
            
        except Exception as e:
            logger.error(f"❌ Pexels Error: {e}", exc_info=True)
            return None
    
    def has_cached(self, query: str, orientation: str = 'landscape') -> bool:
        """Verifica si ya existe B-Roll cacheado"""
        safe_query = query.replace(" ", "_").lower()[:50]
        save_path = self.output_dir / f"broll_{safe_query}_{orientation}.mp4"
        return save_path.exists()


if __name__ == "__main__":
    # Test básico
    manager = BRollManager()
    
    test_queries = [
        ("car engine running", "landscape"),
        ("mechanic working", "portrait"),
        ("highway driving", "landscape")
    ]
    
    for query, orientation in test_queries:
        result = manager.get_cinematic_clip(query, orientation)
        if result:
            print(f"✓ Success: {result}")
        else:
            print(f"✗ Failed: {query}")
