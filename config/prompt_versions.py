"""
CineLab Suite - Prompt Version Management
Control which prompt/logic version is active for each tool
"""

# Active Prompt Versions
ACTIVE_PROMPTS = {
    "cinelab": "cinelab_v1",
    "camera_override": "camera_override_v1",
    "product_studio": "product_studio_v1"
}

# Active Logic Versions
ACTIVE_LOGIC = {
    "fine_art_nude": "fine_art_nude_v1",
    "factory_bridge": "factory_bridge_v1"
}

def get_prompt_version(tool_name):
    """Get active prompt version for tool"""
    return ACTIVE_PROMPTS.get(tool_name, f"{tool_name}_v1")

def get_logic_version(logic_name):
    """Get active logic version"""
    return ACTIVE_LOGIC.get(logic_name, f"{logic_name}_v1")
