"""
Visual Assembly: Generate clean technical visuals for video scenes.

Phase 1: Static diagrams and text overlays with minimalist aesthetic.
Phase 2: Will integrate AI-generated video and stock footage.
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .models import Scene, Platform


class VisualAssembly:
    """
    Generates minimalist technical visuals optimized for automotive content.
    
    Design philosophy: Clean, high-contrast, professional. 
    Think Ferrari pit wall displays, not consumer infographics.
    """
    
    def __init__(
        self,
        output_dir: str = "./assets/diagrams",
        platform: Platform = Platform.LINKEDIN
    ):
        """
        Initialize visual assembly system.
        
        Args:
            output_dir: Directory to save generated visuals
            platform: Target platform for resolution/aspect ratio
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform
        
        # Platform-specific resolutions
        self.resolutions = {
            Platform.LINKEDIN: (1080, 1080),      # Square
            Platform.TIKTOK: (1080, 1920),        # Vertical
            Platform.INSTAGRAM: (1080, 1920),     # Vertical
            Platform.YOUTUBE: (1080, 1920),       # Vertical
        }
        
        self.resolution = self.resolutions[platform]
        
        # Color palette: High-end minimalist (dark mode)
        self.colors = {
            "background": "#0A0A0A",        # Near black
            "primary": "#FFFFFF",            # Pure white
            "accent": "#FF0000",             # Ferrari red
            "secondary": "#1E1E1E",          # Dark grey
            "text_dim": "#8A8A8A",          # Medium grey
            "grid": "#2A2A2A",               # Subtle grid
        }
        
        # Typography
        self.fonts = {
            "title": 72,
            "subtitle": 48,
            "body": 36,
            "caption": 24,
        }
    
    def generate_scene_visual(
        self,
        scene: Scene,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate visual for a specific scene based on its type.
        
        Args:
            scene: Scene object with visual configuration
            output_filename: Custom output filename
            
        Returns:
            Path to generated visual
        """
        if not output_filename:
            output_filename = f"scene_{scene.scene_number:02d}.png"
        
        output_path = self.output_dir / output_filename
        
        # Route to appropriate generator based on visual type
        if scene.visual_type == "text":
            return self._generate_text_visual(scene, output_path)
        elif scene.visual_type == "diagram":
            return self._generate_technical_diagram(scene, output_path)
        elif scene.visual_type == "stock_video":
            # Placeholder for Phase 2
            return self._generate_placeholder(scene, output_path, "Stock Video")
        else:
            return self._generate_placeholder(scene, output_path, scene.visual_type)
    
    def _generate_text_visual(self, scene: Scene, output_path: Path) -> Path:
        """
        Generate clean text overlay visual (for hooks and CTAs).
        """
        width, height = self.resolution
        img = Image.new('RGB', (width, height), color=self.colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Get visual configuration
        style = scene.visual_config.get("style", "title_card")
        text = scene.visual_config.get("text", scene.narration_text[:100])
        
        # Load font (fallback to default if custom not available)
        try:
            font_size = self.fonts["title"] if style == "title_card" else self.fonts["body"]
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Add accent line (top or bottom depending on style)
        if style == "title_card":
            draw.rectangle([(0, 0), (width, 10)], fill=self.colors["accent"])
        else:
            draw.rectangle([(0, height-10), (width, height)], fill=self.colors["accent"])
        
        # Text wrapping and centering
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width * 0.85:  # 85% of width
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center text vertically
        line_height = font_size * 1.3
        total_height = line_height * len(lines)
        y_start = (height - total_height) / 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) / 2
            y = y_start + (i * line_height)
            draw.text((x, y), line, fill=self.colors["primary"], font=font)
        
        img.save(output_path, quality=95)
        return output_path
    
    def _generate_technical_diagram(self, scene: Scene, output_path: Path) -> Path:
        """
        Generate minimalist technical diagram.
        
        Phase 1: Abstract geometric representations
        Phase 2: Will use matplotlib for data visualization
        """
        width, height = self.resolution
        dpi = 100
        fig_width = width / dpi
        fig_height = height / dpi
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
        fig.patch.set_facecolor(self.colors["background"])
        ax.set_facecolor(self.colors["background"])
        
        # Remove axes
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        
        # Add subtle grid (optional, based on configuration)
        theme = scene.visual_config.get("theme", "dark")
        if theme == "dark":
            # Minimalist grid lines
            for i in range(0, 101, 20):
                ax.axhline(y=i, color=self.colors["grid"], linewidth=0.5, alpha=0.3)
                ax.axvline(x=i, color=self.colors["grid"], linewidth=0.5, alpha=0.3)
        
        # Add geometric element (placeholder for actual technical diagrams)
        # In production, this would be customized per content type
        circle = patches.Circle((50, 50), 25, 
                                linewidth=3, 
                                edgecolor=self.colors["accent"], 
                                facecolor='none')
        ax.add_patch(circle)
        
        # Add accent lines
        ax.plot([20, 80], [50, 50], color=self.colors["primary"], linewidth=2, alpha=0.6)
        ax.plot([50, 50], [20, 80], color=self.colors["primary"], linewidth=2, alpha=0.6)
        
        # Add text annotation
        text_snippet = scene.narration_text[:40] + "..." if len(scene.narration_text) > 40 else scene.narration_text
        ax.text(50, 10, text_snippet, 
                color=self.colors["text_dim"],
                fontsize=12,
                ha='center',
                va='center',
                fontfamily='monospace')
        
        plt.tight_layout(pad=0)
        plt.savefig(output_path, 
                    facecolor=self.colors["background"], 
                    dpi=dpi,
                    bbox_inches='tight',
                    pad_inches=0)
        plt.close()
        
        return output_path
    
    def _generate_placeholder(self, scene: Scene, output_path: Path, label: str) -> Path:
        """
        Generate placeholder visual for未来features.
        """
        width, height = self.resolution
        img = Image.new('RGB', (width, height), color=self.colors["secondary"])
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        text = f"[{label}]\nScene {scene.scene_number}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        
        draw.text((x, y), text, fill=self.colors["text_dim"], font=font, align="center")
        
        img.save(output_path, quality=95)
        return output_path
    
    def generate_thumbnail(
        self,
        title: str,
        output_filename: str = "thumbnail.png"
    ) -> Path:
        """
        Generate video thumbnail for platform upload.
        
        Args:
            title: Video title
            output_filename: Thumbnail filename
            
        Returns:
            Path to generated thumbnail
        """
        width, height = self.resolution
        img = Image.new('RGB', (width, height), color=self.colors["background"])
        draw = ImageDraw.Draw(img)
        
        # Add Ferrari red accent bar
        draw.rectangle([(0, 0), (width, 20)], fill=self.colors["accent"])
        draw.rectangle([(0, height-20), (width, height)], fill=self.colors["accent"])
        
        # Title text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        except:
            font = ImageFont.load_default()
        
        # Wrap title
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width * 0.9:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center text
        line_height = 80
        total_height = line_height * len(lines)
        y_start = (height - total_height) / 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) / 2
            y = y_start + (i * line_height)
            draw.text((x, y), line, fill=self.colors["primary"], font=font)
        
        output_path = self.output_dir / output_filename
        img.save(output_path, quality=95)
        return output_path


# Convenience function
def generate_visuals_for_script(script, platform: Platform = Platform.LINKEDIN) -> list[Path]:
    """
    Generate all visuals for a complete script.
    
    Args:
        script: VideoScript object
        platform: Target platform
        
    Returns:
        List of paths to generated visual files
    """
    assembly = VisualAssembly(platform=platform)
    visual_paths = []
    
    for scene in script.scenes:
        path = assembly.generate_scene_visual(scene)
        visual_paths.append(path)
    
    return visual_paths
