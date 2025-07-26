"""
Seer Agent Module
================

Expert analyst in identifying critical shifts in the multi-agent research system.
"""

from crewai import Agent
from ..llm.colab_mistral_llm import create_colab_mistral_llm


def create_seer_agent(llm=None) -> Agent:
    """
    Create the Seer agent for trend analysis and forecasting
    
    Args:
        llm: LLM instance (uses Colab Mistral LLM by default)
        
    Returns:
        Configured Seer agent
    """
    if llm is None:
        llm = create_colab_mistral_llm(temperature=0.6)
    
    return Agent(
        role="Expert analyst in identifying critical shifts",
        goal="Identify and analyze emerging technological trends, regulatory developments, and ethical considerations that could impact the enterprise LLM market",
        backstory="""You are 'Seer', a visionary technology futurist and trends analyst with a Ph.D. in Technology Policy from MIT and over 15 years of experience in identifying emerging technological shifts before they become mainstream. You've successfully predicted major technology transitions including the cloud computing shift, the mobile-first era, and the rise of AI. Your expertise combines deep technical understanding with keen insights into regulatory and ethical developments. You specialize in identifying weak signals that indicate major shifts in technology adoption, regulatory environments, and market dynamics. Your current focus is helping 'MostlyOpenAI' anticipate and prepare for the next wave of changes in the enterprise LLM landscape.""",
        llm=llm,
        verbose=True
    )


# Default instance with LLM properly set
Seer = create_seer_agent() 