"""
Script Engine: Converts ContentBrief into structured VideoScript using LLM APIs.

This is the "brain" of the system - it takes technical content and transforms it
into engaging, well-paced narration suitable for video format.

Supports multiple LLM providers with Gemini Pro as default (free via 42 Madrid).
"""

import os
from enum import Enum
from typing import Optional
from dotenv import load_dotenv

from .models import ContentBrief, VideoScript, Scene, AudienceLevel

load_dotenv()


class LLMProvider(str, Enum):
    """Supported LLM providers for script generation."""
    GEMINI = "gemini"  # Default: Free via 42 Madrid Pro
    CLAUDE = "claude"  # Fallback: Paid API


class ScriptEngine:
    """
    Generates video scripts from content briefs using LLM APIs.
    
    Optimized for technical automotive content with precise pacing and structure.
    """
    
    def __init__(
        self,
        provider: LLMProvider = LLMProvider.GEMINI,
        api_key: Optional[str] = None
    ):
        """
        Initialize the script engine.
        
        Args:
            provider: LLM provider to use (default: Gemini for cost optimization)
            api_key: API key for chosen provider (defaults to env var)
        """
        self.provider = provider
        
        if provider == LLMProvider.GEMINI:
            import google.generativeai as genai
            
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in environment or provided")
            
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.model_name = "gemini-2.0-flash-exp"
            
        elif provider == LLMProvider.CLAUDE:
            from anthropic import Anthropic
            
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")
            
            self.client = Anthropic(api_key=self.api_key)
            self.model_name = "claude-3-7-sonnet-20250219"
    
    def generate_script(
        self,
        brief: ContentBrief,
        enable_research: bool = True
    ) -> VideoScript:
        """
        Generate a complete video script from a content brief.
        
        Args:
            brief: ContentBrief object with topic and requirements
            enable_research: Whether to use DuckDuckGo for context enrichment
            
        Returns:
            VideoScript with structured scenes and timing
        """
        # Build base prompt
        system_prompt = self._build_system_prompt(brief)
        
        # Inject research data if enabled
        if enable_research:
            try:
                from .researcher import ResearchEngine
                print(f"🕵️  Enriching script context for: {brief.topic}...")
                researcher = ResearchEngine()
                research_context = researcher.get_enriched_prompt_context(brief.topic)
                system_prompt += f"\n\n{research_context}"
                print("   ✓ Research context injected")
            except ImportError:
                print("⚠️  ResearchEngine not available (missing dependencies). Skipping.")
            except Exception as e:
                print(f"⚠️  Research failed: {e}. Proceeding with base knowledge.")

        user_prompt = self._build_user_prompt(brief)
        
        # Call appropriate LLM API
        if self.provider == LLMProvider.GEMINI:
            response = self.client.generate_content(
                f"{system_prompt}\n\n{user_prompt}",
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2000,
                }
            )
            script_text = response.text
            
        elif self.provider == LLMProvider.CLAUDE:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            script_text = response.content[0].text
        
        # Parse response into structured scenes
        scenes = self._parse_script_into_scenes(script_text, brief)
        
        # CRITICAL FIX: Build clean script_text from narration only
        # Do NOT use raw script_text which includes [VISUAL: ...] tags
        clean_script_text = " ".join([scene.narration_text for scene in scenes])
        
        # Calculate total duration based on word count and natural pacing
        total_duration = self._calculate_duration(clean_script_text, brief.target_duration)
        
        return VideoScript(
            brief=brief,
            scenes=scenes,
            total_duration=total_duration,
            script_text=clean_script_text  # Clean text without visual tags
        )
    
    def _build_system_prompt(self, brief: ContentBrief) -> str:
        """Build system prompt based on content requirements."""
        
        tone_map = {
            AudienceLevel.BEGINNER: "approachable and educational, avoiding jargon",
            AudienceLevel.INTERMEDIATE: "professional and technical, assuming some background",
            AudienceLevel.ADVANCED: "highly technical and precise, using industry terminology"
        }
        
        tone = tone_map[brief.audience_level]
        
        return f"""You are an expert technical content writer specializing in automotive engineering.

Your writing style:
- Tone: {tone}
- Precision: Every technical claim must be accurate and verifiable
- Structure: Clear, logical flow with strong hooks
- Pacing: Optimized for {brief.target_duration}-second video narration
- Aesthetic: Minimalist, focusing on substance over hype

Your goal is to create narration that feels like a senior engineer mentoring a colleague,
not a typical social media influencer. Think Ferrari technical briefing, not clickbait.

Format output as blocks. Each block MUST start with a VISUAL tag, followed by the Spanish narration.

Visual Types supported:
1. `[VISUAL: title | title: "Text" | subtitle: "Text"]` -> For intro/hooks.
2. `[VISUAL: list | title: "Header" | items: ["Item1", "Item2"]]` -> For features/specs.
3. `[VISUAL: graph | x_label: "Label" | y_label: "Label"]` -> For performance data.
4. `[VISUAL: image | image_path: "filename.jpg" | caption: "Text"]` -> For real technical photos.
5. `[VISUAL: concept]` -> For abstract narration.

PROSODY CONTROL (Authority Voice):
Use these tags to control speech pacing for dramatic effect:
- `[PAUSE]` - Creates an 800ms dramatic silence (use sparingly for emphasis)
- `[SHORT_PAUSE]` - Creates a 400ms natural break (use like commas for rhythm)

**CRITICAL NUMBERS RULE:**
When stating performance figures (horsepower, torque, 0-100 times, top speed), ALWAYS add a SHORT_PAUSE before the number to give it weight and respect.

Examples with prosody:
- "El V12 atmosférico es eterno [PAUSE] pero complejo. Cada cilindro es una orquesta."
- "Este motor genera [SHORT_PAUSE] 830 caballos. [SHORT_PAUSE] No es potencia, [PAUSE] es violencia controlada."
- "De 0 a 100 en [SHORT_PAUSE] 2.9 segundos. [SHORT_PAUSE] Más rápido que parpadear."

STRATEGIC MONETIZATION LAYER:
Identify ONE (1) professional tool, software, or technical component relevant to the topic.
Mention it naturally as "industry standard" or "essential equipment" WITHOUT sounding promotional.

Example:
"Para diagnosticar esto en tiempo real, necesitas telemetría CAN-FD de grado profesional, no un escáner genérico."

DO NOT use specific brand names unless they are generic industry terms (e.g., "OBDII" is fine, "Bosch XYZ" is not).
Focus on the TYPE of tool a professional would need.

Example Output Format:

[VISUAL: title | title: "Aeroactiva" | subtitle: "Porsche 911 GT3 RS"]
La aerodinámica activa del GT3 RS redefine lo posible en un coche de calle. [SHORT_PAUSE]

[VISUAL: graph | x_label: "Velocidad" | y_label: "Downforce"]
A 285 kilómetros por hora, este alerón genera 860 kilos de carga. [PAUSE] Es el doble que su predecesor.

CRITICAL: The entire script and narration MUST be written in SPANISH (Español de España)."""

    def _build_user_prompt(self, brief: ContentBrief) -> str:
        """Build user prompt with specific content requirements."""
        
        key_points_text = "\n".join(f"- {point}" for point in brief.key_points)
        
        visual_text = ""
        if brief.visual_references:
            visual_text = "\n\nVisual references to incorporate:\n" + "\n".join(
                f"- {ref}" for ref in brief.visual_references
            )
        
        cta_text = ""
        if brief.call_to_action:
            cta_text = f"\n\nCall to action: {brief.call_to_action}"
        
        # Calculate maximum word count (150 WPM = 2.5 words/sec)
        max_words = int(brief.target_duration * 2.5)
        
        return f"""Create a {brief.target_duration}-second video script about: {brief.topic}

Key technical points to cover:
{key_points_text}{visual_text}{cta_text}

Platform: {brief.platform.value.upper()}
Target audience: {brief.audience_level.value}

CRITICAL CONSTRAINTS:
1. Maximum {max_words} words total (150 WPM pacing for {brief.target_duration}s)
2. Start with a strong hook (first 3 seconds must grab attention)
3. Cover all key points with technical accuracy
4. Use concrete examples (specific models, systems, numbers)
5. End with a clear takeaway or question that encourages engagement
6. Break into 3-5 clear scene segments (paragraphs)

Write the narration now (STAY UNDER {max_words} WORDS):"""

    def _parse_script_into_scenes(self, script_text: str, brief: ContentBrief) -> list[Scene]:
        """
        Parse script text with [VISUAL: ...] tags into timed scenes.
        """
        import re
        import json
        
        # Regex to match [VISUAL: type | key: val | ...]
        # Matches the tag and then the following text until next tag or end
        pattern = r'\[VISUAL:\s*(\w+)(.*?)\]\s*(.*?)(?=\[VISUAL:|$)'
        matches = re.finditer(pattern, script_text, re.DOTALL)
        
        scenes = []
        current_time = 0.0
        words_per_second = 2.5  # 150 WPM
        
        for i, match in enumerate(matches, 1):
            vtype = match.group(1).lower() # title, list, etc
            raw_params = match.group(2)    # | key: val ...
            narration = match.group(3).strip()
            
            # Parse params (quick and dirty key: val parser)
            config = {}
            if raw_params:
                # Split by | and parse key: val
                parts = raw_params.split('|')
                for part in parts:
                    if ':' in part:
                        k, v = part.split(':', 1)
                        key = k.strip()
                        val = v.strip().strip('"').strip("'")
                        
                        # Handle list items slightly differently if needed
                        # Ideally LLM outputs valid JSON, but this pipe format is more robust for simple LLMs
                        # Special case for items: ["a", "b"]
                        if key == 'items' and val.startswith('[') and val.endswith(']'):
                            try:
                                # Safe eval for list
                                import ast
                                val = ast.literal_eval(val)
                            except:
                                val = []
                        
                        config[key] = val
            
            # Fallback for narration empty (e.g. title card with no voice)
            # But specific logic says "narration follows". 
            # If narration is empty, assign minimal duration
            
            if not narration:
                duration = 3.0
                narration = " " # Space to allow generation
            else:
                word_count = len(narration.split())
                duration = max(2.0, word_count / words_per_second)
            
            scene = Scene(
                scene_number=i,
                narration_text=narration,
                start_time=current_time,
                duration=duration,
                visual_type=vtype,
                visual_config=config
            )
            scenes.append(scene)
            current_time += duration
            
        return scenes
    
    def _calculate_duration(self, script_text: str, target_duration: int) -> float:
        """
        Calculate actual duration based on word count and natural pacing.
        
        Uses 150 WPM as base (2.5 words/second), which is optimal for
        technical narration with good comprehension.
        """
        word_count = len(script_text.split())
        calculated_duration = word_count / 2.5
        
        # If significantly off from target, we may need regeneration
        # For now, return calculated duration
        return round(calculated_duration, 1)
    
    def validate_script(self, script: VideoScript) -> tuple[bool, Optional[str]]:
        """
        Validate script meets quality standards.
        
        Returns:
            (is_valid, error_message)
        """
        # Check duration is within acceptable range of target
        duration_diff = abs(script.total_duration - script.brief.target_duration)
        max_variance = script.brief.target_duration * 0.2  # 20% tolerance
        
        if duration_diff > max_variance:
            return False, f"Duration {script.total_duration}s exceeds target {script.brief.target_duration}s by {duration_diff:.1f}s"
        
        # Check speaking pace is natural (120-180 WPM is acceptable range)
        wpm = script.words_per_minute
        if wpm < 120 or wpm > 180:
            return False, f"Speaking pace {wpm:.0f} WPM is outside natural range (120-180)"
        
        # Check minimum scene count (at least 3: intro, body, outro)
        if len(script.scenes) < 3:
            return False, f"Script has only {len(script.scenes)} scenes, minimum is 3"
        
        return True, None


# Convenience function for quick script generation
def generate_script_from_brief(brief: ContentBrief, enable_research: bool = True) -> VideoScript:
    """
    Quick helper to generate script without instantiating engine.
    
    Args:
        brief: ContentBrief object
        enable_research: Whether to use DuckDuckGo for context enrichment (default: True)
        
    Returns:
        Validated VideoScript
    """
    engine = ScriptEngine()
    script = engine.generate_script(brief, enable_research=enable_research)
    
    is_valid, error = engine.validate_script(script)
    if not is_valid:
        raise ValueError(f"Generated script failed validation: {error}")
    
    return script
