import os
from dotenv import load_dotenv

# --- Load .env BEFORE importing anything that needs env vars ---
load_dotenv()

import streamlit as st
from utils.openai_chat import get_ai_response
from utils.file_handler import extract_text_from_file

st.set_page_config(page_title="AI Chat Agent", page_icon="💬", layout="centered")

# Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Top bar
top_bar = st.columns([5, 1, 1])
with top_bar[0]:
    st.markdown("<h1 style='margin-bottom: 0;'>💬 Chat with AI Agent</h1>", unsafe_allow_html=True)
with top_bar[1]:
    st.download_button(
        label="💾",
        data="\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.get("messages", [])]),
        file_name="chat_history.txt",
        help="Download Chat",
        key="download_top"
    )
with top_bar[2]:
    if st.button("🔄", help="Reset Chat", key="reset_top"):
        st.session_state.messages = []
        st.rerun()
st.markdown("---")

# File upload
if "file_content" not in st.session_state:
    st.session_state.file_content = ""

uploaded_file = st.file_uploader("📎 Upload a text or PDF file", type=["txt", "pdf"])
if uploaded_file:
    st.session_state.file = uploaded_file.name
    st.success(f"✅ {uploaded_file.name} uploaded!")
    text = extract_text_from_file(uploaded_file)
    st.session_state.file_content = text[:3000]

# View file context
if st.session_state.file_content:
    with st.expander("📄 View Uploaded File Content"):
        st.code(st.session_state.file_content[:1000])

# Display chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f'<div class="message-container"><div class="chat-message {role_class}">{msg["content"]}</div></div>',
        unsafe_allow_html=True
    )

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("_Bot is typing..._")

    file_context = f"Use this context from file:\n{st.session_state.file_content}" if st.session_state.file_content else ""
    try:
        reply = get_ai_response(st.session_state.messages, file_context)
    except Exception as e:
        reply = f"❌ Failed to get response: {e}"

    message_placeholder.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Footer
st.markdown("---")
st.markdown("<center><small>🤖 Built with ❤️ by Ahsan's AI Lab</small></center>", unsafe_allow_html=True)
