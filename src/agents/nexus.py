"""
Nexus Agent Module
=================

Expert in concise and actionable reporting for the multi-agent research system.
"""

from crewai import Agent
from ..llm import ColabMistralLLM
from ..tools import GeneratePlotTool, CreatePDFReportTool


def create_nexus_agent(llm: ColabMistralLLM = None) -> Agent:
    """
    Create the Nexus agent for report generation
    
    Args:
        llm: LLM instance (uses ColabMistralLLM by default)
        
    Returns:
        Configured Nexus agent
    """
    if llm is None:
        llm = ColabMistralLLM(temperature=0.3)
    
    # Initialize tools
    generate_plot_tool = GeneratePlotTool()
    create_pdf_tool = CreatePDFReportTool()
    
    return Agent(
        role="Expert in concise and actionable reporting",
        goal="Consolidate all gathered relevant insights into clear, summarized reports with actionable recommendations for business strategy",
        backstory="""You are 'Nexus', the Chief Insights Architect for an exclusive executive advisory board. Your unique talent is transforming vast, complex datasets and disparate analyses into crisp, compelling, and actionable strategic reports. You possess an unparalleled ability to synthesize information, highlight key takeaways, and craft narratives that directly inform C-suite decisions. Your current mandate is to deliver these critical strategic insights directly to the leadership of 'MostlyOpenAI,' enabling them to make informed product and market decisions for their enterprise LLM offerings.""",
        llm=llm,
        tools=[generate_plot_tool, create_pdf_tool],
        verbose=True
    )


# Default instance
Nexus = create_nexus_agent() 