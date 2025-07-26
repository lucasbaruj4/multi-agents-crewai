"""
Seer Agent Module
================

Expert analyst in identifying critical shifts for the multi-agent research system.
"""

from crewai import Agent
from crewai_tools import FirecrawlScrapeWebsiteTool
from ..llm import ColabMistralLLM


def create_seer_agent(llm: ColabMistralLLM = None) -> Agent:
    """
    Create the Seer agent for trend analysis
    
    Args:
        llm: LLM instance (uses ColabMistralLLM by default)
        
    Returns:
        Configured Seer agent
    """
    if llm is None:
        llm = ColabMistralLLM(temperature=0.5)
    
    # Initialize web scraping tool
    web_crawl_scrape_tool = FirecrawlScrapeWebsiteTool()
    
    return Agent(
        role="Expert analyst in identifying critical shifts",
        goal="With a strong foundation on ground truths, detect emerging market trends, technological advancements and changes in consumer behavior",
        backstory="""You are 'Seer', an innovative Futures and Trends Forecaster with a track record of predicting significant market shifts years in advance for leading consultancies. Your methods combine deep pattern recognition with an intuitive grasp of socio-economic and technological currents. You excel at identifying nascent trends and disruptive innovations that will shape tomorrow's markets. Your current focus is exclusively on the rapidly evolving landscape of enterprise-grade LLMs, aiming to guide 'MostlyOpenAI' toward future opportunities.""",
        llm=llm,
        tools=[web_crawl_scrape_tool],
        verbose=True
    )


# Default instance
Seer = create_seer_agent() 