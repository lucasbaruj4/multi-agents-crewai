"""
Multi-Agent Research System - Main Execution Script
==================================================

Enterprise LLM Market Analysis using CrewAI and Colab-hosted Mistral model.
"""

import os
import sys
from dotenv import load_dotenv
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
from src.llm.colab_mistral_llm import test_colab_mistral_llm

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def setup_environment():
    """Setup environment variables and API keys"""
    print("🔧 Setting up environment...")
    
    # First, try to load from .env.local file
    env_file = ".env.local"
    if os.path.exists(env_file):
        print(f"✅ Loading environment variables from {env_file}")
        load_dotenv(env_file)
        
        # Check if keys were loaded successfully
        if os.getenv("SERPER_API_KEY") and os.getenv("FIRECRAWL_API_KEY"):
            print("✅ API keys loaded successfully from .env.local")
            return True
        else:
            print("⚠️  .env.local file found but missing required keys")
    
    # If .env.local didn't work, check if running in Colab
    try:
        from google.colab import userdata
        print("✅ Running in Google Colab - using Colab Secrets")
        
        # Set API keys from Colab Secrets
        os.environ["SERPER_API_KEY"] = userdata.get("SERPER_API_KEY")
        os.environ["FIRECRAWL_API_KEY"] = userdata.get("FIRECRAWL_API_KEY")
        
    except ImportError:
        print("⚠️  Running locally - checking environment variables")
        print("Required environment variables:")
        print("  - SERPER_API_KEY (for web search)")
        print("  - FIRECRAWL_API_KEY (for web scraping)")
        print("Note: GOOGLE_API_KEY not needed since we're using Colab Mistral model")
        
        # Check if keys are set
        required_keys = ["SERPER_API_KEY", "FIRECRAWL_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print(f"❌ Missing environment variables: {missing_keys}")
            print("Please set these variables in .env.local file or as environment variables.")
            return False
    
    return True


def test_llm_integration():
    """Test CrewAI LLM integration with Colab Mistral server"""
    print("🤖 Testing CrewAI LLM integration...")
    
    try:
        success = test_colab_mistral_llm()
        if success:
            print("✅ CrewAI LLM integration working!")
            return True
        else:
            print("❌ CrewAI LLM integration failed")
            return False
            
    except Exception as e:
        print(f"❌ LLM integration test failed: {e}")
        print("Please ensure the Colab server is running with OpenAI-compatible endpoints")
        return False


def create_crew():
    """Create the research crew with all agents and tasks"""
    print("🤖 Creating research crew...")
    
    # Create agents (they will use the default Colab Mistral LLM)
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
    
    # Test LLM integration
    if not test_llm_integration():
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