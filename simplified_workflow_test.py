#!/usr/bin/env python3
"""
Simplified Workflow Test
=======================

This script tests the core functionality without CrewAI's LLM integration issues.
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_llm_directly():
    """Test LLM directly without CrewAI"""
    print("🤖 Testing LLM Directly...")
    
    try:
        from src.llm.colab_mistral_llm import ColabMistralLLM
        
        llm = ColabMistralLLM()
        
        # Test health
        health = llm.health_check()
        print(f"✅ Health check: {health}")
        
        # Test generation
        prompt = "Identify the top 3 market segments in enterprise LLM industry. Provide a brief overview of each."
        result = llm.generate(prompt, max_tokens=200)
        print(f"✅ Generation test: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def test_task_execution_simulation():
    """Simulate task execution without CrewAI"""
    print("\n📋 Simulating Task Execution...")
    
    try:
        from src.llm.colab_mistral_llm import ColabMistralLLM
        
        llm = ColabMistralLLM()
        
        # Simulate the 7 tasks
        tasks = [
            {
                "name": "Market Segments",
                "prompt": "Identify and list the primary market segments within the enterprise-grade LLM industry. For each segment, provide a brief overview of its specific LLM needs and growth potential.",
                "agent": "Archivist"
            },
            {
                "name": "Research Collection", 
                "prompt": "Conduct an exhaustive search for the most recent and comprehensive market reports, news articles, and industry analyses related to enterprise LLM adoption, market size, and growth trends.",
                "agent": "Archivist"
            },
            {
                "name": "Competitor Profiles",
                "prompt": "Based on the research, identify and profile 3-5 major competitors in the enterprise LLM space, including their market positioning, key products, and competitive advantages.",
                "agent": "Shadow"
            },
            {
                "name": "Marketing Analysis",
                "prompt": "Examine the marketing messaging, public statements, and strategic positioning of the identified competitors to understand their market approach and target segments.",
                "agent": "Shadow"
            },
            {
                "name": "Technology Trends",
                "prompt": "Analyze the research to pinpoint 3-5 emerging technology trends that are shaping the enterprise LLM market, including new capabilities and innovations.",
                "agent": "Seer"
            },
            {
                "name": "Regulatory Shifts",
                "prompt": "Research and identify 2-3 significant emerging regulatory or ethical considerations that could impact enterprise LLM adoption and market dynamics.",
                "agent": "Seer"
            },
            {
                "name": "Final Report",
                "prompt": "Compile all insights and findings from the previous tasks into a comprehensive executive summary report with key market insights and strategic recommendations.",
                "agent": "Nexus"
            }
        ]
        
        results = []
        
        for i, task in enumerate(tasks, 1):
            print(f"\n🔄 Executing Task {i}: {task['name']} (Agent: {task['agent']})")
            
            # Execute task
            result = llm.generate(task['prompt'], max_tokens=300)
            results.append({
                "task": task['name'],
                "agent": task['agent'],
                "result": result[:200] + "..." if len(result) > 200 else result
            })
            
            print(f"✅ Task {i} completed: {result[:50]}...")
            
            # Small delay between tasks
            time.sleep(1)
        
        print(f"\n✅ All {len(tasks)} tasks completed successfully!")
        return results
        
    except Exception as e:
        print(f"❌ Task simulation failed: {e}")
        return None

def save_simulation_results(results):
    """Save the simulation results"""
    print("\n💾 Saving Simulation Results...")
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save results to file
        result_file = f"output/logs/simulation_result_{timestamp}.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"Simplified Workflow Simulation Results\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Tasks Completed: {len(results)}\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"Task {i}: {result['task']}\n")
                f.write(f"Agent: {result['agent']}\n")
                f.write(f"Result: {result['result']}\n")
                f.write("-" * 50 + "\n\n")
        
        print(f"✅ Results saved to: {result_file}")
        
        # Save metrics
        metrics_file = f"output/logs/simulation_metrics_{timestamp}.json"
        import json
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "tasks_completed": len(results),
            "agents_used": len(set(r['agent'] for r in results)),
            "status": "completed",
            "workflow_type": "simplified_simulation"
        }
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"✅ Metrics saved to: {metrics_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
        return False

def main():
    """Main execution function"""
    print("🎯 Starting Simplified Workflow Test")
    print("=" * 60)
    
    # Test 1: Direct LLM
    if not test_llm_directly():
        print("❌ LLM test failed. Exiting.")
        return False
    
    # Test 2: Task simulation
    results = test_task_execution_simulation()
    if not results:
        print("❌ Task simulation failed. Exiting.")
        return False
    
    # Test 3: Save results
    save_success = save_simulation_results(results)
    
    print("\n" + "=" * 60)
    print("🎉 Simplified Workflow Test Results:")
    print(f"✅ LLM functionality: Working")
    print(f"✅ Task execution: {len(results)}/7 tasks completed")
    print(f"✅ Agents simulated: {len(set(r['agent'] for r in results))}/4 agents")
    print(f"💾 Results saved: {'Yes' if save_success else 'No'}")
    print(f"📊 Total workflow: {'SUCCESS' if save_success else 'PARTIAL'}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 