"""
Unified Navigation Bar Component
Used across all pages for consistent navigation
"""

import streamlit as st

def render_navbar(current_page=None):
    """
    Render navigation bar
    
    Args:
        current_page: Optional string to highlight current page
    """
    
    # Hide Streamlit header
    st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Navbar HTML
    navbar_html = f"""
    <style>
    .cinelab-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 2rem;
        background-color: rgba(34, 33, 33, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(48, 54, 61, 0.5);
        position: sticky;
        top: 0;
        z-index: 1000;
    }}
    
    .cinelab-logo {{
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: 2px;
        color: #F9FEFF;
        text-transform: uppercase;
        cursor: pointer;
        text-decoration: none;
    }}
    
    .cinelab-logo:hover {{
        color: #F7BE14;
        transition: color 0.3s ease;
    }}
    
    .cinelab-nav-links {{
        display: flex;
        gap: 2rem;
        align-items: center;
    }}
    
    .cinelab-nav-link {{
        color: #CCD4D7;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    }}
    
    .cinelab-nav-link:hover {{
        color: #F7BE14;
        background-color: rgba(247, 190, 20, 0.1);
    }}
    
    .cinelab-nav-link.active {{
        color: #F7BE14;
        font-weight: 700;
    }}
    
    /* Light theme */
    @media (prefers-color-scheme: light) {{
        .cinelab-navbar {{
            background-color: rgba(249, 254, 255, 0.95);
            border-bottom-color: rgba(224, 224, 224, 0.5);
        }}
        
        .cinelab-logo {{
            color: #222121;
        }}
        
        .cinelab-logo:hover {{
            color: #F7BE14;
        }}
        
        .cinelab-nav-link {{
            color: #666666;
        }}
        
        .cinelab-nav-link:hover {{
            color: #F7BE14;
        }}
        
        .cinelab-nav-link.active {{
            color: #F7BE14;
        }}
    }}
    </style>
    
    <div class="cinelab-navbar">
        <a href="/" target="_self" class="cinelab-logo">CineLab</a>
        <div class="cinelab-nav-links">
            <a href="/1_🎨_Prompt_Generator" target="_self" class="cinelab-nav-link {'active' if current_page == 'prompt_generator' else ''}">Prompt Generator</a>
            <a href="/2_🏭_Factory" target="_self" class="cinelab-nav-link {'active' if current_page == 'factory' else ''}">Factory</a>
            <a href="/3_📐_Camera_Override" target="_self" class="cinelab-nav-link {'active' if current_page == 'camera_override' else ''}">Camera Override</a>
            <a href="/4_💎_Product_Studio" target="_self" class="cinelab-nav-link {'active' if current_page == 'product_studio' else ''}">Product Studio</a>
            <a href="https://github.com/ItzZChrizZ" target="_blank" class="cinelab-nav-link">GitHub</a>
        </div>
    </div>
    """
    
    st.markdown(navbar_html, unsafe_allow_html=True)
