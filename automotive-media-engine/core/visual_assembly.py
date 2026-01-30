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
from .models import Scene as DataScene, Platform, StyleArchetype

# --- STYLE CONFIGURATIONS ---

class StylePalette:
    """Aesthetic tokens for different content archetypes."""
    
    CONFIGS = {
        StyleArchetype.TECHNICAL: {
            "bg_color": "#0F1115",
            "accent": "#E0E0E0",
            "highlight": "#FF3333",
            "grid_color": "#2A2F3A",
            "font": "Monospace",
            "show_grid": True,
            "animation_style": "precise"
        },
        StyleArchetype.STORYTELLING: {
            "bg_color": "#121212",
            "accent": "#FFFFFF",
            "highlight": "#FFD700", # Gold for storytelling hooks
            "grid_color": "#1A1A1A",
            "font": "Sans-serif",
            "show_grid": False,
            "animation_style": "dynamic"
        },
        StyleArchetype.DOCUMENTARY: {
            "bg_color": "#F0F0F0", # Light mode documentary style
            "accent": "#333333",
            "highlight": "#007AFF", # Blue for pedagogical clarity
            "grid_color": "#D0D0D0",
            "font": "Serif",
            "show_grid": True,
            "animation_style": "pedagogical"
        },
        StyleArchetype.MINIMALIST: {
            "bg_color": "#000000",
            "accent": "#FFFFFF",
            "highlight": "#FFFFFF",
            "grid_color": "#000000",
            "font": "Monospace",
            "show_grid": False,
            "animation_style": "minimal"
        }
    }

    @classmethod
    def get(cls, archetype: StyleArchetype) -> Dict:
        return cls.CONFIGS.get(archetype, cls.CONFIGS[StyleArchetype.TECHNICAL])

# Global Config
config.verbosity = "WARNING"
config.frame_rate = 60  # Hyperluxury standard: buttery smooth 60 FPS

class RYA_Scene(Scene):
    """RYA.ai Base scene with style awareness."""
    def __init__(self, data: DataScene, style: StyleArchetype = StyleArchetype.TECHNICAL, **kwargs):
        self.data = data
        self.style_config = StylePalette.get(style)
        self.clip_duration = data.duration
        super().__init__(**kwargs)
        self.camera.background_color = self.style_config["bg_color"]

    def construct(self):
        # 1. Background (Grid if enabled)
        if self.style_config["show_grid"]:
            grid = NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-9, 9, 1],
                background_line_style={
                    "stroke_color": self.style_config["grid_color"],
                    "stroke_width": 2,
                    "stroke_opacity": 0.5
                },
                axis_config={"stroke_opacity": 0}
            )
            self.add(grid)
            
            # Subtly animate grid if technical
            if self.style_config["animation_style"] == "precise":
                grid.set_opacity(0.3)
                self.play(grid.animate.set_opacity(0.6), rate_func=there_and_back, run_time=2)
        
        # 2. Scene Logic Dispatch
        self.build_scene_content()
        
        # 3. Wait Duration
        self.wait(max(0.5, self.clip_duration - 1))

    def build_scene_content(self):
        pass


class TitleScene(RYA_Scene):
    """Big typography for Intro/Hook."""
    def build_scene_content(self):
        title = Text(
            self.data.visual_config.get("title", "TOPIC"), 
            font=self.style_config["font"], 
            font_size=60,
            color=self.style_config["accent"]
        ).to_edge(UP, buff=2.0)
        
        subtitle = Text(
            self.data.visual_config.get("subtitle", ""), 
            font=self.style_config["font"], 
            font_size=30,
            color=self.style_config["highlight"]
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)


class BulletListScene(RYA_Scene):
    """Technical specs or key points list."""
    def build_scene_content(self):
        title = Text(
            self.data.visual_config.get("title", "KEY POINTS"), 
            font=self.style_config["font"], 
            font_size=40,
            color=self.style_config["highlight"]
        ).to_edge(UP, buff=1.0)
        self.add(title)
        
        items = self.data.visual_config.get("items", [])
        bullets = VGroup()
        
        for item in items:
            row = Text(f"> {item}", font=self.style_config["font"], font_size=28, color=self.style_config["accent"])
            bullets.add(row)
            
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullets.next_to(title, DOWN, buff=1.0)
        
        self.play(Create(bullets), run_time=min(3, len(items)*0.8))


