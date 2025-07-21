# Finsight AI

**AI-Powered Financial Forecasting & Risk Management Platform**

Finsight AI is an advanced AI-driven platform designed to streamline financial analysis, forecasting, and decision-making for **banks, financial institutions, and credit rating agencies**.  
Built with cutting-edge **LLMs, multimodal document processing, and predictive analytics**, Finsight AI empowers organizations to make **smarter, data-driven financial decisions**.

---

## 🚀 Features

- **Financial Q&A with Fine-Tuned LLM**
  - Ask natural language questions and get accurate, context-aware financial answers.
  - Powered by a fine-tuned LLM and a Retrieval-Augmented Generation (RAG) system.

- **Multimodal Document Extraction**
  - Extract **text, tables, and images** from complex financial documents.
  - Supports automated parsing of PDFs, financial statements, and reports.

- **Predictive Financial Analysis** *(upcoming)*
  - Generate **future financial forecasts** and perform **risk assessments**.
  - AI-powered insights for **loan approval** and **credit risk management**.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python, FastAPI (planned)
- **LLMs & Embeddings:** 
  - gpt4-0 as llm
  - text embedding 002 for embeddings
- **Data Handling:** SEC API integration, Vector Databases
- **Document Parsing:** LlamaParser
- **Deployment:** Azure (Cloud-hosted)

---

## 📂 Project Structure

FinsightAI/
│
├── module_1_finetuned_llm/ # Financial Q&A with fine-tuned LLM and RAG
├── module_2_multimodal/ # Multimodal document extraction
├── main.py # Entry point (Streamlit UI)
├── requirements.txt # Dependencies
├── README.md # Project documentation


---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sharybhatti/FinsightAI.git
cd FinsightAI

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

streamlit run main.py

📌 Usage

    Module 1: Ask financial questions, get AI-powered answers based on your data.

    Module 2: Upload complex financial documents and extract structured data.

    Upcoming Module: Predict loan repayment risk and generate financial forecasts.

🎯 Target Users

    Banks & Financial Institutions

    Credit Rating Agencies

    Small Business Lenders & Microfinance Institutions

💡 Future Roadmap

Add financial forecasting & risk assessment module.

Implement loan approval automation.

Expand support for additional financial document formats.

    Enhance real-time predictive analytics.

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request with improvements.

📞 Contact

For questions, suggestions, or collaboration opportunities:
Shaharyar Shabbir Bhatti
📧 Email: shaharyarshabbir348@gmail.com
