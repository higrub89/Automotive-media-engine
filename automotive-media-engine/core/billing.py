from pydantic import BaseModel
from typing import Optional

class UsageMetrics(BaseModel):
    """Raw usage counts."""
    llm_input_tokens: int = 0
    llm_output_tokens: int = 0
    llm_model: str = "gemini-2.0-flash"
    
    tts_characters: int = 0
    tts_provider: str = "elevenlabs"
    
    image_count_pollinations: int = 0
    image_count_replicate: int = 0
    image_count_dalle: int = 0
    
    def add(self, other: "UsageMetrics"):
        self.llm_input_tokens += other.llm_input_tokens
        self.llm_output_tokens += other.llm_output_tokens
        self.tts_characters += other.tts_characters
        self.image_count_pollinations += other.image_count_pollinations
        self.image_count_replicate += other.image_count_replicate
        self.image_count_dalle += other.image_count_dalle

class CostEstimator:
    """Calculates estimated costs based on usage."""
    
    # Pricing constants (USD)
    PRICING = {
        "gemini-2.0-flash": {"input": 0.10 / 1_000_000, "output": 0.40 / 1_000_000}, # Example pricing
        "gemini-1.5-flash": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
        "claude-3-7-sonnet-20250219": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
        
        "elevenlabs": 0.30 / 1_000, # Approx $0.30 per 1k chars
        "edge_tts": 0.0,
        
        "pollinations": 0.0,
        "replicate_flux": 0.003,
        "dalle_3": 0.040
    }
    
    @staticmethod
    def calculate_cost(metrics: UsageMetrics) -> dict:
        total_usd = 0.0
        details = {}
        
        # 1. LLM Cost
        llm_p = CostEstimator.PRICING.get(metrics.llm_model, {"input": 0, "output": 0})
        llm_cost = (metrics.llm_input_tokens * llm_p["input"]) + \
                   (metrics.llm_output_tokens * llm_p["output"])
        total_usd += llm_cost
        details["llm_cost"] = round(llm_cost, 6)
        
        # 2. TTS Cost
        tts_p = CostEstimator.PRICING.get(metrics.tts_provider, 0.0)
        tts_cost = metrics.tts_characters * tts_p
        total_usd += tts_cost
        details["tts_cost"] = round(tts_cost, 4)
        
        # 3. Image Cost
        img_cost = 0.0
        img_cost += metrics.image_count_pollinations * CostEstimator.PRICING["pollinations"]
        img_cost += metrics.image_count_replicate * CostEstimator.PRICING["replicate_flux"]
        img_cost += metrics.image_count_dalle * CostEstimator.PRICING["dalle_3"]
        total_usd += img_cost
        details["image_cost"] = round(img_cost, 4)
        
        details["total_usd"] = round(total_usd, 4)
        return details
