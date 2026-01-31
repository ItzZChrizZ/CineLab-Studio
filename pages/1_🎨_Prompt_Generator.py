import streamlit as st
import google.generativeai as genai
import json
import os
import sys
import importlib

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.colors import get_theme_css
from config.models import get_model, get_api_key_name
from config.prompt_versions import get_prompt_version, get_logic_version
from components.navbar import render_navbar

# --- PAGE CONFIG ---
st.set_page_config(page_title="Prompt Generator - CineLab", layout="wide", page_icon="🎨")

# --- APPLY THEME ---
st.markdown(get_theme_css(), unsafe_allow_html=True)

# --- RENDER NAVBAR ---
render_navbar(current_page='prompt_generator')

# --- LOAD LIBRARY ---
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
api_key_name = get_api_key_name("cinelab")
if api_key_name in st.secrets:
    genai.configure(api_key=st.secrets[api_key_name])
else:
    st.error(f"Error: {api_key_name} not found in Streamlit secrets.")
    st.stop()

# --- LOAD ACTIVE PROMPT VERSION ---
prompt_version = get_prompt_version("cinelab")
prompt_module = importlib.import_module(f"prompts.{prompt_version}")

# --- LOAD FINE ART NUDE LOGIC ---
logic_version = get_logic_version("fine_art_nude")
logic_module = importlib.import_module(f"logic.{logic_version}")


# --- CORE ENGINE ---
def run_cine_engine(params, img_data):
    # Get prompt structure from active version
    prompt_data = prompt_module.generate_prompt(params, img_data)
    
    # Apply Fine Art Nude logic if needed
    genre = params.get('genre', '')
    if logic_module.should_apply(genre):
        prompt_data['user_prompt'] = logic_module.apply_workaround(
            prompt_data['user_prompt'], 
            genre
        )
    
    # Get active model
    model_name = get_model("cinelab")
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

# --- UI LAYOUT ---
c1, c2, c3 = st.columns([0.9, 1.2, 1.2])

with c1:
    st.markdown("### REFERENCE")
    up = st.file_uploader("Upload Image", type=['jpg','png','jpeg'], label_visibility="collapsed")
    if up: 
        st.image(up, use_container_width=True)

with c2:
    st.markdown("### EQUIPMENT")
    cam_list = sorted(lib['cameras'].keys()) if lib else []
    cam = st.selectbox("Camera Body", cam_list, label_visibility="collapsed")
    if lib:
        st.markdown(f"<div class='info-box'>{lib['cameras'][cam]['info']} | {lib['cameras'][cam]['vibe']}</div>", unsafe_allow_html=True)
    
    lens_list = sorted(lib['lenses'].keys()) if lib else []
    lens = st.selectbox("Lens", lens_list, label_visibility="collapsed")
    if lib:
        st.markdown(f"<div class='info-box'>{lib['lenses'][lens]['info']} | {lib['lenses'][lens]['character']}</div>", unsafe_allow_html=True)
    
    sc1, sc2 = st.columns(2)
    with sc1:
        f_stop = st.select_slider("F-Stop", options=["f/1.2", "f/1.4", "f/1.8", "f/2.0", "f/2.8", "f/4", "f/5.6", "f/8", "f/11", "f/16", "f/22"])
    with sc2:
        iso = st.select_slider("ISO", options=["50", "100", "200", "400", "800", "1600", "3200", "6400", "Grainy"])

    st.markdown("### ART DIRECTION")
    if lib:
        genre = st.selectbox("Genre", sorted(lib['photographers'].keys()))
        artist = st.selectbox("Artist", sorted(lib['photographers'][genre].keys()))
        inf = lib['photographers'][genre][artist]
        st.markdown(f"<div class='info-box'><b>Style:</b> {inf['style']}<br><b>Lighting:</b> {inf['lighting']}</div>", unsafe_allow_html=True)
    
    notes = st.text_input("Director's Notes", placeholder="Mood, skin details, textures...", key="notes_input")

