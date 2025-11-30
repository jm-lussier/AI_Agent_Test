import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# 1. Configure the Page
st.set_page_config(page_title="My Gemini Agent", page_icon="🤖")
st.title("🤖 My First AI Agent")

# 2. Add a Sidebar for the API Key
with st.sidebar:
    api_key = st.text_input("Enter Google API Key:", type="password")
    st.markdown("[Get a key here](https://aistudio.google.com/app/apikey)")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! You can type or speak to me now. How can I help?"}
    ]

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- NEW: VOICE INPUT SECTION ---
# We create a placeholder for the user's input (either text or voice)
user_input = None

# Option A: The standard text box
text_input = st.chat_input("Type your message here...")
if text_input:
    user_input = text_input

# Option B: The microphone button
# This renders a button. When you click it, it records. When you stop, it returns text.
if not user_input:  # Only show voice if they haven't typed yet
    st.write("🎙️ **Speak to your agent:**")
    voice_text = speech_to_text(
        language='en',
        start_prompt="Click to Record",
        stop_prompt="Stop Recording",
        just_once=True,
        key='STT'
    )
    if voice_text:
        user_input = voice_text

# 5. Handle the Input (Text OR Voice)
if user_input:
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check for API Key
    if not api_key:
        st.info("Please add your API key in the sidebar to continue.")
        st.stop()

    # Call Gemini API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = model.generate_content(user_input)
                st.write(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"An error occurred: {e}")
