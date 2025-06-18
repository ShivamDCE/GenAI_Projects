import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background: #000000;
        max-width: 1200px;
        margin: 0 auto;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    .stChatMessage {
        max-width: 90%;
        margin: 0 auto;
    }
    
    .stChatMessage [data-testid="stChatMessageContent"] {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 0.5rem;
    }
    
    .stChatInput {
        position: relative;
        width: 90%;
        max-width: 1000px;
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 4px;
        margin: 2rem auto;
    }
    
    .stButton button {
        background-color: #333333;
        color: white;
        border: none;
        width: 200px;
        margin: 0 auto;
        display: block;
    }
    
    .heading1 {
        color: #000000;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 4px;
    }
    
    .heading2 {
        color: #ffffff;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .heading3 {
        color: #ffffff;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stTextInput input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: none;
        width: 100%;
    }

    /* Hide all unnecessary elements */
    .stDeployButton, 
    .stAppViewContainer > div:first-child,
    .stChatMessageContent > div:first-child {
        display: none;
    }

    /* Make the app container wider */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Adjust the main container */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    /* Chat container */
    .chat-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2rem 0;
    }

    /* Clear chat button container */
    .clear-chat-container {
        text-align: center;
        margin-top: 1rem;
    }

    /* Message container */
    .message-container {
        max-height: 50vh;
        overflow-y: auto;
        margin: 2rem auto;
        width: 90%;
        max-width: 1000px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

def get_ai_response(message, history):
    """
    Get response from Groq API
    Args:
        message (str): User message
        history (list): Chat history
    Returns:
        str: AI response
    """
    # Add user message to history
    history.append({
        "role": "user",
        "content": message
    })
    
    # Get response from Groq
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama-3.3-70b-versatile"
    )
    
    # Get the response content
    response = chat_completion.choices[0].message.content
    
    # Add assistant response to history
    history.append({
        "role": "assistant",
        "content": response
    })
    
    return response

# Page layout
st.markdown('<div class="heading1">Jarvis AI LLM Powered bot</div>', unsafe_allow_html=True)
st.markdown('<div class="heading2">Capable to converse</div>', unsafe_allow_html=True)
st.markdown('<div class="heading3">How can I help you today?</div>', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Message container
st.markdown('<div class="message-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(prompt, st.session_state.messages)
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Clear chat button
st.markdown('<div class="clear-chat-container">', unsafe_allow_html=True)
if st.button("Clear Chat", use_container_width=False):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 