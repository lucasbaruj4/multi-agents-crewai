#!/usr/bin/env python3
"""
Enhanced End-to-End Test with CrewAI Integration
==============================================

This script tests the complete CrewAI integration with the new LLM approach.
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_connection():
    """Test basic connection to Colab server"""
    print("🔌 Testing basic connection to Colab server...")
    
    try:
        from scripts.local_mistral_client import ColabMistralClient
        
        client = ColabMistralClient()
        health = client.health_check()
        print(f"✅ Health check: {health}")
        
        # Test basic generation
        result = client.generate_text("Hello", max_tokens=20)
        if "response" in result:
            print(f"✅ Basic generation: {result['response'][:50]}...")
            return True
        else:
            print(f"❌ Basic generation failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
        return False

def test_crewai_llm_integration():
    """Test CrewAI LLM integration"""
    print("\n🤖 Testing CrewAI LLM Integration...")
    
    try:
        from src.llm.colab_mistral_llm import test_colab_mistral_llm
        
        success = test_colab_mistral_llm()
        if success:
            print("✅ CrewAI LLM integration working!")
            return True
        else:
            print("❌ CrewAI LLM integration failed")
            return False
            
    except Exception as e:
        print(f"❌ CrewAI LLM integration test failed: {e}")
        print("This is expected if the Colab server doesn't have OpenAI-compatible endpoints yet")
        return False

def test_fallback_approach():
    """Test fallback approach with direct LLM usage"""
    print("\n🔄 Testing fallback approach...")
    
    try:
        from crewai import LLM
        from config.connection_credentials import COLAB_MISTRAL_URL
        
        # Try to create an LLM instance pointing to our server
        llm = LLM(
            model="openai/gpt-3.5-turbo",  # Use a standard model name
            base_url=f"{COLAB_MISTRAL_URL}/v1",
            api_key="dummy-key"
        )
        
        print("✅ LLM instance created successfully")
        
        # Try a simple call (this might fail due to endpoint compatibility)
        try:
            result = llm.call("Hello, this is a test")
            print(f"✅ Fallback approach successful: {result[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️  LLM call failed (expected): {e}")
            print("✅ LLM instance creation works, endpoint compatibility needed")
            return False
            
    except Exception as e:
        print(f"❌ Fallback approach failed: {e}")
        return False

def test_agent_creation():
    """Test agent creation with new LLM approach"""
    print("\n👥 Testing Agent Creation...")
    
    try:
        from src.agents.archivist import create_archivist_agent
        from src.agents.shadow import create_shadow_agent
        from src.agents.seer import create_seer_agent
        from src.agents.nexus import create_nexus_agent
        
        agents = []
        agent_creators = [
            ("Archivist", create_archivist_agent),
            ("Shadow", create_shadow_agent),
            ("Seer", create_seer_agent),
            ("Nexus", create_nexus_agent)
        ]
        
        for name, creator in agent_creators:
            try:
                agent = creator()
                agents.append(agent)
                print(f"✅ Created {name} agent")
            except Exception as e:
                print(f"❌ Failed to create {name} agent: {e}")
                return False
        
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
        print(f"✅ Created {len(tasks)} tasks")
        
        for i, task in enumerate(tasks, 1):
            print(f"  Task {i}: {task.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False

def test_crew_creation():
    """Test crew creation"""
    print("\n🚢 Testing Crew Creation...")
    
    try:
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
        
        # Create crew
        crew = Crew(
            agents=[Archivist, Shadow, Seer, Nexus],
            tasks=[
                identify_key_market_segments,
                collect_reports_news,
                profile_competitor,
                analyze_comp_markt_position,
                identify_trends,
                identify_reg_ethic_shift,
                compile_all
            ],
            process=Process.sequential,
            verbose=False  # Disable verbose for testing
        )
        
        print("✅ Crew created successfully")
        print(f"  Agents: {len(crew.agents)}")
        print(f"  Tasks: {len(crew.tasks)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        return False

def save_test_results(results):
    """Save test results"""
    print("\n💾 Saving Test Results...")
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure output directory exists
        os.makedirs("output/logs", exist_ok=True)
        
        result_file = f"output/logs/end_to_end_test_{timestamp}.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"End-to-End Test Results\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Total Tests: {len(results)}\n")
            f.write(f"Passed: {sum(results.values())}\n")
            f.write(f"Failed: {len(results) - sum(results.values())}\n\n")
            
            for test_name, result in results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                f.write(f"{test_name}: {status}\n")
        
        print(f"✅ Results saved to: {result_file}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
        return False

def main():
    """Main execution function"""
    print("🎯 Enhanced End-to-End Test with CrewAI Integration")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Basic connection
    results["Basic Connection"] = test_basic_connection()
    
    # Test 2: CrewAI LLM integration
    results["CrewAI LLM Integration"] = test_crewai_llm_integration()
    
    # Test 3: Fallback approach
    results["Fallback Approach"] = test_fallback_approach()
    
    # Test 4: Agent creation
    results["Agent Creation"] = test_agent_creation()
    
    # Test 5: Task creation
    results["Task Creation"] = test_task_creation()
    
    # Test 6: Crew creation
    results["Crew Creation"] = test_crew_creation()
    
    # Save results
    save_test_results(results)
    
    print("\n" + "=" * 60)
    print("🎉 End-to-End Test Results:")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n📊 Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for operation.")
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Minor issues to resolve.")
    else:
        print("❌ Multiple test failures. Significant issues to resolve.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 