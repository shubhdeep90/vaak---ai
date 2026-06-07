import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. SECURITY SETUP (100% SAFE)
# ==========================================
# Ab hum apni API Key ko code ke andar nahi likhenge.
# Yeh line Streamlit ke khufiya locker (Secrets) se key automatic utha legi.
try:
   genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
except Exception as e:
    st.error("🔒 Security Error: GEMINI_API_KEY missing in Streamlit Secrets!")
    st.stop()

# ==========================================
# 2. SYSTEM INSTRUCTIONS FOR VAAK AI
# ==========================================
system_instruction = """
You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). You possess vast knowledge about world history, science, literature, all kinds of books, coding, philosophy, and general trivia.

RULES:
1. Answer any question the user asks with deep knowledge, logic, and accuracy, drawing from your vast database of books and global wisdom.
2. Keep your tone friendly, incredibly smart, and helpful.
3. Always respond in the language the user speaks (Hindi, English, Hinglish, etc.).
"""

# Gemini ka sabse latest aur fast model load karein
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ==========================================
# 3. WEBSITE LOOK & DESIGN (STREAMLIT)
# ==========================================
st.set_page_config(page_title="VAAK AI - The Cosmic Voice", page_icon="🎙️", layout="centered")

st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana.")

# Chat history ko maintain (save) rakhne ke liye
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Purani baatein (chat history) screen par dikhane ke liye
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User se naya sawal lene ke liye input box
user_input = st.chat_input("VAAK se kuch bhi puchein (Books, History, Science, Coding...)...")

if user_input:
    # User ka message screen par dikhayein
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # AI se live jawab mangein
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: Jawab dhoondhne mein dikkat hui. Kripya check karein ki API Key sahi hai ya nahi.")
              
