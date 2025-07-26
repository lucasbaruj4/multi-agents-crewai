"""
Colab Mistral LLM Module
========================

Custom LLM wrapper for Colab-hosted Mistral model integration with CrewAI.
"""

from crewai import LLM
from scripts.local_mistral_client import ColabMistralClient
from config.connection_credentials import COLAB_MISTRAL_URL


class ColabMistralLLM(LLM):
    """
    Custom LLM wrapper for Colab-hosted Mistral model
    """
    
    def __init__(self, colab_url: str = None, temperature: float = 0.5):
        """
        Initialize the Colab Mistral LLM wrapper
        
        Args:
            colab_url: Optional URL override (uses connection_credentials.py by default)
            temperature: Sampling temperature for text generation
        """
        self.client = ColabMistralClient(colab_url or COLAB_MISTRAL_URL)
        self.temperature = temperature
        
    def generate(self, prompt: str, **kwargs):
        """
        Generate text using the remote Mistral model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        try:
            result = self.client.generate_text(
                prompt=prompt,
                max_tokens=kwargs.get('max_tokens', 512),
                temperature=kwargs.get('temperature', self.temperature)
            )
            
            if "error" in result:
                raise Exception(f"Model error: {result['error']}")
                
            return result["response"]
            
        except Exception as e:
            print(f"Error generating text: {e}")
            # Fallback to a simple response
            return f"Error occurred: {str(e)}"
    
    def health_check(self):
        """
        Check if the Colab server is healthy
        
        Returns:
            Health status dictionary
        """
        return self.client.health_check()
    
    def get_model_info(self):
        """
        Get information about the loaded model
        
        Returns:
            Model information dictionary
        """
        return self.client.get_model_info() 