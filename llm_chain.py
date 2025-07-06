import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from Retriver import Retriever

# Load environment variables
load_dotenv()

# Initialize LLM
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment="gpt-4o",
    model="gpt-4o"
)

# Prompt templates
retriever_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for answering questions about movies provide."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """"You are a helpful and engaging movie recommendation assistant.
    Based on the following list of movies, answer the user's question.
    If no relevant movies are found, politely inform the user.
    When listing movies, provide their title, release year, and a very brief summary/description.
    Format the movie list clearly"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("user", "{context}")
])

# Memory
memory = ConversationBufferMemory(return_messages=True)

# Retriever
history_aware_retriever = create_history_aware_retriever(
    llm=llm,
    retriever=Retriever,
    prompt=retriever_prompt
)

# QA chain
document_chain = create_stuff_documents_chain(llm, qa_prompt)
retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
