# Eliza Support Bot - Gemini 2.5 Flash Integrated Version
import streamlit as st
from pathlib import Path
import time
import os
from google import genai  # ✅ Google Gemini import
from dotenv import load_dotenv

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False


# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Initialize Gemini client ---
client = genai.Client(api_key=API_KEY)

# --- Initialize session state safely ---
if "selected_reply" not in st.session_state:
    st.session_state.selected_reply = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# --- Page Config ---
st.set_page_config(page_title="Eliza Support Bot", page_icon="💬", layout="wide")

# --- Sidebar ---
with st.sidebar:
    if Path("static/logo.png").exists():
        st.image("static/logo.png", width=120)

    st.title("Eliza — Support Bot 🤖")
    st.caption("AI-Powered Customer Support Assistant")

    # 🌗 Dark Mode Toggle
    st.session_state.dark_mode = st.toggle(
    "🌗 Dark Mode",
    value=st.session_state.dark_mode
)


    # 💬 System Prompt
    system_prompt = st.text_area(
        "System Prompt",
        height=100,
        value="You are Eliza, a friendly AI support agent. Keep responses short, polite, and solution-focused."
    )

    # ✨ Canned Responses
    CANNED = [
        "Hello! How can I assist you today?",
        "I understand your issue. Let me help you resolve it.",
        "Can you please provide more details?",
        "Thank you for contacting support!",
    ]

    st.markdown("#### ✨ Canned Responses")
    for r in CANNED:
        btn_label = r[:35] + "..." if len(r) > 35 else r
        if st.button(btn_label, key=f"canned_{r}"):
            st.session_state.selected_reply = r
            st.rerun()

# --- Theme Colors ---
if st.session_state.dark_mode:
    BG_COLOR = "#1E1E2F"
    TEXT_COLOR = "#E4E6EB"
    USER_BUBBLE = "#3A3F58"
    BOT_BUBBLE = "#2C2F3A"
    BORDER_COLOR = "#4A4A5A"
else:
    BG_COLOR = "#f9fafb"
    TEXT_COLOR = "#000000"
    USER_BUBBLE = "#dbeafe"
    BOT_BUBBLE = "#f0fdf4"
    BORDER_COLOR = "#c3d4ff"

# --- CSS Styling ---
st.markdown(f"""
<style>
.main {{
    background-color: {BG_COLOR};
    color: {TEXT_COLOR};
    font-family: 'Segoe UI', sans-serif;
}}
.user-bubble {{
    background-color: {USER_BUBBLE};
    padding: 12px 15px;
    border-radius: 14px;
    max-width: 70%;
    margin: 8px 0 8px auto;
    color: {TEXT_COLOR};
}}
.bot-bubble {{
    background-color: {BOT_BUBBLE};
    padding: 12px 15px;
    border-radius: 14px;
    max-width: 70%;
    margin: 8px auto 8px 0;
    color: {TEXT_COLOR};
}}
</style>
""", unsafe_allow_html=True)

# --- Chat Section ---
st.markdown("## 💬 Live Support Chat")
chat_container = st.container()

# --- Chat Function with Retry ---
def chat_with_gemini(messages, max_retries=3, wait_time=3):
    """
    Uses Google Gemini 2.5 Flash to generate a response with retry logic for 503 errors.
    """
    conversation = []
    for m in messages:
        role = m.get("role")
        content = m.get("content")
        if role == "system":
            conversation.append(f"System: {content}")
        elif role == "user":
            conversation.append(f"User: {content}")
        elif role == "assistant":
            conversation.append(f"Assistant: {content}")

    prompt = "\n".join(conversation)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                if attempt < max_retries - 1:
                    st.warning("⚠️ Just a minute... the server is busy. Retrying your question...")
                    time.sleep(wait_time)
                    continue
            return f"⚠️ Error: {error_msg}"

# --- Render Chat ---
def render_chat():
    with chat_container:
        for role, text in st.session_state.history:
            if role == "user":
                st.markdown(f"""
                    <div class="user-bubble">
                        <div class="sender">🧑 You</div>{text}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="bot-bubble">
                        <div class="sender">🤖 Eliza</div>{text}
                    </div>
                """, unsafe_allow_html=True)

# --- Message Input ---
st.markdown("---")
input_col, send_col = st.columns([6, 1])
with input_col:
   txt = st.text_area(
    "💬 Message",
    key="message_input",
    placeholder="Type your message here...",
    height=65
)
   
with send_col:
    send = st.button("Send", use_container_width=True)

# --- Send Logic ---
if send and txt.strip():
    user_text = txt.strip()
    st.session_state.history.append(("user", user_text))
    st.session_state.messages.append({"role": "user", "content": user_text})

    with chat_container:
        typing_placeholder = st.empty()
        typing_placeholder.markdown("💭 **Eliza is typing...**")
        time.sleep(1.2)

    reply = chat_with_gemini(st.session_state.messages)
    typing_placeholder.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.history.append(("assistant", reply))

    # 🔥 CORRECT CLEAN LOGIC → delete BEFORE rerun
    if "message_input" in st.session_state:
        del st.session_state["message_input"]

    st.session_state.selected_reply = ""

    st.rerun()


# # --- Send Logic 1-time wala ye jo pehle tha--
# if send and txt.strip():
#     user_text = txt.strip()
#     st.session_state.history.append(("user", user_text))
#     st.session_state.messages.append({"role": "user", "content": user_text})

#     with chat_container:
#         typing_placeholder = st.empty()
#         typing_placeholder.markdown("💭 **Eliza is typing...**")
#         time.sleep(1.2)

#     reply = chat_with_gemini(st.session_state.messages)
#     typing_placeholder.empty()

#     st.session_state.messages.append({"role": "assistant", "content": reply})
#     st.session_state.history.append(("assistant", reply))

#     # ✅ Clear input safely (fixes Streamlit error)
#     st.session_state.selected_reply = ""
#     st.session_state.pop("message_input", None)
#     st.rerun()

# --- Initial Render ---
render_chat()
