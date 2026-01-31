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
st.set_page_config(page_title="Camera Override - CineLab", layout="wide", page_icon="📐")

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)

# --- RENDER NAVBAR ---
render_back_button()

# --- CUSTOM CSS FOR SELECTION BUTTONS ---
st.markdown("""
<style>
/* Camera Override Button Styling */
/* Normal buttons */
div[data-testid="column"] .stButton > button {
    background-color: #222121 !important;
    color: #F9FEFF !important;
    border: 1px solid transparent !important;
    padding: 1rem !important;
    border-radius: 6px !important;
    text-align: center !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    height: auto !important;
}

/* Selected buttons (primary type) */
div[data-testid="column"] .stButton > button[kind="primary"] {
    border: 1px solid #F7BE14 !important;
}

/* Light Theme */
@media (prefers-color-scheme: light) {
    div[data-testid="column"] .stButton > button {
        background-color: #F9FEFF !important;
        color: #222121 !important;
    }
    
    div[data-testid="column"] .stButton > button[kind="primary"] {
        border: 1px solid #F7BE14 !important;
    }
}

/* Section Headers */
.section-title {
    color: #CCD4D7;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 2.5rem 0 0.5rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #30363d;
}

@media (prefers-color-scheme: light) {
    .section-title {
        color: #666666;
        border-bottom-color: #e0e0e0;
    }
}

/* Description text */
.description-text {
    color: #a3a3a3;
    font-size: 0.8rem;
    margin: 0.5rem 0 1rem 0;
    font-style: italic;
}
    font-style: italic;
}

/* Aspect Ratio Display */
.ratio-display {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 0.8rem;
    text-align: center;
    font-size: 1rem;
    color: #F9FEFF;
    margin: 1rem 0;
}

@media (prefers-color-scheme: light) {
    .ratio-display {
        background-color: white;
        border-color: #e0e0e0;
        color: #222121;
    }
}
</style>
""", unsafe_allow_html=True)

