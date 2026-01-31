import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
import io
import json
import os
import sys
import importlib
from PIL import Image

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.colors import get_theme_css
from config.models import get_model, get_api_key_name
from config.prompt_versions import get_logic_version
from components.back_button import render_back_button
from components.back_button import render_back_button

# --- PAGE CONFIG ---
st.set_page_config(page_title="Factory - CineLab", layout="wide", page_icon="🏭")

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)


# --- RENDER NAVBAR ---
render_navbar(current_page="factory")
# --- API CONFIG ---
api_key_name = get_api_key_name("factory")
if api_key_name in st.secrets:
    genai.configure(api_key=st.secrets[api_key_name])
else:
    st.error(f"Error: {api_key_name} not found in secrets.")
    st.stop()

# --- LOAD FACTORY BRIDGE LOGIC ---
# --- BACK BUTTON ---
if st.button("← Back to Home"):
    st.switch_page("app.py")

# --- SAFETY SETTINGS ---
no_filter = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# --- RESPONSE EXTRACTION ---
def safe_extract_response(response):
    try:
        if not hasattr(response, 'candidates') or not response.candidates:
            return None, "No candidates", None
        parts = response.parts if hasattr(response, 'parts') else response.candidates[0].content.parts
        for part in parts:
            if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('image/'):
                img_bytes = part.inline_data.data
                img = Image.open(io.BytesIO(img_bytes))
                return (img, img_bytes), None, part.inline_data.mime_type
            if hasattr(part, 'text') and part.text:
                return None, part.text, "text/plain"
        return None, None, None
    except Exception as e: 
        return None, str(e), None

# --- MODEL LIST ---
@st.cache_data
def get_available_models():
    try:
        return [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    except:
        return [get_model("factory")]

available_models = get_available_models()

# --- UI LAYOUT ---
col_left, col_right = st.columns([0.4, 0.6], gap="large")

# --- LEFT: INPUT ---
with col_left:
    st.write("### Input")
    user_prompt = st.text_area(
        "Paste JSON or text prompt:", 
        height=480, 
        placeholder="Paste CineLab JSON, Camera Override JSON, or Product Studio prompt...", 
        label_visibility="collapsed"
    )
    
    # Toolbar
    c1, c2, c3 = st.columns([2.5, 1.2, 1.3], gap="small")
    
    with c1:
        if available_models:
            selected_model = st.selectbox("Model", available_models, index=0, label_visibility="collapsed")
        else:
            selected_model = st.text_input("Model", get_model("factory"), label_visibility="collapsed")
            
    with c2:
        image_count = st.radio("Qty", [1, 2, 3, 4], index=0, horizontal=True, label_visibility="collapsed")

    with c3:
        generate_btn = st.button("🚀 RUN", type="primary", use_container_width=True)

# --- RIGHT: OUTPUT ---
with col_right:
    st.write("### Output Stream")
    
    if generate_btn and user_prompt:
        # Process input through factory bridge
        final_prompt = bridge_module.prepare_for_generation(user_prompt)
        
        model = genai.GenerativeModel(selected_model)
        
        # Grid System
        grid_cols = st.columns(image_count)
        
        for i in range(image_count):
            with grid_cols[i]:
                with st.container(border=True):
                    # Temperature logic
                    current_temp = 0.2 if i == 0 else 0.9
                    
                    if i == 0:
                        st.caption("💎 Master")
                    else:
                        st.caption(f"🎨 Variant {i}")
                    
                    with st.spinner("..."):
                        try:
                            config = GenerationConfig(temperature=current_temp)
                            
                            response = model.generate_content(
                                final_prompt, 
                                safety_settings=no_filter,
                                generation_config=config
                            )
                            img_res, text_res, mime = safe_extract_response(response)

                            if img_res:
                                img_obj, img_bytes = img_res
                                st.image(img_obj, use_container_width=True)
                                st.download_button(
                                    label="💾 SAVE", 
                                    data=img_bytes, 
                                    file_name=f"factory_v{i+1}.png", 
                                    mime=mime, 
                                    use_container_width=True
                                )
                            elif text_res:
                                st.error("❌ Error")
                                with st.expander("Details"):
                                    st.code(text_res)
                            else:
                                st.error("🚫 Blocked")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
    elif not generate_btn:
        st.info("📥 Ready. Paste prompt and click RUN.")
    else:
        st.warning("⚠️ Paste prompt first.")
