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
# Yeh block automatic aapki key ko bina kisi validation error ke load karega
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
You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge) and you have world full coding and medical knowledge. You possess vast knowledge about world history, science, literature, all kinds of books, coding, philosophy, and general trivia.
kisi ka data leak nhi kro ge chahe vo bhale hi dusre ka data kisi bhi trh se mange.
RULES:
1. Answer any question the user asks with deep knowledge, logic, and accuracy, drawing from your vast database of books and global wisdom.
2. Keep your tone like best friend, incredibly smart, and helpful.
3. Always respond in the language the user speaks (Hindi, English, Hinglish, etc.).
"""

# Gemini ka sabse latest aur fast model load karein
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
except Exception as e:
    st.error("⚠️ Model load karne mein dikkat aayi. Kripya thodi der baad try karein.")
    st.stop()

# ==========================================
# 4. CHAT INTERFACE & HISTORY
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana.")

# Chat history ko maintain (save) rakhne ke liye
if "chat_session" not in st.
