import streamlit as st
import google.generativeai as genai

# 1. Configure Page
st.set_page_config(page_title="Gemini Voice Agent", page_icon="🎙️")
st.title("🎙️ Gemini Voice Agent")

# 2. Sidebar API Key
with st.sidebar:
    api_key = st.text_input("Enter Google API Key:", type="password")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Speak or type. I can hear you!"}
    ]

# 4. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- INPUT AREA ---
# We create a container so the mic and text box don't clutter the screen
with st.container():
    # A. Text Input
    text_prompt = st.chat_input("Type a message...")
    
    # B. Audio Input (Native Streamlit Widget)
    # This creates a built-in mic button
    audio_file = st.audio_input("Or speak to me")

# --- LOGIC ---
user_input = None
is_audio = False

# Determine if user typed or spoke
if text_prompt:
    user_input = text_prompt
elif audio_file:
    user_input = audio_file
    is_audio = True

if user_input:
    # 1. Show User Input
    with st.chat_message("user"):
        if is_audio:
            st.audio(user_input)  # Play back what you said
            st.write("*(Voice Message)*")
        else:
            st.write(user_input)
    
    # Add to history (we store a placeholder for audio in history to keep it simple)
    st.session_state.messages.append({"role": "user", "content": "*(Voice Message)*" if is_audio else user_input})

    # 2. Check API Key
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
        st.stop()

    # 3. Call Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        with st.chat_message("assistant"):
            with st.spinner("Listening & Thinking..."):
                # MAGIC: We send the audio file DIRECTLY to Gemini!
                # It "hears" the audio without us needing to transcribe it first.
                if is_audio:
                    # Create a dictionary for the audio blob
                    audio_bytes = user_input.read()
                    response = model.generate_content([
                        "Listen to this audio and respond naturally to the user.",
                        {"mime_type": "audio/wav", "data": audio_bytes}
                    ])
                else:
                    # Standard text chat
                    response = model.generate_content(user_input)
                
                st.write(response.text)
        
        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {e}")
