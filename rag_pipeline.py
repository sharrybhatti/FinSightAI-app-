# rag_pipeline.py

import os
from dotenv import load_dotenv

# LangChain Imports
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Import utility functions
from utils import get_filings
# Import LLMs and the initialization function from the new llm_setup.py
from llm_setup import embedding_llm, llm, initialize_llms 

# --- Load Environment Variables ---
load_dotenv() # Still load in rag_pipeline in case other parts need it

# --- Global Chain and Vectorstore Instances ---
# LLMs are now managed in llm_setup.py
conversational_qa_chain = None
vectorstore = None

# --- Configuration ---
SEC_API_KEY = os.getenv("SEC_API_KEY") # Get SEC API key from environment
TICKERS = ["AAPL", "MSFT", "TSLA"]
FAISS_FOLDER_NAME = f"faiss_{'_'.join(TICKERS)}_10K"

# Define a custom prompt to guide the LLM's response
QA_TEMPLATE = """You are a senior financial analyst working for Finsight AI.
Your job is to analyze SEC filings, risk factors, and financial statements.
Use the following pieces of context to answer the user's question.
If you don't know the answer based on the provided context, politely state that you cannot find the information in the available filings.
Provide professional, concise, and data-backed summaries.

Context: {context}
Question: {question}

Answer:"""
QA_PROMPT = PromptTemplate(
    template=QA_TEMPLATE, input_variables=["context", "question"]
)

# Removed initialize_llms() function from here, it's now in llm_setup.py

def prepare_and_load_vectorstore():
    """
    Prepares documents, splits them into chunks, and builds/loads the FAISS vector store.
    """
    global vectorstore
    # Check if embedding_llm is initialized (from llm_setup.py)
    if embedding_llm is None:
        print("Embedding LLM not initialized. Cannot prepare documents or vectorstore.")
        return False

    all_documents = []
    print("\nPreparing Documents and Splitting into Chunks...")
    for tkr in TICKERS:
        text, url = get_filings(tkr, SEC_API_KEY) # Pass SEC_API_KEY to get_filings
        doc = Document(page_content=text, metadata={"ticker": tkr, "source": url})
        all_documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_documents)
    print(f"Split {len(all_documents)} documents into {len(chunks)} chunks.")

    print(f"\nBuilding/Loading FAISS Index for '{FAISS_FOLDER_NAME}'...")
    if os.path.exists(FAISS_FOLDER_NAME):
        print(f"Loading FAISS index from {FAISS_FOLDER_NAME}...")
        try:
            vectorstore = FAISS.load_local(FAISS_FOLDER_NAME, embedding_llm, allow_dangerous_deserialization=True)
            print("FAISS index loaded successfully.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}. Recreating...")
            vectorstore = FAISS.from_documents(chunks, embedding_llm)
            vectorstore.save_local(FAISS_FOLDER_NAME)
            print("FAISS index recreated and saved.")
    else:
        print(f"Creating FAISS index and saving to {FAISS_FOLDER_NAME}...")
        vectorstore = FAISS.from_documents(chunks, embedding_llm)
        vectorstore.save_local(FAISS_FOLDER_NAME)
        print("FAISS index created and saved.")
    
    return True

def setup_conversational_chain():
    """Sets up the Conversational RetrievalQA Chain with memory."""
    global conversational_qa_chain
    # Check if llm and vectorstore are initialized
    if llm is None or vectorstore is None:
        print("Chat LLM or Vectorstore not initialized. Cannot set up conversational chain.")
        return False

    print("\nSetting up Conversational RetrievalQA Chain (with memory)...")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    conversational_qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )
    print("ConversationalRetrievalChain initialized with memory.")
    return True

def query_finsight_ai_rag(prompt: str, chat_history: list = None) -> dict:
    """
    Queries the Finsight AI RAG pipeline for financial analysis tasks,
    including document retrieval and conversational memory.

    Args:
        prompt (str): The user input or query.
        chat_history (list, optional): List of LangChain messages (HumanMessage, AIMessage)
                                      for conversational context. Defaults to an empty list.

    Returns:
        dict: A dictionary containing the model's 'answer' and 'source_documents'.
    """
    if conversational_qa_chain is None:
        return {"answer": "Ã¢ÂÅ’ Error: RAG pipeline not initialized. Please restart the application.", "source_documents": []}

    if chat_history is None:
        chat_history = []

    try:
        result = conversational_qa_chain.invoke(
            {"question": prompt, "chat_history": chat_history}
        )
        answer = result.get("answer", "Ã¢Å¡Â Ã¯Â¸Â No answer returned.")
        source_docs = result.get("source_documents", [])
        
        return {"answer": answer, "source_documents": source_docs}

    except Exception as e:
        print(f"Error during AI query: {str(e)}")
        return {"answer": f"Ã¢ÂÅ’ Error during AI query: {str(e)}", "source_documents": []}

# --- Initialization on module load ---
# Call the initialization from llm_setup.py first
# Then proceed with preparing the vectorstore and setting up the chain
if initialize_llms(): # This call sets the global embedding_llm and llm
    if prepare_and_load_vectorstore():
        setup_conversational_chain()
    else:
        print("Vectorstore setup failed. RAG pipeline will not be fully functional.")
else:
    print("LLMs failed to initialize. RAG pipeline will not be functional.")

