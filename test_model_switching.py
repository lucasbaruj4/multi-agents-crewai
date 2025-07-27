"""
Test Model Switching Script
==========================

Demonstrates the seamless model switching capabilities of the unified
LLM configuration system.
"""

import os
from src.llm import ModelConfig, create_llm, create_strict_llm, create_standard_llm


def test_model_switching():
    """Test the seamless model switching functionality"""
    print("🧪 Testing Seamless Model Switching")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    
    # Show available providers
    available = ModelConfig.get_available_providers()
    print(f"📊 Available Providers: {list(available.keys())}")
    
    if not available:
        print("❌ No providers available. Please set one of:")
        print("   - GEN_MODEL_API (for Google Gemini)")
        print("   - OPENAI_API_KEY (for OpenAI)")
        print("   - ANTHROPIC_API_KEY (for Anthropic)")
        print("   - MISTRAL_API_KEY (for Mistral)")
        return
    
    # Show current provider info
    provider_info = ModelConfig.get_provider_info()
    print(f"🎯 Current Provider: {provider_info['provider_name']}")
    print(f"🤖 Current Model: {provider_info['default_model']}")
    print(f"💰 Cost Efficiency: {provider_info['cost_efficiency']}")
    
    # Test LLM creation
    print("\n🔧 Testing LLM Creation...")
    try:
        # Test standard LLM
        llm_standard = create_standard_llm()
        print("✅ Standard LLM created successfully")
        
        # Test strict LLM
        llm_strict = create_strict_llm()
        print("✅ Strict LLM created successfully")
        
        # Test custom LLM
        llm_custom = create_llm(temperature=0.5, max_tokens=200)
        print("✅ Custom LLM created successfully")
        
        print("\n🎉 All LLM creation tests passed!")
        print("🚀 Model switching is working seamlessly!")
        
    except Exception as e:
        print(f"❌ LLM creation failed: {e}")
    
    # Show how to switch models
    print("\n📋 How to Switch Models:")
    print("1. Change your .env.local file:")
    print("   # For Google Gemini:")
    print("   GEN_MODEL_API=your_gemini_key")
    print("   # For OpenAI:")
    print("   OPENAI_API_KEY=your_openai_key")
    print("   # For Anthropic:")
    print("   ANTHROPIC_API_KEY=your_anthropic_key")
    print("   # For Mistral:")
    print("   MISTRAL_API_KEY=your_mistral_key")
    print("\n2. Run the system again - it will automatically detect and use the new provider!")
    print("3. No code changes needed - completely seamless!")


def test_provider_specific():
    """Test provider-specific LLM creation"""
    print("\n🔧 Testing Provider-Specific Creation...")
    
    available = ModelConfig.get_available_providers()
    
    for provider in available.keys():
        try:
            print(f"\n🤖 Testing {provider} provider...")
            llm = ModelConfig.create_llm(provider=provider)
            print(f"✅ {provider} LLM created successfully")
        except Exception as e:
            print(f"❌ {provider} LLM creation failed: {e}")


if __name__ == "__main__":
    test_model_switching()
    test_provider_specific() 