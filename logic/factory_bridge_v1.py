"""
Factory Bridge Logic - Version 1
Prepares different prompt formats for image generation
"""

import json

def prepare_for_generation(raw_input):
    """
    Analyze input and prepare it for Gemini image generation
    
    Args:
        raw_input: String input (could be JSON or plain text)
    
    Returns:
        Final prompt string ready for image generation
    """
    
    try:
        # Try to parse as JSON
        data = json.loads(raw_input)
        
        # Detect format type and route to appropriate handler
        if "cinematography_recipe" in data:
            return handle_cinelab_format(data)
        elif "camera_override_protocol" in data:
            return handle_camera_override_format(data)
        else:
            # Unknown JSON format, return as-is stringified
            return json.dumps(data)
    
    except json.JSONDecodeError:
        # Not JSON, assume it's a plain text prompt (Product Studio)
        return handle_plain_text_format(raw_input)

def handle_cinelab_format(data):
    """
    Process CineLab cinematography recipe JSON
    Original Factory logic bridge
    """
    
    recipe = data.get("cinematography_recipe", {})
    lp = recipe.get("phase_4_lighting_physics", {})
    
    # Equipment terminology replacement
    for key in ["key_light", "fill_light", "back_light", "setup"]:
        if key in lp:
            lp[key] = lp[key].lower().replace("softbox", "diffused volumetric light source") \
                                     .replace("bounce board", "indirect fill reflection") \
                                     .replace("light stand", "invisible point source") \
                                     .replace("setup", "lighting physics")
    
    # Framing rules
    framing_rules = """
    - SHOT TYPE: Extreme Wide Shot (EWS).
    - COMPOSITION: The subject must occupy roughly 60-70% of the vertical frame height.
    - HEADROOM & FOOTROOM: Leave clear empty grey space above the head and below the shoes.
    - NO CROPPING: Full body visible, centered against the seamless cyc wall.
    """
    
    # Pose correction logic
    phase1 = recipe.get("phase_1_subject_retention", {})
    location = phase1.get("environment_override", {}).get("location", "").lower()
    notes = lp.get("director_notes", "").lower()
    original_pose_details = ", ".join(phase1.get("four_by_four_analysis", {}).get("pose", []))
    
    pose_rules = ""
    if "studio" in location and "leaning" in original_pose_details.lower():
        if not any(word in notes for word in ["chair", "car", "table", "wall", "prop", "object", "block"]):
            pose_rules = f"""
            - POSE CORRECTION (PHYSICS): The subject cannot 'lean' against air.
            - NEW DIRECTION: Convert the 'leaning' pose into a strong, self-supporting HIGH-FASHION STANDING stance. Do not be robotic.
            - CRITICAL RETENTION: You MUST maintain these specific stylistic details from the original request while standing: "Hands tucked in pockets", "Slightly tilted head", "stoic gaze".
            - NO FURNITURE: No blocks, no props. Just the subject standing confidently.
            """
    
    # Build final prompt
    refined_prompt = f"""
    ACT AS: Professional Fashion Director of Photography (Kacper Kasprzyk style).
    
    {json.dumps(data)}
    
    STRICT EXECUTION DIRECTIVES:
    {framing_rules}
    {pose_rules}
    - RENDER RULE: 100% Invisible studio equipment. Only render the light effect.
    - ATMOSPHERE: High-end, minimalist, moody editorial feel.
    """
    
    return refined_prompt

def handle_camera_override_format(data):
    """
    Process Camera Override JSON format
    Extracts the final_technical_prompt and adds architectural rendering rules
    """
    
    # Get the final technical prompt
    final_prompt = data.get("final_technical_prompt", "")
    
    # Add architectural rendering directives
    rendering_rules = """
    
    ARCHITECTURAL RENDERING DIRECTIVES:
    - BUILDING CONSISTENCY: Maintain 90-95% fidelity to the reference architecture
    - MATERIAL ACCURACY: Preserve exact materials, textures, and colors
    - NO HALLUCINATION: Do not invent architectural features not present in reference
    - LIGHTING REALISM: Use natural, physically accurate lighting for the time of day
    - CONTEXT APPROPRIATE: Include appropriate environmental context (sky, landscape, urban fabric)
    - TECHNICAL PRECISION: Apply camera angle and lens characteristics as specified
    """
    
    # Combine with consistency anchors for emphasis
    consistency = data.get("consistency_anchors", "")
    if consistency:
        consistency_emphasis = f"\n\nCRITICAL CONSISTENCY REQUIREMENTS:\n{consistency}"
    else:
        consistency_emphasis = ""
    
    refined_prompt = f"{final_prompt}{rendering_rules}{consistency_emphasis}"
    
    return refined_prompt

def handle_plain_text_format(text):
    """
    Process plain text prompts (Product Studio)
    These are already formatted, just return as-is
    """
    return text
