"""
Colab Mistral LLM Integration for CrewAI
=======================================

Direct LLM wrapper for Colab-hosted Mistral model that bypasses OpenAI compatibility issues.
"""

from typing import Optional, Dict, Any, List
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
        
        # CrewAI and LiteLLM compatibility attributes
        self.model = "custom/mistral-7b-instruct-v0.3"  # Add custom provider
        self.model_name = "custom/mistral-7b-instruct-v0.3"
        self.provider = "custom"
        
        # Additional LiteLLM compatibility
        self._llm_type = "custom"
        self.api_base = "https://mistral-server.loca.lt"
        self.api_key = "dummy-key"  # Required by LiteLLM but not used
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API server is healthy"""
        return self.client.health_check()
    
    def generate(self, messages, **kwargs) -> str:
        """
        Generate text using the remote Mistral model
        
        Args:
            messages: Chat messages (CrewAI format) or string prompt
            **kwargs: Additional generation parameters
                
        Returns:
            Generated text response
        """
        try:
            # Handle different input formats
            if isinstance(messages, list):
                # Extract content from chat messages format
                prompt = ""
                for msg in messages:
                    if isinstance(msg, dict) and 'content' in msg:
                        prompt += f"{msg.get('role', 'user')}: {msg['content']}\n"
                    else:
                        prompt += str(msg) + "\n"
            elif isinstance(messages, str):
                prompt = messages
            else:
                prompt = str(messages)
            
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
            return f"I apologize, but I'm currently unable to process this request due to a connection issue with the AI model. Error: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return self.client.get_model_info()
    
    # CrewAI compatibility methods
    def __call__(self, messages, **kwargs) -> str:
        """Make the class callable for CrewAI compatibility"""
        return self.generate(messages, **kwargs)
    
    def _call(self, prompt: str, **kwargs) -> str:
        """Internal method called by CrewAI framework"""
        return self.generate(prompt, **kwargs)
    
    def invoke(self, input_data, **kwargs) -> str:
        """CrewAI invoke method compatibility"""
        return self.generate(input_data, **kwargs)
    
    def completion(self, messages, **kwargs):
        """LiteLLM-style completion method"""
        response = self.generate(messages, **kwargs)
        # Return in LiteLLM format
        return type('MockResponse', (), {
            'choices': [type('Choice', (), {
                'message': type('Message', (), {'content': response})()
            })()]
        })()
    
    def get_supported_params(self) -> List[str]:
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