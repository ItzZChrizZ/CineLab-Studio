import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.colors import get_theme_css
from components.navbar import render_navbar

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CineLab Suite",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)

# --- RENDER NAVBAR ---
render_navbar()

# --- HERO SECTION ---
st.markdown("""
<div style="
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    text-align: center;
    padding: 2rem;
">
    <h1 style="
        font-size: 5rem;
        font-weight: 300;
        letter-spacing: -2px;
        margin-bottom: 1.5rem;
        color: #F9FEFF;
        line-height: 1.1;
    ">
        Welcome to CineLab
    </h1>
    <p style="
        font-size: 1.4rem;
        color: #CCD4D7;
        font-weight: 300;
        letter-spacing: 1px;
        max-width: 800px;
        line-height: 1.6;
    ">
        Professional Prompt Engineering Suite for AI Image Generation
    </p>
</div>

<style>
/* Light theme override for hero text */
@media (prefers-color-scheme: light) {
    h1 {
        color: #222121 !important;
    }
    p {
        color: #666666 !important;
    }
}
</style>
""", unsafe_allow_html=True)
