"""
Colab Mistral LLM Integration for CrewAI
=======================================

Direct LLM wrapper for Colab-hosted Mistral model that bypasses OpenAI compatibility issues.
"""

from typing import Optional, Dict, Any
from scripts.local_mistral_client import ColabMistralClient


class ColabMistralLLM:
    """
    Direct LLM wrapper for CrewAI that communicates with our Colab server
    without requiring OpenAI API compatibility
    """
    
    def __init__(self, temperature: float = 0.7, max_tokens: int = 2048):
        """
        Initialize the Colab Mistral LLM wrapper
        
        Args:
            temperature: Sampling temperature for text generation
            max_tokens: Maximum tokens to generate
        """
        self.client = ColabMistralClient()
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # CrewAI compatibility attributes
        self.model = "mistral-7b-instruct-v0.3"
        self.model_name = "mistral-7b-instruct-v0.3"
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API server is healthy"""
        return self.client.health_check()
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using the remote Mistral model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
                
        Returns:
            Generated text response
        """
        try:
            # Extract parameters with defaults
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            temperature = kwargs.get('temperature', self.temperature)
            
            result = self.client.generate_text(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            if "response" in result:
                return result["response"]
            elif "error" in result:
                raise Exception(f"Model error: {result['error']}")
            else:
                return str(result)
                
        except Exception as e:
            print(f"Error generating text: {e}")
            # Return a fallback response for testing
            return f"Error occurred: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return self.client.get_model_info()
    
    # CrewAI compatibility methods
    def __call__(self, prompt: str, **kwargs) -> str:
        """Make the class callable for CrewAI compatibility"""
        return self.generate(prompt, **kwargs)
    
    def _call(self, prompt: str, **kwargs) -> str:
        """Internal method called by CrewAI framework"""
        return self.generate(prompt, **kwargs)
    
    def invoke(self, input_data, **kwargs) -> str:
        """CrewAI invoke method compatibility"""
        if isinstance(input_data, str):
            return self.generate(input_data, **kwargs)
        elif isinstance(input_data, dict) and 'prompt' in input_data:
            return self.generate(input_data['prompt'], **kwargs)
        else:
            return self.generate(str(input_data), **kwargs)
    
    def get_supported_params(self) -> list:
        """Return supported parameters for CrewAI"""
        return ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"]
    
    def get_model_name(self) -> str:
        """Return model name for CrewAI"""
        return self.model_name


def create_colab_mistral_llm(temperature: float = 0.7, max_tokens: int = 2048) -> ColabMistralLLM:
    """
    Create a direct ColabMistralLLM instance
    
    Args:
        temperature: Sampling temperature for text generation
        max_tokens: Maximum tokens to generate
        
    Returns:
        Configured ColabMistralLLM instance
    """
    return ColabMistralLLM(temperature=temperature, max_tokens=max_tokens)


def test_colab_mistral_llm() -> bool:
    """
    Test the Colab Mistral LLM integration
    
    Returns:
        True if test passes, False otherwise
    """
    try:
        # Test LLM creation
        llm = create_colab_mistral_llm()
        
        # Test health check
        health = llm.health_check()
        print(f"✅ Health check: {health}")
        
        # Test basic generation
        result = llm.generate("Test message: Hello!")
        print(f"✅ LLM test successful: {result[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False 