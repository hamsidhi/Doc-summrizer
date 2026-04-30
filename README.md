# 📜 Huntii Analyser (Document Intelligence)

**Huntii Analyser** is a professional-grade multi-document analysis tool built with Streamlit and Groq LLMs. It is designed to extract, analyze, and synthesize insights from financial, agricultural, educational, and other domain-specific documents.

## ✨ Features
- **Multi-Format Support**: Analyze PDF, DOCX, and TXT files simultaneously.
- **Intelligent Extraction**: Automatic text extraction and meta-data detection.
- **Domain Adaptation**: Automatically detects the domain (Finance, Tech, Agri, etc.) and adjusts the analysis framework.
- **Investor-Grade Reports**: Generates structured summaries with key metrics, insights, risks, and opportunities.
- **Professional Export**: Download analysis reports in **Word (.docx)** format with preserved tables and structure.
- **Smart Truncation**: Handles large documents by preserving critical introductory and concluding contexts within model token limits.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **LLM Engine**: Groq (Llama 3.3 70B, etc.)
- **Libraries**: `python-docx`, `PyPDF2`, `mammoth`, `markdown`

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Groq API Key (Get one at [console.groq.com](https://console.groq.com))

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/hamsidhi/Doc-summrizer.git
   cd Doc-summrizer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🔐 Privacy & Security
The app stores your API key locally in a `config/` directory. This directory is excluded from version control via `.gitignore` to keep your credentials safe.

## 📁 Repository Structure
- `app.py`: Main application logic and UI.
- `key_manager.py`: Secure API key handling.
- `requirements.txt`: Project dependencies.
- `logo.png`: Application branding.

---
Built with ❤️ for professional document intelligence.
