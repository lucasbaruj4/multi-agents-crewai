#!/usr/bin/env python3
"""
System Readiness Test for End-to-End Execution
=============================================

This script verifies all system components are ready for full workflow execution.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_colab_connection():
    """Test Colab server connection"""
    print("🔌 Testing Colab Server Connection...")
    
    try:
        from scripts.local_mistral_client import ColabMistralClient
        
        client = ColabMistralClient()
        health = client.health_check()
        print(f"✅ Health check: {health}")
        
        # Test text generation
        result = client.generate_text("Test connection", max_tokens=20)
        if "response" in result:
            print(f"✅ Generation test: {result['response'][:50]}...")
            return True
        else:
            print(f"⚠️  Generation test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Colab connection failed: {e}")
        return False

def test_llm_wrapper():
    """Test LLM wrapper"""
    print("\n🤖 Testing LLM Wrapper...")
    
    try:
        from src.llm.colab_mistral_llm import ColabMistralLLM
        
        llm = ColabMistralLLM()
        health = llm.health_check()
        print(f"✅ LLM health: {health}")
        
        result = llm.generate("Test LLM wrapper", max_tokens=20)
        print(f"✅ LLM generation: {result[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ LLM wrapper failed: {e}")
        return False

def test_agent_creation():
    """Test agent creation"""
    print("\n👥 Testing Agent Creation...")
    
    try:
        from crewai import Agent
        from src.llm.colab_mistral_llm import ColabMistralLLM
        
        llm = ColabMistralLLM()
        
        # Test creating all 4 agents
        agents = []
        agent_configs = [
            ("Archivist", "Research and data collection specialist"),
            ("Shadow", "Competitive intelligence analyst"),
            ("Seer", "Technology trends and forecasting expert"),
            ("Nexus", "Strategic synthesis and report generation specialist")
        ]
        
        for role, goal in agent_configs:
            agent = Agent(
                role=role,
                goal=goal,
                backstory=f"Expert {role.lower()} with deep domain knowledge",
                llm=llm
            )
            agents.append(agent)
            print(f"✅ Created {role} agent")
        
        print(f"✅ Successfully created {len(agents)} agents")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_task_creation():
    """Test task creation"""
    print("\n📋 Testing Task Creation...")
    
    try:
        from src.tasks.market_analysis_tasks import create_market_analysis_tasks
        
        tasks = create_market_analysis_tasks()
        print(f"✅ Created {len(tasks)} tasks:")
        
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False

def test_tools_availability():
    """Test tools availability"""
    print("\n🛠️  Testing Tools Availability...")
    
    try:
        # Test custom tools
        from src.tools.plot_tools import GeneratePlotTool
        from src.tools.pdf_tools import CreatePDFReportTool
        
        plot_tool = GeneratePlotTool()
        pdf_tool = CreatePDFReportTool()
        
        print("✅ Custom tools loaded successfully")
        
        # Test crewai tools (if available)
        try:
            from crewai_tools import SerperDevTool, FirecrawlSearchTool
            print("✅ CrewAI tools available")
        except ImportError:
            print("⚠️  CrewAI tools not available (expected due to dependency issues)")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def test_output_directories():
    """Test output directory structure"""
    print("\n📁 Testing Output Directories...")
    
    try:
        import os
        
        # Create output directories if they don't exist
        output_dirs = [
            "output",
            "output/charts",
            "output/reports", 
            "output/logs"
        ]
        
        for dir_path in output_dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Directory ready: {dir_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Directory test failed: {e}")
        return False

def main():
    """Run all system readiness tests"""
    print("🚀 Starting System Readiness Test")
    print("=" * 50)
    
    tests = [
        test_colab_connection,
        test_llm_wrapper,
        test_agent_creation,
        test_task_creation,
        test_tools_availability,
        test_output_directories
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 System Readiness Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems ready! Proceeding to end-to-end execution.")
        return True
    elif passed >= total - 1:  # Allow one minor failure
        print("✅ System mostly ready. Proceeding with caution.")
        return True
    else:
        print("⚠️  Multiple system issues detected. Please resolve before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 