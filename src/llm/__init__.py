"""
LLM Integration Package
======================

This package contains LLM integration components for the multi-agent system.
Supports multiple providers with automatic detection and seamless switching.
"""

# Import the new unified model configuration system
from .model_config import (
    ModelConfig,
    create_llm,
    create_strict_llm,
    create_standard_llm
)

# Backward compatibility imports
from .model_config import (
    create_gemini_llm,
    create_gemini_llm_strict,
    create_gemini_llm_standard
)

__all__ = [
    # New unified system (recommended)
    'ModelConfig',
    'create_llm',
    'create_strict_llm',
    'create_standard_llm',
    
    # Backward compatibility
    'create_gemini_llm',
    'create_gemini_llm_strict',
    'create_gemini_llm_standard'
] 