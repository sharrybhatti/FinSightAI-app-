import streamlit as st
from llama_parse import LlamaParse
from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
import os, pickle, hashlib
from dotenv import load_dotenv

load_dotenv()

def run_multimodal_extraction():
    st.set_page_config(page_title="Annual Report Query App", layout="wide", initial_sidebar_state="collapsed")
    st.title(":bookmark_tabs: PDF Query App")
    st.markdown("### Upload a PDF to extract content and query it!")

    # Parser with table extraction enabled
    parser = LlamaParse(
        result_type="markdown",
        use_vendor_multimodal_model=True,
        extract_tables=True,
        vendor_multimodal_model_name="anthropic-sonnet-3.5",
        api_key=os.getenv('LLAMAPARSE_API_KEY')
    )

    # Azure OpenAI LLM
    llm = AzureOpenAI(
        engine='gpt-4o',  # from first working code
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    # Azure OpenAI Embeddings
    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    Settings.llm = llm
    Settings.embed_model = embed_model

    def extract_text_nodes(json_list):
        return [TextNode(text=page["md"], metadata={"page": page["page"]}) for page in json_list]

    def process_pdf(pdf_path):
        json_objs = parser.get_json_result(pdf_path)
        return extract_text_nodes(json_objs[0]["pages"])

    def save_index(index, file_path):
        with open(file_path, "wb") as f:
            pickle.dump(index, f)

    def load_index(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def get_file_hash(file):
        file.seek(0)
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)
        return file_hash

    uploaded_file = st.file_uploader(":open_file_folder: Upload your PDF", type="pdf")

    if uploaded_file:
        file_hash = get_file_hash(uploaded_file)
        vector_index_file = f"{file_hash}_vector_index.pkl"

        if not os.path.exists(vector_index_file):
            with st.spinner(":hourglass: Parsing PDF..."):
                with open("uploaded_file.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                docs = process_pdf("uploaded_file.pdf")
                index = VectorStoreIndex(docs)
                save_index(index, vector_index_file)
            st.success(":white_check_mark: PDF parsed and index created successfully!")
        else:
            with st.spinner(":hourglass: Loading stored index..."):
                index = load_index(vector_index_file)
            st.success(":white_check_mark: Loaded existing index for this PDF!")

        query = st.text_input("Enter your query:", placeholder="Type your question here...")

        if query:
            with st.spinner(":mag: Fetching response..."):
                query_engine = index.as_query_engine(similarity_top_k=5)
                response = query_engine.query(query)

            st.markdown("### :memo: LLM Answer")
            st.info(response.response)

            st.markdown("### :page_with_curl: Extracted Content (Tables & Text)")
            for i, node in enumerate(response.source_nodes, start=1):
                with st.expander(f"Source {i} (Page {node.node.metadata.get('page', 'N/A')})"):
                    st.markdown(node.node.get_content(), unsafe_allow_html=True)
