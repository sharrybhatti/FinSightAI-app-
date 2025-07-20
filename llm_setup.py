# llm_setup.py

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

# --- Load Environment Variables ---
load_dotenv()

# --- Global LLM Instances ---
# These will be initialized by the function below
embedding_llm = None
llm = None

def initialize_llms():
    """
    Initializes Azure OpenAI Embedding and Chat LLMs.
    Sets the global embedding_llm and llm variables.
    """
    global embedding_llm, llm
    try:
        embedding_llm = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        print("AzureOpenAIEmbeddings initialized successfully.")

        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=1500,
        )
        print("AzureChatOpenAI (chat model) initialized successfully.")
        return True
    except Exception as e:
        print(f"Error initializing LLMs: {e}")
        # Reset LLMs to None if initialization fails
        embedding_llm = None
        llm = None
        return False

# Call initialization when this module is imported
# This ensures LLMs are ready when rag_pipeline.py imports them
if not initialize_llms():
    print("LLM setup failed during module import. Check your .env configuration.")

