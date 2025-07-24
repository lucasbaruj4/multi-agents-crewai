"""
CrewAI Integration with Colab Mistral API
This file shows how to integrate your Colab-hosted Mistral model with your existing CrewAI project
"""

from crewai import Agent, Task, Process, Crew, LLM
from local_mistral_client import ColabMistralClient
import os
from google.colab import userdata
from crewai_tools import SerperDevTool, FirecrawlSearchTool, FirecrawlScrapeWebsiteTool

# Import your custom tools
from tools import GeneratePlotTool, CreatePDFReportTool

class ColabMistralLLM(LLM):
    """
    Custom LLM wrapper for Colab-hosted Mistral model
    """
    def __init__(self, colab_url: str, temperature: float = 0.5):
        self.client = ColabMistralClient(colab_url)
        self.temperature = temperature
        
    def generate(self, prompt: str, **kwargs):
        """
        Generate text using the remote Mistral model
        """
        try:
            result = self.client.generate_text(
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 512),
                temperature=kwargs.get('temperature', self.temperature)
            )
            
            if "error" in result:
                raise Exception(f"Model error: {result['error']}")
                
            return result["response"]
            
        except Exception as e:
            print(f"Error generating text: {e}")
            # Fallback to a simple response
            return f"Error occurred: {str(e)}"

def setup_environment():
    """
    Set up the environment with API keys and tools
    """
    # Set up API keys (these should be in Colab Secrets)
    os.environ["SERPER_API_KEY"] = userdata.get("SERPER_API_KEY")
    os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
    os.environ["FIRECRAWL_API_KEY"] = userdata.get("FIRECRAWL_API_KEY")
    
    # Create output directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("output_charts", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)
    
    # Initialize tools
    web_search_tool = SerperDevTool()
    web_crawl_tool = FirecrawlSearchTool()
    web_crawl_scrape_tool = FirecrawlScrapeWebsiteTool()
    generate_plot_tool = GeneratePlotTool()
    create_pdf_tool = CreatePDFReportTool()
    
    return {
        'web_search_tool': web_search_tool,
        'web_crawl_tool': web_crawl_tool,
        'web_crawl_scrape_tool': web_crawl_scrape_tool,
        'generate_plot_tool': generate_plot_tool,
        'create_pdf_tool': create_pdf_tool
    }

def create_agents(colab_url: str, tools: dict):
    """
    Create agents using the Colab Mistral model
    """
    # Create LLM instances with different temperatures for different roles
    archivist_llm = ColabMistralLLM(colab_url, temperature=0.3)
    shadow_llm = ColabMistralLLM(colab_url, temperature=0.4)
    seer_llm = ColabMistralLLM(colab_url, temperature=0.5)
    nexus_llm = ColabMistralLLM(colab_url, temperature=0.3)
    
    # Create agents
    Archivist = Agent(
        role="Expert in finding relevant market data",
        goal="Efficiently collect comprehensive, relevant and up-to-date information, industry reports and news, from reliable sources",
        backstory="You are 'Archivist', a world-renowned, AI & Tech Intelligence Specialist from a top-tier global market research and technology analysis firm. Your unparalleled skill lies in meticulously extracting and verifying raw market data, cutting-edge research papers, industry reports, and real-time news from sources you consider trustworthy, reliable, and important within the rapidly evolving AI and LLM landscape.",
        llm=archivist_llm,
        tools=[tools['web_search_tool'], tools['web_crawl_tool'], tools['web_crawl_scrape_tool']],
        verbose=True
    )
    
    Shadow = Agent(
        role="Expert in dissecting competitor strategies",
        goal='Provide detailed, relevant and useful insights into competitor products, pricing, marketing, general business strategies and market position',
        backstory="You are 'Shadow', a highly decorated Competitive Intelligence Strategist, formerly leading the CI division for a Fortune 100 tech giant. Your expertise is in dissecting competitor moves, product launches, pricing models, marketing campaigns and business strategies with surgical precision.",
        llm=shadow_llm,
        tools=[tools['web_crawl_scrape_tool']],
        verbose=True
    )
    
    Seer = Agent(
        role='Expert analyst in identifying critical shifts',
        goal='With a strong foundation on ground truths, detect emerging market trends, technological advancements and changes in consumer behavior',
        backstory="You are 'Seer', an innovative Futures and Trends Forecaster with a track record of predicting significant market shifts years in advance for leading consultancies. Your methods combine deep pattern recognition with an intuitive grasp of socio-economic and technological currents.",
        llm=seer_llm,
        tools=[tools['web_crawl_scrape_tool']],
        verbose=True
    )
    
    Nexus = Agent(
        role='Expert in concise and actionable reporting',
        goal='Consolidate all gathered relevant insights into clear, summarized reports with actionable recommendations for business strategy',
        backstory="You are 'Nexus', the Chief Insights Architect for an exclusive executive advisory board. Your unique talent is transforming vast, complex datasets and disparate analyses into crisp, compelling, and actionable strategic reports.",
        llm=nexus_llm,
        tools=[tools['generate_plot_tool'], tools['create_pdf_tool']],
        verbose=True
    )
    
    return Archivist, Shadow, Seer, Nexus

