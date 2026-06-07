import streamlit as st
from groq import Groq

# ==========================================
# 1. WEBSITE CONFIGURATION (LOOK & FEEL)
# ==========================================
st.set_page_config(
    page_title="VAAK AI - The Cosmic Voice", 
    page_icon="🎙️", 
    layout="centered"
)

# ==========================================
# 2. SECURITY & CLIENT INITIALIZATION
# ==========================================
# Streamlit secrets se Groq API Key check aur initialize karein
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔒 Security Error: Streamlit Secrets mein 'GROQ_API_KEY' nahi mila!")
    st.stop()

# Groq ka official client initialize karein
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 3. CHAT INTERFACE & HISTORY
# ==========================================
st.title("🎙️ VAAK AI")
st.caption("The Cosmic Voice: Duniya ki saari books aur gyaan ka ek hi thikana (Powered by Groq).")

# System instruction jo AI ko smart banayegi
system_prompt = (
    "You are VAAK AI, a highly intelligent, universal, and all-knowing AI Assistant "
    "inspired by the ancient Vedic concept of 'Vak' (The Cosmic Voice & Absolute Knowledge). "
    "You possess vast knowledge about world history, science, literature, all kinds of books, "
    "coding, philosophy, and general trivia. Keep your tone friendly, smart, and helpful. "
    "Always respond in the language the user speaks (Hindi, English, Hinglish, etc.)."
)

# Chat history ko maintain rakhne ke liye safe structure
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Purani baatein screen par dikhane ke liye (System prompt ko chhupakar)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User se naya sawal lene ke liye input box
user_input = st.chat_input("VAAK se kuch bhi puchein (Books, History, Science, Coding...)...")

if user_input:
    # 1. User ka message screen par dikhayein aur save karein
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. AI se live jawab mangein
    with st.chat_message("assistant"):
        with st.spinner("VAAK soch raha hai..."):
            try:
                # Groq ka sabse naya aur powerful model: Llama 3 8B
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama3-8b-8192",
                )
                
                # Jawab ko extract karein aur screen par dikhayein
                reply = chat_completion.choices[0].message.content
                st.markdown(reply)
                
                # Assistant ke jawab ko history mein save karein
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error("⚠️ Error: Response lene mein dikkat aayi. Kripya check karein ki Secrets mein GROQ_API_KEY sahi hai ya nahi.")
