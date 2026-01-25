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
config.frame_rate = 30
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


class VisualAssembly:
    """Factory to generate specific scene types."""
    
    def __init__(self, output_dir: str = "./assets/video", platform: Platform = Platform.LINKEDIN):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform
        
        # Config aspect ratio
        if platform in [Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE]:
            config.pixel_width = 1080
            config.pixel_height = 1920
        else:
            config.pixel_width = 1080
            config.pixel_height = 1080

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
        else:
            scene_cls = ConceptScene  # Fallback
            
        # Instantiate and render
        scene_instance = scene_cls(data=scene_data)
        scene_instance.render()
        
        return output_path
