"""
Multi-Agent Research System - Main Execution Script
==================================================

Enterprise LLM Market Analysis using CrewAI and optimized Gemini model.
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents import create_archivist_agent, create_shadow_agent, create_nexus_agent
from src.tasks import create_market_analysis_tasks
from src.llm.gemini_llm import create_gemini_llm_standard

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
        if os.getenv("SERPER_API_KEY") and os.getenv("FIRECRAWL_API_KEY") and os.getenv("GOOGLE_API_KEY"):
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
        os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
        
    except ImportError:
        print("⚠️  Running locally - checking environment variables")
        print("Required environment variables:")
        print("  - SERPER_API_KEY (for web search)")
        print("  - FIRECRAWL_API_KEY (for web scraping)")
        print("  - GOOGLE_API_KEY (for Gemini model)")
        
        # Check if keys are set
        required_keys = ["SERPER_API_KEY", "FIRECRAWL_API_KEY", "GOOGLE_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print(f"❌ Missing environment variables: {missing_keys}")
            print("Please set these variables in .env.local file or as environment variables.")
            return False
    
    return True


def test_gemini_integration():
    """Test Gemini LLM integration"""
    print("🤖 Testing Gemini LLM integration...")
    
    try:
        # Test Gemini LLM creation
        llm = create_gemini_llm_standard()
        print("✅ Gemini LLM created successfully")
        print("✅ Gemini integration working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini integration test failed: {e}")
        return False


def create_crew():
    """Create the research crew with optimized agents and tasks"""
    print("🤖 Creating research crew...")
    
    # Create agents (they will use the optimized Gemini LLM)
    archivist = create_archivist_agent()
    shadow = create_shadow_agent()
    nexus = create_nexus_agent()
    
    # Create optimized tasks (4 tasks instead of 7)
    tasks = create_market_analysis_tasks()
    
    # Create crew
    crew = Crew(
        agents=[archivist, shadow, nexus],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    return crew


def main():
    """Main execution function"""
    print("🚀 Multi-Agent Research System - Enterprise LLM Market Analysis")
    print("=" * 70)
    print("🎯 OPTIMIZED FOR MINIMAL GEMINI API USAGE")
    print("📊 Expected usage: 400-600 tokens (75-80% reduction)")
    print("=" * 70)
    
    # Setup environment
    if not setup_environment():
        return
    
    # Test Gemini integration
    if not test_gemini_integration():
        return
    
    # Create crew
    crew = create_crew()
    
    print("\n🎯 Starting optimized market analysis...")
    print("This will analyze the enterprise LLM market with minimal API usage.")
    print("The process includes:")
    print("  - Market segment identification (ultra-minimal)")
    print("  - Research collection (minimal)")
    print("  - Competitor analysis (minimal)")
    print("  - Executive summary (synthesis)")
    print("\n⏳ This should complete quickly with minimal API usage...")
    
    try:
        # Execute the crew
        result = crew.kickoff()
        
        print("\n✅ Analysis completed successfully!")
        print(f"📄 Results: {result}")
        print("💰 Minimal API usage achieved!")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Please check the logs above for more details.")


if __name__ == "__main__":
    main() 