class GraphScene(RYA_Scene):
    """Data visualization."""
    def build_scene_content(self):
        # Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=4,
            axis_config={"color": self.style_config["accent"]},
        ).to_edge(DOWN, buff=1.5)
        
        # Manually create labels
        x_lbl = Text("X", font=self.style_config["font"], font_size=20, color=self.style_config["accent"]).next_to(axes.x_axis, DOWN)
        y_lbl = Text("Y", font=self.style_config["font"], font_size=20, color=self.style_config["accent"]).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=1.5)
        
        # Curve
        curve = axes.plot(
            lambda x: 2 * x - 0.1 * x**2,
            color=self.style_config["highlight"]
        )
        self.play(Create(curve), run_time=2)


class ConceptScene(RYA_Scene):
    """Abstract parametric visualizations."""
    def build_scene_content(self):
        text = Text(
            self.data.narration_text[:60] + "...", 
            font=self.style_config["font"], 
            font_size=24,
            color=self.style_config["accent"]
        ).to_edge(DOWN)
        
        # Abstract Shape
        def func(t):
            return np.array([
                np.sin(t) * (1 + np.cos(t)),
                np.cos(t) * np.sin(t),
                0
            ])
            
        curve = ParametricFunction(
            func, t_range=[0, 2*PI], fill_opacity=0, stroke_color=self.style_config["highlight"], stroke_width=4
        ).scale(2.5)
        
        self.play(Create(curve), run_time=3)
        self.play(Write(text), run_time=1)


class CodeScene(RYA_Scene):
    """
    Renders code snippets with syntax highlighting.
    """
    def build_scene_content(self):
        code_source = self.data.visual_config.get("code", 
            "#include <stdio.h>\n\n// RYA.ai Engine\nvoid main() {\n    printf(\"Initializing...\");\n}"
        )
        language = self.data.visual_config.get("language", "c")
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix=f".{language}", delete=False) as tmp:
            tmp.write(code_source)
            tmp_path = tmp.name
            
        try:
            code_obj = Code(tmp_path, language=language)
        finally:
            pass
        
        code_obj.scale(0.8).to_edge(UP, buff=1.5)
        
        glow = SurroundingRectangle(
            code_obj, 
            color=self.style_config["highlight"], 
            buff=0.1,
            stroke_width=2,
            stroke_opacity=0.8
        )
        
        filename = Text(
            self.data.visual_config.get("filename", "rya_module.c"),
            font=self.style_config["font"], 
            font_size=20, 
            color=self.style_config["accent"]
        ).next_to(glow, UP, aligned_edge=LEFT)

        self.play(Write(filename), run_time=0.5)
        self.play(Create(glow), FadeIn(code_obj, shift=DOWN), run_time=1.5)


class ImageTechnicalScene(RYA_Scene):
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
                color=self.style_config["highlight"], 
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
                color=self.style_config["grid_color"], 
                fill_opacity=0.2,
                stroke_width=2
            )
            warning_text = Text(
                "IMAGE NOT AVAILABLE", 
                font="Monospace", 
                font_size=28, 
                color=self.style_config["accent"]
            )
            visual_group = VGroup(placeholder, warning_text).arrange(ORIGIN).to_edge(UP, buff=1.8)
            self.play(FadeIn(visual_group), run_time=1.0)

        # 2. Caption overlay (always shown)
        caption = Text(
            self.data.visual_config.get("caption", "TECHNICAL ANALYSIS"),
            font="Monospace", 
            font_size=30, 
            color=self.style_config["accent"],
            weight=BOLD
        ).next_to(visual_group, DOWN, buff=0.6)
        
        # Technical data bar (simulated metadata)
        metadata = Text(
            f"SCENE {self.data.scene_number} | DURATION {self.clip_duration:.1f}s",
            font="Monospace",
            font_size=18,
            color=self.style_config["grid_color"]
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(caption), FadeIn(metadata), run_time=1.2)



