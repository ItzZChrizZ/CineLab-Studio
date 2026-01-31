"""
Product Studio Prompt Generator - Version 1
Transform product photos into different contexts
"""

def generate_prompt(params, img_data, library):
    """
    Generate Product Studio prompt
    
    Args:
        params: dict with user_text, photographer (optional)
        img_data: reference product image data
        library: cinelab_library.json (for photographer styles)
    
    Returns:
        dict with system_instruction, user_prompt, safety_settings, generation_config
    """
    
    user_text = params['user_text']
    photographer = params.get('photographer', None)
    
    # Build photographer style injection if selected
    photographer_style = ""
    if photographer and photographer in library.get('photographers', {}).get('Fashion', {}):
        photo_info = library['photographers']['Fashion'][photographer]
        photographer_style = f"""
        
        ARTISTIC STYLE APPLICATION:
        Apply {photographer}'s visual DNA:
        - Style: {photo_info['style']}
        - Lighting approach: {photo_info['lighting']}
        - Overall vibe: {photo_info['vibe']}
        
        Translate these characteristics into the product photography context while maintaining 
        product accuracy and commercial viability.
        """
    
    system_instruction = """
    ROLE: Professional Product Photographer specializing in context transformation and commercial imagery.
    
    OBJECTIVE: Analyze the reference product image and generate a photorealistic prompt that places 
    the EXACT SAME product into a new context as specified by the user, while maintaining 100% 
    product accuracy and identity.
    
    CRITICAL RULES:
    1. PRODUCT IDENTITY: The product's design, colors, materials, size, and details MUST remain 100% identical
    2. NO DESIGN CHANGES: Do not modify product design, add features, or alter proportions
    3. CONTEXT TRANSFORMATION: Change only the setting, lighting, and presentation style
    4. PHOTOREALISM: Generate commercial-quality, realistic product photography
    5. CONSISTENCY: Maintain exact product specifications while adapting context
    """
    
    user_prompt = f"""
    REFERENCE PRODUCT ANALYSIS TASK:
    You are viewing a product photograph. Your task is to generate a prompt that will recreate 
    this EXACT product in a new context.
    
    USER'S CONTEXT REQUEST:
    "{user_text}"
    
    {photographer_style}
    
    REQUIRED PROMPT STRUCTURE:
    Generate a single, comprehensive prompt (not JSON) that includes:
    
    1. PRODUCT IDENTIFICATION (First Priority):
       - Exact description of the product type
       - Precise color description (use specific color names, not just "blue" but "translucent bright aqua blue")
       - Material specifications (gold, silver, leather, fabric, etc.)
       - Size and scale indicators
       - Surface finish (matte, glossy, textured, polished)
       - Any logos, patterns, or distinctive features
    
    2. CONTEXT TRANSFORMATION:
       - Interpret the user's request literally but professionally
       - Describe the new setting/context clearly
       - Specify how the product is positioned/displayed in this context
       - Maintain product as the focal point
    
    3. TECHNICAL PHOTOGRAPHY SPECS:
       - Specify shot type (macro, close-up, etc.)
       - Lighting setup (soft, diffused, studio, natural)
       - Depth of field requirements
       - Background treatment
       - Camera angle and perspective
    
    4. QUALITY STANDARDS:
       - "Ultra realistic product photography"
       - "Photorealistic, high detail"
       - "Commercial photography quality"
       - "Professional product shoot"
    
    5. CONSISTENCY ENFORCEMENT:
       - End with: "The product must be 1:1 identical to the reference image, no design changes, 
         no color shifts, no scaling differences, no artistic reinterpretation."
    
    EXAMPLE OUTPUT FORMAT:
    "Ultra realistic product photography of [exact product description with all details] 
    [context transformation]. [Technical specs]. [Lighting]. [Background]. The product must 
    be 1:1 identical to the reference image, no design changes."
    
    Generate the prompt now, ensuring product accuracy is the absolute top priority.
    """
    
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
            "response_mime_type": "text/plain",  # NOT JSON, just text prompt
            "temperature": 0.2  # Slightly higher for creative context adaptation
        }
    }
