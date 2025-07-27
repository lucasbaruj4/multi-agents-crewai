"""
Unified Model Configuration Module
=================================

Smart model selection system that automatically detects and configures
different LLM providers based on environment variables for seamless
model switching.
"""

import os
from typing import Dict, Any, Optional
from crewai import LLM


class ModelConfig:
    """
    Unified model configuration system for seamless model switching.
    
    Automatically detects available API keys and configures the appropriate
    model provider. Supports multiple providers with fallback options.
    """
    
    # Model configurations for different providers
    MODEL_CONFIGS = {
        # Google Gemini Models
        'gemini': {
            'models': {
                'gemini-2.0-flash-lite': {
                    'model_name': 'gemini/gemini-2.0-flash-lite',
                    'temperature': 0.3,
                    'max_tokens': 300,
                    'timeout': 60,
                    'cost_efficiency': 'high'
                },
                'gemini-2.0-flash': {
                    'model_name': 'gemini/gemini-2.0-flash',
                    'temperature': 0.3,
                    'max_tokens': 500,
                    'timeout': 60,
                    'cost_efficiency': 'medium'
                },
                'gemini-1.5-flash': {
                    'model_name': 'gemini/gemini-1.5-flash',
                    'temperature': 0.3,
                    'max_tokens': 400,
                    'timeout': 60,
                    'cost_efficiency': 'medium'
                }
            },
            'api_key_env': 'GEN_MODEL_API',
            'provider_name': 'Google Gemini'
        },
        
        # OpenAI Models
        'openai': {
            'models': {
                'gpt-4o-mini': {
                    'model_name': 'gpt-4o-mini',
                    'temperature': 0.3,
                    'max_tokens': 300,
                    'timeout': 60,
                    'cost_efficiency': 'medium'
                },
                'gpt-3.5-turbo': {
                    'model_name': 'gpt-3.5-turbo',
                    'temperature': 0.3,
                    'max_tokens': 300,
                    'timeout': 60,
                    'cost_efficiency': 'high'
                }
            },
            'api_key_env': 'OPENAI_API_KEY',
            'provider_name': 'OpenAI'
        },
        
        # Anthropic Models
        'anthropic': {
            'models': {
                'claude-3-haiku': {
                    'model_name': 'claude-3-haiku-20240307',
                    'temperature': 0.3,
                    'max_tokens': 300,
                    'timeout': 60,
                    'cost_efficiency': 'high'
                },
                'claude-3-sonnet': {
                    'model_name': 'claude-3-sonnet-20240229',
                    'temperature': 0.3,
                    'max_tokens': 400,
                    'timeout': 60,
                    'cost_efficiency': 'medium'
                }
            },
            'api_key_env': 'ANTHROPIC_API_KEY',
            'provider_name': 'Anthropic'
        },
        
        # Mistral Models (via API)
        'mistral': {
            'models': {
                'mistral-large': {
                    'model_name': 'mistral-large-latest',
                    'temperature': 0.3,
                    'max_tokens': 400,
                    'timeout': 60,
                    'cost_efficiency': 'medium'
                },
                'mistral-medium': {
                    'model_name': 'mistral-medium-latest',
                    'temperature': 0.3,
                    'max_tokens': 300,
                    'timeout': 60,
                    'cost_efficiency': 'high'
                }
            },
            'api_key_env': 'MISTRAL_API_KEY',
            'provider_name': 'Mistral AI'
        }
    }
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all available providers based on environment variables.
        
        Returns:
            Dictionary of available providers with their configurations
        """
        available = {}
        
        for provider, config in cls.MODEL_CONFIGS.items():
            api_key = os.getenv(config['api_key_env'])
            if api_key:
                available[provider] = config
                available[provider]['api_key'] = api_key
        
        return available
    
    @classmethod
    def get_default_provider(cls) -> Optional[str]:
        """
        Get the default provider (first available).
        
        Returns:
            Provider name or None if no providers available
        """
        available = cls.get_available_providers()
        return list(available.keys())[0] if available else None
    
    @classmethod
    def get_default_model(cls, provider: str) -> Optional[str]:
        """
        Get the default model for a provider (most cost-efficient).
        
        Args:
            provider: Provider name
            
        Returns:
            Model name or None if provider not available
        """
        if provider not in cls.MODEL_CONFIGS:
            return None
            
        models = cls.MODEL_CONFIGS[provider]['models']
        # Return the first model (usually most cost-efficient)
        return list(models.keys())[0] if models else None
    
    @classmethod
    def create_llm(cls, 
                  provider: Optional[str] = None,
                  model: Optional[str] = None,
                  temperature: Optional[float] = None,
                  max_tokens: Optional[int] = None,
                  timeout: Optional[int] = None) -> LLM:
        """
        Create an LLM instance with automatic provider/model selection.
        
        Args:
            provider: Provider name (auto-detected if None)
            model: Model name (auto-selected if None)
            temperature: Override temperature
            max_tokens: Override max tokens
            timeout: Override timeout
            
        Returns:
            Configured LLM instance
            
        Raises:
            ValueError: If no providers available or invalid configuration
        """
        # Auto-detect provider if not specified
        if provider is None:
            provider = cls.get_default_provider()
            if provider is None:
                raise ValueError("No LLM providers available. Please set one of: GEN_MODEL_API, OPENAI_API_KEY, ANTHROPIC_API_KEY, MISTRAL_API_KEY")
        
        # Validate provider
        if provider not in cls.MODEL_CONFIGS:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Check if provider is available
        available = cls.get_available_providers()
        if provider not in available:
            raise ValueError(f"Provider '{provider}' not available. Missing API key: {cls.MODEL_CONFIGS[provider]['api_key_env']}")
        
        # Auto-select model if not specified
        if model is None:
            model = cls.get_default_model(provider)
            if model is None:
                raise ValueError(f"No models available for provider: {provider}")
        
        # Get model configuration
        provider_config = cls.MODEL_CONFIGS[provider]
        if model not in provider_config['models']:
            raise ValueError(f"Unknown model '{model}' for provider '{provider}'")
        
        model_config = provider_config['models'][model]
        
        # Use provided values or defaults
        final_temperature = temperature if temperature is not None else model_config['temperature']
        final_max_tokens = max_tokens if max_tokens is not None else model_config['max_tokens']
        final_timeout = timeout if timeout is not None else model_config['timeout']
        
        # Create LLM instance
        return LLM(
            model=model_config['model_name'],
            api_key=available[provider]['api_key'],
            temperature=final_temperature,
            max_tokens=final_max_tokens,
            timeout=final_timeout,
            drop_params=True,
            additional_drop_params=["stop", "frequency_penalty", "presence_penalty"]
        )
    
    @classmethod
    def create_strict_llm(cls, provider: Optional[str] = None) -> LLM:
        """
        Create a strict LLM for minimal token usage.
        
        Args:
            provider: Provider name (auto-detected if None)
            
        Returns:
            Configured LLM instance with minimal token usage
        """
        return cls.create_llm(
            provider=provider,
            temperature=0.1,
            max_tokens=150
        )
    
    @classmethod
    def create_standard_llm(cls, provider: Optional[str] = None) -> LLM:
        """
        Create a standard LLM for balanced usage.
        
        Args:
            provider: Provider name (auto-detected if None)
            
        Returns:
            Configured LLM instance with standard settings
        """
        return cls.create_llm(provider=provider)
    
    @classmethod
    def get_provider_info(cls) -> Dict[str, Any]:
        """
        Get information about the current provider setup.
        
        Returns:
            Dictionary with provider information
        """
        available = cls.get_available_providers()
        default_provider = cls.get_default_provider()
        
        info = {
            'available_providers': list(available.keys()),
            'default_provider': default_provider,
            'total_providers': len(available)
        }
        
        if default_provider:
            default_model = cls.get_default_model(default_provider)
            info.update({
                'default_model': default_model,
                'provider_name': cls.MODEL_CONFIGS[default_provider]['provider_name'],
                'cost_efficiency': cls.MODEL_CONFIGS[default_provider]['models'][default_model]['cost_efficiency']
            })
        
        return info


# Convenience functions for backward compatibility
def create_gemini_llm(temperature: float = 0.3, max_tokens: int = 300) -> LLM:
    """Create Gemini LLM (backward compatibility)"""
    return ModelConfig.create_llm(provider='gemini', temperature=temperature, max_tokens=max_tokens)


def create_gemini_llm_strict() -> LLM:
    """Create strict Gemini LLM (backward compatibility)"""
    return ModelConfig.create_strict_llm(provider='gemini')


def create_gemini_llm_standard() -> LLM:
    """Create standard Gemini LLM (backward compatibility)"""
    return ModelConfig.create_standard_llm(provider='gemini')


# New unified functions
def create_llm(temperature: float = 0.3, max_tokens: int = 300) -> LLM:
    """Create LLM with auto-detection (recommended)"""
    return ModelConfig.create_llm(temperature=temperature, max_tokens=max_tokens)


def create_strict_llm() -> LLM:
    """Create strict LLM with auto-detection (recommended)"""
    return ModelConfig.create_strict_llm()


def create_standard_llm() -> LLM:
    """Create standard LLM with auto-detection (recommended)"""
    return ModelConfig.create_standard_llm() 