with c3:
    st.markdown("### LIGHTING")
    l_type = st.radio("Category", ["Studio", "Outdoor"], horizontal=True, label_visibility="collapsed")
    
    selected_p = ""
    if lib:
        presets = sorted(lib['lighting_presets'][l_type].keys())
        selected_p = st.selectbox("Scenario", presets, label_visibility="collapsed")
        st.markdown(f"<div class='info-box'>{lib['lighting_presets'][l_type][selected_p]['info']} | Result: {lib['lighting_presets'][l_type][selected_p]['result']}</div>", unsafe_allow_html=True)

    light_specs = ""
    if selected_p == "Low Key Lighting":
        st.markdown("---")
        is_std_lk = st.checkbox("Standard Low Key", value=True)
        if not is_std_lk:
            with st.expander("🎛️ LOW KEY CONTROL", expanded=True):
                darkness = st.slider("Darkness (%)", 0, 100, 80)
                l1c1, l1c2 = st.columns(2)
                with l1c1:
                    p = st.slider("Pan", -180, 180, 0, key="lkp")
                    t = st.slider("Tilt", -90, 90, 45, key="lkt")
                with l1c2:
                    cl = st.color_picker("Color", "#FFFFFF", key="lkc")
                    it = st.slider("Power", 0, 100, 80, key="lki")
                light_specs = f"Low Key ({darkness}% dark). L1: {cl}, {it}% @ Pan:{p}°, Tilt:{t}°"
        else: 
            light_specs = "Standard Low Key Setup."
            
    elif selected_p == "Custom Studio Lights":
        st.markdown("---")
        is_std_custom = st.checkbox("Standard Setup", value=True, key="std_custom")
        if not is_std_custom:
            with st.expander("🎛️ CUSTOM CONTROL", expanded=True):
                n_l = st.radio("Lights", [1, 2, 3], horizontal=True, key="std_num")
                parts = []
                for i in range(1, n_l + 1):
                    st.markdown(f"**L{i}**")
                    sl1, sl2 = st.columns(2)
                    with sl1: 
                        p_val = st.slider(f"Pan {i}", -180, 180, 0, key=f"sp{i}")
                        t_val = st.slider(f"Tilt {i}", -90, 90, 45, key=f"st_t{i}")
                    with sl2: 
                        cl_val = st.color_picker(f"Color {i}", "#FFFFFF", key=f"sc{i}")
                        it_val = st.slider(f"Power {i}", 0, 100, 80, key=f"si{i}")
                    parts.append(f"L{i}: {cl_val} {it_val}% @ Pan:{p_val}°, Tilt:{t_val}°")
                light_specs = " | ".join(parts)
        else:
            light_specs = "Standard 3-Point Setup."
    else: 
        light_specs = f"Preset: {selected_p}."

    ratio = st.radio("Ratio", ["4:5", "16:9", "1:1", "9:16"], horizontal=True)

    if st.button("🚀 GENERATE JSON RECIPE"):
        if up:
            with st.spinner("Analyzing..."):
                try:
                    params = {
                        "cam": cam, 
                        "cam_info": f"{lib['cameras'][cam]['info']} | {lib['cameras'][cam]['vibe']}",
                        "lens": lens, 
                        "lens_info": f"{lib['lenses'][lens]['info']} | {lib['lenses'][lens]['character']}",
                        "f_stop": f_stop, 
                        "iso": iso, 
                        "ratio": ratio,
                        "artist": artist,
                        "genre": genre,  # Important for Fine Art Nude logic
                        "category": l_type, 
                        "scenario": selected_p,
                        "light_details": light_specs, 
                        "notes": notes
                    }
                    img_data = {"mime_type": up.type, "data": up.getvalue()}
                    st.session_state.res = run_cine_engine(params, img_data)
                    st.success("✅ Recipe Generated!")
                except Exception as e: 
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Upload image first.")

# --- OUTPUT ---
if 'res' in st.session_state:
    st.markdown("---")
    st.markdown("### 📋 GENERATED RECIPE")
    st.code(st.session_state.res, language="json")
    st.download_button(
        label="💾 Download JSON",
        data=st.session_state.res,
        file_name="cinelab_recipe.json",
        mime="application/json",
        use_container_width=True
    )
