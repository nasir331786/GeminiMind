---
title: GeminiMind
emoji: 🤯
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# 🤯 GeminiMind

> ChatGPT-style multimodal AI chatbot powered by Google Gemini — chat with text, images, PDFs & documents.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-orange)](https://deepmind.google/technologies/gemini/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![Live Demo](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/huntnasir/GeminiMind)

## 🚀 Live Demo

**Try it now → [https://huggingface.co/spaces/huntnasir/GeminiMind](https://huggingface.co/spaces/huntnasir/GeminiMind)**

> No setup required. Just open and start chatting!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Chat** | Full conversational memory, multi-turn dialogue |
| 🖼️ **Images** | Upload PNG, JPG, WEBP, GIF — Gemini analyzes them |
| 📄 **PDFs** | Upload PDFs — ask questions about their content |
| 📝 **DOCX** | Upload Word documents for analysis |
| 📃 **TXT** | Upload plain text files |
| 🌚 **Dark Theme** | ChatGPT-style dark UI |
| ➕ **New Chat** | Reset conversation anytime |
| 💡 **Suggestions** | Quick-start prompts on welcome screen |

## 🏗️ Architecture

```
User Input (text + files)
        ↓
File Processor → PDF/DOCX/TXT → Text Extraction
              → Images → PIL Image Objects
        ↓
Gemini 1.5 Flash API (multi-turn chat)
        ↓
Streaming Response → Streamlit Chat UI
```

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/nasir331786/GeminiMind
cd GeminiMind
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Set API Key
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
# Get free key at: https://aistudio.google.com/app/apikey
```

### 4. Run
```bash
streamlit run app.py
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey) (free) |

## 📦 Tech Stack

| Tool | Purpose |
|------|---------|
| Google Gemini 1.5 Flash | LLM + Vision model (free tier) |
| `google-generativeai` | Official Gemini Python SDK |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX file reading |
| Pillow | Image processing |
| Streamlit | Web UI with chat interface |
| Docker | Container deployment |

## ⚙️ Configuration (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `GEMINI_MODEL` | `gemini-1.5-flash` | Model to use |
| `TEMPERATURE` | `0.7` | Response creativity |
| `MAX_TOKENS` | `8192` | Max output tokens |
| `MAX_FILE_SIZE_MB` | `20` | Max upload size |

## 💻 Author

**Nasir Husain Tamanne**  
[GitHub](https://github.com/nasir331786) · [LinkedIn](https://www.linkedin.com/in/nasir-husain-tamanne)

## 📄 License

MIT License — free to use, modify and distribute.