class VisualAssembly:
    """Factory to generate specific scene types."""
    
    def __init__(self, output_dir: str = "./assets/video", platform: Platform = Platform.LINKEDIN):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.platform = platform
        
        # ✨ NUEVO: Motores de adquisición visual
        from .ai_visual_engine import AIVisualEngine
        from .broll_manager import BRollManager
        
        self.ai_engine = AIVisualEngine()
        self.broll_manager = BRollManager()
        
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

    def _generate_ai_scene_video(self, scene_data: DataScene, output_path: Path, style: StyleArchetype) -> Optional[Path]:
        """
        Genera video estático con AI (Blueprint/Cinematic) + zoom/pan usando FFmpeg.
        """
        # 1. Generar imagen usando el motor universal
        topic = scene_data.visual_config.get("prompt", scene_data.narration_text[:60]) # Use explicit prompt or fallback to narration
        
        # Determine tier (optional override in visual_config)
        tier = scene_data.visual_config.get("tier", "auto")
        
        print(f"🎨 Visual Engine Request: '{topic}' [{style.value}] (Tier: {tier})")
        image_path = self.ai_engine.generate_image(topic, style, tier)
        
        if not image_path:
            return None
        
        # 2. Convertir imagen estática a video con zoom (Ken Burns effect)
        import subprocess
        duration = scene_data.duration
        
        # Determine aspect ratio based on platform configuration
        if config.pixel_width == 1920:
            scale_filter = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1"
            zoom_filter = f"zoompan=z='min(zoom+0.0015,1.5)':d={int(duration*30)}:s=1920x1080"
        else:
            scale_filter = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1"
            zoom_filter = f"zoompan=z='min(zoom+0.0015,1.5)':d={int(duration*30)}:s=1080x1920"
            
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf", f"{scale_filter},{zoom_filter}",
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            return output_path if output_path.exists() else None
        except Exception as e:
            print(f"⚠️  FFmpeg AI render failed: {e}")
            return None

    def _generate_broll_video(self, scene_data: DataScene, output_path: Path) -> Optional[Path]:
        """
        Descarga y recorta B-Roll de Pexels.
        """
        query = scene_data.visual_config.get("broll_query", "modern technology")
        orientation = "landscape" if self.platform in [Platform.LINKEDIN] else "portrait"
        
        # 1. Descargar B-Roll
        broll_path = self.broll_manager.get_cinematic_clip(query, orientation)
        
        if not broll_path:
            return None
        
        # 2. Recortar a la duración exacta
        import subprocess
        duration = scene_data.duration
        
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(broll_path),
            "-t", str(duration),
            "-c:v", "libx264",
            "-crf", "23",
            str(output_path)
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            return output_path if output_path.exists() else None
        except Exception as e:
            print(f"⚠️  FFmpeg B-Roll render failed: {e}")
            return None

    def generate_scene_visual(
        self, 
        scene_data: DataScene, 
        style: StyleArchetype = StyleArchetype.TECHNICAL,
        output_filename: Optional[str] = None
    ) -> Path:
        if not output_filename:
            output_filename = f"scene_{scene_data.scene_number}.mp4"
            
        output_path = (self.output_dir / output_filename).resolve()
        config.output_file = str(output_path)
        
        # 1. B-Roll if requested
        if scene_data.visual_config.get("broll_query"):
            print(f"🎬 Generating B-Roll for {style.value}: {scene_data.visual_config['broll_query']}")
            result = self._generate_broll_video(scene_data, output_path)
            if result:
                return result
        
        
        # 2. AI Visuals (Universal Engine)
        # If it's TECHNICAL => Blueprint style
        # If it's STORYTELLING/DOC => Cinematic style (via visual_config 'prompt' key from script engine)
        if scene_data.visual_config.get("technical_component") or scene_data.visual_config.get("prompt"):
             result = self._generate_ai_scene_video(scene_data, output_path, style)
             if result:
                 return result
        
        # 3. Manim Generation
        vtype = scene_data.visual_type.lower()
        scene_map = {
            "title": TitleScene,
            "list": BulletListScene,
            "graph": GraphScene,
            "image": ImageTechnicalScene,
            "code": CodeScene,
            "concept": ConceptScene
        }
        
        scene_cls = scene_map.get(vtype, ConceptScene)
        
        # Instantiate with style data
        scene_instance = scene_cls(data=scene_data, style=style)
        scene_instance.render()
        
        return output_path
