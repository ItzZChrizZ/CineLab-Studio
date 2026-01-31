import streamlit as st
import google.generativeai as genai
import json
import os
import sys
import importlib

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.colors import get_theme_css
from config.models import get_model, get_api_key_name
from config.prompt_versions import get_prompt_version
from components.back_button import render_back_button

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Studio - CineLab", layout="wide", page_icon="💎")

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)

# --- RENDER NAVBAR ---
render_navbar(current_page="product_studio")

# --- LOAD LIBRARY (for photographer styles) ---
def load_library():
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cinelab_library.json')
    try:
        with open(lib_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("cinelab_library.json not found!")
        return {}

lib = load_library()

# --- API CONFIG ---
api_key_name = get_api_key_name("product_studio")
if api_key_name in st.secrets:
    genai.configure(api_key=st.secrets[api_key_name])
else:
    st.error(f"Error: {api_key_name} not found in secrets.")
    st.stop()

# --- LOAD ACTIVE PROMPT VERSION ---
prompt_version = get_prompt_version("product_studio")
prompt_module = importlib.import_module(f"prompts.{prompt_version}")
# --- BACK BUTTON ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- CORE ENGINE ---
def run_product_studio(params, img_data):
    prompt_data = prompt_module.generate_prompt(params, img_data, lib)
    
    model_name = get_model("product_studio")
    model = genai.GenerativeModel(
        model_name,
        system_instruction=prompt_data['system_instruction']
    )
    
    res = model.generate_content(
        [prompt_data['user_prompt'], img_data],
        generation_config=prompt_data['generation_config'],
        safety_settings=prompt_data['safety_settings']
    )
    
    return res.text

# --- LAYOUT ---
col_left, col_right = st.columns([0.4, 0.6])

with col_left:
    st.markdown("### REFERENCE PRODUCT")
    up = st.file_uploader("Upload product image", type=['jpg','png','jpeg'], label_visibility="collapsed")
    if up:
        st.image(up, use_container_width=True)

with col_right:
    st.markdown("### CONTEXT TRANSFORMATION")
    
    # User text input
    user_text = st.text_area(
        "Describe new context:",
        height=150,
        placeholder="Example: Show this gold necklace on a female model's neck with soft studio lighting...",
        help="Describe how you want to see the product in a new context"
    )
    
    st.markdown("---")
    
    # Photographer preset (optional)
    st.markdown("### PHOTOGRAPHER STYLE (Optional)")
    
    use_photographer = st.checkbox("Apply photographer style")
    
    photographer = None
    if use_photographer and lib:
        # Only show Fashion photographers for product photography
        fashion_photographers = lib.get('photographers', {}).get('Fashion', {})
        if fashion_photographers:
            photographer = st.selectbox(
                "Select photographer",
                options=["None"] + sorted(fashion_photographers.keys())
            )
            
            if photographer != "None":
                photo_info = fashion_photographers[photographer]
                st.markdown(f"""
                <div class='info-box'>
                    <b>Style:</b> {photo_info['style']}<br>
                    <b>Lighting:</b> {photo_info['lighting']}<br>
                    <b>Vibe:</b> {photo_info['vibe']}
                </div>
                """, unsafe_allow_html=True)
            else:
                photographer = None
    
    st.markdown("---")
    
    # Generate button
    if st.button("🚀 GENERATE PRODUCT PROMPT", use_container_width=True, type="primary"):
        if up and user_text.strip():
            with st.spinner("Analyzing product..."):
                try:
                    params = {
                        "user_text": user_text,
                        "photographer": photographer if photographer != "None" else None
                    }
                    img_data = {"mime_type": up.type, "data": up.getvalue()}
                    st.session_state.product_result = run_product_studio(params, img_data)
                    st.success("✅ Prompt Generated!")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif not up:
            st.warning("⚠️ Upload product image first.")
        else:
            st.warning("⚠️ Describe the context first.")

# --- OUTPUT ---
if 'product_result' in st.session_state:
    st.markdown("---")
    st.markdown("### 📋 GENERATED PRODUCT PROMPT")
    st.text_area(
        "Final prompt:",
        value=st.session_state.product_result,
        height=300,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="💾 Download as TXT",
            data=st.session_state.product_result,
            file_name="product_studio_prompt.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        # Wrap in JSON for Factory compatibility
        json_wrapped = json.dumps({"prompt": st.session_state.product_result}, indent=2)
        st.download_button(
            label="💾 Download as JSON",
            data=json_wrapped,
            file_name="product_studio_prompt.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.info("💡 Tip: Copy this prompt and paste into Factory to generate the image!")
