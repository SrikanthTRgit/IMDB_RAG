Got it. Here's the updated and standardized `README.md` incorporating the fact that you use an `imdb_data_preprocess.ipynb` notebook to build your persistent Chroma DB.

-----

# 🎬 Conversational Movie AI Assistant

This project develops a prototype system capable of identifying movies from an IMDb dataset based on natural language queries. It leverages a large language model (LLM) and a persistent vector store (Chroma DB), built using the Langchain framework, to provide a conversational interface for movie discovery.

-----

## ✨ Key Features

  * **Natural Language Queries:** Ask about movies using everyday language, even with partial information or subjective descriptions.
  * **Context-Aware Conversations:** The bot remembers previous turns, allowing for natural follow-up questions related to initial queries.
  * **Intelligent Filtering:** Interprets queries to apply relevant filters such as genre, actors, director, and release year, using a combination of DataFrame filtering and vector database metadata filtering.
  * **Persistent Vector Store (Chroma DB):** Utilizes Chroma DB for efficient, persistent, and semantic search. Embeddings are stored on disk, significantly speeding up subsequent application runs by avoiding re-indexing.
  * **Clear Summaries:** Generates concise, natural language summaries of search results, highlighting pertinent details.
  * **Interactive UI:** Provides a user-friendly web interface powered by **Streamlit**.

-----

## 🚀 Get Started

Follow these steps to set up and run the Movie AI Assistant on your local machine.

### 📋 Prerequisites

Before you begin, ensure you have:

  * **Python 3.8+** installed.
  * Access to an **Azure OpenAI Service** deployment with models like `gpt-4o` (or your chosen models) for both chat and embeddings.

### 📦 Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/movie-qa-bot.git
    cd movie-qa_bot
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    All required libraries are listed in `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

    Your `requirements.txt` file should contain:

    ```
    streamlit
    langchain
    langchain-openai
    python-dotenv
    pandas
    pydantic
    chromadb
    jupyter # Required to run the preprocessing notebook
    ```

4.  **Configure Azure OpenAI Credentials:**
    Create a file named `.env` in the root directory of your project (`movie_qa_bot/`). Add your Azure OpenAI service details to this file, referencing the `.env.example` provided:

    ```
    AZURE_OPENAI_API_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
    AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_KEY"
    AZURE_OPENAI_API_VERSION="2024-02-15-preview" # Use your specific API version
    AZURE_OPENAI_API_EMBEDDINGS_ENDPOINT="YOUR_AZURE_OPENAI_EMBEDDINGS_ENDPOINT
    ```

    *Replace the placeholder values with your actual Azure OpenAI credentials.*

5.  **Prepare the IMDb Dataset:**

      * Create a directory named `data/` in the root of your project:
        ```bash
        mkdir data
        ```
      * Download your IMDb movie dataset (e.g., a CSV or JSON file). For a quick start, use a **smaller subset** (e.g., 10,000-20,00 rows) as generating embeddings for very large datasets can be time-consuming and resource-intensive.
      * Place your downloaded raw data file (e.g., `movies.json` or `imdb_movies_subset.csv`) inside the `data/` directory.

### ▶️ Build the Vector Database (Crucial First Step\!)

**Before running the Streamlit application for the first time, you must process your raw IMDb data and build the persistent Chroma DB.** This is handled by the provided Jupyter notebook.

1.  **Start Jupyter Notebook:**

    ```bash
    jupyter notebook
    ```

    Your web browser will open to the Jupyter interface.

2.  **Run `imdb_data_preprocess.ipynb`:**

      * Navigate to and open `imdb_data_preprocess.ipynb` in your Jupyter environment.
      * Follow the instructions within the notebook. It will guide you through:
          * Loading your raw IMDb JSON/CSV file.
          * Preprocessing the data.
          * Splitting the text into manageable chunks (if necessary).
          * Generating embeddings using Azure OpenAI.
          * Loading these embeddings and associated metadata into the **persistent Chroma DB** in the `chroma_db/` directory.

    **Ensure the notebook runs completely without errors.** This step will create the `chroma_db/` directory in your project root, which `Retriver.py` will then load.

### ▶️ Run the Application

Once the Chroma DB has been successfully built by the notebook:

```bash
streamlit run main_app.py
```

This command will open the Streamlit application in your web browser. Subsequent runs will be much faster as the Chroma DB is loaded directly from disk.

-----

## 🎬 How to Use

Simply type your questions or requests about movies into the chat input box at the bottom of the screen.

**Here are some examples of what you can ask:**

  * "Find me a sci-fi movie."
  * "What movies star Tom Hanks?"
  * "Suggest a comedy from the 1990s Telugu."
  * "Tell me about movies directed by SS Rajamoli.n."
  * "Are there any thrilling dramas about space?"
  * "What about more like that last one?" (Example of a follow-up question)

-----

## 📁 Project Structure

The project is organized into the following directories and files:
 ```
