# app.py - GeminiMind: ChatGPT-style Multimodal Chatbot
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
import base64
import fitz  # PyMuPDF
import docx
from config import (
    APP_TITLE, APP_ICON, GEMINI_MODEL, MAX_TOKENS,
    TEMPERATURE, SUPPORTED_IMAGE_TYPES, SUPPORTED_DOC_TYPES,
    MAX_FILE_SIZE_MB, AUTHOR_NAME, AUTHOR_GITHUB, AUTHOR_LINKEDIN
)

# --- Page Config ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (ChatGPT-style dark theme) ---
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #212121; color: #ececec; }
    .stChatMessage { background-color: transparent !important; }
    /* User message bubble */
    [data-testid="stChatMessageContent"]:has(> div > p) {
        background-color: #2f2f2f;
        border-radius: 12px;
        padding: 12px 16px;
    }
    /* Input box */
    .stChatInputContainer { background-color: #2f2f2f !important; border-radius: 16px !important; }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #171717 !important; }
    /* Buttons */
    .stButton>button {
        background-color: #2f2f2f;
        color: #ececec;
        border: 1px solid #444;
        border-radius: 8px;
        width: 100%;
    }
    .stButton>button:hover { background-color: #404040; }
    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stFileUploader { background-color: #2f2f2f; border-radius: 12px; padding: 8px; }
    h1, h2, h3 { color: #ececec !important; }
    .stSelectbox > div > div { background-color: #2f2f2f !important; color: #ececec !important; }
</style>
""", unsafe_allow_html=True)

# --- Initialize Gemini ---
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config={
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_TOKENS,
        }
    )

# --- File Processing ---
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:15000]  # limit context

def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])[:15000]

def process_uploaded_file(uploaded_file):
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type
    name = uploaded_file.name
    size_mb = len(file_bytes) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        return None, None, f"File too large ({size_mb:.1f}MB). Max {MAX_FILE_SIZE_MB}MB."

    if file_type in ["image/jpeg", "image/png", "image/webp", "image/gif"]:
        img = Image.open(io.BytesIO(file_bytes))
        return "image", img, name
    elif file_type == "application/pdf":
        text = extract_text_from_pdf(file_bytes)
        return "document", text, name
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        text = extract_text_from_docx(file_bytes)
        return "document", text, name
    elif file_type == "text/plain":
        return "document", file_bytes.decode("utf-8")[:15000], name
    else:
        return None, None, f"Unsupported file type: {file_type}"

# --- Build Gemini Message ---
def build_gemini_parts(prompt, attachments):
    parts = []
    for att in attachments:
        if att["type"] == "image":
            parts.append(att["data"])
        elif att["type"] == "document":
            parts.append(f"[File: {att['name']}]\n{att['data']}\n")
    parts.append(prompt)
    return parts

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "attachments" not in st.session_state:
    st.session_state.attachments = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "model" not in st.session_state:
    st.session_state.model = init_gemini()

# --- Sidebar ---
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.markdown("*Powered by Google Gemini*")
    st.divider()

    # New Chat
    if st.button("+ New Chat"):
        st.session_state.messages = []
        st.session_state.attachments = []
        st.session_state.chat_session = None
        st.rerun()

    st.divider()

    # File Upload
    st.markdown("### Attach Files")
    uploaded_files = st.file_uploader(
        "Images, PDFs, DOCX, TXT",
        type=["png", "jpg", "jpeg", "webp", "gif", "pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.session_state.attachments = []
        for f in uploaded_files:
            ftype, fdata, fname = process_uploaded_file(f)
            if ftype:
                st.session_state.attachments.append({"type": ftype, "data": fdata, "name": fname})
                if ftype == "image":
                    st.image(fdata, caption=fname, use_column_width=True)
                else:
                    st.success(f"📄 {fname}")
            else:
                st.error(fdata)  # error message

    if st.session_state.attachments and st.button("Clear Attachments"):
        st.session_state.attachments = []
        st.rerun()

    st.divider()

    # Model Info
    st.markdown("### Model")
    st.code(GEMINI_MODEL, language=None)
    st.markdown(f"🌡️ Temp: `{TEMPERATURE}` | 💬 Tokens: `{MAX_TOKENS}`")

    st.divider()
    st.markdown(f"Built by **{AUTHOR_NAME}**")
    st.markdown(f"[GitHub]({AUTHOR_GITHUB}) · [LinkedIn]({AUTHOR_LINKEDIN})")

# --- Main Chat Area ---
if not st.session_state.model:
    st.error("🔑 GEMINI_API_KEY not set. Please add it in the Hugging Face Space settings under Repository Secrets.")
    st.stop()

# Welcome screen
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center; padding: 60px 0 20px 0;'>
        <h1 style='font-size: 2.5rem; font-weight: 700;'>GeminiMind 🤯</h1>
        <p style='font-size: 1.1rem; color: #aaa;'>Your multimodal AI assistant. Chat with text, images, PDFs & documents.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    suggestions = [
        ("📚", "Summarize a document", "Can you summarize the uploaded document for me?"),
        ("🖼️", "Analyze an image", "What's in this image? Describe it in detail."),
        ("💡", "Explain a concept", "Explain quantum computing in simple terms."),
    ]
    for col, (icon, title, prompt) in zip(cols, suggestions):
        with col:
            if st.button(f"{icon} {title}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt, "attachments": []})
                st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Show attachments
        for att in msg.get("attachments", []):
            if att["type"] == "image":
                st.image(att["data"], width=300)
            elif att["type"] == "document":
                st.info(f"📄 {att['name']}")
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Message GeminiMind..."):
    current_attachments = st.session_state.attachments.copy()

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "attachments": current_attachments
    })

    with st.chat_message("user"):
        for att in current_attachments:
            if att["type"] == "image":
                st.image(att["data"], width=300)
            elif att["type"] == "document":
                st.info(f"📄 {att['name']}")
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                parts = build_gemini_parts(prompt, current_attachments)

                # Build history for multi-turn
                history = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    history.append({"role": role, "parts": [m["content"]]})

                chat = st.session_state.model.start_chat(history=history)
                response = chat.send_message(parts)
                reply = response.text

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply, "attachments": []})

                # Clear attachments after sending
                st.session_state.attachments = []

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "attachments": []})
