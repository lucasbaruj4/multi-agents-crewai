"""
Gemini LLM Configuration Module
==============================

Optimized Gemini LLM configuration for minimal API usage with CrewAI.
"""

import os
from crewai import LLM


def create_gemini_llm(temperature: float = 0.3, max_tokens: int = 300) -> LLM:
    """
    Create an optimized Gemini LLM for minimal API usage
    
    Args:
        temperature: Sampling temperature (lower = more focused)
        max_tokens: Maximum tokens to generate (strict limit for cost control)
        
    Returns:
        Configured Gemini LLM instance
    """
    # Ensure API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    return LLM(
        model="gemini/gemini-2.0-flash-lite",  # Most cost-efficient model
        api_key=api_key,  # Explicitly pass API key
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=60,  # Shorter timeout for faster responses
        drop_params=True,  # Drop unnecessary parameters to reduce complexity
        additional_drop_params=["stop", "frequency_penalty", "presence_penalty"]
    )


def create_gemini_llm_strict() -> LLM:
    """
    Create ultra-strict Gemini LLM for minimal usage (150 tokens max)
    """
    return create_gemini_llm(temperature=0.1, max_tokens=150)


def create_gemini_llm_standard() -> LLM:
    """
    Create standard Gemini LLM for balanced usage (300 tokens max)
    """
    return create_gemini_llm(temperature=0.3, max_tokens=300) 