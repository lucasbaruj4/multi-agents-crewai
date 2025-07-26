"""
Connection Credentials Configuration
==================================

This file centralizes all connection URLs and credentials for the Multi-Agent System.
This approach replaces the need for .env.local files and makes the project open-source ready.

For future use with more powerful models, you can:
1. Create a .env.local file with your specific URLs
2. Update this file to read from environment variables
3. Keep this file in .gitignore for sensitive credentials

Current setup uses localtunnel for Colab connection.
"""

# =============================================================================
# COLAB MISTRAL SERVER CONNECTION
# =============================================================================

# Primary Colab Mistral Server URL (localtunnel)
COLAB_MISTRAL_URL = "https://mistral-server.loca.lt"

# Alternative URLs (for backup or different models)
# COLAB_MISTRAL_URL_BACKUP = "https://your-backup-subdomain.loca.lt"
# COLAB_MISTRAL_URL_DEV = "https://your-dev-subdomain.loca.lt"

# =============================================================================
# API ENDPOINTS
# =============================================================================

# Health check endpoint
HEALTH_ENDPOINT = f"{COLAB_MISTRAL_URL}/health"

# Text generation endpoint
GENERATE_ENDPOINT = f"{COLAB_MISTRAL_URL}/generate"

# Model information endpoint
MODEL_INFO_ENDPOINT = f"{COLAB_MISTRAL_URL}/model_info"

# OpenAI-compatible endpoints for CrewAI integration
OPENAI_BASE_URL = f"{COLAB_MISTRAL_URL}/v1"
OPENAI_CHAT_COMPLETIONS_ENDPOINT = f"{COLAB_MISTRAL_URL}/v1/chat/completions"
OPENAI_COMPLETIONS_ENDPOINT = f"{COLAB_MISTRAL_URL}/v1/completions"

# =============================================================================
# CONNECTION HEADERS
# =============================================================================

# Headers required for localtunnel connection
LOCALTUNNEL_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'bypass-tunnel-reminder': 'true',
    'Content-Type': 'application/json'
}

# =============================================================================
# CONNECTION SETTINGS
# =============================================================================

# Timeout settings (in seconds)
DEFAULT_TIMEOUT = 60
HEALTH_CHECK_TIMEOUT = 10
GENERATION_TIMEOUT = 30

# Default generation parameters
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.5

# =============================================================================
# FUTURE EXPANSION
# =============================================================================

# For future use with environment variables:
# import os
# COLAB_MISTRAL_URL = os.getenv('COLAB_MISTRAL_URL', "https://mistral-server.loca.lt")
# 
# For multiple model support:
# MISTRAL_7B_URL = os.getenv('MISTRAL_7B_URL', "https://mistral-7b.loca.lt")
# MISTRAL_LARGE_URL = os.getenv('MISTRAL_LARGE_URL', "https://mistral-large.loca.lt")
# CLAUDE_URL = os.getenv('CLAUDE_URL', "https://claude-api.loca.lt")

# =============================================================================
# VALIDATION
# =============================================================================

def validate_connection_url():
    """Validate that the connection URL is properly formatted"""
    if not COLAB_MISTRAL_URL.startswith("https://"):
        raise ValueError("COLAB_MISTRAL_URL must start with 'https://'")
    
    if "loca.lt" not in COLAB_MISTRAL_URL and "ngrok" not in COLAB_MISTRAL_URL:
        print("Warning: URL doesn't appear to be a localtunnel or ngrok URL")
    
    return True

def get_connection_info():
    """Get connection information for debugging"""
    return {
        "url": COLAB_MISTRAL_URL,
        "health_endpoint": HEALTH_ENDPOINT,
        "generate_endpoint": GENERATE_ENDPOINT,
        "model_info_endpoint": MODEL_INFO_ENDPOINT,
        "headers": LOCALTUNNEL_HEADERS,
        "timeouts": {
            "default": DEFAULT_TIMEOUT,
            "health": HEALTH_CHECK_TIMEOUT,
            "generation": GENERATION_TIMEOUT
        }
    }

# Validate on import
if __name__ == "__main__":
    try:
        validate_connection_url()
        print("✅ Connection credentials validated successfully!")
        print(f"🔗 Server URL: {COLAB_MISTRAL_URL}")
        print(f"🏥 Health endpoint: {HEALTH_ENDPOINT}")
        print(f"🤖 Generate endpoint: {GENERATE_ENDPOINT}")
    except Exception as e:
        print(f"❌ Connection validation failed: {e}")
else:
    # Validate when imported
    validate_connection_url() 