"""
Research Engine: Zero-Cost Autonomous Knowledge Gathering.

Uses DuckDuckGo (Free) to fetch technical specifications, news, and context
for automotive content, eliminating the need for paid SERP APIs.
"""

from typing import List, Dict, Optional
from duckduckgo_search import DDGS
from pydantic import BaseModel
import json

class ResearchResult(BaseModel):
    """Structured research data for script enrichment."""
    topic: str
    summary: str
    technical_specs: List[str]
    recent_news: List[str]
    sources: List[str]

class ResearchEngine:
    """
    Autonomous researcher using DuckDuckGo.
    """
    
    def __init__(self, region: str = "wt-wt", safesearch: str = "moderate"):
        self.region = region
        self.safesearch = safesearch
        self.ddgs = DDGS()

    def research_topic(self, topic: str, max_results: int = 5) -> ResearchResult:
        """
        Perform comprehensive research on a topic.
        """
        print(f"🕵️  Researching: {topic}...")
        
        # 1. Technical Specs Search
        specs_query = f"{topic} technical specifications engine performance engineering"
        specs_results = self.ddgs.text(specs_query, max_results=max_results)
        
        # 2. News/Context Search
        news_query = f"{topic} latest news reviews automotive engineering"
        news_results = self.ddgs.news(news_query, max_results=max_results)
        
        # Process and structure data
        specs = [r['body'] for r in specs_results if 'body' in r]
        news = [r['title'] + ": " + r['body'] for r in news_results if 'body' in r]
        sources = [r['href'] for r in specs_results if 'href' in r]
        
        # Create a synthesis (simple concatenation for now, LLM will refine)
        summary = f"Research data for {topic}."
        
        return ResearchResult(
            topic=topic,
            summary=summary,
            technical_specs=specs[:5],  # Top 5 technical snippets
            recent_news=news[:3],       # Top 3 news items
            sources=sources[:3]
        )

    def get_enriched_prompt_context(self, topic: str) -> str:
        """
        Get a string block to inject into LLM system prompt.
        """
        result = self.research_topic(topic)
        
        context = f"""
        REAL-WORLD DATA CONTEXT (DO NOT HALLUCINATE, USE THIS):
        
        TOPIC: {result.topic}
        
        TECHNICAL SPECS & FACTS:
        {json.dumps(result.technical_specs, indent=2)}
        
        RECENT CONTEXT/NEWS:
        {json.dumps(result.recent_news, indent=2)}
        """
        return context

# Quick test
if __name__ == "__main__":
    researcher = ResearchEngine()
    data = researcher.research_topic("Porsche 911 GT3 RS 992.2")
    print("\nSpecs Found:")
    for spec in data.technical_specs:
        print(f"- {spec[:100]}...")
