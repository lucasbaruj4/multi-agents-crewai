"""
Local Mistral Client for Colab Integration
=========================================

Client for connecting to Colab-hosted Mistral model via HTTP API.
"""

import requests
import json
import time
from typing import Optional, Dict, Any
from config.connection_credentials import (
    COLAB_MISTRAL_URL,
    HEALTH_ENDPOINT,
    GENERATE_ENDPOINT,
    MODEL_INFO_ENDPOINT,
    LOCALTUNNEL_HEADERS,
    DEFAULT_TIMEOUT,
    HEALTH_CHECK_TIMEOUT,
    GENERATION_TIMEOUT,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE
)

class ColabMistralClient:
    def __init__(self, colab_url: str = None):
        """
         Initialize the client
         
         Args:
             colab_url: Optional URL override (uses connection_credentials.py by default)
         """
        self.base_url = COLAB_MISTRAL_URL if colab_url is None else colab_url
        self.session = requests.Session()
        # Set default headers for all requests
        self.session.headers.update(LOCALTUNNEL_HEADERS)
        
    def health_check(self) -> Dict[str, Any]:
        """Check if the API server is healthy"""
        try:
            response = self.session.get(HEALTH_ENDPOINT, timeout=HEALTH_CHECK_TIMEOUT)
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def generate_text(self, prompt: str, max_tokens: int = None, temperature: float = None) -> Dict[str, Any]:
        """
         Generate text using the remote Mistral model
         
         Args:
             prompt: The input prompt
             max_tokens: Maximum tokens to generate (uses DEFAULT_MAX_TOKENS if None)
             temperature: Sampling temperature (uses DEFAULT_TEMPERATURE if None)
                 
         Returns:
             Dictionary with response and metadata
         """
        try:
            # Use defaults from connection_credentials if not provided
            max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
            temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
            
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.session.post(
                GENERATE_ENDPOINT,
                json=payload,
                timeout=GENERATION_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        try:
            response = self.session.get(MODEL_INFO_ENDPOINT, timeout=HEALTH_CHECK_TIMEOUT)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize client (uses connection_credentials.py by default)
    client = ColabMistralClient()
    
    # Check health
    health = client.health_check()
    print(f"Health check: {health}")
    
    # Test generation
    result = client.generate_text("Hello, how are you?")
    print(f"Generation result: {result}") 