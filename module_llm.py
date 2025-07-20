import streamlit as st
from rag_pipeline import query_finsight_ai_rag
from langchain_core.messages import HumanMessage, AIMessage

def run_finetuned_llm():
    st.title("📈 Finsight AI: Your Financial Analyst Assistant")
    st.markdown("Ask questions about SEC filings (10‑K for AAPL, MSFT, TSLA) and financial statements.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("Sources Used"):
                        for i, doc in enumerate(message["sources"]):
                            st.write(f"**Source {i+1}:**")
                            st.write(f"  **Ticker:** {doc.metadata.get('ticker', 'N/A')}")
                            st.write(f"  **Source URL:** {doc.metadata.get('source', 'N/A')}")
                            st.markdown(f"  **Content (excerpt):** {doc.page_content[:300]}...")

    if user_query := st.chat_input("Ask a financial question..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Finsight AI is thinking..."):
            langchain_chat_history = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    langchain_chat_history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_chat_history.append(AIMessage(content=msg["content"]))

            response_dict = query_finsight_ai_rag(user_query, langchain_chat_history)
            ai_response_content = response_dict["answer"]
            source_documents = response_dict["source_documents"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response_content,
                "sources": source_documents
            })

            with st.chat_message("assistant"):
                st.markdown(ai_response_content)
                if source_documents:
                    with st.expander("Sources Used"):
                        for i, doc in enumerate(source_documents):
                            st.write(f"**Source {i+1}:**")
                            st.write(f"  **Ticker:** {doc.metadata.get('ticker', 'N/A')}")
                            st.write(f"  **Source URL:** {doc.metadata.get('source', 'N/A')}")
                            st.markdown(f"  **Content (excerpt):** {doc.page_content[:300]}...")

    st.sidebar.title("Options")
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Finsight AI provides financial analysis based on SEC filings. Verify with official sources.")
