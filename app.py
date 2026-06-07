import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="VAAK AI", page_icon="🎙️", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 2. Key Check
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔒 Secrets mein 'GEMINI_API_KEY' nahi mili!")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]

# 3. Super Simple REST Call (No Complex Formatting)
def ask_gemini(user_message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    # Ekdam basic payload jo kabhi fail nahi hota
    payload = {
        "contents": [{
            "parts": [{"text": f"You are VAAK AI, a smart assistant. Respond in Hindi/Hinglish. User says: {user_message}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in res_json:
            return f"⚠️ Google Error: {res_json['error'].get('message')}"
        return "⚠️ Kuch galti hui hai server par."
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# 4. UI
st.title("🎙️ VAAK AI")
st.caption("Powered by Gemini (Official Key)")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Yahan likhein...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            reply = ask_gemini(user_input)
            st.markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
