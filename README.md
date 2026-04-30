# Streamlit Document Analysis App

A beginner-friendly, client-usable Streamlit app to upload DOCX/PDF/TXT documents, extract text, and generate a structured AI analysis.

## Folder structure

```text
Doc-summrizer/
├── app.py
├── requirements.txt
└── README.md
```

## What this app does

1. Uploads a document (`.docx`, `.pdf`, `.txt`)
2. Extracts clean text using:
   - `mammoth` for DOCX
   - `PyPDF2` for PDF
   - UTF-8 decode for TXT
3. Sends text (truncated to 2500 characters) to OpenAI or Groq
4. Returns structured analysis in this exact format:
   1. 🧾 DOCUMENT OVERVIEW
   2. 🔑 KEY INSIGHTS
   3. 💰 FINANCIALS (if present)
   4. ⚙️ BUSINESS / OPERATIONAL MODEL
   5. 🚀 STRENGTHS
   6. ⚠️ RISKS / GAPS
   7. 📈 OPPORTUNITIES
   8. 🧠 DECISION INSIGHT
   9. 📌 FINAL SUMMARY

## Step-by-step setup

### 1) Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app locally

```bash
streamlit run app.py
```

### 4) Use the app

1. Open the local URL shown by Streamlit (usually `http://localhost:8501`)
2. In the sidebar:
   - Choose **OpenAI** or **Groq**
   - Paste your API key
   - Keep default model or change it
3. Upload a DOCX/PDF/TXT file
4. Click **Analyze Document**
5. Read the structured output

## Error handling included

- Empty upload protection
- Unsupported file type protection
- Empty-text extraction protection
- API key validation
- AI call exception handling

## Notes

- This app is intentionally simple and easy to extend.
- For better quality on long documents, chunking can be added later.