movie_qa_bot/
├── main.py                     # The core Streamlit application.
├── Retriver.py                 # Contains the `Retriever` class for data loading and retrieval from Chroma DB.
├── llm_chain.py                # Contains LLM and Langchain chain definitions and logic
├── .env.example                # Template for environment variables.
├── requirements.txt            # Lists all Python dependencies.
├── README.md                   # This project documentation file.
├── imdb_data_preprocess.ipynb  # Jupyter notebook for initial data preprocessing and building the Chroma DB.
├── data/                       # Directory for your raw IMDb dataset.
│   └── imdb_movies_subset.csv  # Example raw dataset file (or .json).
├── chroma_db/                  # Directory where Chroma DB persists its data (automatically created by the notebook).
├── Add-on_langraph_Agent.py    # Additional langraph Agent
 ```
-----

## 📐 Design & Architecture Highlights

This Movie AI Assistant is built upon the **Langchain framework**, enabling a modular and robust design:

  * **Streamlit User Interface (`main_app.py`):** Provides an intuitive and interactive chat experience for users.
  * **Azure OpenAI LLM:** An LLM (e.g., `gpt-4o`) powers the natural language understanding, conversational context management, and answer generation.
  * **Prompt Templates:**
      * **History-Aware Prompt (`retriever_prompt`):** Used to rephrase user queries based on the conversation history, making retrieval more accurate.
      * **QA Prompt (`qa_prompt`):** Formulates the LLM's final response by integrating the retrieved movie information into a natural language answer.
  * **Conversation Memory (`ConversationBufferMemory`):** Stores the ongoing chat history, allowing the bot to maintain context and handle follow-up questions seamlessly.
  * **Data Preprocessing Notebook (`imdb_data_preprocess.ipynb`):** This dedicated notebook handles the crucial initial steps:
      * Loading raw IMDb data (e.g., from a JSON file).
      * Performing necessary data cleaning and text splitting.
      * Generating embeddings for the processed movie information.
      * **Building and persisting the Chroma DB** to disk, making the vector store ready for use by the main application.
  * **Custom Retriever (`Retriver.py`):** This is the crucial component for data access during runtime. It's responsible for:
      * Loading the necessary movie metadata into a Pandas DataFrame for efficient structured filtering.
      * **Loading the pre-built persistent Chroma DB** from the disk (created by the notebook).
      * Implementing a sophisticated `get_relevant_documents` method that intelligently applies structured filters (e.g., genre, actor, year) to narrow down the dataset *before* performing a vector-based semantic search on the relevant subset via Chroma DB's `similarity_search` with a `where` clause. This combined approach ensures highly precise and relevant results.
  * **Langchain Chains:** Different Langchain "chains" orchestrate the flow:
      * `create_history_aware_retriever`: Adapts user queries considering past interactions.
      * `create_stuff_documents_chain`: Feeds the retrieved movie information into the LLM's context for answer synthesis.
      * `create_retrieval_chain`: Combines the history-aware retrieval and document summarization steps into a single, cohesive process.

-----

## 🌟 Evaluation Criteria

This project is designed as an intense, rapid development challenge that prioritizes your approach to problem-solving and innovation. The evaluation focuses on:

  * **Thought Process and Problem-Solving:** How you tackled the complex requirements and technical challenges.
  * **Design Decisions & Trade-offs:** Your ability to articulate choices made in architecture, LLM usage, and data handling (including the choice of Chroma DB and the separate preprocessing step).
  * **Documentation Quality:** The clarity and completeness of the project's documentation.
  * **Scalability Potential:** The system's inherent potential for handling larger datasets and more complex queries, beyond its current prototype accuracy.

-----

## 🔮 Future Enhancements

This prototype can be significantly expanded. Here are some ideas for future development:

  * **Advanced Filter Extraction:** Integrate a more robust method for extracting structured filters from user queries, potentially using a dedicated LLM call with a Pydantic-based output parser.
  * **Refined Result Ranking:** Implement custom logic for ranking retrieved movies based on factors like IMDb rating, popularity, or specific relevance metrics.
  * **Interactive Filter UI:** Allow users to see and modify the filters the bot has identified from their query directly within the Streamlit interface.
  * **Enhanced Error Handling & Feedback:** Provide more specific error messages and proactive suggestions to the user when queries are unclear or fail.
  * **Live Data Integration:** Explore integrating with live IMDb APIs (respecting API limits) for the most up-to-date movie information.
  * **Containerization:** Package the application using Docker for easier deployment and portability.
  * **Distributed ChromaDB:** For very large-scale production deployments, consider a distributed ChromaDB setup.

-----

**Disclaimer:** This is a prototype system. Its accuracy and performance are directly influenced by the quality and size of the IMDb dataset used, the capabilities of the LLM, and the robustness of the `Retriver.py` implementation.



