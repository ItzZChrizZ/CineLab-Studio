"""
Back Button Component
Consistent back-to-home navigation for all tool pages
"""

import streamlit as st

def render_back_button():
    """Render back button at the top of tool pages"""
    
    st.markdown("""
    <style>
    /* Back button styling */
    .back-btn-container {
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    .back-btn-container .stButton > button {
        background-color: #222121 !important;
        color: #F9FEFF !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        height: auto !important;
    }
    
    /* Light theme */
    @media (prefers-color-scheme: light) {
        .back-btn-container .stButton > button {
            background-color: #222121 !important;
            color: #F9FEFF !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container with custom class
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    
    if st.button("← BACK TO HOME", key="back_home_btn"):
        st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
