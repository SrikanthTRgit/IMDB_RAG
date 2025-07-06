import streamlit as st
from datetime import datetime
from llm_chain import retrieval_chain
# Set page configuration
st.set_page_config(
    page_title="🎬 Conversational Movie QA Bot",
    page_icon="🎥",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .chat-bubble {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-width: 80%;
        word-break: break-word;
    }
    .user-bubble {
        background-color: #dff9fb;
        text-align: right;
        margin-left: 20%;
    }
    .assistant-bubble {
        background-color: #f1f2f6;
        text-align: left;
        margin-right: 20%;
    }
    .thinking-bubble {
        background-color: #f6e58d;
        color: #636e72;
        text-align: left;
        margin-right: 20%;
        font-style: italic;
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #95a5a6;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with instructions
with st.sidebar:
    st.title("📖 Instructions")
    st.markdown("""
    - Ask about movies using natural language.
    - Include genres, actors, plot elements, or moods.
    - Try follow-up questions like "Only from the 90s?" or "Anything more recent?"
    """)

# Title and subtitle
st.markdown('<div class="title">🎬 Conversational Movie QA Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find movies using natural language queries</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history (including first user question and assistant answer)
for idx, msg in enumerate(st.session_state.messages):
    role_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Chat input and response
prompt = st.chat_input("Ask about movies...")
if prompt:
    # Show user question immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)
    # Show "thinking..." bubble
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown('<div class="chat-bubble thinking-bubble">Let me find some great movie details for you...</div>', unsafe_allow_html=True)
    # Prepare chat history for retrieval_chain
    chat_history = [
        (m["role"], m["content"])
        for m in st.session_state.messages
        if m["role"] in ["user", "assistant"]
    ]
    try:
        response = retrieval_chain.invoke({"input": prompt, "chat_history": chat_history})
        answer = response.get("answer", "Sorry, I couldn't find an answer.")
    except Exception as e:
        answer = f"Error: {str(e)}"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    thinking_placeholder.empty()
    st.markdown(f'<div class="chat-bubble assistant-bubble">{answer}</div>', unsafe_allow_html=True)

# Footer
st.markdown(f'<div class="footer">© {datetime.now().year} Movie QA Bot | Powered by LangChain & Streamlit | Developed by Srikanth T R</div>', unsafe_allow_html=True)
