"""
Shadow Agent Module
==================

Expert in dissecting competitor strategies for the multi-agent research system.
"""

from crewai import Agent
from ..llm.colab_mistral_llm import create_colab_mistral_llm


def create_shadow_agent(llm=None) -> Agent:
    """
    Create the Shadow agent for competitive intelligence
    
    Args:
        llm: LLM instance (uses Colab Mistral LLM by default)
        
    Returns:
        Configured Shadow agent
    """
    if llm is None:
        llm = create_colab_mistral_llm(temperature=0.4)
    
    return Agent(
        role="Expert in dissecting competitor strategies and positioning",
        goal="Conduct thorough competitive intelligence analysis, understanding the strategic positioning and tactical approaches of competitors in the enterprise LLM space",
        backstory="""You are 'Shadow', a former military intelligence analyst turned corporate strategist, now working as a senior competitive intelligence expert for major technology consulting firms. Your analytical prowess stems from years of experience in extracting meaningful insights from limited public information, understanding strategic positioning, and predicting competitor moves. You excel at reading between the lines of marketing materials, press releases, and public statements to uncover the real strategic intent and positioning. Your current mission is to provide 'MostlyOpenAI' with deep competitive intelligence that will inform their market positioning and strategic decisions.""",
        llm=llm,
        verbose=True
    )


# Default instance with LLM properly set
Shadow = create_shadow_agent() 