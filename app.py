import streamlit as st
import google.generativeai as genai

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
# 2. SECURITY & GOOGLE AI CONFIGURATION
# ==========================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔒 Security Error: Streamlit Secrets mein 'GEMINI_API_KEY' nahi mila!")
    st.stop()

# Configure the official Google SDK
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==========================================
# 3. CORE AI FUNCTION (OFFICIAL SDK METHOD)
# ==========================================
def generate_gemini_response(history):
    system_instruction = (
        "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
        "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
        "Keep your tone friendly, smart, and helpful. Always respond in the language the user speaks (Hindi, English, Hinglish)."
    )
    
    try:
        # Initializing the model using official Google SDK configuration
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # Formatting history structure for the official SDK
        formatted_messages = []
        for msg in history:
            formatted_messages.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })
            
        response = model.generate_content(formatted_messages)
        
        if response.text:
            return response.text
        return "⚠️ Error: Model se response nahi mil paya."
        
    except Exception as e:
        return f"⚠️ SDK Error: {str(e)}"

# ==========================================
# 4. USER INTERFACE (UI) & RENDERING
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Gemini).")

# Sidebar settings for user flexibility
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.sidebar.success("History cleared!")
        st.rerun()

# Render existing chat logs
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Interface Entry Point
user_input = st.chat_input("VAAK se Gemini par kuch bhi puchein...", key="vaak_chat_input")

if user_input:
    # Render user prompt locally
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Store context in runtime engine state
    st.session_state.chat_history.append({"role": "user", "content": user_input})
        
    # Trigger model container interface pipeline
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            ai_response = generate_gemini_response(st.session_state.chat_history)
            st.markdown(ai_response)
            
    # Conditional stack validation for transaction history integrity
    if not ai_response.startswith("⚠️"):
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    else:
        st.session_state.chat_history.pop()
