"""
Archivist Agent Module
=====================

Expert in finding relevant market data for the multi-agent research system.
"""

from crewai import Agent
from ..llm.gemini_llm import create_gemini_llm_strict


def create_archivist_agent(llm=None) -> Agent:
    """
    Create the Archivist agent for market data collection
    
    Args:
        llm: LLM instance (uses optimized Gemini LLM by default)
        
    Returns:
        Configured Archivist agent
    """
    if llm is None:
        llm = create_gemini_llm_strict()  # Ultra-strict for data collection
    
    return Agent(
        role="Expert in finding relevant market data",
        goal="Efficiently collect comprehensive, relevant and up-to-date information, industry reports and news, from reliable sources",
        backstory="""You are 'Archivist', a world-renowned, AI & Tech Intelligence Specialist from a top-tier global market research and technology analysis firm. Your unparalleled skill lies in meticulously extracting and verifying raw market data, cutting-edge research papers, industry reports, and real-time news from sources you consider trustworthy, reliable, and important within the rapidly evolving AI and LLM landscape. You pride yourself on your speed, accuracy, and ability to unearth the most relevant, granular information that others overlook. You are currently serving 'MostlyOpenAI,' a leading developer of enterprise-grade, highly customizable LLMs, providing them with the foundational intelligence they need.""",
        llm=llm,
        verbose=True
    ) 