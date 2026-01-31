"""
CineLab Prompt Generator - Version 1
Original DP Logic for cinematography recipe generation
"""

def generate_prompt(params, img_data):
    """
    Generate CineLab cinematography recipe
    
    Args:
        params: dict with cam, lens, f_stop, iso, ratio, artist, category, scenario, light_details, notes
        img_data: reference image data
    
    Returns:
        dict with system_instruction, user_prompt, safety_settings, generation_config
    """
    
    # Location logic based on Studio/Outdoor
    if params['category'] == "Studio":
        location_logic = """
        LOCATION SWITCH: 100% EMPTY STUDIO. 
        - REMOVE the reference image background completely.
        - Use a neutral, minimalist, empty CYCLORAMA WALL as the background.
        - Ensure the subject remains centered and in the same pose.
        """
    else:
        location_logic = "LOCATION KEEP: Maintain the exact outdoor environment and location from the reference image."
    
    # Build DP instructions
    dp_instructions = f"""
    ROLE: Professional Director of Photography (DP).
    OBJECTIVE: Create a '4x4' (Dört Dörtlük) FLAWLESS and comprehensive cinematography recipe.

    PHASE 1: SUBJECT RETENTION & GENDER LOCK (80% Weight)
    - **GENDER LOCK**: You MUST maintain the exact GENDER and IDENTITY of the person in the reference image. If it's a woman, keep her as a woman. Do not change sex based on clothing style.
    - Perform a '4x4' analysis: Describe the subject in 4 categories (Anatomy, Pose, Outfit, Identity) with 4 high-fidelity descriptors each.
    - Recreate the subject's exact facial features, skin tone, and clothing with absolute precision.
    - {location_logic}

    PHASE 2: TECHNICAL OVERRIDE (Mandatory)
    - Body: {params['cam']} -> {params['cam_info']}
    - Lens: {params['lens']} -> {params['lens_info']}
    - Aperture: {params['f_stop']} | ISO: {params['iso']} | Ratio: {params['ratio']}
    - Apply the specific optical character and sensor DNA of this equipment. Discard metadata from the source image.

    PHASE 3: ARTISTIC DNA (20% Weight)
    - Artist: '{params['artist']}'. Infuse their specific color science, film grain, and texture.

    PHASE 4: LIGHTING PHYSICS
    - Setup: {params['scenario']}
    - Precise Physical Specs: {params['light_details']}
    - Director's Notes: {params['notes']}
    
    OUTPUT: Provide ONLY raw, valid JSON.
    """
    
    system_instruction = "Act as a technical Director of Photography. Focus on light physics and professional cinematography."
    
    safety = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    return {
        "system_instruction": system_instruction,
        "user_prompt": dp_instructions,
        "safety_settings": safety,
        "generation_config": {
            "response_mime_type": "application/json",
            "temperature": 0.1
        }
    }
