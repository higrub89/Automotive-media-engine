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
    
    def generate_script(self, brief: ContentBrief) -> VideoScript:
        """
        Generate a complete video script from a content brief.
        
        Args:
            brief: ContentBrief object with topic and requirements
            
        Returns:
            VideoScript with structured scenes and timing
        """
        # Build the prompt based on audience level and platform
        system_prompt = self._build_system_prompt(brief)
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
        
        # Parse response into structured script
        scenes = self._parse_script_into_scenes(script_text, brief)
        
        # Calculate total duration based on word count and natural pacing
        total_duration = self._calculate_duration(script_text, brief.target_duration)
        
        return VideoScript(
            brief=brief,
            scenes=scenes,
            total_duration=total_duration,
            script_text=script_text
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

Format your output as natural narration text, with clear paragraph breaks for scene changes.
Each paragraph should represent one complete thought/scene (roughly 8-15 seconds of speaking)."""
    
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
        
        return f"""Create a {brief.target_duration}-second video script about: {brief.topic}

Key technical points to cover:
{key_points_text}{visual_text}{cta_text}

Platform: {brief.platform.value.upper()}
Target audience: {brief.audience_level.value}

Requirements:
1. Start with a strong hook (first 3 seconds must grab attention)
2. Cover all key points with technical accuracy
3. Use concrete examples (specific models, systems, numbers)
4. End with a clear takeaway or question that encourages engagement
5. Keep pacing natural for voice narration (~150 words per minute)
6. Break into clear scene segments (paragraphs)

Write the narration now:"""
    
    def _parse_script_into_scenes(self, script_text: str, brief: ContentBrief) -> list[Scene]:
        """
        Parse script text into timed scenes.
        
        Each paragraph becomes a scene with calculated timing.
        """
        paragraphs = [p.strip() for p in script_text.split('\n\n') if p.strip()]
        
        # Calculate words per second for pacing (150 WPM = 2.5 WPS)
        words_per_second = 2.5
        
        scenes = []
        current_time = 0.0
        
        for i, paragraph in enumerate(paragraphs, 1):
            word_count = len(paragraph.split())
            duration = word_count / words_per_second
            
            # Determine visual type based on scene position
            if i == 1:
                visual_type = "text"  # Opening hook with bold text
                visual_config = {"style": "title_card", "text": brief.topic}
            elif i == len(paragraphs):
                visual_type = "text"  # Closing CTA
                visual_config = {"style": "call_to_action", "text": brief.call_to_action or "Follow for more"}
            else:
                visual_type = "diagram"  # Technical diagram for body content
                visual_config = {"style": "technical", "theme": "dark"}
            
            scene = Scene(
                scene_number=i,
                narration_text=paragraph,
                start_time=current_time,
                duration=duration,
                visual_type=visual_type,
                visual_config=visual_config
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
def generate_script_from_brief(brief: ContentBrief) -> VideoScript:
    """
    Quick helper to generate script without instantiating engine.
    
    Args:
        brief: ContentBrief object
        
    Returns:
        Validated VideoScript
    """
    engine = ScriptEngine()
    script = engine.generate_script(brief)
    
    is_valid, error = engine.validate_script(script)
    if not is_valid:
        raise ValueError(f"Generated script failed validation: {error}")
    
    return script
