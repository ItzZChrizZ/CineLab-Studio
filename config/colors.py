"""
CineLab Suite - Color System
Unified color palette for dark/light themes
"""

# Dark Theme Colors
DARK_THEME = {
    "background": "#222121",
    "background_secondary": "#161b22",
    "text_primary": "#F9FEFF",
    "text_secondary": "#CCD4D7",
    "accent": "#F7BE14",
    "border": "#30363d",
    "slider": "#CCD4D7"
}

# Light Theme Colors
LIGHT_THEME = {
    "background": "#F9FEFF",
    "background_secondary": "#FFFFFF",
    "text_primary": "#222121",
    "text_secondary": "#666666",
    "accent": "#CCD4D7",
    "border": "#e0e0e0",
    "slider": "#F7BE14"
}

def get_theme_css():
    """Returns complete CSS for both themes with animated gradient"""
    return f"""
    <style>
    /* Global Styles */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}
    
    /* Dark Theme (Default) - Animated Gradient */
    .stApp {{
        background: linear-gradient(270deg, #1a1a1a, #2d2d2d, #222121, #1a1a1a);
        background-size: 800% 800%;
        animation: gradientShift 15s ease infinite;
        color: {DARK_THEME['text_primary']};
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Page Headers */
    .page-header {{
        color: {DARK_THEME['text_secondary']};
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 1.1rem;
        border-left: 5px solid {DARK_THEME['accent']};
        padding-left: 15px;
        margin-bottom: 25px;
    }}
    
    /* Section Headers */
    h3 {{
        border-bottom: 1px solid {DARK_THEME['border']};
        padding-bottom: 4px;
        color: {DARK_THEME['text_secondary']} !important;
        text-transform: uppercase;
        font-size: 0.9rem;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {DARK_THEME['accent']};
        color: {DARK_THEME['background']};
        font-weight: 800;
        width: 100%;
        text-transform: uppercase;
        height: 3.2em;
        border: none;
        border-radius: 6px;
        letter-spacing: 1px;
    }}
    
    .stButton > button:hover {{
        opacity: 0.9;
    }}
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea {{
        background-color: {DARK_THEME['background_secondary']};
        color: {DARK_THEME['text_primary']};
        border: 1px solid {DARK_THEME['border']};
        border-radius: 6px;
    }}
    
    /* Select Boxes */
    .stSelectbox select {{
        background-color: {DARK_THEME['background_secondary']};
        color: {DARK_THEME['text_primary']};
        border: 1px solid {DARK_THEME['border']};
    }}
    
    /* Info Boxes */
    .info-box {{
        background-color: {DARK_THEME['background_secondary']};
        border: 1px solid {DARK_THEME['border']};
        padding: 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        color: #a3a3a3;
        margin-top: 5px;
        line-height: 1.5;
    }}
    
    /* Light Theme Override - Animated Gradient */
    @media (prefers-color-scheme: light) {{
        .stApp {{
            background: linear-gradient(270deg, #f5f5f5, #ffffff, #fafafa, #f5f5f5);
            background-size: 800% 800%;
            animation: gradientShift 15s ease infinite;
            color: {LIGHT_THEME['text_primary']};
        }}
        
        .page-header, h3 {{
            color: {LIGHT_THEME['text_primary']} !important;
            border-color: {LIGHT_THEME['border']};
        }}
        
        .page-header {{
            border-left-color: {LIGHT_THEME['slider']};
        }}
        
        .stButton > button {{
            background-color: {LIGHT_THEME['slider']};
            color: {LIGHT_THEME['background']};
        }}
        
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            background-color: {LIGHT_THEME['background_secondary']};
            color: {LIGHT_THEME['text_primary']};
            border-color: {LIGHT_THEME['border']};
        }}
        
        .info-box {{
            background-color: {LIGHT_THEME['background_secondary']};
            border-color: {LIGHT_THEME['border']};
            color: {LIGHT_THEME['text_secondary']};
        }}
    }}
    </style>
    """
