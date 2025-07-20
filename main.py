import streamlit as st
from module_llm import run_finetuned_llm
from module_multimodel import run_multimodal_extraction

st.set_page_config(page_title="Finsight AI", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page):
    st.session_state.page = page

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e3f2fd, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .logo:hover {
        transform: rotate(5deg) scale(1.05);
    }
    .title {
        text-align: center;
        font-size: 52px;
        font-weight: 700;
        color: #004d61;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 22px;
        color: #555;
        margin-bottom: 50px;
    }
    .card {
        background: #ffffff;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        border: 1px solid #e0e0e0;
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
        color: #00796b;
        margin-bottom: 12px;
    }
    .card-desc {
        font-size: 16px;
        color: #555;
        margin-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Landing Page ---
if st.session_state.page == "home":
    st.markdown("<img src='https://dummyimage.com/200x200/00796b/ffffff&text=Finsight+AI' class='logo'>", unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Welcome to Finsight AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-powered Financial Forecasting & Multimodal Analysis</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c1, c2 = st.columns(2, gap="large")

        with c1:
            if st.button("🤖 Fine‑Tuned LLM", use_container_width=True):
                switch_page("finetuned_llm")
            st.markdown(
                """
                <div class='card' onclick="window.location.href='#'">
                    <div style='font-size:42px;'>🤖</div>
                    <div class='card-title'>Fine‑Tuned LLM</div>
                    <div class='card-desc'>Ask complex financial questions with our fine‑tuned AI model.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            if st.button("📊 Multimodal Data Extraction", use_container_width=True):
                switch_page("multimodal_extraction")
            st.markdown(
                """
                <div class='card'>
                    <div style='font-size:42px;'>📊</div>
                    <div class='card-title'>Multimodal Data Extraction</div>
                    <div class='card-desc'>Upload reports, extract text, tables, and visuals effortlessly.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Fine‑Tuned LLM Module ---
elif st.session_state.page == "finetuned_llm":
    run_finetuned_llm()
    if st.button("⬅️ Back to Home"):
        switch_page("home")

# --- Multimodal Data Extraction Module ---
elif st.session_state.page == "multimodal_extraction":
    run_multimodal_extraction()
    if st.button("⬅️ Back to Home"):
        switch_page("home")
