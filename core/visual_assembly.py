"""
Visual Assembly: Generate high-end technical animations using Manim (Free).

Engineers' choice for precise, programmatic visualization.
"""

import os
from pathlib import Path
from typing import Optional, List
from manim import *
from .models import Scene, Platform

# Configure Manim for headless rendering
config.verbosity = "WARNING"
config.pixel_height = 1080
config.pixel_width = 1080  # Default square
config.frame_rate = 30


class TechnicalSceneTemplate(Scene):
    """
    Base Manim scene for technical content.
    Provides the blueprint aesthetic and grid systems.
    """
    def __init__(self, title_text: str, body_text: str, duration: float, **kwargs):
        self.title_text = title_text
        self.body_text = body_text
        self.clip_duration = duration
        super().__init__(**kwargs)

    def construct(self):
        # 1. Technical Grid Background
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.2
            }
        )
        self.add(grid)
        
        # 2. Header
        header = Text(self.title_text, font="Monospace", font_size=36)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # 3. Main Content (Abstract Technical Visualization)
        # In production, this would be specific diagrams per topic
        # For MVP, we generate a parametric curve representing efficiency/performance
        curve = ParametricFunction(
            lambda t: np.array([
                2 * np.cos(t),
                1.5 * np.sin(2*t),
                0
            ]),
            t_range=[0, 2*PI],
            color=RED
        ).scale(1.5)
        
        self.play(Create(curve), run_time=2)
        
        # 4. Text Body
        body = Text(
            self.body_text[:100] + "...", 
            font="Monospace", 
            font_size=24,
            t2c={'important': RED}
        )
        body.next_to(curve, DOWN, buff=0.5)
        self.play(FadeIn(body), run_time=1)
        
        # Hold for remainder of duration
        remaining_time = max(0.5, self.clip_duration - 4)
        self.wait(remaining_time)


class VisualAssembly:
    """
    Generates programmatic technical animations using Manim.
    """
    
    def __init__(self, output_dir: str = "./assets/video", platform: Platform = Platform.LINKEDIN):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform
        
        # Adjust aspect ratio
        if platform in [Platform.TIKTOK, Platform.REELS, Platform.SHORTS]:
            config.pixel_width = 1080
            config.pixel_height = 1920
        else:
            config.pixel_width = 1080
            config.pixel_height = 1080
            
    def generate_scene_visual(self, scene_data: 'Scene', output_filename: Optional[str] = None) -> Path:
        """
        Render a Manim scene for the specific script segment.
        """
        if not output_filename:
            output_filename = f"scene_{scene_data.scene_number}.mp4"
            
        output_path = self.output_dir / output_filename
        
        # Configure output for this specific render
        config.output_file = str(output_path)
        
        # Create and render the scene
        # Note: Manim typically runs as a script, so we instantiate the class directly
        scene_instance = TechnicalSceneTemplate(
            title_text=f"SCENE {scene_data.scene_number}", 
            body_text=scene_data.narration_text,
            duration=scene_data.duration
        )
        scene_instance.render()
        
        # Manim saves to media_dir by default, we need to locate the file
        # This is a simplification; in production, you'd manage paths more strictly
        expected_path = Path(config.media_dir) / "videos" / "1080p30" / "TechnicalSceneTemplate.mp4"
        
        if expected_path.exists():
            # Move/Rename to desired location
            os.rename(expected_path, output_path)
            return output_path
        
        # Fallback if render location varies (Manim config dependent)
        # Returning path assuming Manim config routed it correctly or we find it
        return output_path

    def generate_thumbnail(self, title: str) -> Path:
        """Generate static thumbnail using Manim's last frame."""
        return Path("thumbnail_placeholder.png")  # MVP Placeholder


def generate_visuals_for_script(script, platform: Platform = Platform.LINKEDIN) -> List[Path]:
    assembly = VisualAssembly(platform=platform)
    visual_paths = []
    
    for scene in script.scenes:
        path = assembly.generate_scene_visual(scene)
        visual_paths.append(path)
    
    return visual_paths