# --- LOAD LIBRARY ---
def load_library():
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'camera_override_library.json')
    try:
        with open(lib_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("camera_override_library.json not found!")
        return {}

lib = load_library()

# --- API CONFIG ---
api_key_name = get_api_key_name("camera_override")
if api_key_name in st.secrets:
    genai.configure(api_key=st.secrets[api_key_name])
else:
    st.error(f"Error: {api_key_name} not found in secrets.")
    st.stop()

# --- LOAD ACTIVE PROMPT VERSION ---
prompt_version = get_prompt_version("camera_override")
prompt_module = importlib.import_module(f"prompts.{prompt_version}")

# --- INITIALIZE SESSION STATE ---
if 'selected_angle' not in st.session_state:
    st.session_state.selected_angle = 'eye_level'
if 'selected_scale' not in st.session_state:
    st.session_state.selected_scale = 'full_shot'
if 'selected_lens' not in st.session_state:
    st.session_state.selected_lens = '50mm_natural'
if 'selected_ratio' not in st.session_state:
    st.session_state.selected_ratio = '16:9'

# --- CORE ENGINE ---
def run_camera_override(params, img_data):
    prompt_data = prompt_module.generate_prompt(params, img_data, lib)
    
    model_name = get_model("camera_override")
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
col_left, col_right = st.columns([0.35, 0.65])

with col_left:
    st.markdown("### REFERENCE")
    up = st.file_uploader("Upload architectural image", type=['jpg','png','jpeg'], label_visibility="collapsed")
    if up:
        st.image(up, use_container_width=True)

with col_right:
    # CAMERA ANGLE
    st.markdown('<div class="section-title">Camera Angle</div>', unsafe_allow_html=True)
    
    angles = lib.get('camera_angles', {})
    angle_keys = list(angles.keys())
    
    # Create button grid HTML
    angle_buttons_html = '<div class="button-grid">'
    for angle_key in angle_keys:
        selected_class = 'selected' if st.session_state.selected_angle == angle_key else ''
        angle_buttons_html += f'<div class="custom-button {selected_class}" onclick="window.parent.postMessage({{type: \'streamlit:setComponentValue\', value: \'{angle_key}\'}}, \'*\')">{angles[angle_key]["ui_label"]}</div>'
    angle_buttons_html += '</div>'
    
    # Display buttons (not interactive yet, using st.columns as fallback)
    angle_cols = st.columns(4)
    for idx, angle_key in enumerate(angle_keys):
        col_idx = idx % 4
        with angle_cols[col_idx]:
            is_selected = st.session_state.selected_angle == angle_key
            if st.button(
                angles[angle_key]['ui_label'],
                key=f"angle_{angle_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_angle = angle_key
                st.rerun()
    
    if st.session_state.selected_angle in angles:
        st.markdown(f'<div class="description-text">📝 {angles[st.session_state.selected_angle]["ui_description"]}</div>', unsafe_allow_html=True)
    
    # SHOT SCALE
    st.markdown('<div class="section-title">Shot Scale</div>', unsafe_allow_html=True)
    
    scales = lib.get('shot_scales', {})
    scale_keys = list(scales.keys())
    
    scale_cols = st.columns(4)
    for idx, scale_key in enumerate(scale_keys):
        col_idx = idx % 4
        with scale_cols[col_idx]:
            is_selected = st.session_state.selected_scale == scale_key
            if st.button(
                scales[scale_key]['ui_label'],
                key=f"scale_{scale_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_scale = scale_key
                st.rerun()
    
    if st.session_state.selected_scale in scales:
        st.markdown(f'<div class="description-text">📝 {scales[st.session_state.selected_scale]["ui_description"]}</div>', unsafe_allow_html=True)
    
    # LENS
    st.markdown('<div class="section-title">Lens Choice</div>', unsafe_allow_html=True)
    
    lenses = lib.get('lenses', {})
    lens_keys = list(lenses.keys())
    
    lens_cols = st.columns(4)
    for idx, lens_key in enumerate(lens_keys):
        col_idx = idx % 4
        with lens_cols[col_idx]:
            is_selected = st.session_state.selected_lens == lens_key
            if st.button(
                lenses[lens_key]['ui_label'],
                key=f"lens_{lens_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_lens = lens_key
                st.rerun()
    
    if st.session_state.selected_lens in lenses:
        st.markdown(f'<div class="description-text">📝 {lenses[st.session_state.selected_lens]["ui_description"]}</div>', unsafe_allow_html=True)
    
    # ASPECT RATIO
    st.markdown('<div class="section-title">Aspect Ratio</div>', unsafe_allow_html=True)
    
    ratios = lib.get('aspect_ratios', {})
    ratio_keys = list(ratios.keys())
    
    ratio_cols = st.columns(8)
    for idx, ratio_key in enumerate(ratio_keys):
        with ratio_cols[idx]:
            ratio_label = ratios[ratio_key]['ui_label'].split()[0]
            is_selected = st.session_state.selected_ratio == ratio_label
            if st.button(
                ratio_label,
                key=f"ratio_{ratio_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_ratio = ratio_label
                st.rerun()
    
    st.markdown(f'<div class="ratio-display">Selected: {st.session_state.selected_ratio}</div>', unsafe_allow_html=True)
    
    # GENERATE BUTTON
    st.markdown("---")
    if st.button("🚀 GENERATE JSON PROTOCOL", use_container_width=True, type="primary"):
        if up:
            with st.spinner("Analyzing architecture..."):
                try:
                    params = {
                        "camera_angle": st.session_state.selected_angle,
                        "shot_scale": st.session_state.selected_scale,
                        "lens": st.session_state.selected_lens,
                        "aspect_ratio": st.session_state.selected_ratio
                    }
                    img_data = {"mime_type": up.type, "data": up.getvalue()}
                    st.session_state.camera_result = run_camera_override(params, img_data)
                    st.success("✅ Protocol Generated!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Upload image first.")

# --- OUTPUT ---
if 'camera_result' in st.session_state:
    st.markdown("---")
    st.markdown("### 📋 GENERATED CAMERA OVERRIDE PROTOCOL")
    st.code(st.session_state.camera_result, language="json")
    st.download_button(
        label="💾 Download JSON",
        data=st.session_state.camera_result,
        file_name="camera_override_protocol.json",
        mime="application/json",
        use_container_width=True
    )
