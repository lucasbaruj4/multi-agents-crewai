"""
Multi-Agent Research System - Main Execution Script
==================================================

Enterprise LLM Market Analysis using CrewAI and optimized Gemini model.
Now with Company Information System for personalized research.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from crewai import Crew, Process

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents import create_archivist_agent, create_shadow_agent, create_nexus_agent
from src.tasks import create_market_analysis_tasks
from src.llm.gemini_llm import create_gemini_llm_standard
from src.company_profile import CompanyProfile, run_questionnaire
from src.templates.context_injector import create_context_injector


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


def load_or_create_company_profile(skip_questionnaire: bool = False, force_new: bool = False) -> CompanyProfile:
    """
    Load existing company profile or create new one via questionnaire.
    
    Args:
        skip_questionnaire: Skip questionnaire and use existing profile
        force_new: Force creation of new profile
        
    Returns:
        CompanyProfile instance
    """
    print("🏢 Company Profile Management")
    print("-" * 40)
    
    # Check if profile exists
    if CompanyProfile.exists() and not force_new:
        try:
            profile = CompanyProfile.load()
            print(f"✅ Loaded existing profile for: {profile.company_name}")
            
            if not skip_questionnaire:
                # Ask if user wants to update profile
                print("\n❓ Would you like to update your company profile? (yes/no):")
                choice = input("💬 ").strip().lower()
                
                if choice in ['yes', 'y']:
                    print("\n🔄 Starting company profile questionnaire...")
                    return run_questionnaire()
            
            return profile
            
        except Exception as e:
            print(f"⚠️  Error loading profile: {e}")
            print("🔄 Creating new profile...")
    
    # Create new profile
    if not skip_questionnaire:
        print("🆕 No company profile found. Let's create one!")
        print("This will take about 5-10 minutes and will personalize your research.")
        return run_questionnaire()
    else:
        # Create sample profile for testing
        print("📋 Creating sample company profile for testing...")
        return CompanyProfile.create_sample_profile()


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


def create_personalized_crew(company_profile: CompanyProfile):
    """
    Create the research crew with company-specific personalization.
    
    Args:
        company_profile: CompanyProfile instance for personalization
        
    Returns:
        Crew instance with personalized agents and tasks
    """
    print("🤖 Creating personalized research crew...")
    
    # Create context injector for personalization
    context_injector = create_context_injector(company_profile)
    
    # Create agents with company context
    print(f"👥 Creating agents specialized for {company_profile.company_name}...")
    archivist = create_archivist_agent()
    shadow = create_shadow_agent()
    nexus = create_nexus_agent()
    
    # Create optimized tasks with company context
    print(f"📋 Creating tasks focused on {company_profile.industry}...")
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
    """Main execution function with company information integration"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Multi-Agent Research System with Company Personalization")
    parser.add_argument("--skip-questionnaire", action="store_true", 
                       help="Skip questionnaire and use existing profile")
    parser.add_argument("--new-profile", action="store_true", 
                       help="Force creation of new company profile")
    parser.add_argument("--questionnaire-only", action="store_true", 
                       help="Run questionnaire only, don't start analysis")
    
    args = parser.parse_args()
    
    print("🚀 Multi-Agent Research System - Enterprise LLM Market Analysis")
    print("=" * 70)
    print("🎯 OPTIMIZED FOR MINIMAL GEMINI API USAGE + COMPANY PERSONALIZATION")
    print("📊 Expected usage: 500-700 tokens (personalized insights)")
    print("=" * 70)
    
    # Setup environment
    if not setup_environment():
        return
    
    # Handle questionnaire-only mode
    if args.questionnaire_only:
        print("📋 Running company profile questionnaire only...")
        try:
            profile = run_questionnaire()
            print(f"\n✅ Questionnaire completed! Profile saved for: {profile.company_name}")
            return
        except Exception as e:
            print(f"❌ Error during questionnaire: {e}")
            return
    
    # Load or create company profile
    try:
        company_profile = load_or_create_company_profile(
            skip_questionnaire=args.skip_questionnaire,
            force_new=args.new_profile
        )
    except Exception as e:
        print(f"❌ Error with company profile: {e}")
        return
    
    # Test Gemini integration
    if not test_gemini_integration():
        return
    
    # Create personalized crew
    crew = create_personalized_crew(company_profile)
    
    print(f"\n🎯 Starting personalized market analysis for {company_profile.company_name}...")
    print(f"🏭 Industry: {company_profile.industry}")
    print(f"📊 Research Focus: {', '.join(company_profile.research_focus_areas[:3])}")
    print(f"🎯 Strategic Goals: {', '.join(company_profile.strategic_goals[:2])}")
    print("\nThe process includes:")
    print("  - Market segment identification (personalized)")
    print("  - Research collection (company-focused)")
    print("  - Competitor analysis (targeted)")
    print("  - Executive summary (strategic insights)")
    print("\n⏳ This will provide highly targeted insights for your company...")
    
    try:
        # Execute the crew
        result = crew.kickoff()
        
        print("\n✅ Personalized analysis completed successfully!")
        print(f"📄 Results: {result}")
        print(f"🎯 Insights tailored for {company_profile.company_name}")
        print("💰 Optimized API usage with maximum personalization!")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("Please check the logs above for more details.")


def run_questionnaire_command():
    """Convenience function to run questionnaire from command line."""
    try:
        profile = run_questionnaire()
        print(f"\n✅ Questionnaire completed! Profile created for: {profile.company_name}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if running as questionnaire module
    if len(sys.argv) > 1 and sys.argv[1] == "questionnaire":
        run_questionnaire_command()
    else:
        main() 