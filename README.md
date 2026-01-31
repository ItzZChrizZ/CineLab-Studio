# CineLab Suite v1.0 - Modular Architecture

Professional AI image generation toolkit for prompt engineers. Fully modular design for easy maintenance and extensibility.

## 🏗️ Modular Architecture

```
CineLab-Suite/
├── config/                     # Configuration modules
│   ├── colors.py              # Color system (dark/light themes)
│   ├── models.py              # Model & API assignments
│   └── prompt_versions.py     # Active prompt/logic versions
│
├── data/                       # Libraries (separate per tool)
│   ├── cinelab_library.json
│   └── camera_override_library.json
│
├── prompts/                    # Prompt generators (versioned)
│   ├── cinelab_v1.py
│   ├── camera_override_v1.py
│   └── product_studio_v1.py
│
├── logic/                      # Logic modules (versioned)
│   ├── fine_art_nude_v1.py
│   └── factory_bridge_v1.py
│
├── pages/                      # UI pages (Streamlit multi-page)
│   ├── 1_🎨_Prompt_Generator.py
│   ├── 2_🏭_Factory.py
│   ├── 3_📐_Camera_Override.py
│   └── 4_💎_Product_Studio.py
│
├── components/                 # Shared UI components
│   └── theme.py
│
├── app.py                      # Landing page
└── requirements.txt
```

## 🎯 Key Features

### 1. **Version Management**
Change active versions without touching code:
```python
# config/prompt_versions.py
ACTIVE_PROMPTS = {
    "cinelab": "cinelab_v1",  # Change to v2, v3, etc.
}
```

### 2. **Separate Libraries**
Each tool has its own data file - no conflicts:
- `cinelab_library.json` → CineLab only
- `camera_override_library.json` → Camera Override only
- `product_studio_library.json` → Product Studio only

### 3. **Model Configuration**
Manage AI models centrally:
```python
# config/models.py
MODELS = {
    "cinelab": "gemini-2.0-flash-exp",
    "factory": "gemini-2.0-flash-thinking-exp"
}
```

### 4. **Logic Modules**
Special handling (Fine Art Nude, Factory Bridge) in separate files.

## 🚀 Quick Start

### Streamlit Cloud Deployment

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "v1.0 - Modular architecture"
git push origin main
```

2. **Deploy**
- Go to share.streamlit.io
- Connect repository
- Add secrets:
```toml
CINELAB_API_KEY = "your-api-key-1"
FACTORY_API_KEY = "your-api-key-2"
```

3. **Launch!**

## 🔧 Customization Guide

### Adding New Prompt Version

1. Create new file:
```bash
touch prompts/cinelab_v2.py
```

2. Implement `generate_prompt()` function

3. Activate in config:
```python
# config/prompt_versions.py
ACTIVE_PROMPTS["cinelab"] = "cinelab_v2"
```

### Changing Models

```python
# config/models.py
MODELS["factory"] = "gemini-4.0-ultra"  # When available
```

### Updating Colors

```python
# config/colors.py
DARK_THEME["accent"] = "#NEW_COLOR"
```

## 📚 Tools

1. **🎨 Prompt Generator (CineLab)** - Cinematography recipes
2. **🏭 Factory** - Image generation from JSON
3. **📐 Camera Override** - Multi-angle architectural visualization
4. **💎 Product Studio** - Product context transformation

## 🔑 API Configuration

Two API keys required:
- **API 1** (Prompt Generation): CineLab, Camera Override, Product Studio
- **API 2** (Image Generation): Factory

## 📝 Version History

### v1.0 (Current)
- ✅ Modular architecture
- ✅ Version management system
- ✅ Separate libraries per tool
- ✅ Dark/Light theme support
- ✅ Camera Override tool
- ✅ Product Studio tool (basic)
- ✅ Fine Art Nude logic module
- ✅ Factory bridge (multi-format support)

## 🛣️ Roadmap v2.0

- Virtual Fashion tool
- Batch processing
- Advanced UI customization
- More photographer presets
- Enhanced logic modules

---

**Built for prompt engineers, by a prompt engineer** 🎬
