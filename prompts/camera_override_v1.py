"""
Camera Override Prompt Generator - Version 1
Generates multi-angle architectural visualization prompts
"""

import json

def generate_prompt(params, img_data, library):
    """
    Generate Camera Override JSON prompt
    
    Args:
        params: dict with camera_angle, shot_scale, lens, aspect_ratio
        img_data: reference image data
        library: camera_override_library.json loaded data
    
    Returns:
        JSON string with camera override protocol
    """
    
    # Extract selections
    angle_key = params['camera_angle']
    scale_key = params['shot_scale']
    lens_key = params['lens']
    ratio = params['aspect_ratio']
    
    # Get detailed descriptions from library
    angle_desc = library['camera_angles'][angle_key]['prompt_text']
    scale_desc = library['shot_scales'][scale_key]['prompt_text']
    lens_desc = library['lenses'][lens_key]['prompt_text']
    
    # Build system instruction
    system_instruction = """
    ROLE: Professional Architectural Photographer with expertise in multi-angle documentation.
    
    OBJECTIVE: Analyze the reference architectural image and generate a precise camera override protocol 
    that will recreate the EXACT SAME building/structure from a different camera position and framing.
    
    CRITICAL RULES:
    1. BUILDING IDENTITY: The structure's design, materials, colors, and architectural character MUST remain 100% identical
    2. CONSISTENCY ANCHORS: Extract and preserve key identifying features (materials, textures, colors, proportions)
    3. SPATIAL UNDERSTANDING: Understand the 3D form to accurately predict how it appears from the new angle
    4. NO HALLUCINATION: Do not invent architectural features not present in the reference
    5. TECHNICAL ACCURACY: Apply the specified camera angle, framing, and lens characteristics precisely
    """
    
    # Build user prompt
    user_prompt = f"""
    REFERENCE IMAGE ANALYSIS TASK:
    You are viewing an architectural photograph. Your task is to generate a camera override protocol 
    that will recreate this EXACT structure from a different viewpoint.
    
    NEW CAMERA SPECIFICATIONS:
    
    1. CAMERA ANGLE OVERRIDE:
    {angle_desc}
    
    2. SHOT SCALE/FRAMING:
    {scale_desc}
    
    3. LENS OPTICAL CHARACTER:
    {lens_desc}
    
    4. ASPECT RATIO: {ratio}
    
    REQUIRED OUTPUT STRUCTURE (JSON):
    {{
      "camera_override_protocol": "Explicit command describing how the camera position changes from the reference to achieve the new angle. Be specific about vertical/horizontal movement and rotation.",
      
      "volumetric_reconstruction": "Detailed description of how the building's 3D form will appear from the new angle. Explain foreshortening, perspective effects, what surfaces become visible/hidden, and how spatial relationships change.",
      
      "consistency_anchors": "List of specific architectural features that MUST remain identical: exact materials (name them), colors (describe them), textures (specify them), proportions, ornamental details, window patterns, structural elements. Be extremely specific.",
      
      "framing_boundaries": "Precise description of what should be included in the frame based on the shot scale. Specify foreground, subject, and background elements. Define edges of the composition.",
      
      "optical_physics": "Explanation of how the specified lens will render the scene: perspective compression/expansion, distortion characteristics, depth of field effects, and how parallel lines will behave.",
      
      "final_technical_prompt": "A complete, production-ready technical prompt that synthesizes all above elements into clear shooting instructions. This should read like a professional architectural photography brief."
    }}
    
    CONSISTENCY REMINDER: The building's architectural identity must be preserved with 90-95% fidelity. 
    Only the camera position, framing, and optical rendering change - NOT the building design itself.
    """
    
    # Safety settings
    safety = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    return {
        "system_instruction": system_instruction,
        "user_prompt": user_prompt,
        "safety_settings": safety,
        "generation_config": {
            "response_mime_type": "application/json",
            "temperature": 0.1  # Low temperature for consistency
        }
    }
