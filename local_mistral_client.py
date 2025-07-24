"""
Local Client for Colab Mistral API
Use this locally to connect to your Colab-hosted Mistral model
"""

import requests
import json
import time
from typing import Optional, Dict, Any

class ColabMistralClient:
    def __init__(self, colab_url: str):
        """
        Initialize the client
        
        Args:
            colab_url: The URL of your Colab notebook (e.g., 'https://colab.research.google.com/drive/...')
        """
        self.base_url = self._extract_api_url(colab_url)
        self.session = requests.Session()
        
    def _extract_api_url(self, colab_url: str) -> str:
        """
        Extract the API URL from Colab notebook URL
        Updated with localtunnel URL
        """
        # Updated with the actual localtunnel URL
        return "https://mistral-server.loca.lt"
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API server is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def generate_text(self, prompt: str, max_tokens: int = 512, temperature: float = 0.5) -> Dict[str, Any]:
        """
        Generate text using the remote Mistral model
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.session.post(
                f"{self.base_url}/generate",
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}", "details": response.text}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        try:
            response = self.session.get(f"{self.base_url}/model_info")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = ColabMistralClient("your_colab_url_here")
    
    # Check health
    health = client.health_check()
    print("Health check:", health)
    
    # Generate text
    if health.get("status") == "healthy":
        result = client.generate_text(
            prompt="Explain the benefits of multi-agent systems in business intelligence.",
            max_tokens=256,
            temperature=0.3
        )
        print("Generated text:", result)
    else:
        print("Server is not healthy. Please check your Colab setup.") 