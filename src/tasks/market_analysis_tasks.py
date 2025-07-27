"""
Market Analysis Tasks Module
===========================

Optimized market analysis tasks for minimal Gemini API usage.
"""

from crewai import Task


def create_market_analysis_tasks():
    """
    Create optimized market analysis tasks for minimal API usage
    
    Returns:
        List of 4 optimized tasks
    """
    
    # Import agent creation functions here to avoid circular imports
    from ..agents import create_archivist_agent, create_shadow_agent, create_nexus_agent
    
    # Task 1: Market Segments (Ultra-minimal)
    identify_key_market_segments = Task(
        description="List the top 3-4 market segments in enterprise LLM industry. For each segment, provide: name, brief description (1 sentence), and estimated market size.",
        expected_output="""JSON with structure:
        {
          "segments": [
            {
              "name": "string",
              "description": "string (1 sentence)",
              "market_size": "string (e.g., $X billion)"
            }
          ]
        }""",
        agent=create_archivist_agent(),
        output_key='market_segments'
    )
    
    # Task 2: Research Collection (Minimal)
    collect_reports_news = Task(
        description="Find the top 3 most relevant recent sources (last 3 months) about enterprise LLM market. Focus on: adoption trends, key players, and market growth.",
        expected_output="""JSON with structure:
        {
          "sources": [
            {
              "title": "string",
              "url": "string",
              "key_finding": "string (1 sentence)"
            }
          ]
        }""",
        agent=create_archivist_agent(),
        output_key='research_sources'
    )
    
    # Task 3: Competitor Analysis (Minimal)
    profile_competitor = Task(
        description="Analyze the top 3 competitors in enterprise LLM market. For each: name, main strength, and market position.",
        expected_output="""JSON with structure:
        {
          "competitors": [
            {
              "name": "string",
              "strength": "string (1 sentence)",
              "position": "string (leader/challenger/niche)"
            }
          ]
        }""",
        agent=create_shadow_agent(),
        output_key='competitor_analysis'
    )
    
    # Task 4: Executive Summary (Synthesis)
    compile_all = Task(
        description="Create a 3-4 bullet point executive summary combining all previous findings. Focus on: key market insights, competitive landscape, and strategic recommendations.",
        expected_output="""JSON with structure:
        {
          "summary": {
            "key_insights": ["string (3-4 bullet points)"],
            "competitive_landscape": "string (1 sentence)",
            "recommendations": ["string (2-3 recommendations)"]
          }
        }""",
        agent=create_nexus_agent(),
        output_key='executive_summary'
    )
    
    return [
        identify_key_market_segments,
        collect_reports_news,
        profile_competitor,
        compile_all
    ] 