from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from Retriver import vector_store
from llm_chain import llm 
import uuid
import streamlit as st
checkpoint = MemorySaver()

@tool
def Retriver(Query: str) -> str:
    """    Retrieve information from the vector store based on the question.
    Args:
        Query (str): The question to ask the vector store."""
    # This function retrieves information from the vector store based on the question.

    return vector_store.similarity_search(Query, k=1)

llm=llm.bind_tools([Retriver])

prompt = """You are a helpful and engaging movie recommendation assistant.
    Based on the following list of movies, answer the user's question.
    If no relevant movies are found, politely inform the user.
    When listing movies, provide their title, release year, and a very brief summary/description.
    Format the movie list clearly, and ask the user if they need more information or have any other questions."""



agent = create_react_agent(
    model=llm,
    tools=[Retriver],
    prompt=prompt,
    checkpointer=checkpoint,
)
config = {"configurable": {"thread_id": str(uuid.uuid4())}}




st.set_page_config(page_title="Movie QA Bot", page_icon="🎬")
st.title("🎬 Movie QA Bot")
st.write("Ask me anything about movies!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    response = agent.invoke({'messages': st.session_state.chat_history}, config=config)
    # The response may be a dict with 'messages' key, or just a message object.
    # Adjust accordingly:
    if isinstance(response, dict) and 'messages' in response:
        ai_message = response['messages'][-1]
    else:
        ai_message = response
    st.session_state.chat_history.append(ai_message)
    st.session_state.user_input = ""  # Clear input

# Display chat history
for msg in st.session_state.chat_history:
    if hasattr(msg, "content"):
        if isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        else:
            st.markdown(f"**AI:** {msg.content}")
            
# To run this Streamlit app, save this file and run:
# streamlit run ./Add-on_langraph_Agent/Langgraph_Agent.py