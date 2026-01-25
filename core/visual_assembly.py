"""
Visual Assembly: Advanced Manim Scene Generation.

Supports:
- Semantic Scene Types (Title, Text, Graph, Concept)
- Dark Mode "Technical Blueprint" Aesthetic
- Dynamic visual configuration from ScriptEngine
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from manim import *
from .models import Scene as DataScene, Platform

# Global Config
config.verbosity = "WARNING"
config.frame_rate = 60  # Hyperluxury standard: buttery smooth 60 FPS
BACKGROUND_COLOR = "#0F1115"  # Deep dark technical grey
ACCENT_COLOR = "#E0E0E0"      # Off-white for text
HIGHLIGHT_COLOR = "#FF3333"   # Ferrari Red for highlights
GRID_COLOR = "#2A2F3A"        # Subtle grid

class TechnicalScene(Scene):
    """Base class with shared aesthetic."""
    def __init__(self, data: DataScene, **kwargs):
        self.data = data
        self.clip_duration = data.duration
        super().__init__(**kwargs)
        self.camera.background_color = BACKGROUND_COLOR

    def construct(self):
        # 1. Background Grid
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-9, 9, 1],
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            },
            axis_config={"stroke_opacity": 0} # Hide axes, keept grid
        )
        self.add(grid)
        
        # 2. Scene Logic Dispatch
        self.build_scene_content()
        
        # 3. Wait Duration
        # Wait remaining time (accounting for animation time)
        # Note: In a real advanced engine, we'd track self.renderer.time
        # For MVP, we just wait full duration minus a small buffer
        self.wait(max(0.5, self.clip_duration - 1))

    def build_scene_content(self):
        """Override in subclasses."""
        pass


class TitleScene(TechnicalScene):
    """Big typography for Intro/Hook."""
    def build_scene_content(self):
        title = Text(
            self.data.visual_config.get("title", "TOPIC"), 
            font="Monospace", 
            font_size=60,
            color=ACCENT_COLOR
        ).to_edge(UP, buff=2.0)
        
        subtitle = Text(
            self.data.visual_config.get("subtitle", ""), 
            font="Monospace", 
            font_size=30,
            color=HIGHLIGHT_COLOR
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)


class BulletListScene(TechnicalScene):
    """Technical specs list."""
    def build_scene_content(self):
        title = Text(
            self.data.visual_config.get("title", "SPECS"), 
            font="Monospace", 
            font_size=40,
            color=HIGHLIGHT_COLOR
        ).to_edge(UP, buff=1.0)
        self.add(title)
        
        items = self.data.visual_config.get("items", [])
        bullets = VGroup()
        
        for item in items:
            row = Text(f"> {item}", font="Monospace", font_size=28, color=ACCENT_COLOR)
            bullets.add(row)
            
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullets.next_to(title, DOWN, buff=1.0)
        
        self.play(Create(bullets), run_time=min(3, len(items)*0.8))


class GraphScene(TechnicalScene):
    """Data visualization (Abstract or Concrete)."""
    def build_scene_content(self):
        # Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=4,
            axis_config={"color": ACCENT_COLOR},
        ).to_edge(DOWN, buff=1.5)
        
        # Manually create non-LaTeX labels
        x_lbl = Text("RPM", font="Monospace", font_size=20, color=ACCENT_COLOR).next_to(axes.x_axis, DOWN)
        y_lbl = Text("Torque", font="Monospace", font_size=20, color=ACCENT_COLOR).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=1.5)
        
        # Curve
        curve = axes.plot(
            lambda x: 2 * x - 0.1 * x**2,
            color=HIGHLIGHT_COLOR
        )
        self.play(Create(curve), run_time=2)


class ConceptScene(TechnicalScene):
    """Abstract parametric visualizations for narration filler."""
    def build_scene_content(self):
        text = Text(
            self.data.narration_text[:60] + "...", 
            font="Monospace", 
            font_size=24,
            color=ACCENT_COLOR
        ).to_edge(DOWN)
        
        # Abstract Engineering Shape
        def func(t):
            return np.array([
                np.sin(t) * (1 + np.cos(t)),
                np.cos(t) * np.sin(t),
                0
            ])
            
        curve = ParametricFunction(
            func, t_range=[0, 2*PI], fill_opacity=0, stroke_color=HIGHLIGHT_COLOR, stroke_width=4
        ).scale(2.5)
        
        self.play(Create(curve), run_time=3)
        self.play(Write(text), run_time=1)


class ImageTechnicalScene(TechnicalScene):
    """
    Displays real technical photos (engine blocks, blueprints, chassis) 
    with professional overlay and caption.
    
    Transforms generic tutorials into F1-grade technical analysis.
    Uses smart matching to find best available image when exact match not found.
    """
    
    def _find_best_image(self, requested_filename: str) -> Optional[Path]:
        """
        Smart image matching: finds best available image based on keywords.
        
        If exact file doesn't exist, searches for images containing similar keywords.
        """
        images_dir = Path("./assets/images")
        
        # First, try exact match
        exact_path = images_dir / requested_filename
        if exact_path.exists():
            return exact_path
        
        # If not found, try smart matching based on keywords
        if not images_dir.exists():
            return None
            
        available_images = list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg"))
        
        if not available_images:
            return None
        
        # Extract keywords from requested filename
        keywords = requested_filename.lower().replace("_", " ").replace("-", " ").replace(".", " ").split()
        keywords = [k for k in keywords if len(k) > 2 and k not in ["jpg", "png", "the", "and"]]
        
        # Score each available image by keyword matches
        best_match = None
        best_score = 0
        
        for img_path in available_images:
            img_name = img_path.stem.lower().replace("_", " ").replace("-", " ")
            score = sum(1 for kw in keywords if kw in img_name)
            
            # Bonus for specific technical terms
            if "engine" in img_name and "engine" in keywords:
                score += 2
            if "motor" in img_name and any(k in keywords for k in ["motor", "engine", "v6", "v8", "v12"]):
                score += 2
            if "chassis" in img_name and "chassis" in keywords:
                score += 2
            if "powertrain" in img_name and any(k in keywords for k in ["power", "hybrid", "electric"]):
                score += 2
            
            if score > best_score:
                best_score = score
                best_match = img_path
        
        # Return best match if score is reasonable, otherwise return any image
        if best_match and best_score > 0:
            return best_match
        elif available_images:
            # Fallback: return first available image rather than placeholder
            return available_images[0]
        
        return None
    
    def build_scene_content(self):
        # 1. Load image using smart matching
        image_filename = self.data.visual_config.get("image_path", "default_engine.jpg")
        image_path = self._find_best_image(image_filename)
        
        if image_path and image_path.exists():
            # Create Manim ImageMobject
            img = ImageMobject(str(image_path))
            img.height = 5  # Adjust to leave space for caption
            
            # Blueprint aesthetic: Desaturate and add technical border
            img.set_opacity(0.85)
            border = SurroundingRectangle(
                img, 
                color=HIGHLIGHT_COLOR, 
                buff=0.15, 
                stroke_width=3
            )
            
            # Group and position
            visual_group = Group(img, border).to_edge(UP, buff=1.8)
            
            self.play(FadeIn(img, scale=0.95), Create(border), run_time=1.5)
            
        else:
            # Fallback: Elegant placeholder when no images available at all
            placeholder = Rectangle(
                width=8, 
                height=4.5, 
                color=GRID_COLOR, 
                fill_opacity=0.2,
                stroke_width=2
            )
            warning_text = Text(
                "IMAGE NOT AVAILABLE", 
                font="Monospace", 
                font_size=28, 
                color=ACCENT_COLOR
            )
            visual_group = VGroup(placeholder, warning_text).arrange(ORIGIN).to_edge(UP, buff=1.8)
            self.play(FadeIn(visual_group), run_time=1.0)

        # 2. Caption overlay (always shown)
        caption = Text(
            self.data.visual_config.get("caption", "TECHNICAL ANALYSIS"),
            font="Monospace", 
            font_size=30, 
            color=ACCENT_COLOR,
            weight=BOLD
        ).next_to(visual_group, DOWN, buff=0.6)
        
        # Technical data bar (simulated metadata)
        metadata = Text(
            f"SCENE {self.data.scene_number} | DURATION {self.clip_duration:.1f}s",
            font="Monospace",
            font_size=18,
            color=GRID_COLOR
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(caption), FadeIn(metadata), run_time=1.2)



class VisualAssembly:
    """Factory to generate specific scene types."""
    
    def __init__(self, output_dir: str = "./assets/video", platform: Platform = Platform.LINKEDIN):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform
        
        # Config aspect ratio and resolution
        # HYPERLUXURY STANDARD: Full HD minimum (1920x1080 or 1080x1920)
        if platform in [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE]:
            # Vertical format for social media
            config.pixel_width = 1080
            config.pixel_height = 1920  # Full HD Vertical
        else:
            # Horizontal format for LinkedIn/professional platforms
            config.pixel_width = 1920   # Full HD Horizontal
            config.pixel_height = 1080  # Full HD Horizontal

    def generate_scene_visual(self, scene_data: DataScene, output_filename: Optional[str] = None) -> Path:
        if not output_filename:
            output_filename = f"scene_{scene_data.scene_number}.mp4"
            
        output_path = (self.output_dir / output_filename).resolve()
        config.output_file = str(output_path)
        
        # Dispatch logic based on visual_type
        vtype = scene_data.visual_type.lower()
        
        if vtype == "title":
            scene_cls = TitleScene
        elif vtype == "list":
            scene_cls = BulletListScene
        elif vtype == "graph":
            scene_cls = GraphScene
        elif vtype == "image":
            scene_cls = ImageTechnicalScene
        else:
            scene_cls = ConceptScene  # Fallback
            
        # Instantiate and render
        scene_instance = scene_cls(data=scene_data)
        scene_instance.render()
        
        return output_path
