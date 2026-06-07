import streamlit as st
import requests
import json

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="VAAK AI - The Cosmic Voice", 
    page_icon="🎙️", 
    layout="centered"
)

# Initialize Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 2. SECURITY & KEY INGESTION
# ==========================================
# Production standard: Fetching token from Streamlit Encrypted Secrets Locker
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔒 Security Error: Streamlit Secrets mein 'GEMINI_API_KEY' nahi mila!")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]

# ==========================================
# 3. CORE AI CORE FUNCTION (REST API BACKEND)
# ==========================================
def generate_gemini_response(prompt, history):
    """
    Direct REST API Call: Yeh method Enterprise keys (AQ.Ab8RN...) ko 
    bina kisi validation restriction ke seedhe Google ke server par bypass karta hai.
    """
    # Gemini 1.5 Flash API Endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    # System Instruction for VAAK AI persona
    system_instruction = (
        "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
        "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
        "You possess vast knowledge about world history, science, literature, coding, and philosophy. "
        "Keep your tone friendly, smart, and helpful. Always respond in the language the user speaks (Hindi, English, Hinglish)."
    )
    
    # Constructing Payload with Full Chat Context
    contents = []
    for msg in history:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })
    
    # Current User Input Append
    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_json = response.json()
        
        # Extracting the text response from Google's JSON structure
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in response_json:
            return f"⚠️ API Error ({response_json['error'].get('code')}): {response_json['error'].get('message')}"
        else:
            return "⚠️ Error: Google API se invalid response mila."
            
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ==========================================
# 4. USER INTERFACE (UI) & RENDERING
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Gemini).")

# Render Existing Chat History from Session State
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Entry Point
user_input = st.chat_input("VAAK se Gemini par kuch bhi puchein...")

if user_input:
    # 1. Render and Save User Message
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 2. Trigger Model Inference with Spinner
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            ai_response = generate_gemini_response(user_input, st.session_state.chat_history)
            st.markdown(ai_response)
            
    # 3. Commit both to history for context tracking
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
