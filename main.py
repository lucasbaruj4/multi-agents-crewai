"""
Multi-Agent Research System - Main Execution Script
==================================================

Enterprise LLM Market Analysis using CrewAI and Colab-hosted Mistral model.
"""

import os
import sys
from crewai import Crew, Process
from src.agents import Archivist, Shadow, Seer, Nexus
from src.tasks import (
    identify_key_market_segments,
    collect_reports_news,
    profile_competitor,
    analyze_comp_markt_position,
    identify_trends,
    identify_reg_ethic_shift,
    compile_all
)
from src.llm import ColabMistralLLM
from scripts.local_mistral_client import ColabMistralClient
from config.connection_credentials import COLAB_MISTRAL_URL


def setup_environment():
    """Setup environment variables and API keys"""
    print("🔧 Setting up environment...")
    
    # Check if running in Colab (for API key access)
    try:
        from google.colab import userdata
        print("✅ Running in Google Colab - using Colab Secrets")
        
        # Set API keys from Colab Secrets
        os.environ["SERPER_API_KEY"] = userdata.get("SERPER_API_KEY")
        os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
        os.environ["FIRECRAWL_API_KEY"] = userdata.get("FIRECRAWL_API_KEY")
        
    except ImportError:
        print("⚠️  Running locally - please ensure API keys are set in environment variables")
        print("Required environment variables:")
        print("  - SERPER_API_KEY")
        print("  - GOOGLE_API_KEY") 
        print("  - FIRECRAWL_API_KEY")
        
        # Check if keys are set
        required_keys = ["SERPER_API_KEY", "GOOGLE_API_KEY", "FIRECRAWL_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print(f"❌ Missing environment variables: {missing_keys}")
            print("Please set these variables before running the script.")
            return False
    
    return True


def test_connection():
    """Test connection to Colab Mistral server"""
    print("🔗 Testing connection to Colab Mistral server...")
    
    try:
        client = ColabMistralClient()
        health = client.health_check()
        
        if health.get("status") == "healthy":
            print("✅ Colab server is healthy!")
            return True
        else:
            print(f"❌ Colab server is not healthy: {health}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Please ensure the Colab server is running at:", COLAB_MISTRAL_URL)
        return False


def create_crew():
    """Create the research crew with all agents and tasks"""
    print("🤖 Creating research crew...")
    
    # Create agents with Colab Mistral LLM
    archivist = Archivist
    shadow = Shadow  
    seer = Seer
    nexus = Nexus
    
    # Create tasks
    tasks = [
        identify_key_market_segments,
        collect_reports_news,
        profile_competitor,
        analyze_comp_markt_position,
        identify_trends,
        identify_reg_ethic_shift,
        compile_all
    ]
    
    # Create crew
    crew = Crew(
        agents=[archivist, shadow, seer, nexus],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    return crew


def main():
    """Main execution function"""
    print("🚀 Multi-Agent Research System - Enterprise LLM Market Analysis")
    print("=" * 70)
    
    # Setup environment
    if not setup_environment():
        return
    
    # Test connection
    if not test_connection():
        return
    
    # Create crew
    crew = create_crew()
    
    print("\n🎯 Starting market analysis...")
    print("This will analyze the enterprise LLM market and generate a comprehensive report.")
    print("The process includes:")
    print("  - Market segment identification")
    print("  - Competitor analysis")
    print("  - Trend identification")
    print("  - Regulatory analysis")
    print("  - Executive report generation")
    print("\n⏳ This may take several minutes...")
    
    try:
        # Execute the crew
        result = crew.kickoff()
        
        print("\n✅ Analysis completed successfully!")
        print(f"📄 Report generated: {result}")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Please check the logs above for more details.")


if __name__ == "__main__":
    main() 