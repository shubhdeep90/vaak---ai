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
# 3. CORE AI FUNCTION (UPGRADED TO 1.5 FLASH)
# ==========================================
def generate_gemini_response(history):
    # Upgraded to stable 'gemini-1.5-flash' endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
        "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
        "Keep your tone friendly, smart, and helpful. Always respond in the language the user speaks (Hindi, English, Hinglish)."
    )
    
    contents = []
    for msg in history:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })
    
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # Safe Data Extraction
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                return candidate["content"]["parts"][0]["text"]
        
        if "error" in response_json:
            return f"⚠️ API Error ({response_json['error'].get('code')}): {response_json['error'].get('message')}"
            
        return "⚠️ Error: Google API se valid response nahi mila."
            
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ==========================================
# 4. USER INTERFACE (UI) & RENDERING
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Gemini).")

# Purani saari chat screen par render karna
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
user_input = st.chat_input("VAAK se Gemini par kuch bhi puchein...")

if user_input:
    # 1. Screen par user ka message dikhao
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. History mein temporary save karo taaki AI sawal samajh sake
    st.session_state.chat_history.append({"role": "user", "content": user_input})
        
    # 3. Assistant ka response generate karna
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            ai_response = generate_gemini_response(st.session_state.chat_history)
            st.markdown(ai_response)
            
    # 4. Professional Fix: Agar response sahi hai, tabhi permanently save karo aur rerun karo
    if not ai_response.startswith("⚠️"):
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        # UI refresh state update karne ke liye
        st.rerun()
    else:
        # Agar API fail ho gayi, toh user ka chhutaa hua sawal bhi history se hata do taaki data clean rahe
        st.session_state.chat_history.pop()
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
# 3. CORE AI FUNCTION (UPGRADED TO 1.5 FLASH)
# ==========================================
def generate_gemini_response(history):
    # Upgraded to stable 'gemini-1.5-flash' endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
        "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
        "Keep your tone friendly, smart, and helpful. Always respond in the language the user speaks (Hindi, English, Hinglish)."
    )
    
    contents = []
    for msg in history:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })
    
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        
        # Safe Data Extraction
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                return candidate["content"]["parts"][0]["text"]
        
        if "error" in response_json:
            return f"⚠️ API Error ({response_json['error'].get('code')}): {response_json['error'].get('message')}"
            
        return "⚠️ Error: Google API se valid response nahi mila."
            
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# ==========================================
# 4. USER INTERFACE (UI) & RENDERING
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Gemini).")

# Purani saari chat screen par render karna
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
user_input = st.chat_input("VAAK se Gemini par kuch bhi puchein...")

if user_input:
    # 1. Screen par user ka message dikhao
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 2. History mein temporary save karo taaki AI sawal samajh sake
    st.session_state.chat_history.append({"role": "user", "content": user_input})
        
    # 3. Assistant ka response generate karna
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            ai_response = generate_gemini_response(st.session_state.chat_history)
            st.markdown(ai_response)
            
    # 4. Professional Fix: Agar response sahi hai, tabhi permanently save karo aur rerun karo
    if not ai_response.startswith("⚠️"):
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        # UI refresh state update karne ke liye
        st.rerun()
    else:
        # Agar API fail ho gayi, toh user ka chhutaa hua sawal bhi history se hata do taaki data clean rahe
        st.session_state.chat_history.pop()
        
