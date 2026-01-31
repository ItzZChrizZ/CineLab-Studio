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
    
    /* Navbar Container */
    .cinelab-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 2rem;
        background-color: rgba(34, 33, 33, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(48, 54, 61, 0.3);
        margin-bottom: 2rem;
    }
    
    .cinelab-logo {
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 2px;
        color: #F9FEFF;
        text-transform: uppercase;
    }
    
    .cinelab-nav-links {
        display: flex;
        gap: 2.5rem;
        align-items: center;
    }
    
    /* Streamlit button styling override for navbar */
    .cinelab-nav-links .stButton > button {
        background-color: transparent !important;
        color: #F9FEFF !important;
        border: none !important;
        padding: 0.3rem 0 !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        height: auto !important;
        margin: 0 !important;
    }
    
    .cinelab-nav-links .stButton > button:hover {
        background-color: transparent !important;
        border-bottom-color: transparent !important;
    }
    
    /* Active state - handled by page parameter */
    
    /* Light theme */
    @media (prefers-color-scheme: light) {
        .cinelab-navbar {
            background-color: rgba(249, 254, 255, 0.95);
            border-bottom-color: rgba(224, 224, 224, 0.5);
        }
        
        .cinelab-logo {
            color: #222121;
        }
        
        .cinelab-nav-links .stButton > button {
            color: #222121 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navbar layout
    col_logo, col_spacer, col_nav = st.columns([1, 3, 8])
    
    with col_logo:
        if st.button("CINELAB", key="nav_home", help="Go to home"):
            st.switch_page("app.py")
    
    with col_nav:
        nav_cols = st.columns(4)
        
        with nav_cols[0]:
            # Prompt Generator
            label = "PROMPT GENERATOR"
            if current_page == 'prompt_generator':
                st.markdown(f'<span style="color: #F7BE14; border-bottom: 2px solid #F7BE14; padding-bottom: 0.3rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;">{label}</span>', unsafe_allow_html=True)
            else:
                if st.button(label, key="nav_prompt"):
                    st.switch_page("pages/1_🎨_Prompt_Generator.py")
        
        with nav_cols[1]:
            # Factory
            label = "FACTORY"
            if current_page == 'factory':
                st.markdown(f'<span style="color: #F7BE14; border-bottom: 2px solid #F7BE14; padding-bottom: 0.3rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;">{label}</span>', unsafe_allow_html=True)
            else:
                if st.button(label, key="nav_factory"):
                    st.switch_page("pages/2_🏭_Factory.py")
        
        with nav_cols[2]:
            # Camera Override
            label = "CAMERA OVERRIDE"
            if current_page == 'camera_override':
                st.markdown(f'<span style="color: #F7BE14; border-bottom: 2px solid #F7BE14; padding-bottom: 0.3rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;">{label}</span>', unsafe_allow_html=True)
            else:
                if st.button(label, key="nav_camera"):
                    st.switch_page("pages/3_📐_Camera_Override.py")
        
        with nav_cols[3]:
            # Product Studio
            label = "PRODUCT STUDIO"
            if current_page == 'product_studio':
                st.markdown(f'<span style="color: #F7BE14; border-bottom: 2px solid #F7BE14; padding-bottom: 0.3rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;">{label}</span>', unsafe_allow_html=True)
            else:
                if st.button(label, key="nav_product"):
                    st.switch_page("pages/4_💎_Product_Studio.py")
    
    st.markdown("---")
