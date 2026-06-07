import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. WEBSITE CONFIGURATION (LOOK & FEEL)
# ==========================================
st.set_page_config(
    page_title="VAAK AI - The Cosmic Voice", 
    page_icon="🎙️", 
    layout="centered"
)

# ==========================================
# 2. SECURITY SETUP (STREAMLIT SECRETS)
# ==========================================
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🔒 Security Error: Streamlit Secrets mein 'GEMINI_API_KEY' nahi mila!")
        st.stop()
except Exception as e:
    st.error(f"🔒 Configuration Error: {str(e)}")
    st.stop()

# ==========================================
# 3. SYSTEM INSTRUCTIONS FOR VAAK AI
# ==========================================
system_instruction = """
You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). You possess vast knowledge about world history, science, literature, all kinds of books, coding, philosophy, and general trivia.

RULES:
1. Answer any question the user asks with deep knowledge, logic, and accuracy, drawing from your vast database of books and global wisdom.
2. Keep your tone friendly, incredibly smart, and helpful.
3. Always respond in the language the user speaks (Hindi, English, Hinglish, etc.).
"""

# Gemini model ko load karein
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
except Exception as e:
    st.error("⚠️ Model load karne mein dikkat aayi.")
    st.stop()

# ==========================================
# 4. CHAT INTERFACE & HISTORY
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana.")

# Chat history ko maintain rakhne ke liye ekdam sahi syntax
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Purani baatein screen par dikhane ke liye
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# User input box
user_input = st.chat_input("VAAK se kuch bhi puchein...")

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
                st.error("⚠️ Error: Jawab nahi mil paya. Kripya check karein ki Streamlit Secrets mein API Key sahi se save hai ya nahi.")
                
