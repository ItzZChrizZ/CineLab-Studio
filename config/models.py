"""
CineLab Suite - Model & API Configuration
Manage model versions and API keys
"""

# Model Assignments
MODELS = {
    "cinelab": "gemini-2.0-flash-exp",           # API 1 - Prompt generation
    "camera_override": "gemini-2.0-flash-exp",   # API 1 - Prompt generation
    "product_studio": "gemini-2.0-flash-exp",    # API 1 - Prompt generation
    "factory": "gemini-2.0-flash-thinking-exp"   # API 2 - Image generation
}

# API Key Mapping (from Streamlit secrets)
API_KEYS = {
    "api_1": "CINELAB_API_KEY",      # For prompt generation tools
    "api_2": "FACTORY_API_KEY"       # For image generation
}

# Tool to API Mapping
TOOL_API_MAP = {
    "cinelab": "api_1",
    "camera_override": "api_1",
    "product_studio": "api_1",
    "factory": "api_2"
}

def get_model(tool_name):
    """Get model for specific tool"""
    return MODELS.get(tool_name, "gemini-2.0-flash-exp")

def get_api_key_name(tool_name):
    """Get API key secret name for specific tool"""
    api = TOOL_API_MAP.get(tool_name, "api_1")
    return API_KEYS[api]
