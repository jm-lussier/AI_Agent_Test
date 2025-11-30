import streamlit as st
import google.generativeai as genai

# 1. Configure the Page
st.set_page_config(page_title="My Gemini Agent", page_icon="🤖")
st.title("🤖 My First AI Agent")

# 2. Add a Sidebar for the API Key (Secure way)
with st.sidebar:
    api_key = st.text_input("Enter Google API Key:", type="password")
    st.markdown("[Get a key here](https://aistudio.google.com/app/apikey)")

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you?"}
    ]

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if API Key is present
    if not api_key:
        st.info("Please add your API key in the sidebar to continue.")
        st.stop()

    # Call Gemini API
    try:
        genai.configure(api_key=api_key)
        # SWAP MODEL NAME HERE if you want to use a different version
        model = genai.GenerativeModel('gemini-3-pro-preview') 
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)
                st.write(response.text)
        
        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"An error occurred: {e}")
