"""
Configuration Package
====================

Centralized configuration and credentials management.
"""

from .connection_credentials import (
    COLAB_MISTRAL_URL,
    HEALTH_ENDPOINT,
    GENERATE_ENDPOINT,
    MODEL_INFO_ENDPOINT,
    LOCALTUNNEL_HEADERS,
    DEFAULT_TIMEOUT,
    HEALTH_CHECK_TIMEOUT,
    GENERATION_TIMEOUT,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    validate_connection_url,
    get_connection_info
)

__all__ = [
    'COLAB_MISTRAL_URL',
    'HEALTH_ENDPOINT',
    'GENERATE_ENDPOINT',
    'MODEL_INFO_ENDPOINT',
    'LOCALTUNNEL_HEADERS',
    'DEFAULT_TIMEOUT',
    'HEALTH_CHECK_TIMEOUT',
    'GENERATION_TIMEOUT',
    'DEFAULT_MAX_TOKENS',
    'DEFAULT_TEMPERATURE',
    'validate_connection_url',
    'get_connection_info'
] 