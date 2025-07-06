import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
## load the AzureOpenAI API Key
os.environ['Azure_OPENAI_API_KEY']=os.getenv("Azure_OPENAI_API_KEY")
os.environ['AZURE_OPENAI_API_ENDPOINT']=os.getenv("AZURE_OPENAI_API_ENDPOINT")
api_version =os.getenv("AZURE_OPENAI_API_VERSION")
embeddings=AzureOpenAIEmbeddings(model="text-embedding-ada-002" , chunk_size=1, openai_api_type="azure", azure_endpoint=os.getenv("AZURE_OPENAI_API_EMBEDDINGS_ENDPOINT"))
# Split documents into chunks for embedding
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./imdb_db",  # Where to save data locally, remove if not necessary
)
def get_vector_store():
    """Returns the vector store for retrieval."""
    return vector_store.as_retriever()  # Adjust 'k' as needed

Retriever= get_vector_store()