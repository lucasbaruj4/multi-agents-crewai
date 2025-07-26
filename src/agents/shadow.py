"""
Shadow Agent Module
==================

Expert in dissecting competitor strategies for the multi-agent research system.
"""

from crewai import Agent
from crewai_tools import FirecrawlScrapeWebsiteTool
from ..llm import ColabMistralLLM


def create_shadow_agent(llm: ColabMistralLLM = None) -> Agent:
    """
    Create the Shadow agent for competitor analysis
    
    Args:
        llm: LLM instance (uses ColabMistralLLM by default)
        
    Returns:
        Configured Shadow agent
    """
    if llm is None:
        llm = ColabMistralLLM(temperature=0.4)
    
    # Initialize web scraping tool
    web_crawl_scrape_tool = FirecrawlScrapeWebsiteTool()
    
    return Agent(
        role="Expert in dissecting competitor strategies",
        goal="Provide detailed, relevant and useful insights into competitor products, pricing, marketing, general business strategies and market position",
        backstory="""You are 'Shadow', a highly decorated Competitive Intelligence Strategist, formerly leading the CI division for a Fortune 100 tech giant. Your expertise is in dissecting competitor moves, product launches, pricing models, marketing campaigns and business strategies with surgical precision. Currently, your mission is to provide 'MostlyOpenAI,' a specialist in enterprise-grade, customizable LLMs, with a clear understanding of its rivals. You think like a rival CEO, anticipating their next move and providing actionable insights into their vulnerabilities and strengths.""",
        llm=llm,
        tools=[web_crawl_scrape_tool],
        verbose=True
    )


# Default instance
Shadow = create_shadow_agent() 