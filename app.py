import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.colors import get_theme_css

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CineLab Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)

# --- CUSTOM CSS FOR HOME PAGE ---
st.markdown("""
<style>
/* Import Playfair Display font */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

/* Hero title with Playfair Display */
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1.5rem;
    color: #F9FEFF;
    letter-spacing: 2px;
}

.hero-subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #CCD4D7;
    font-weight: 300;
    letter-spacing: 1px;
    margin-bottom: 4rem;
}

/* Tool buttons - 2x2 grid styling */
.stButton > button {
    background-color: #222121 !important;
    color: #F9FEFF !important;
    border: 1px solid transparent !important;
    padding: 3rem 2rem !important;
    border-radius: 8px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    height: auto !important;
}

/* Light theme */
@media (prefers-color-scheme: light) {
    .hero-title {
        color: #222121 !important;
    }
    
    .hero-subtitle {
        color: #666666 !important;
    }
    
    .stButton > button {
        background-color: #F9FEFF !important;
        color: #222121 !important;
        border: 1px solid transparent !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<h1 class="hero-title">CineLab Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Professional Prompt Engineering Suite for AI Image Generation</p>', unsafe_allow_html=True)

# --- TOOL BUTTONS - 2x2 GRID ---
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🎨 PROMPT GENERATOR", key="btn_prompt"):
        st.switch_page("pages/1_#L01f3a8_Prompt_Generator.py")
    
    if st.button("📐 CAMERA OVERRIDE", key="btn_camera"):
        st.switch_page("pages/3_#L01f4d0_Camera_Override.py")

with col2:
    if st.button("🏭 FACTORY", key="btn_factory"):
        st.switch_page("pages/2_#L01f3ed_Factory.py")
    
    if st.button("💎 PRODUCT STUDIO", key="btn_product"):
        st.switch_page("pages/4_#L01f48e_Product_Studio.py")