def create_tasks(agents):
    """
    Create tasks for the crew
    """
    Archivist, Shadow, Seer, Nexus = agents
    
    # Research tasks
    identify_key_market_segments = Task(
        description="Identify and list the primary market segments within the enterprise-grade LLM industry (e.g., finance, healthcare, legal, specialized customer service, R&D). For each segment, provide a brief overview of its specific LLM needs and growth potential.",
        expected_output="Format JSON, A structured list of 3-5 key enterprise LLM market segments, with a 1-2 paragraph summary for each, including estimated market size and growth rates if available. Name the output 'key_market_segments'",
        agent=Archivist,
        output_key='key_market_segments'
    )
    
    collect_reports_news = Task(
        description="Conduct an exhaustive search for the most recent and highly relevant industry reports, whitepapers, research papers, academic studies, and significant news articles (published within the last 4 months) pertaining to the enterprise-grade LLM market.",
        expected_output="Format JSON, A curated, categorized list of high-quality external resources (links to PDFs or web articles). Each link must be accompanied by a concise summary highlighting its main findings or key contribution to understanding the enterprise LLM market within the specified segments. Name the output: 'key_market_research'",
        context=[identify_key_market_segments],
        agent=Archivist,
        output_key='key_market_research'
    )
    
    # Business analysis tasks
    profile_competitor = Task(
        description="Based on the {key_market_research} and its analysis of relevant market segments, identify and create a detailed profile for the top 3-5 direct competitors to 'MostlyOpenAI' in the enterprise-grade LLM space.",
        expected_output="A JSON object structured with two main keys: 'plot_data' and 'summary_text'.",
        context=[collect_reports_news],
        agent=Shadow,
        output_key='competitor_profiles'
    )
    
    # Add more tasks as needed...
    
    return [identify_key_market_segments, collect_reports_news, profile_competitor]

def run_crew(colab_url: str):
    """
    Main function to run the crew with Colab Mistral integration
    """
    print("Setting up environment...")
    tools = setup_environment()
    
    print("Creating agents...")
    agents = create_agents(colab_url, tools)
    
    print("Creating tasks...")
    tasks = create_tasks(agents)
    
    print("Setting up crew...")
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("Starting crew execution...")
    try:
        result = crew.kickoff()
        print(f"Crew execution completed: {result}")
        return result
    except Exception as e:
        print(f"Error during crew execution: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your actual Colab API URL
    COLAB_URL = "https://7606211221ff.ngrok-free.app"
    
    # Test the connection first
    client = ColabMistralClient(COLAB_URL)
    health = client.health_check()
    
    if health.get("status") == "healthy":
        print("Colab server is healthy, starting crew...")
        result = run_crew(COLAB_URL)
    else:
        print("Colab server is not healthy. Please check your setup.")
        print(f"Health check result: {health}") 