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
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔒 Security Error: Streamlit Secrets mein 'GEMINI_API_KEY' nahi mila!")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]

# ==========================================
# 3. CORE AI FUNCTION (REST API BACKEND)
# ==========================================
def generate_gemini_response(prompt, history):
    # Google REST API ka absolute correct model path
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
        "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
        "You possess vast knowledge about world history, science, literature, coding, and philosophy. "
        "Keep your tone friendly, smart, and helpful. Always respond in the language the user speaks (Hindi, English, Hinglish)."
    )
    
    contents = []
    # Purani chat history ko sahi format mein jodein
    for msg in history:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })
    
    # Naya message jodein
    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    # Google API standard body structure
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # Jawab nikalne ka professional tarika
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                return candidate["content"]["parts"][0]["text"]
        
        if "error" in response_json:
            return f"⚠️ API Error ({response_json['error'].get('code')}): {response_json['error'].get('message')}"
            
        return "⚠️ Error: Google API se sahi data nahi mil paya."
            
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ==========================================
# 4. USER INTERFACE (UI) & RENDERING
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Gemini).")

# Purani chat history ko screen par dikhayein
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
user_input = st.chat_input("VAAK se Gemini par kuch bhi puchein...")

if user_input:
    # User message rendering
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Assistant response generation
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            ai_response = generate_gemini_response(user_input, st.session_state.chat_history)
            st.markdown(ai_response)
            
    # History update
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
